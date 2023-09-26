import os
import shutil

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QListWidgetItem, QTreeWidget, \
    QTreeWidgetItem

from settings.settings_manager import SettingsManager
from ui.button import Button
from unit_testing.check_converter import CheckConverter
from unit_testing.test_edit import UnitTestEdit
from unit_testing.unit_test import UnitTest, UnitTestSuite

BUTTONS_MAX_WIDTH = 40


class UnitTestingWidget(QWidget):
    def __init__(self, sm: SettingsManager, cm, tm):
        super().__init__()
        self.sm = sm
        self.cm = cm
        self.tm = tm

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(left_layout, 1)

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
        self.data_dir = f"{self.sm.data_lab_path()}/unit_tests"
        self._tree_widget.clear()
        if not os.path.isdir(self.data_dir):
            return
        for el in os.listdir(self.data_dir):
            if os.path.isdir(os.path.join(self.data_dir, el)):
                self._tree_widget.addTopLevelItem(item := TreeModuleItem(self.tm, os.path.join(self.data_dir, el)))
                item.load()
                item.set_theme()

    def store_task(self):
        if not self._tree_widget.topLevelItemCount():
            if os.path.isdir(self.data_dir):
                shutil.rmtree(self.data_dir)
            return

        converter = CheckConverter(self.sm.lab_path())
        for i in range(self._tree_widget.topLevelItemCount()):
            item = self._tree_widget.topLevelItem(i)
            if not isinstance(item, TreeModuleItem):
                continue
            item.store()
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

    def set_theme(self):
        for el in [self._tree_widget, self.button_add, self.button_delete, self.button_down,
                   self.button_up, self.button_copy, self.button_add_dir]:
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

    def _create_temp_file(self):
        path = f"{self._suite.path()}/temp_{self._temp_file_index}"
        self._temp_file_index += 1
        return path

    def set_theme(self):
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


