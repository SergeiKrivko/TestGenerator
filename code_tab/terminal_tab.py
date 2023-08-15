from PyQt5.QtWidgets import QVBoxLayout

from other.terminal import Terminal
from ui.side_panel_widget import SidePanelWidget


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
