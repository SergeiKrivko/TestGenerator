import asyncio

from qasync import asyncSlot

from src.other.terminal import Terminal
from src.ui.widgets.side_panel_widget import SidePanelWidget, SidePanelButton


class ConsoleTab(SidePanelWidget):
    def __init__(self, bm):
        super().__init__(bm, 'Выполнение')
        self.setMinimumWidth(175)

        self.terminal = Console(bm, id='2')
        self.terminal.setReadOnly(True)
        self.setWidget(self.terminal)

        self.button_cancel = SidePanelButton('line-ban')
        self.button_cancel.on_click = self.terminal.terminate_process
        self.buttons_layout.addWidget(self.button_cancel)

    def command(self, command: str, cwd=None):
        self.terminal.clear()
        if cwd:
            self.terminal.set_cwd(cwd)
        self.terminal.command(command)

    def select_project(self):
        self.terminal.set_cwd(self.bm.projects.current.path())
        self.terminal.clear()


class Console(Terminal):
    def write_prompt(self):
        pass

    def start_process(self, command):
        self.write_text(command + '\n')
        super().start_process(command)
        self.setReadOnly(False)

    def end_process(self):
        super().end_process()
        if self.isReadOnly():
            return
        self._print_return_code()

    @asyncSlot()
    async def _print_return_code(self):
        await asyncio.sleep(0.1)
        self.write_text(f"\nProcess finished with exit code {self.return_code}\n")
        self.setReadOnly(True)
