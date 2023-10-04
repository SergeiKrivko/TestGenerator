import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QTreeWidget, \
    QTreeWidgetItem

from backend.backend_manager import BackendManager
from backend.settings_manager import SettingsManager
from backend.types.unit_test import UnitTest
from backend.types.unit_tests_module import UnitTestsModule
from backend.types.unit_tests_suite import UnitTestsSuite
from main_tabs.tests.commands import CommandManager
from main_tabs.unit_testing.test_edit import UnitTestEdit, TestSuiteEdit
from side_tabs.builds.commands_list import MakeScenarioBox
from ui.button import Button
from ui.main_tab import MainTab

BUTTONS_MAX_WIDTH = 40


class UnitTestingWidget(MainTab):
    def __init__(self, sm: SettingsManager, bm: BackendManager, cm: CommandManager, tm):
        super().__init__()
        self.sm = sm
        self.bm = bm
        self.cm = cm
        self.tm = tm

        super().hide()

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(left_layout, 1)

        self.scenario_box = MakeScenarioBox(self.sm, self.bm)
        left_layout.addWidget(self.scenario_box)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addLayout(buttons_layout)

        self.button_add_dir = Button(self.tm, 'add_dir', css='Bg')
        self.button_add_dir.setFixedHeight(22)
        self.button_add_dir.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_add_dir.clicked.connect(self.add_suite)
        buttons_layout.addWidget(self.button_add_dir)

        self.button_add = Button(self.tm, 'plus', css='Bg')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_add.clicked.connect(self.add_test)
        buttons_layout.addWidget(self.button_add)

        self.button_delete = Button(self.tm, 'delete', css='Bg')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_delete.clicked.connect(self.delete_item)
        buttons_layout.addWidget(self.button_delete)

        self.button_up = Button(self.tm, 'button_up', css='Bg')
        self.button_up.setFixedHeight(22)
        self.button_up.setMaximumWidth(BUTTONS_MAX_WIDTH)
        buttons_layout.addWidget(self.button_up)

        self.button_down = Button(self.tm, 'button_down', css='Bg')
        self.button_down.setFixedHeight(22)
        self.button_down.setMaximumWidth(BUTTONS_MAX_WIDTH)
        buttons_layout.addWidget(self.button_down)

        self.button_copy = Button(self.tm, 'copy', css='Bg')
        self.button_copy.setFixedHeight(22)
        self.button_copy.setMaximumWidth(BUTTONS_MAX_WIDTH)
        buttons_layout.addWidget(self.button_copy)

        self.button_run = Button(self.tm, 'button_run', css='Bg')
        self.button_run.setFixedHeight(22)
        self.button_run.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_run.clicked.connect(self.run_tests)
        buttons_layout.addWidget(self.button_run)

        self._tree_widget = QTreeWidget()
        self._tree_widget.setHeaderHidden(True)
        self._tree_widget.currentItemChanged.connect(self._on_test_selected)
        left_layout.addWidget(self._tree_widget)

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(right_layout, 2)

        self._test_edit = UnitTestEdit(self.sm, self.tm)
        self._test_edit.hide()
        right_layout.addWidget(self._test_edit)

        self._test_suite_edit = TestSuiteEdit(self.sm, self.tm)
        self._test_suite_edit.hide()
        right_layout.addWidget(self._test_suite_edit)

        self.data_dir = ""
        self.bm.addUnitTestModule.connect(self.add_module)
        self.bm.clearUnitTests.connect(self.clear_tests)

    def add_module(self, module: UnitTestsModule):
        self._tree_widget.addTopLevelItem(TreeModuleItem(self.tm, module))

    def clear_tests(self):
        self._tree_widget.clear()

    def run_tests(self):
        pass

    def _on_test_selected(self):
        item = self._tree_widget.currentItem()
        if isinstance(item, TreeItem):
            self._test_suite_edit.hide()
            self._test_edit.show()
            self._test_edit.open_test(item.test)
        elif isinstance(item, TreeSuiteItem):
            self._test_edit.hide()
            self._test_suite_edit.show()
            self._test_suite_edit.open_suite(item.suite)
        else:
            self._test_edit.hide()
            self._test_edit.open_test(None)

    def delete_item(self):
        selected = self._tree_widget.selectedItems()
        if len(selected) == 0:
            return
        selected = selected[0]
        self._test_edit.open_test(None)
        for i in range(self._tree_widget.topLevelItemCount()):
            if self._tree_widget.topLevelItem(i).delete(selected):
                break

    def add_test(self):
        for i in range(self._tree_widget.topLevelItemCount()):
            if self._tree_widget.topLevelItem(i).add_test():
                break

    def add_suite(self):
        for i in range(self._tree_widget.topLevelItemCount()):
            if self._tree_widget.topLevelItem(i).add_suite():
                return

    def set_theme(self):
        for el in [self._tree_widget, self.button_add, self.button_delete, self.button_down, self.scenario_box,
                   self.button_up, self.button_copy, self.button_add_dir, self.button_run]:
            self.tm.auto_css(el)
        for i in range(self._tree_widget.topLevelItemCount()):
            item = self._tree_widget.topLevelItem(i)
            if not isinstance(item, TreeModuleItem):
                continue
            item.set_theme()
        self._test_edit.set_theme()
        self._test_suite_edit.set_theme()


