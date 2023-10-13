import os
from PyQt5.QtWidgets import QVBoxLayout

from backend.commands import cmd_command
from main_tabs.code_tab.compiler_errors_window import CompilerErrorWindow
from language.languages import languages
from other.terminal import Terminal
from side_tabs.builds.commands_list import ScenarioBox
from ui.side_panel_widget import SidePanelWidget


class Console(Terminal):
    def __init__(self, sm, tm, bm):
        super().__init__(sm, tm)
        self.bm = bm

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

    def run_build(self, build_id):
        self.bm.compile_build(build_id)
        self.write_text(command := self.bm.build_running_command(build_id))
        self.start_process(command)


class ConsolePanel(SidePanelWidget):
    def __init__(self, sm, tm, bm):
        super().__init__(sm, tm, 'Выполнение', ['run', 'cancel'])
        self.bm = bm

        self._build_box = ScenarioBox(self.sm, self.bm, self.tm)
        self.sm.projectChanged.connect(lambda: self._build_box.load(self.sm.get('last')))
        self._top_layout.insertWidget(1, self._build_box)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.terminal = Console(sm, tm, self.bm)
        layout.addWidget(self.terminal)
        self.setLayout(layout)

        self.buttons['run'].clicked.connect(self.run_main)
        self.buttons['cancel'].clicked.connect(self.terminal.terminate_process)

    def run_main(self):
        self.terminal.run_build(self._build_box.current_scenario())
        # res, errors = self.cm.compile()
        # if res:
        #     self.terminal.start_process(languages[self.sm.get('language', 'C')]['run'](
        #         self.sm.lab_path(), self.sm, coverage=False))
        # elif errors:
        #     dialog = CompilerErrorWindow(errors, self.tm, languages[self.sm.get('language', 'C')].get('compiler_mask'))
        #     if dialog.exec():
        #         pass
                # if dialog.goto:
                #     self.jump_to_code.emit(*dialog.goto)

    def set_theme(self):
        super().set_theme()
        self.terminal.set_theme()

    def run_file(self, path):
        self.terminal.run_file(path)
