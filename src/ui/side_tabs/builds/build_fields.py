import asyncio
import os
from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQtUIkit.widgets import *
from qasync import asyncSlot

from src.backend.backend_types.program import Program
from src.backend.commands import get_files
from src.ui.widgets.program_box import ProgramBox


class BuildField(KitVBoxLayout):
    valueChanged = pyqtSignal(object)

    def __init__(self, key: str, default=None):
        super().__init__()
        self._key = key
        self._children: dict[Any: list[BuildField]] = dict()
        self._default = default

    def value(self):
        return None

    def set_value(self, value):
        pass

    def get_children(self):
        if isinstance(self._children, dict):
            return

    def load(self, data):
        if len(self._children):
            children_data = data.get(self._key, dict()).get('data', dict())
            self.set_value(value := data.get(self._key, dict()).get('type', self._default))
            for el in self._children[value]:
                el.load(children_data)
        else:
            self.set_value(data.get(self._key, self._default))

    def store(self, data: dict):
        if len(self._children):
            children_data = data.get(self._key, dict()).get('data')
            data[self._key]['type'] = self.value()
            for el in self._children[self.value()]:
                el.store(children_data)
        else:
            data[self._key] = self.value()


class LineField(BuildField):
    def __init__(self, key, default='', name=''):
        super().__init__(key, default)
        self.spacing = 6

        self._label = KitLabel(name)
        self.addWidget(self._label)
        if not name:
            self._label.hide()

        self._line_edit = KitLineEdit()
        self._line_edit.textEdited.connect(lambda: self.valueChanged.emit(self._line_edit.text))
        self.addWidget(self._line_edit)

    def value(self):
        return self._line_edit.text

    def set_value(self, value):
        self._line_edit.setText(str(value))


# class ComboFiled(BuildField):
#     def __init__(self, key, children: dict[int: list[BuildField]], default=0, name=''):
#         super().__init__(key, default)
#
#         self._label = KitLabel(name)
#         self.addWidget(self._label)
#         if not name:
#             self._label.hide()
#
#         self._combo_box = KitComboBox()
#         for el in children.keys():
#             if isinstance(el, tu)
#             self._combo_box.addItem(KitComboBoxItem(*el))
#         self._combo_box.addItems(list(children.keys()))
#         self.addWidget(self._combo_box)
#
#         self._children_layout = KitVBoxLayout()
#         self.addWidget(self._children_layout)
#
#         if children:
#             self._children = children
#             for item in self._children.values():
#                 for el in item:
#                     self._children_layout.addWidget(item)
#
#     def show_children(self):
#         for key, item in self._children:
#             if key == self.value():
#                 for el in item:
#                     el.show()
#             else:
#                 for el in item:
#                     el.hide()
#
#     def value(self):
#         return self._combo_box.currentIndex()
#
#     def set_value(self, value):
#         self._combo_box.setCurrentIndex(value)
#         self.show_children()


class TreeField(BuildField):
    def __init__(self, key, path='', files=tuple(), name=''):
        super().__init__(key, [])
        self._extensions = list(files)
        self._path = path
        self._data = dict()
        self.__items: dict[str: 'TreeFile'] = dict()

        self._label = KitLabel(name)
        self.addWidget(self._label)
        if not name:
            self._label.hide()

        self._tree_widget = KitTreeWidget()
        self._tree_widget.selection_type = KitTreeWidget.SelectionType.NO
        self._tree_widget.setFixedHeight(320)
        self.addWidget(self._tree_widget)

    def set_value(self, value: list):
        self._update_tree([] if not isinstance(value, list) else value)

    def value(self):
        lst = []
        for item in self.__items.values():
            if isinstance(item, TreeFile) and item.state:
                lst.append(item.path)
        return lst

    @asyncSlot()
    async def _update_tree(self, files):
        for file in get_files(self._path, self._extensions):
            file = os.path.relpath(file, self._path).replace('\\', '/')
            self._add_item(item := TreeFile(file), file)
            if file in files:
                item.state = True
            await asyncio.sleep(0.01)

    def _add_item(self, item, path: str):
        self.__items[path] = item
        if '/' not in path:
            self._tree_widget.addItem(item)
        elif os.path.dirname(path) in self.__items:
            self.__items[os.path.dirname(path)].addItem(item)
        else:
            lst = []
            parent = self._tree_widget
            for el in path.split('/')[:-1]:
                lst.append(el)
                path_part = '/'.join(lst)
                if path_part in self.__items:
                    parent = self.__items[path_part]
                else:
                    it = TreeElement(path_part)
                    self.__items[path_part] = it
                    parent.addItem(it)
                    parent = it
            parent.addItem(item)


class TreeElement(KitTreeWidgetItem):
    def __init__(self, path):
        super().__init__(os.path.basename(path))
        self.checkable = True
        self.path = path


class TreeFile(TreeElement):
    pass


class ProgramField(BuildField):
    def __init__(self, bm, program: Program, name='', checkbox=True):
        super().__init__(program.key(), program.basic())
        self.bm = bm
        self._use_checkbox = checkbox
        self.spacing = 6

        self._label = KitLabel(name)
        self.addWidget(self._label)
        if not name:
            self._label.hide()

        layout = KitVBoxLayout()
        layout.spacing = 6
        layout.setContentsMargins(10, 0, 0, 0)
        self.addWidget(layout)

        self._checkbox = KitCheckBox("По умолчанию")
        if not self._use_checkbox:
            self._checkbox.hide()
        layout.addWidget(self._checkbox)

        self._program_box = ProgramBox(bm, program)
        layout.addWidget(self._program_box)

        self._checkbox.stateChanged.connect(self._program_box.setHidden)

    def value(self):
        if self._use_checkbox and self._checkbox.isChecked():
            return None
        return self._program_box.current().to_json()

    def set_value(self, value):
        if value is None and self._use_checkbox:
            self._checkbox.setChecked(True)
            self._program_box.hide()
        else:
            self._checkbox.setChecked(False)
            self._program_box.show()
            self._program_box.set_value(value)


class CheckboxField(BuildField):
    def __init__(self, key, default='', name=''):
        super().__init__(key, default)

        self._checkbox = KitCheckBox(name)
        self.addWidget(self._checkbox)

    def value(self):
        return self._checkbox.isChecked()

    def set_value(self, value):
        self._checkbox.setChecked(value)
