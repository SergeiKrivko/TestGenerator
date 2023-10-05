import os
from typing import Any

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox

from language.utils import get_files
from ui.tree_widget import TreeWidget, TreeWidgetItemCheckable


class BuildField(QWidget):
    def __init__(self, tm, key: str, default=None):
        super().__init__()
        self.tm = tm
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

    def set_theme(self):
        pass


class LineField(BuildField):
    def __init__(self, tm, key, default='', name=''):
        super().__init__(tm, key, default)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._label = QLabel(name)
        layout.addWidget(self._label)
        if not name:
            self._label.hide()

        self._line_edit = QLineEdit()
        layout.addWidget(self._line_edit)

    def value(self):
        return self._line_edit.text()

    def set_value(self, value):
        self._line_edit.setText(str(value))

    def set_theme(self):
        super().set_theme()
        for el in [self._label, self._line_edit]:
            self.tm.auto_css(el)


class ComboFiled(BuildField):
    def __init__(self, tm, key, children: dict[int: list[BuildField]], default=0, name=''):
        super().__init__(tm, key, default)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._label = QLabel(name)
        layout.addWidget(self._label)
        if not name:
            self._label.hide()

        self._combo_box = QComboBox()
        self._combo_box.addItems(list(children.keys()))
        layout.addWidget(self._combo_box)

        self._children_layout = QVBoxLayout()
        layout.addLayout(self._children_layout)

        if children:
            self._children = children
            for item in self._children.values():
                for el in item:
                    self._children_layout.addWidget(item)

    def show_children(self):
        for key, item in self._children:
            if key == self.value():
                for el in item:
                    el.show()
            else:
                for el in item:
                    el.hide()

    def value(self):
        return self._combo_box.currentIndex()

    def set_value(self, value):
        self._combo_box.setCurrentIndex(value)
        self.show_children()


class TreeField(BuildField):
    def __init__(self, tm, key, path='', files=tuple(), name=''):
        super().__init__(tm, key, [])
        self._files = list(files)
        self._path = path
        self._data = dict()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._label = QLabel(name)
        layout.addWidget(self._label)
        if not name:
            self._label.hide()

        self._tree_widget = TreeWidget(self.tm, TreeWidget.CHECKABLE)
        self._tree_widget.setFixedHeight(320)
        layout.addWidget(self._tree_widget)

    def set_value(self, value: list):
        self._update_tree([] if not isinstance(value, list) else value)

    def value(self):
        lst = []
        for key, item in self._data.items():
            if item:
                lst.append(key)
        return lst

    def _set_file_status(self, file, status):
        self._data[file] = status

    def _update_tree(self, files):
        self._tree_widget.clear()
        for el in get_files(self._path, self._files):
            el = os.path.relpath(el, self._path).replace('\\', '/')
            lst = el.split('/')[:-1]
            tree_elem = TreeElement(self.tm, el)
            self._tree_widget.add_item(tree_elem, key=lst)
            self._connect_tree_elem(tree_elem, el)
            if el in files:
                tree_elem.set_checked(True)
        self._tree_widget.set_theme()

    def _connect_tree_elem(self, elem: 'TreeElement', path):
        elem.stateChanged.connect(lambda flag: self._set_file_status(path, flag))

    def set_theme(self):
        self.tm.auto_css(self._label)
        self._tree_widget.set_theme()


class TreeElement(TreeWidgetItemCheckable):
    def __init__(self, tm, path):
        super().__init__(tm, os.path.basename(path))
        self.path = path

    def set_checked(self, flag):
        if self._checkbox.isChecked() == flag:
            return
        self._checkbox.setChecked(flag)

    def set_theme(self):
        super().set_theme()