class TreeModuleItem(QTreeWidgetItem):
    def __init__(self, tm, module: UnitTestsModule):
        super().__init__()
        self._tm = tm
        self.module = module
        self.setText(0, os.path.basename(module.name()))

        self.module.addSuite.connect(self._on_suite_add)
        self.module.deleteSuite.connect(self._on_suite_delete)

        for suite in self.module.suits():
            self.addChild(TreeSuiteItem(self._tm, suite))

    def add_suite(self):
        if self.isSelected():
            self.module.insert_suite(UnitTestsSuite('-'), 0)
            return True

        for i in range(self.childCount()):
            if self.child(i).isSelected():
                self.module.insert_suite(UnitTestsSuite('-'), i + 1)
                return True
        return False

    def add_test(self):
        if self.isSelected():
            return True
        for i in range(self.childCount()):
            return self.child(i).add_test()

    def delete_item(self):
        for i in range(self.childCount()):
            if self.child(i).isSelected():
                self.module.delete_suite(i)
                return True
            if self.child(i).delete_item():
                return True
        return False

    def _on_suite_add(self, suite, index):
        self.insertChild(index, TreeSuiteItem(self._tm, suite))

    def _on_suite_delete(self, index):
        self.takeChild(index)

    def set_theme(self):
        self.setIcon(0, QIcon(self._tm.get_image('c')))
        self.setFont(0, self._tm.font_medium)
        for i in range(self.childCount()):
            self.child(i).set_theme()


class TreeSuiteItem(QTreeWidgetItem):
    def __init__(self, tm, suite: UnitTestsSuite):
        super().__init__()
        self._tm = tm
        self.suite = suite
        self.setText(0, suite.name())

        self.suite.addTest.connect(self._on_test_add)
        self.suite.deleteTest.connect(self._on_test_delete)
        self.suite.nameChanged.connect(self._on_name_changed)

        for test in self.suite.tests():
            self.addChild(TreeItem(self._tm, test))

    def add_test(self):
        if self.isSelected():
            self.suite.insert_test(UnitTest('-'), 0)
            return True

        for i in range(self.childCount()):
            if self.child(i).isSelected():
                self.suite.insert_test(UnitTest('-'), i)
                return True
        return False

    def delete_item(self):
        for i in range(self.childCount()):
            if self.child(i).isSelected():
                self.suite.delete_test(i)
                return True
        return False

    def _on_test_add(self, test, index):
        self.insertChild(index, TreeItem(self._tm, test))

    def _on_test_delete(self, index):
        self.takeChild(index)

    def _on_name_changed(self):
        self.setText(0, self.suite.name())

    def set_theme(self):
        self.setIcon(0, QIcon(self._tm.get_image('c')))
        self.setFont(0, self._tm.font_medium)
        for i in range(self.childCount()):
            self.child(i).set_theme()


class TreeItem(QTreeWidgetItem):
    def __init__(self, tm, test: UnitTest):
        super().__init__()
        self._tm = tm
        self.test = test
        self.test.load()
        self.set_theme()

        self.test.nameChanged.connect(self._on_name_changed)
        self.test.statusChanged.connect(self.set_theme)
        self._on_name_changed()

    def _on_name_changed(self):
        self.setText(0, self.test.get('desc', ''))
        if not self.text(0).strip():
            self.setText(0, self.test.get('name', '-'))

    def set_theme(self):
        self.setFont(0, self._tm.font_medium)
        match self.test.get('status', UnitTest.CHANGED):
            case UnitTest.PASSED:
                self.setIcon(0, QIcon(self._tm.get_image('passed', color=self._tm['TestPassed'].name())))
            case UnitTest.FAILED:
                self.setIcon(0, QIcon(self._tm.get_image('failed', color=self._tm['TestFailed'].name())))
            case UnitTest.CHANGED:
                self.setIcon(0, QIcon(self._tm.get_image('running', color=self._tm['TestInProgress'].name())))


