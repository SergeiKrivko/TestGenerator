import json

from PyQt6.QtCore import QMimeData, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QTreeWidget, \
    QTreeWidgetItem, QApplication

from backend.backend_manager import BackendManager
from backend.settings_manager import SettingsManager
from backend.backend_types.unit_test import UnitTest
from backend.backend_types.unit_tests_suite import UnitTestsSuite
from main_tabs.code_tab.compiler_errors_window import CompilerErrorWindow
from main_tabs.tests.commands import CommandManager
from main_tabs.unit_testing.test_edit import UnitTestEdit, TestSuiteEdit
from side_tabs.builds.commands_list import ScenarioBox
from ui.button import Button
from ui.main_tab import MainTab

BUTTONS_MAX_WIDTH = 40


class UnitTestingWidget(MainTab):
    def __init__(self, sm: SettingsManager, bm: BackendManager, cm: CommandManager, tm, app: QApplication):
        super().__init__()
        self.sm = sm
        self.bm = bm
        self.cm = cm
        self.tm = tm
        self.app = app

        super().hide()

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(left_layout, 1)

        self.scenario_box = ScenarioBox(self.sm, self.bm, self.tm)
        self.sm.projectChanged.connect(lambda: self.scenario_box.load(self.sm.get('unit_build')))
        self.scenario_box.currentIndexChanged.connect(self._on_build_changed)
        left_layout.addWidget(self.scenario_box)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addLayout(buttons_layout)

        self.button_add_dir = Button(self.tm, 'buttons/add_dir', css='Bg')
        self.button_add_dir.setFixedHeight(22)
        self.button_add_dir.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_add_dir.clicked.connect(self.bm.new_suite)
        buttons_layout.addWidget(self.button_add_dir)

        self.button_add = Button(self.tm, 'buttons/plus', css='Bg')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_add.clicked.connect(self.add_test)
        buttons_layout.addWidget(self.button_add)

        self.button_delete = Button(self.tm, 'buttons/delete', css='Bg')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_delete.clicked.connect(self.delete_item)
        buttons_layout.addWidget(self.button_delete)

        self.button_up = Button(self.tm, 'buttons/button_up', css='Bg')
        self.button_up.setFixedHeight(22)
        self.button_up.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_up.clicked.connect(self.move_up)
        buttons_layout.addWidget(self.button_up)

        self.button_down = Button(self.tm, 'buttons/button_down', css='Bg')
        self.button_down.setFixedHeight(22)
        self.button_down.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_down.clicked.connect(self.move_down)
        buttons_layout.addWidget(self.button_down)

        self.button_copy = Button(self.tm, 'buttons/copy', css='Bg')
        self.button_copy.setFixedHeight(22)
        self.button_copy.setMaximumWidth(BUTTONS_MAX_WIDTH)
        buttons_layout.addWidget(self.button_copy)

        self.button_run = Button(self.tm, 'buttons/run', css='Bg')
        self.button_run.setFixedHeight(22)
        self.button_run.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_run.clicked.connect(self.run_tests)
        buttons_layout.addWidget(self.button_run)

        self._tree_widget = QTreeWidget()
        self._tree_widget.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self._tree_widget.setHeaderHidden(True)
        self._tree_widget.currentItemChanged.connect(self._on_test_selected)
        self._tree_widget.itemSelectionChanged.connect(self._on_selection_changed)
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
        self.bm.addUnitTestSuite.connect(self.add_suite)
        self.bm.deleteSuite.connect(self._tree_widget.takeTopLevelItem)
        self.bm.clearUnitTests.connect(self.clear_tests)

        self.bm.unitTestingError.connect(self._on_testing_failed)

        self.ctrl_pressed = False
        self.shift_pressed = False

    def _on_testing_failed(self, errors):
        dialog = CompilerErrorWindow(errors, self.tm)
        dialog.exec()

    def _on_build_changed(self):
        self.sm.set('unit_build', self.scenario_box.current_scenario())

    def clear_tests(self):
        self._tree_widget.clear()

    def run_tests(self):
        self.bm.run_unit_tests()

    def _get_modules_set(self):
        modules = set()
        for item in self._tree_widget.selectedItems():
            modules.add(item.parent())
        if None in modules:
            for item in self._tree_widget.selectedItems():
                if isinstance(item, TreeSuiteItem):
                    item.select_all()
        return modules

    def _on_selection_changed(self):
        modules = self._get_modules_set()
        if len(modules) > 1:
            for m in modules:
                if isinstance(m, TreeSuiteItem):
                    if m == self._tree_widget.currentItem():
                        m.select_all(m.isSelected())
                    else:
                        m.select_all()

    def copy_tests(self):
        modules = self._get_modules_set()
        if None in modules:
            modules.remove(None)
            data = {'type': 'suites', 'data': [{
                'data': suite.suite.to_dict(),
                'tests': [test.get_data() for test in suite.suite.tests()]
            } for suite in modules]}
            mime_data = QMimeData()
            mime_data.setData('TestGeneratorUnitTests', json.dumps(data).encode('utf-8'))
            self.app.clipboard().setMimeData(mime_data)
        elif len(modules) == 1:
            suite = modules.pop()
            data = {'type': 'tests', 'data': [test.test.get_data() for test in self._tree_widget.selectedItems()]}
            mime_data = QMimeData()
            mime_data.setData('TestGeneratorUnitTests', json.dumps(data).encode('utf-8'))
            self.app.clipboard().setMimeData(mime_data)

    def paste_tests(self):
        item = self._tree_widget.currentItem()
        if isinstance(item, TreeSuiteItem):
            suite = item.suite
        elif isinstance(item, TreeItem):
            suite = item.parent().suite
        else:
            return

        data = self.app.clipboard().mimeData().data(f'TestGeneratorUnitTests')
        if data:
            try:
                data = json.loads(data.data().decode('utf-8'))
                if data.get('type') == 'tests':
                    tests = data.get('data')
                    for el in tests:
                        suite.new_test(data=el)
                elif data.get('type') == 'suites':
                    suites = data.get('data')
                    print(suites)
                    for el in suites:
                        suite = self.bm.new_suite(el.get('data'))
                        for test in el.get('tests', []):
                            suite.new_test(data=test)
            except UnicodeDecodeError:
                pass
            except json.JSONDecodeError:
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

    def keyPressEvent(self, a0) -> None:
        match a0.key():
            case Qt.Key.Key_C:
                if self.ctrl_pressed:
                    self.copy_tests()
            case Qt.Key.Key_V:
                if self.ctrl_pressed:
                    self.paste_tests()
            # case Qt.Key.Key_Z:
            #     if self.ctrl_pressed:
            #         self.undo.emit()
            case Qt.Key.Key_Control:
                self.ctrl_pressed = True
            case Qt.Key.Key_Shift:
                self.shift_pressed = True
            case Qt.Key.Key_Delete:
                self.delete_item()

    def keyReleaseEvent(self, a0) -> None:
        if a0.key() == Qt.Key.Key_Control:
            self.ctrl_pressed = False
        if a0.key() == Qt.Key.Key_Shift:
            self.shift_pressed = False

    def delete_item(self):
        self._test_edit.open_test(None)
        for i in range(self._tree_widget.topLevelItemCount()):
            item = self._tree_widget.topLevelItem(i)
            if isinstance(item, TreeSuiteItem):
                if item.isSelected():
                    self.bm.delete_suite(i)
                if item.delete_item():
                    break

    def add_test(self):
        for i in range(self._tree_widget.topLevelItemCount()):
            if self._tree_widget.topLevelItem(i).add_test():
                break

    def add_suite(self, suite):
        self._tree_widget.addTopLevelItem(TreeSuiteItem(self.tm, suite))

    def move_up(self):
        for i in range(self._tree_widget.topLevelItemCount()):
            if self._tree_widget.topLevelItem(i).move('up'):
                return

    def move_down(self):
        for i in range(self._tree_widget.topLevelItemCount()):
            if self._tree_widget.topLevelItem(i).move('down'):
                return

    def set_theme(self):
        for el in [self._tree_widget, self.button_add, self.button_delete, self.button_down,
                   self.button_up, self.button_copy, self.button_add_dir, self.button_run]:
            self.tm.auto_css(el)
        for i in range(self._tree_widget.topLevelItemCount()):
            item = self._tree_widget.topLevelItem(i)
            if not isinstance(item, TreeSuiteItem):
                continue
            item.set_theme()
        self.scenario_box.set_theme()
        self._test_edit.set_theme()
        self._test_suite_edit.set_theme()


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
            self.suite.new_test(0)
            return True

        for i in range(self.childCount()):
            if self.child(i).isSelected():
                self.suite.new_test(i + 1)
                return True
        return False

    def delete_item(self):
        flag = False
        for i in range(self.childCount() - 1, -1, -1):
            if self.child(i).isSelected():
                self.suite.delete_test(i)
                flag = True
        return flag

    def move(self, direction):
        for i in range(self.childCount()):
            if self.child(i).isSelected():
                self.suite.move_test(direction, i)
                return True
        return False

    def select_all(self, flag=True):
        self.setSelected(flag)
        for i in range(self.childCount()):
            self.child(i).setSelected(flag)

    def _on_test_add(self, test, index):
        self.insertChild(index, TreeItem(self._tm, test))

    def _on_test_delete(self, index):
        self.takeChild(index)

    def _on_name_changed(self):
        self.setText(0, self.suite.name())

    def __hash__(self):
        return self.suite.id.__hash__()

    def set_theme(self):
        self.setIcon(0, QIcon(self._tm.get_image('files/c')))
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

    def __hash__(self):
        return self.test.id.__hash__()

    def _on_name_changed(self):
        self.setText(0, self.test.get('desc', ''))
        if not self.text(0).strip():
            self.setText(0, self.test.get('name', '-'))

    def set_theme(self):
        self.setFont(0, self._tm.font_medium)
        match self.test.get('status', UnitTest.CHANGED):
            case UnitTest.PASSED:
                self.setIcon(0, QIcon(self._tm.get_image('icons/passed', color=self._tm['TestPassed'].name())))
            case UnitTest.FAILED:
                self.setIcon(0, QIcon(self._tm.get_image('icons/failed', color=self._tm['TestFailed'].name())))
            case UnitTest.CHANGED:
                self.setIcon(0, QIcon(self._tm.get_image('icons/running', color=self._tm['TestInProgress'].name())))


