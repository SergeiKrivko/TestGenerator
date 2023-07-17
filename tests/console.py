import os
import subprocess
from time import sleep

from PyQt5.Qsci import QsciScintilla
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QColor


class Console(QsciScintilla):
    def __init__(self, sm, tm, command, path):
        super().__init__(None)
        self.sm = sm
        self.tm = tm
        self.resize(640, 480)

        self.fixed_text = ""
        self.current_text = ""
        self.not_check = False

        os.makedirs(f"{self.sm.app_data_dir}/console", exist_ok=True)
        self.input_file = open(f"{self.sm.app_data_dir}/console/input.txt", 'w', encoding='utf-8')
        self.program_output = open(f"{self.sm.app_data_dir}/console/output.txt", 'w', encoding='utf-8')
        self.output_file = open(f"{self.sm.app_data_dir}/console/output.txt", encoding='utf-8')

        with open(f"{self.sm.app_data_dir}/console/reader.py", 'w', encoding='utf-8') as f:
            code = f"from time import sleep\n" \
                   f"file = open('{self.sm.app_data_dir}/console/input.txt', encoding='utf-8')\n" \
                   f"while True:\n    print(file.read(), end='')\n    sleep(0.1)"
            f.write(code)

        self.reader = subprocess.Popen([self.sm.get_general('python', 'python'),
                                        f"{self.sm.app_data_dir}/console/reader.py"], cwd=path,
                                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        self.program = subprocess.Popen(command, stdin=self.reader.stdout, stdout=self.program_output,
                                        stderr=subprocess.STDOUT, shell=True, cwd=path)

        self.reader.stdout.close()

        self.program_looper = ProgramLooper(self.program)
        self.program_looper.finished.connect(self.stop)

        self.output_looper = OutputLooper(self.output_file)
        self.output_looper.output.connect(self.write_text)

        self.textChanged.connect(self.check_changes)
        self.set_theme()

        self.program_looper.start()
        self.output_looper.start()

    def check_changes(self):
        if self.not_check:
            return
        text = self.text()
        if not text.startswith(self.fixed_text):
            self.setText(self.current_text)
        else:
            self.current_text = text
            command = text[len(self.fixed_text):]
            if '\n' in command:
                command = command[:command.rindex('\n')]
                self.fixed_text += command + '\n'
                self.command(command)

    def write_text(self, text):
        self.not_check = True
        if not text:
            return
        self.fixed_text = self.text() + text
        self.setText(self.fixed_text)
        self.not_check = False

        pos = self.fixed_text.count('\n'), len(self.fixed_text.split('\n')[-1])
        self.setCursorPosition(*pos)

    def command(self, command: str):
        self.input_file.write(command.strip())
        self.input_file.write('\n')
        self.input_file.flush()

    def stop(self):
        self.output_looper.stop = True
        self.setReadOnly(True)
        self.write_text(f"\nProcess finished with exit code {self.program.returncode}\n")

    def set_theme(self):
        self.setStyleSheet(self.tm.scintilla_style_sheet)
        self.setFont(self.tm.code_font)
        self.setPaper(QColor(self.tm['MainColor']))
        self.setMarginsBackgroundColor(QColor(self.tm['MainColor']))
        
    def closeEvent(self, *args, **kwargs):
        if not self.program_looper.isFinished():
            self.program_looper.terminate()
        if not self.output_looper.isFinished():
            self.output_looper.terminate()
        super().closeEvent(*args, **kwargs)


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
