import os
import shutil

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QListWidgetItem, QTreeWidget, \
    QTreeWidgetItem

from code_tab.compiler_errors_window import CompilerErrorWindow
from language.build.commands_list import MakeScenarioBox
from language.languages import languages
from language.utils import get_files
from settings.settings_manager import SettingsManager
from tests.commands import CommandManager
from ui.button import Button
from unit_testing.check_converter import CheckConverter
from unit_testing.test_edit import UnitTestEdit
from unit_testing.unit_test import UnitTest, UnitTestSuite

BUTTONS_MAX_WIDTH = 40


class UnitTestingWidget(QWidget):
    def __init__(self, sm: SettingsManager, cm: CommandManager, tm):
        super().__init__()
        self.sm = sm
        self.cm = cm
        self.tm = tm

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(left_layout, 1)

        self.scenario_box = MakeScenarioBox(self.sm)
        left_layout.addWidget(self.scenario_box)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addLayout(buttons_layout)

        self.button_add_dir = Button(self.tm, 'add_dir', css='Bg')
        self.button_add_dir.setFixedHeight(22)
        self.button_add_dir.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_add_dir.clicked.connect(self.add_section)
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

        self._test_edit = UnitTestEdit(self.tm)
        right_layout.addWidget(self._test_edit)

        self.data_dir = ""
        self.sm.startChangeTask.connect(self.store_task)
        self.sm.finishChangeTask.connect(self.open_task)

    def open_task(self):
        self.scenario_box.load(self.sm.get_task('unit_test_build', ''))
        self.data_dir = f"{self.sm.data_lab_path()}/unit_tests"
        self._tree_widget.clear()
        if not os.path.isdir(self.data_dir):
            return
        items = []
        for el in os.listdir(self.data_dir):
            if os.path.isdir(os.path.join(self.data_dir, el)):
                items.append(el)
                self._tree_widget.addTopLevelItem(item := TreeModuleItem(self.tm, os.path.join(self.data_dir, el)))
                item.load()
                item.set_theme()
        for el in get_files(self.sm.lab_path(), '.c'):
            name = os.path.basename(el)
            if name not in items and not name.startswith('check_') and not name.startswith('main.'):
                self._tree_widget.addTopLevelItem(item := TreeModuleItem(self.tm, os.path.join(self.data_dir, name)))
                item.set_theme()

    def run_tests(self):
        self.store_task()
        res = self.cm.run_scenarios(self.scenario_box.current_scenario())[0]
        if res.returncode:
            dialog = CompilerErrorWindow(res.stderr, self.tm, languages[
                self.sm.get('language', 'C')].get('compiler_mask'))
            dialog.exec()
            return
        res = self.cm.cmd_command(f"{self.sm.lab_path()}/{self.scenario_box.current_scenario()['data']['name']}",
                                  cwd=self.sm.lab_path())
        items = []
        for i in range(self._tree_widget.topLevelItemCount()):
            items.extend(self._tree_widget.topLevelItem(i).get_items())
        i = 0
        for line in res.stdout.split('\n'):
            if line.count(':') >= 6:
                lst = line.split(':')
                items[i].test['status'] = UnitTest.PASSED if lst[2] == 'P' else UnitTest.FAILED
                items[i].test['test_res'] = ':'.join(lst[6:])
                items[i].set_theme()

    def store_task(self):
        self._test_edit.store_test()
        if self.scenario_box.current_scenario() is not None:
            self.sm.set_task('unit_test_build', self.scenario_box.current_scenario())
        if not self._tree_widget.topLevelItemCount():
            if os.path.isdir(self.data_dir):
                shutil.rmtree(self.data_dir)
            return

        converter = CheckConverter(os.path.join(self.sm.lab_path(), self.sm.get('unit_tests_dir', 'unit_tests')))
        for i in range(self._tree_widget.topLevelItemCount()):
            item = self._tree_widget.topLevelItem(i)
            if not isinstance(item, TreeModuleItem):
                continue
            module = converter.add_module(item.name())
            item.to_converter(module)
        converter.convert()

    def _on_test_selected(self):
        item = self._tree_widget.currentItem()
        if isinstance(item, TreeItem):
            self._test_edit.open_test(item.test)
        else:
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
        selected = self._tree_widget.selectedItems()
        if len(selected) == 0:
            return
        selected = selected[0]
        for i in range(self._tree_widget.topLevelItemCount()):
            if self._tree_widget.topLevelItem(i).add_item(selected):
                break

    def add_section(self):
        selected = self._tree_widget.selectedItems()
        if len(selected) == 0:
            return
        selected = selected[0]
        for i in range(self._tree_widget.topLevelItemCount()):
            if self._tree_widget.topLevelItem(i).add_section(selected):
                break

    def hide(self) -> None:
        if not self.isHidden():
            self.store_task()
        super().hide()

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


