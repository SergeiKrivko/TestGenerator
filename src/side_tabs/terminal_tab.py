from PyQt6.QtWidgets import QVBoxLayout

from src.other.terminal import Terminal
from src.ui.side_panel_widget import SidePanelWidget


class TerminalTab(SidePanelWidget):
    def __init__(self, bm, tm):
        super().__init__(bm.sm, tm, 'Терминал', ['cancel'])
        layout = QVBoxLayout()
        self.setMinimumWidth(175)
        layout.setContentsMargins(0, 0, 0, 0)
        self.terminal = Terminal(bm, bm.sm, tm, id='1')
        layout.addWidget(self.terminal)
        self.setLayout(layout)

        self.buttons['cancel'].clicked.connect(lambda: self.terminal.terminate_process())

    def set_theme(self):
        super().set_theme()
        self.terminal.set_theme()
