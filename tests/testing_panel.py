from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QListWidgetItem

from tests.testing_widget import TestingListWidgetItem
from ui.side_panel_widget import SidePanelWidget


class TestingPanel(SidePanelWidget):
    jump_to_testing = pyqtSignal(int)

    def __init__(self, sm, tm):
        super().__init__(sm, tm, 'Тестирование', ['run'])

        self.setFixedWidth(200)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.list_widget.doubleClicked.connect(self.jump)

        self.items = dict()

    def add_item(self, name):
        self.list_widget.addItem(item := TestingPanelItem(name, self.tm))
        self.items[name] = item

    def set_status(self, name, status):
        self.items[name].set_status(status)

    def clear(self):
        self.list_widget.clear()
        self.items.clear()

    def jump(self):
        if self.list_widget.currentItem():
            self.jump_to_testing.emit(self.list_widget.currentRow())

    def set_theme(self):
        super().set_theme()
        self.list_widget.setStyleSheet(self.tm.list_widget_style_sheet)
        for el in self.items.values():
            el.set_theme()


class TestingPanelItem(QListWidgetItem):
    texts = {TestingListWidgetItem.in_progress: 'in progress…',
             TestingListWidgetItem.passed: 'PASSED',
             TestingListWidgetItem.failed: 'FAILED',
             TestingListWidgetItem.crashed: 'CRASHED',
             TestingListWidgetItem.terminated: 'terminated'}

    def __init__(self, name, tm):
        super().__init__()
        self.name = name
        self.tm = tm
        self.status = 0
        self.set_status(TestingListWidgetItem.in_progress)

    def set_status(self, status):
        self.status = status
        self.setText(s := f"{self.name:8} {self.texts[self.status]}")
        self.set_theme()

    def set_theme(self):
        self.setFont(self.tm.code_font)
        if self.status == TestingListWidgetItem.in_progress:
            self.setForeground(self.tm['TestInProgress'])
            self.setIcon(QIcon(self.tm.get_image('running', color=self.tm['TestInProgress'])))
        elif self.status == TestingListWidgetItem.passed:
            self.setForeground(self.tm['TestPassed'])
            self.setIcon(QIcon(self.tm.get_image('passed', color=self.tm['TestPassed'])))
        elif self.status == TestingListWidgetItem.failed:
            self.setForeground(self.tm['TestFailed'])
            self.setIcon(QIcon(self.tm.get_image('failed', color=self.tm['TestFailed'])))
        elif self.status == TestingListWidgetItem.crashed:
            self.setForeground(self.tm['TestFailed'])
            self.setIcon(QIcon(self.tm.get_image('failed', color=self.tm['TestFailed'])))
        elif self.status == TestingListWidgetItem.terminated:
            self.setForeground(self.tm['TestInProgress'])
            self.setIcon(QIcon(self.tm.get_image('running', color=self.tm['TestInProgress'])))