class TreeModuleItem(QTreeWidgetItem):
    def __init__(self, tm, data_path):
        super().__init__()
        self._tm = tm
        self._data_path = data_path
        self._data_path2 = os.path.split(self._data_path)[0]
        self.setText(0, os.path.basename(data_path))

        self._dirs = dict()

    def name(self):
        return os.path.basename(self._data_path)

    def load(self):
        for el in os.listdir(self._data_path):
            if os.path.isdir(os.path.join(self._data_path, el)):
                self.addChild(item := TreeSectionItem(self._tm, UnitTestSuite(
                    self._data_path2, os.path.basename(self._data_path), el)))
                item.load()

    def get_items(self):
        for i in range(self.childCount()):
            for el in self.child(i).get_items():
                yield el

    def add_item(self, after: QTreeWidgetItem):
        if isinstance(after, TreeSectionItem):
            after.add_item()
            return True
        elif isinstance(after, TreeItem):
            for i in range(self.childCount()):
                if self.child(i).add_item(after):
                    return True
            return False
        return False

    def delete(self, item):
        if isinstance(item, TreeSectionItem):
            for i in range(self.childCount()):
                if self.child(i) == item:
                    self.takeChild(i)
                    item.delete_self()
                    return True
        elif isinstance(item, TreeItem):
            for i in range(self.childCount()):
                if self.child(i).delete(item):
                    return True
        return False

    def store(self):
        for i in range(self.childCount()):
            self.child(i).store()

    def to_converter(self, module):
        for i in range(self.childCount()):
            suite = module.add_suite(self.child(i).name())
            self.child(i).to_converter(suite)

    def add_section(self, after=None):
        item = TreeSectionItem(self._tm, UnitTestSuite(self._data_path2, os.path.basename(self._data_path),
                                                       self._create_new_path()))
        if after is not None:
            for i in range(self.childCount()):
                if self.child(i) == after:
                    self.insertChild(i + 1, item)
                    return True
            return False
        self.addChild(item)
        return True

    def _create_new_path(self):
        i = 0
        while os.path.isdir(f"{self._data_path}/NewSection{i}"):
            i += 1
        return f"NewSection{i}"

    def set_theme(self):
        self.setIcon(0, QIcon(self._tm.get_image('c')))
        self.setFont(0, self._tm.font_medium)
        for i in range(self.childCount()):
            self.child(i).set_theme()


class TreeSectionItem(QTreeWidgetItem):
    def __init__(self, tm, suite: UnitTestSuite):
        super().__init__()
        self._tm = tm
        self._suite = suite
        self.setText(0, self._suite.name())

        self._files = dict()
        self._temp_file_index = 0

        os.makedirs(self._suite.path(), exist_ok=True)

    def load(self):
        self._temp_file_index = 0
        self._files.clear()
        for el in os.listdir(self._suite.path()):
            if el.endswith('.json'):
                path = os.path.abspath(os.path.join(self._suite.path(), el))
                item = TreeItem(self._tm, UnitTest(path))
                self._files[el] = item
                self.addChild(item)

    def name(self):
        return self._suite.name()

    def to_converter(self, suite):
        for i in range(self.childCount()):
            suite.add_test(self.child(i).test)

    def delete_self(self):
        self._suite.delete_dir()

    def delete(self, item):
        for i in range(self.childCount()):
            if self.child(i) == item:
                self.takeChild(i)
                item.test.delete_file()
                return True

    def store(self):
        if not self.childCount():
            return
        for i in range(self.childCount()):
            item = self.child(i)
            if not isinstance(item, TreeItem):
                continue
            item.test.store()
            path = os.path.abspath(f"{self._suite.path()}/{i}.json")
            if item.test.path() != path:
                if path in self._files:
                    self._files[os.path.basename(path)].test.rename_file(self._create_temp_file())
                    self._files.pop(os.path.basename(path))
                item.test.rename_file(path)

    def add_item(self, after=None):
        item = TreeItem(self._tm, UnitTest(self._create_temp_file()))
        if after is not None:
            for i in range(self.childCount()):
                if self.child(i) == after:
                    self.insertChild(i + 1, item)
                    return True
            return False
        self.addChild(item)
        return True

    def get_items(self):
        for i in range(self.childCount()):
            yield self.child(i)

    def _create_temp_file(self):
        path = f"{self._suite.path()}/temp_{self._temp_file_index}"
        self._temp_file_index += 1
        return path

    def set_theme(self):
        self.setIcon(0, QIcon(self._tm.get_image('directory')))
        self.setFont(0, self._tm.font_medium)
        for i in range(self.childCount()):
            self.child(i).set_theme()


class TreeItem(QTreeWidgetItem):
    def __init__(self, tm, test: UnitTest):
        super().__init__()
        self._tm = tm
        self.test = test
        self.setText(0, self.test.get('desc', ''))
        if not self.text(0).strip():
            self.setText(0, self.test.get('name', '-'))
        self.set_theme()

    def set_theme(self):
        self.setFont(0, self._tm.font_medium)
        match self.test.get('status', UnitTest.CHANGED):
            case UnitTest.PASSED:
                self.setIcon(0, QIcon(self._tm.get_image('passed', color=self._tm['TestPassed'].name())))
            case UnitTest.FAILED:
                self.setIcon(0, QIcon(self._tm.get_image('failed', color=self._tm['TestFailed'].name())))
            case UnitTest.CHANGED:
                self.setIcon(0, QIcon(self._tm.get_image('running', color=self._tm['TestInProgress'].name())))


