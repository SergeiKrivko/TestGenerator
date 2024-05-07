from PyQtUIkit.widgets import *

from src.backend.backend_types.func_test import FuncTest
from src.backend.managers import BackendManager
from src.ui.widgets.side_panel_widget import SidePanelWidget, SidePanelButton


class TestingPanel(SidePanelWidget):
    def __init__(self, bm: BackendManager):
        super().__init__(bm, 'Тестирование')

        self.setFixedWidth(225)
        self.side_panel_width = 225

        layout = KitVBoxLayout()
        self.setWidget(layout)

        self.list_widget = KitListWidget()
        self.list_widget.font = 'mono'
        layout.addWidget(self.list_widget)
        self.list_widget.currentItemChanged.connect(self._on_item_changed)
        self.list_widget.doubleClicked.connect(self._on_item_double_clicked)

        self._button_run = SidePanelButton('line-play')
        self._button_run.on_click = self.bm.func_tests.testing
        self.buttons_layout.addWidget(self._button_run)

        self._button_run = SidePanelButton('line-ban')
        self._button_run.on_click = self.bm.func_tests.stop_testing
        self.buttons_layout.addWidget(self._button_run)

        self.bm.projects.finishClosing.connect(self.list_widget.clear)
        self.bm.func_tests.startTesting.connect(self.update_items)
        self.bm.func_tests.onStatusChanged.connect(self.set_status)
        self.bm.func_tests.endTesting.connect(self.set_terminated)

        self.items = []

        self._completed = 0

    def update_items(self, tests: list[FuncTest]):
        self._completed = 0
        self.clear()
        for i, el in enumerate(tests):
            self.add_item(el, i)

    def _on_item_changed(self):
        self.bm.main_tab_command('testing', self.list_widget.currentRow())

    def _on_item_double_clicked(self):
        self.bm.main_tab_show('testing')
        self.bm.main_tab_command('testing', self.list_widget.currentRow())

    def set_terminated(self):
        for i in range(self._completed, self.list_widget.count()):
            self.list_widget.item(i).set_status(FuncTest.Status.TERMINATED)

    def add_item(self, test: FuncTest, index):
        if test.type != FuncTest.Type.POS:
            index -= self.bm.func_tests.count(FuncTest.Type.POS)
        self.list_widget.addItem(item := TestingPanelItem(test, f"{test.type.value}{index + 1}"))
        self.items.append(item)

    def set_status(self, test: FuncTest):
        if test.status in [FuncTest.Status.PASSED, FuncTest.Status.FAILED, FuncTest.Status.TIMEOUT]:
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


class TestingPanelItem(KitListWidgetItem):
    texts = {FuncTest.Status.IN_PROGRESS: 'in progress…',
             FuncTest.Status.PASSED: 'PASSED',
             FuncTest.Status.FAILED: 'FAILED',
             FuncTest.Status.TIMEOUT: 'TIMEOUT',
             FuncTest.Status.TERMINATED: 'terminated'}

    def __init__(self, test, name):
        super().__init__('')
        self.test = test
        self.name = name
        self.status = 0
        self.set_status(FuncTest.Status.IN_PROGRESS)

    def set_status(self, status: FuncTest.Status):
        self.status = status
        self.setText(f"{self.name:8} {self.texts[self.status]}")

        match status:
            case FuncTest.Status.IN_PROGRESS:
                self.main_palette = 'Main'
                self.icon = 'line-time'
            case FuncTest.Status.PASSED:
                self.main_palette = 'Success'
                self.icon = 'line-checkmark'
            case FuncTest.Status.FAILED:
                self.main_palette = 'Danger'
                self.icon = 'line-close'
            case FuncTest.Status.TERMINATED:
                self.main_palette = 'Main'
                self.icon = 'line-ban'
            case FuncTest.Status.TIMEOUT:
                self.main_palette = 'Danger'
                self.icon = 'line-timer'

    def update_status(self):
        self.set_status(self.test.status)
