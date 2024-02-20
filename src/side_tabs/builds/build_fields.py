import os
from typing import Any

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QHBoxLayout, QCheckBox

from src.backend.backend_types.program import Program
from src.language.utils import get_files
from src.ui.program_box import ProgramBox
from src.ui.tree_widget import TreeWidget, TreeWidgetItemCheckable


class BuildField(QWidget):
    valueChanged = pyqtSignal(object)

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
        self._line_edit.textEdited.connect(lambda: self.valueChanged.emit(self._line_edit.text()))
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
        self.set_theme()

    def _connect_tree_elem(self, elem: 'TreeElement', path):
        elem.stateChanged.connect(lambda flag: self._set_file_status(path, flag))

    def set_theme(self):
        self.tm.auto_css(self._label)
        self._tree_widget.set_theme()
        self._tree_widget.setStyleSheet(f"background-color: {self.tm['MainColor']};")


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


class ProgramField(BuildField):
    def __init__(self, sm, tm, program: Program, name='', checkbox=True):
        super().__init__(tm, program.key(), program.basic())
        self.sm = sm
        self._use_checkbox = checkbox

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self._label = QLabel(name)
        main_layout.addWidget(self._label)
        if not name:
            self._label.hide()

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 0, 0, 0)
        main_layout.addLayout(layout)

        self._checkbox = QCheckBox("По умолчанию")
        if not self._use_checkbox:
            self._checkbox.hide()
        layout.addWidget(self._checkbox)

        self._program_box = ProgramBox(program, sm, tm)
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

    def set_theme(self):
        for el in [self._label, self._checkbox]:
            self.tm.auto_css(el)
        self._program_box.set_theme()


class CheckboxField(BuildField):
    def __init__(self, tm, key, default='', name=''):
        super().__init__(tm, key, default)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._checkbox = QCheckBox(name)
        layout.addWidget(self._checkbox)

    def value(self):
        return self._checkbox.isChecked()

    def set_value(self, value):
        self._checkbox.setChecked(value)

    def set_theme(self):
        super().set_theme()
        for el in [self._checkbox]:
            self.tm.auto_css(el)
