import os
import shlex

from PyQt5.QtCore import QProcess, QByteArray
from PyQt5.QtGui import QColor, QTextCursor
from PyQt5.QtWidgets import QTextEdit


class Terminal(QTextEdit):
    def __init__(self, sm, tm):
        super().__init__(None)
        self.sm = sm
        self.sm.project_changed.connect(self.select_project)
        self.tm = tm

        self.fixed_text = ""
        self.fixed_html = ""
        self.current_text = ""
        self.not_check = False
        self.current_process = ''
        self.current_dir = self.sm.path
        self.commands = []
        self.current_command = -1

        self._prompt_color = "#000000"
        self._error_color = "#111111"

        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.setWorkingDirectory(self.current_dir)
        self.process.readyReadStandardOutput.connect(lambda: self.write_text(self.process.readAllStandardOutput()))
        self.process.readyReadStandardError.connect(lambda: self.write_text(self.process.readAllStandardError(),
                                                                            color=self.tm['TestFailed']))
        self.process.finished.connect(self.end_process)

        self.process.error.connect(self.terminate_process)

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
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

    def command(self, command: str):
        if self.current_process:
            self.process.write(command.encode(encoding='utf-8'))
            self.process.write(b'\n')
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
        old_dir = os.getcwd()
        os.chdir(self.current_dir)
        csi = shlex.split(command, posix=False)
        program = csi[0]
        if os.path.isfile(program):
            program = os.path.abspath(program)
        os.chdir(old_dir)
        csi.pop(0)
        self.current_process = program
        self.process.start(program, csi)

    def end_process(self):
        self.current_process = ''
        self.write_prompt()

    def terminate_process(self, error_type: QProcess.ProcessError = None):
        if not self.current_process:
            return
        if error_type is not None:
            if error_type == QProcess.ProcessError.FailedToStart and self.current_process:
                self.write_text(f"Имя \"{self.current_process}\" не распознано как имя командлета, функции, "
                                f"файла сценария или выполняемой программы. Проверьте правильность написания имени, "
                                f"а также наличие и правильность пути, после чего повторите попытку.\n",
                                color=self._error_color)
        self.process.kill()
        self.end_process()

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
        self.current_dir = self.sm.path
        self.process.setWorkingDirectory(self.current_dir)
        self.fixed_html = ''
        self.write_prompt()

