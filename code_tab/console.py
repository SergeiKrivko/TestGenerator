import os
from PyQt5.QtWidgets import QVBoxLayout

from code_tab.compiler_errors_window import CompilerErrorWindow
from language.languages import languages
from other.terminal import Terminal
from ui.side_panel_widget import SidePanelWidget


class Console(Terminal):
    def __init__(self, sm, tm, cm):
        super().__init__(sm, tm)
        self.cm = cm

    def write_prompt(self):
        pass

    def end_process(self):
        super().end_process()
        self.write_text(f'\nProcess finished with exit code {self.return_code}\n')
        self.setReadOnly(True)
        
    def start_process(self, command):
        self.command_clear()
        self.write_text(command + '\n')
        self.setReadOnly(False)
        super().start_process(command)

    def run_file(self, path):
        if path.endswith('.exe'):
            self.start_process(path)
            return
        for language in languages.values():
            if language.get('fast_run', False):
                for el in language['files']:
                    if path.endswith(el):
                        if 'compile' in language:
                            language['compile'](os.path.split(path)[0], self.cm, self.sm, coverage=False)
                        self.start_process(language['run'](path, self.sm, coverage=False))
                        return


class ConsolePanel(SidePanelWidget):
    def __init__(self, sm, tm, cm):
        super().__init__(sm, tm, 'Выполнение', ['run', 'cancel'])
        self.cm = cm

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.terminal = Console(sm, tm, cm)
        layout.addWidget(self.terminal)
        self.setLayout(layout)

        self.buttons['run'].clicked.connect(self.run_main)
        self.buttons['cancel'].clicked.connect(self.terminal.terminate_process)

    def run_main(self):
        res, errors = self.cm.compile()
        if res:
            self.terminal.start_process(languages[self.sm.get('language', 'C')]['run'](
                self.sm.lab_path(), self.sm, coverage=False))
        elif errors:
            dialog = CompilerErrorWindow(errors, os.listdir(self.sm.lab_path()), self.tm)
            if dialog.exec():
                pass
                # if dialog.goto:
                #     self.jump_to_code.emit(*dialog.goto)

    def set_theme(self):
        super().set_theme()
        self.terminal.set_theme()

    def run_file(self, path):
        self.terminal.run_file(path)

