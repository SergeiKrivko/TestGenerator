from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QListWidgetItem

from backend.types.func_test import FuncTest
from backend.backend_manager import BackendManager
from ui.side_panel_widget import SidePanelWidget


class TestingPanel(SidePanelWidget):
    def __init__(self, sm, bm: BackendManager, tm):
        super().__init__(sm, tm, 'Тестирование', ['run', 'cancel'])
        self.bm = bm

        self.setFixedWidth(225)
        self.side_panel_width = 225
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.list_widget.currentItemChanged.connect(self._on_item_changed)
        self.list_widget.doubleClicked.connect(self._on_item_double_clicked)

        self.buttons['run'].clicked.connect(self.bm.start_testing)
        self.buttons['cancel'].clicked.connect(self.bm.stop_testing)
        self.sm.projectChanged.connect(self.list_widget.clear)

        self.bm.startTesting.connect(self.update_items)
        self.bm.changeTestStatus.connect(self.set_status)
        self.bm.endTesting.connect(self.set_terminated)

        self.items = []

        self._completed = 0

    def update_items(self, tests: list[FuncTest]):
        self._completed = 0
        self.clear()
        for i, el in enumerate(tests):
            self.add_item(el, i)
        self.set_theme()

    def _on_item_changed(self):
        self.bm.main_tab_command('testing', self.list_widget.currentRow())

    def _on_item_double_clicked(self):
        self.bm.main_tab_show('testing')
        self.bm.main_tab_command('testing', self.list_widget.currentRow())

    def set_terminated(self):
        for i in range(self._completed, self.list_widget.count()):
            self.list_widget.item(i).set_status(FuncTest.TERMINATED)

    def add_item(self, test, index):
        if test.type() != 'pos':
            index -= self.bm.func_tests_count('pos')
        self.list_widget.addItem(item := TestingPanelItem(test, f"{test.type()}{index + 1}", self.tm))
        self.items.append(item)

    def set_status(self, test: FuncTest):
        if test.status() in [FuncTest.PASSED, FuncTest.FAILED, FuncTest.TIMEOUT]:
            self._completed += 1
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if isinstance(item, TestingPanelItem):
                if item.test == test:
                    item.update_status()
                    break

    def clear(self):
        self.list_widget.clear()
        self.items.clear()

    def set_theme(self):
        super().set_theme()
        self.list_widget.setStyleSheet(self.tm.list_widget_css('Main'))
        for el in self.items:
            el.set_theme()


class TestingPanelItem(QListWidgetItem):
    texts = {FuncTest.IN_PROGRESS: 'in progress…',
             FuncTest.PASSED: 'PASSED',
             FuncTest.FAILED: 'FAILED',
             FuncTest.TIMEOUT: 'TIMEOUT',
             FuncTest.TERMINATED: 'terminated'}

    def __init__(self, test, name, tm):
        super().__init__()
        self.test = test
        self.name = name
        self.tm = tm
        self.status = 0
        self.set_status(FuncTest.IN_PROGRESS)

    def set_status(self, status):
        self.status = status
        self.setText(f"{self.name:8} {self.texts[self.status]}")
        self.set_theme()

    def update_status(self):
        self.set_status(self.test.status())

    def set_theme(self):
        self.setFont(self.tm.code_font)
        if self.status == FuncTest.IN_PROGRESS:
            self.setForeground(self.tm['TestInProgress'])
            self.setIcon(QIcon(self.tm.get_image('running', color=self.tm['TestInProgress'])))
        elif self.status == FuncTest.PASSED:
            self.setForeground(self.tm['TestPassed'])
            self.setIcon(QIcon(self.tm.get_image('passed', color=self.tm['TestPassed'])))
        elif self.status == FuncTest.FAILED:
            self.setForeground(self.tm['TestFailed'])
            self.setIcon(QIcon(self.tm.get_image('failed', color=self.tm['TestFailed'])))
        elif self.status == FuncTest.TIMEOUT:
            self.setForeground(self.tm['TestFailed'])
            self.setIcon(QIcon(self.tm.get_image('running', color=self.tm['TestFailed'])))
        elif self.status == FuncTest.TERMINATED:
            self.setForeground(self.tm['TestInProgress'])
            self.setIcon(QIcon(self.tm.get_image('failed', color=self.tm['TestInProgress'])))
