import os
import subprocess

from PyQt6.QtCore import QByteArray, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QTextCursor
from PyQt6.QtWidgets import QTextEdit

from backend.commands import get_si


class Terminal(QTextEdit):
    processFinished = pyqtSignal()

    def __init__(self, sm, tm):
        super().__init__(None)
        self.sm = sm
        self.sm.projectChanged.connect(self.select_project)
        self.tm = tm

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
        self.process = subprocess.Popen(command, text=True, startupinfo=get_si(), cwd=self.current_dir,
                                        shell=True, bufsize=1, encoding='utf-8',
                                        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.stdout_reader = PipeReader(self.process.stdout)
        self.stdout_reader.readyToRead.connect(self.write_text)
        self.stdout_reader.finished.connect(self.end_process)
        self.stdout_reader.start()
        self.stderr_reader = PipeReader(self.process.stderr)
        self.stderr_reader.readyToRead.connect(lambda text: self.write_text(text, self._error_color))
        self.stderr_reader.finished.connect(self.end_process)
        self.stderr_reader.start()

    def end_process(self):
        if not self.stdout_reader.isFinished() or not self.stderr_reader.isFinished() or not self.current_process:
            return False
        self.current_process = ''
        self.process.stdout.close()
        self.process.stderr.close()
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
            self.process.setWorkingDirectory(self.current_dir)
        self.write_prompt()
        os.chdir(old_dir)

    def command_clear(self):
        self.fixed_html = ''
        self.setText('')
        self.write_prompt()

    def write_prompt(self):
        self.write_text(self.current_dir, color=self._prompt_color)
        self.write_text('$ ')

    def set_theme(self):
        command = self.toPlainText()[len(self.fixed_text):]
        self.fixed_html = self.fixed_html.replace(self._prompt_color, self.tm['TestPassed'].name())
        self.fixed_html = self.fixed_html.replace(self._error_color, self.tm['TestFailed'].name())
        self._prompt_color = self.tm['TestPassed'].name()
        self._error_color = self.tm['TestFailed'].name()
        self.setHtml(self.fixed_html + command)

        self.setStyleSheet(self.tm.text_edit_css('Main'))
        self.setFont(self.tm.code_font)

    def select_project(self):
        self.current_dir = self.sm.project.path()
        self.fixed_html = ''
        self.write_prompt()


class PipeReader(QThread):
    readyToRead = pyqtSignal(str)

    def __init__(self, stream):
        super().__init__()
        self._stream = stream

    def run(self) -> None:
        for line in iter(self._stream.readline, ''):
            if line:
                self.readyToRead.emit(line)
