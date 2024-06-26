import os
import subprocess
from time import sleep
from uuid import uuid4

from PyQt6.QtCore import QByteArray, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QTextCursor
from PyQt6.QtWidgets import QTextEdit
from PyQtUIkit.widgets import KitTextEdit

from src.backend.commands import get_si
from src.backend.managers import BackendManager


class Terminal(KitTextEdit):
    processFinished = pyqtSignal()

    def __init__(self, bm: BackendManager, terminal_app='', id=''):
        super().__init__()
        self.bm = bm
        self._id = id or str(uuid4())
        self._terminal_app = terminal_app

        self.font = 'mono'

        self.fixed_text = ""
        self.fixed_html = ""
        self.current_text = ""
        self.not_check = False
        self.current_process = ''
        self.current_dir = os.getcwd()
        self.commands = []
        self.current_command = -1

        self._prompt_color = "#000000"
        self._error_color = "#111111"

        self.process = None
        self.stdout_reader = None
        self.stderr_reader = None

        self.return_code = 0

        self.textChanged.connect(self.check_changes)
        self.write_prompt()

    def check_changes(self):
        if self.not_check:
            return
        text = self.toPlainText()
        if not text.startswith(self.fixed_text):
            self.not_check = True
            self.setText('')
            self.insertHtml(self.current_text)
            self.not_check = False
        else:
            command = text[len(self.fixed_text):]
            self.current_text = self.fixed_html + command
            if '\n' in command:
                command = command[:command.rindex('\n')]
                self.fixed_html += command + '<br>'
                self.fixed_text += command + '\n'
                self.command(command)

    def write_text(self, text, color=None):
        if not text:
            return
        if isinstance(text, QByteArray):
            try:
                text = text.data().decode(encoding='utf-8')
            except UnicodeDecodeError:
                return
        self.not_check = True

        text = text.replace('\n', '<br>')
        if color is not None:
            if isinstance(color, QColor):
                color = color.name()
            text = f"<font color='{color}'>{text}</font>"

        self.fixed_html = self.fixed_html + text
        self.setText('')
        self.insertHtml(self.fixed_html)
        self.fixed_text = self.toPlainText()
        self.current_text = self.fixed_html
        self.not_check = False
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)

    def command(self, command: str):
        if self.current_process:
            self.process.stdin.write(command + '\n')
        elif command.startswith('cd '):
            self.command_cd(command)
        elif (command.startswith('ls ') or command.strip() == 'ls') and os.name == 'nt':
            self.command_ls()
        elif command.strip() == 'clear':
            self.command_clear()
        else:
            self.start_process(command)

    def start_process(self, command):
        if not command.strip():
            self.write_prompt()
            return

        self.current_process = command
        self.process = subprocess.Popen(self._terminal_app + ' ' + command, text=True, startupinfo=get_si(),
                                        cwd=self.current_dir, shell=True, bufsize=1, encoding='utf-8',
                                        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.stdout_reader = BufferReader(self.process.stdout)
        self.stdout_reader.readyToRead.connect(self.write_text)
        self.stdout_reader.finished.connect(self.end_process)
        self.bm.processes.run(self.stdout_reader, f'Terminal-{self._id}', 'STDOUT')
        self.stderr_reader = BufferReader(self.process.stderr)
        self.stderr_reader.readyToRead.connect(lambda text: self.write_text(text, self._error_color))
        self.stderr_reader.finished.connect(self.end_process)
        self.bm.processes.run(self.stderr_reader, f'Terminal-{self._id}', 'STDERR')

    def end_process(self):
        if not self.stdout_reader.isFinished() or not self.stderr_reader.isFinished() or not self.current_process:
            return False
        self.current_process = ''
        self.process.stdout.close()
        self.process.stderr.close()
        self.write_text(self.stdout_reader.read())
        self.write_text(self.stderr_reader.read(), self._error_color)
        self.return_code = self.process.poll()
        self.write_prompt()
        self.processFinished.emit()
        return True

    def terminate_process(self):
        if not self.current_process or not isinstance(self.process, subprocess.Popen):
            return
        self.process.kill()
        self.current_process = None
        # self.stdout_reader.terminate()
        # self.stderr_reader.terminate()
        # self.process.stderr.close()
        # self.process.stdout.close()
        self.return_code = -1
        self.write_prompt()

    def command_ls(self):
        self.write_text('\n'.join(os.listdir(self.current_dir.replace('"', ''))) + "\n")
        self.write_prompt()

    def command_cd(self, command: str):
        old_dir = os.getcwd()
        os.chdir(self.current_dir)
        if os.path.isdir(command[3:].strip()):
            self.current_dir = os.path.abspath(command[3:].strip())
        self.write_prompt()
        os.chdir(old_dir)

    def command_clear(self):
        self.fixed_html = ''
        self.setText('')
        self.write_prompt()

    def write_prompt(self):
        self.write_text(self.current_dir, color=self._prompt_color)
        self.write_text('$ ')

    def clear(self):
        self.fixed_html = ''
        self.write_prompt()

    def set_cwd(self, path):
        self.current_dir = path

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return

        command = self.toPlainText()[len(self.fixed_text):]
        self.fixed_html = self.fixed_html.replace(self._prompt_color, self._tm.palette('Success').text_only)
        self.fixed_html = self.fixed_html.replace(self._error_color, self._tm.palette('Danger').text_only)
        self._prompt_color = self._tm.palette('Success').text_only
        self._error_color = self._tm.palette('Danger').text_only
        self.setHtml(self.fixed_html + command)

        super()._apply_theme()


class PipeReader(QThread):
    def __init__(self, stream, buffer):
        super().__init__()
        self._stream = stream
        self._buffer = buffer

    def run(self) -> None:
        for symbol in iter(lambda: self._stream.read(1), ''):
            self._buffer.buffer.append(symbol)


class BufferReader(QThread):
    readyToRead = pyqtSignal(str)

    def __init__(self, stream):
        super().__init__()
        self._pipe_reader = PipeReader(stream, self)
        self.buffer = []

    def start(self, priority: 'QThread.Priority' = ...) -> None:
        super().start()
        self._pipe_reader.start()

    def terminate(self) -> None:
        super().terminate()
        self._pipe_reader.terminate()

    def run(self) -> None:
        while not self._pipe_reader.isFinished():
            buffer = self.buffer
            self.buffer = []
            self.readyToRead.emit(''.join(buffer))
            sleep(0.3)

    def read(self):
        buffer = self.buffer
        self.buffer = []
        return ''.join(buffer)


