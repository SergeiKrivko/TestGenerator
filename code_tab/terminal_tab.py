import os
import subprocess
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout

from ui.side_panel_widget import SidePanelWidget


class ProgramLooper(QThread):
    def __init__(self, process: subprocess.Popen):
        super().__init__()
        self.process = process

    def run(self):
        self.process.communicate()

    def terminate(self) -> None:
        self.process.terminate()
        super().terminate()


class OutputLooper(QThread):
    output = pyqtSignal(str)

    def __init__(self, file):
        super().__init__()
        self.file = file
        self.pos = 0
        self.stop = False

    def run(self):
        while not self.stop:
            try:
                text = self.file.read()
                if text:
                    self.output.emit(text)
            except EOFError:
                pass
            except UnicodeDecodeError:
                pass
            sleep(0.1)
        sleep(0.1)
        try:
            text = self.file.read()
            if text:
                self.output.emit(text)
        except EOFError:
            pass
        except UnicodeDecodeError:
            pass


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
        self.current_dir = self.sm.path
        self.commands = []
        self.current_command = -1

        os.makedirs(f"{self.sm.app_data_dir}/console", exist_ok=True)
        self.input_file = None
        self.program_output = None
        self.output_file = None
        self.program_errors = None
        self.errors_file = None

        self.reader = None
        self.program = None
        self.program_looper = None
        self.output_looper = None
        self.errors_looper = None
        self.looper = None
        self.return_code = 0
        self.current_process_id = 0

        self.textChanged.connect(self.check_changes)
        self.write_prompt()

    def write_python_file(self, process_id: int):
        with open(f"{self.sm.app_data_dir}/console/reader_{process_id}.py", 'w', encoding='utf-8') as f:
            f.write(f"from time import sleep\n"
                    f"file = open('{self.sm.app_data_dir}/console/input_{process_id}.txt', encoding='utf-8')\n"
                    f"while True:\n"
                    f"    text = file.read()\n"
                    f"    if text == '!!!TestGenerator:process_{process_id}:terminate!!!':\n"
                    f"        break\n"
                    f"    print(text, end='')\n"
                    f"    sleep(0.1)\n")

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
        self.not_check = True
        if not text:
            return

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

    def command(self, command: str):
        if self.program is not None:
            self.input_file.write(command.strip())
            self.input_file.write('\n')
            self.input_file.flush()
        elif command.startswith('cd '):
            self.command_cd(command)
        elif (command.startswith('ls ') or command.strip() == 'ls') and os.name == 'nt':
            self.command_ls()
        elif command.strip() == 'clear':
            self.command_clear()
        else:
            self.start_process(command)

    def start_process(self, command):
        process_id = self.sm.get_general('process_id', 0)
        if not isinstance(process_id, int) or process_id < 0 or process_id > 10000000:
            process_id = 0
        self.sm.set_general('process_id', process_id + 1)
        self.current_process_id = process_id

        self.input_file = open(f"{self.sm.app_data_dir}/console/input_{process_id}.txt", 'w', encoding='utf-8')
        self.program_output = open(f"{self.sm.app_data_dir}/console/output_{process_id}.txt", 'w', encoding='utf-8')
        self.output_file = open(f"{self.sm.app_data_dir}/console/output_{process_id}.txt", encoding='utf-8')
        self.program_errors = open(f"{self.sm.app_data_dir}/console/errors_{process_id}.txt", 'w', encoding='utf-8')
        self.errors_file = open(f"{self.sm.app_data_dir}/console/errors_{process_id}.txt", encoding='utf-8')

        self.write_python_file(process_id)
        self.reader = subprocess.Popen([self.sm.get_general('python', 'python'),
                                        f"{self.sm.app_data_dir}/console/reader_{process_id}.py"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.DEVNULL, shell=True, cwd=self.current_dir)
        self.program = subprocess.Popen(command, stdin=self.reader.stdout, stdout=self.program_output,
                                        stderr=self.program_errors, shell=True, cwd=self.current_dir)

        self.reader.stdout.close()

        self.program_looper = ProgramLooper(self.program)
        self.program_looper.finished.connect(self.end_process)

        self.output_looper = OutputLooper(self.output_file)
        self.output_looper.output.connect(self.write_text)

        self.errors_looper = OutputLooper(self.errors_file)
        self.errors_looper.output.connect(lambda text: self.write_text(text, color=self.tm['TestFailed']))

        self.textChanged.connect(self.check_changes)

        self.program_looper.start()
        self.output_looper.start()
        self.errors_looper.start()

    def end_process(self):
        self.output_looper.stop = True
        self.errors_looper.stop = True
        self.input_file.write(f"!!!TestGenerator:process_{self.current_process_id}:terminate!!!")
        self.input_file.flush()
        if hasattr(self.program, 'returncode'):
            self.return_code = self.program.returncode
        self.program = None
        self.output_looper.finished.connect(self.delete_files)
        self.errors_looper.finished.connect(self.delete_errors_files)
        self.output_looper.finished.connect(self.write_prompt)

    def terminate_process(self):
        if isinstance(self.program, subprocess.Popen) and isinstance(self.program_looper, ProgramLooper):
            self.program_looper.terminate()

    def delete_files(self):
        self.input_file.close()
        self.output_file.close()
        self.program_output.close()
        try:
            os.remove(f"{self.sm.app_data_dir}/console/reader_{self.current_process_id}.py")
        except PermissionError:
            pass
        except FileNotFoundError:
            pass
        try:
            os.remove(f"{self.sm.app_data_dir}/console/input_{self.current_process_id}.txt")
        except PermissionError:
            pass
        except FileNotFoundError:
            pass
        try:
            os.remove(f"{self.sm.app_data_dir}/console/output_{self.current_process_id}.txt")
        except PermissionError:
            pass
        except FileNotFoundError:
            pass

    def delete_errors_files(self):
        self.errors_file.close()
        self.program_errors.close()
        try:
            os.remove(f"{self.sm.app_data_dir}/console/errors_{self.current_process_id}.txt")
        except PermissionError:
            pass
        except FileNotFoundError:
            pass

    def command_ls(self):
        self.write_text('\n'.join(os.listdir(self.current_dir.replace('"', ''))) + "\n")
        self.write_prompt()

    def command_cd(self, command: str):
        if os.path.isdir(command[3:].strip()):
            old_dir = os.getcwd()
            os.chdir(self.current_dir)
            self.current_dir = os.path.abspath(command[3:].strip())
            self.write_prompt()
            os.chdir(old_dir)

    def command_clear(self):
        self.fixed_html = ''
        self.setText('')
        self.write_prompt()

    def write_prompt(self):
        self.write_text(self.current_dir, color=self.tm['TestPassed'])
        self.write_text('$ ')

    def set_theme(self):
        self.setStyleSheet(self.tm.text_edit_css('Main'))
        self.setFont(self.tm.code_font)

    def select_project(self):
        self.stop_loopers()
        self.current_dir = self.sm.path
        self.fixed_html = ''
        self.write_prompt()

    def stop_loopers(self):
        for el in self.__dict__.values():
            if isinstance(el, QThread):
                el.terminate()


class TerminalTab(SidePanelWidget):
    def __init__(self, sm, tm):
        super().__init__(sm, tm, 'Терминал', ['cancel', 'resize'])
        layout = QVBoxLayout()
        self.setMinimumWidth(175)
        layout.setContentsMargins(0, 0, 0, 0)
        self.terminal = Terminal(sm, tm)
        layout.addWidget(self.terminal)
        self.setLayout(layout)

        self.buttons['cancel'].clicked.connect(self.terminal.terminate_process)

    def set_theme(self):
        super().set_theme()
        self.terminal.set_theme()

    def stop_loopers(self):
        self.terminal.stop_loopers()
