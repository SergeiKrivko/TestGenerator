import os
from typing import Any

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QHBoxLayout, QCheckBox

from language.utils import get_files
from ui.button import Button
from ui.tree_widget import TreeWidget, TreeWidgetItemCheckable


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
    def __init__(self, sm, tm, key, name, file):
        super().__init__(tm, key, sm.get('file'))
        self.sm = sm
        self._file = file
        self._items = []

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self.label = QLabel(name)
        main_layout.addWidget(self.label)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(checkbox_layout)

        self._checkbox = QCheckBox("По умолчанию")
        self._checkbox.stateChanged.connect(self._on_state_changed)
        checkbox_layout.addWidget(self._checkbox)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        main_layout.addLayout(layout)

        self.combo_box = QComboBox()
        layout.addWidget(self.combo_box)

        self.line_edit = QLineEdit()
        self.line_edit.hide()
        self.line_edit.returnPressed.connect(self._on_return_pressed)
        layout.addWidget(self.line_edit)

        self.button_update = Button(None, 'update')
        layout.addWidget(self.button_update)
        self.button_update.setFixedSize(24, 22)

        self.button_add = Button(None, 'plus')
        layout.addWidget(self.button_add)
        self.button_add.clicked.connect(self._on_plus_clicked)
        self.button_add.setFixedSize(24, 22)

        self.button_update.clicked.connect(self.sm.start_search)
        self.sm.searching_complete.connect(self.update_items)
        self.update_items()

    def set_items(self, items: list):
        text = self.combo_box.currentText()
        if text not in items:
            items.append(text)
        self._items = items
        self.combo_box.clear()
        self.combo_box.addItems(items)
        self.combo_box.setCurrentText(text)

    def _on_state_changed(self):
        if self._checkbox.isChecked():
            self.line_edit.hide()
            self.combo_box.hide()
            self.button_add.hide()
            self.button_update.hide()
        else:
            self.combo_box.show()
            self.button_add.show()
            self.button_update.show()

    def add_item(self, item: str):
        self._items.append(item)
        self.combo_box.addItem(item, None)

    def _on_plus_clicked(self):
        self.combo_box.hide()
        self.line_edit.show()
        self.line_edit.setText(self.combo_box.currentText())
        self.line_edit.selectAll()
        self.line_edit.setFocus()

    def _on_return_pressed(self):
        if text := self.line_edit.text().strip():
            self.combo_box.addItems([text])
            self.combo_box.setCurrentText(text)
        self.line_edit.hide()
        self.combo_box.show()

    def _on_editing_finished(self):
        self.line_edit.hide()
        self.combo_box.show()

    def update_items(self):
        self.set_items(self.sm.programs.get(self._file, []))

    def set_value(self, text: str | None):
        if text is None:
            self._checkbox.setChecked(True)
        else:
            self._checkbox.setChecked(False)
            if text not in self._items:
                self.add_item(text)
            self.update_items()
            self.combo_box.setCurrentText(text)

    def value(self):
        if self._checkbox.isChecked():
            return None
        return self.combo_box.currentText()

    def set_theme(self):
        for el in [self.combo_box, self.button_update, self.button_add, self.label,
                   self._checkbox]:
            self.tm.auto_css(el)


class CheckboxField(BuildField):
    def __init__(self, tm, key, default='', name=''):
        super().__init__(tm, key, default)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._checkbox = QCheckBox()
        layout.addWidget(self._checkbox)

        self._label = QLabel(name)
        layout.addWidget(self._label)
        if not name:
            self._label.hide()

    def value(self):
        return self._checkbox.isChecked()

    def set_value(self, value):
        self._checkbox.setChecked(value)

    def set_theme(self):
        super().set_theme()
        for el in [self._label, self._checkbox]:
            self.tm.auto_css(el)
