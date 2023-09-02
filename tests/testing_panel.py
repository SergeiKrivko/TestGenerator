from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QListWidgetItem

from tests.testing_widget import Test
from ui.side_panel_widget import SidePanelWidget


class TestingPanel(SidePanelWidget):
    jump_to_testing = pyqtSignal(int, bool)

    def __init__(self, sm, tm):
        super().__init__(sm, tm, 'Тестирование', ['run'])

        self.setFixedWidth(220)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.list_widget.currentItemChanged.connect(lambda: self.jump(False))
        self.list_widget.doubleClicked.connect(lambda: self.jump(True))

        self.items = []

    def add_item(self, test):
        self.list_widget.addItem(item := TestingPanelItem(test, self.tm))
        self.items.append(item)

    def set_status(self, index, status):
        self.items[index].set_status(status)

    def clear(self):
        self.list_widget.clear()
        self.items.clear()

    def jump(self, show_tab=False):
        if self.list_widget.currentItem():
            self.jump_to_testing.emit(self.list_widget.currentRow(), show_tab)

    def set_theme(self):
        super().set_theme()
        self.list_widget.setStyleSheet(self.tm.list_widget_css('Main'))
        for el in self.items:
            el.set_theme()


class TestingPanelItem(QListWidgetItem):
    texts = {Test.IN_PROGRESS: 'in progress…',
             Test.PASSED: 'PASSED',
             Test.FAILED: 'FAILED',
             Test.TIMEOUT: 'TIMEOUT',
             Test.TERMINATED: 'terminated'}

    def __init__(self, test, tm):
        super().__init__()
        self.test = test
        self.name = test.name()
        self.tm = tm
        self.status = 0
        self.set_status(Test.IN_PROGRESS)

    def set_status(self, status):
        self.status = status
        self.setText(f"{self.name:8} {self.texts[self.status]}")
        self.set_theme()

    def set_theme(self):
        self.setFont(self.tm.code_font)
        if self.status == Test.IN_PROGRESS:
            self.setForeground(self.tm['TestInProgress'])
            self.setIcon(QIcon(self.tm.get_image('running', color=self.tm['TestInProgress'])))
        elif self.status == Test.PASSED:
            self.setForeground(self.tm['TestPassed'])
            self.setIcon(QIcon(self.tm.get_image('passed', color=self.tm['TestPassed'])))
        elif self.status == Test.FAILED:
            self.setForeground(self.tm['TestFailed'])
            self.setIcon(QIcon(self.tm.get_image('failed', color=self.tm['TestFailed'])))
        elif self.status == Test.TIMEOUT:
            self.setForeground(self.tm['TestFailed'])
            self.setIcon(QIcon(self.tm.get_image('running', color=self.tm['TestFailed'])))
        elif self.status == Test.TERMINATED:
            self.setForeground(self.tm['TestInProgress'])
            self.setIcon(QIcon(self.tm.get_image('failed', color=self.tm['TestInProgress'])))
