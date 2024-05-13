from src.other.terminal import Terminal
from src.ui.widgets.side_panel_widget import SidePanelWidget, SidePanelButton


class TerminalTab(SidePanelWidget):
    def __init__(self, bm):
        super().__init__(bm, 'Терминал')
        self.setMinimumWidth(175)

        self.terminal = Terminal(bm, id='1')
        self.setWidget(self.terminal)

        self.button_cancel = SidePanelButton('line-ban')
        self.button_cancel.on_click = self.terminal.terminate_process
        self.buttons_layout.addWidget(self.button_cancel)

        self.bm.projects.finishOpening.connect(self.select_project)

    def select_project(self):
        self.terminal.set_cwd(self.bm.projects.current.path())
        self.terminal.clear()
