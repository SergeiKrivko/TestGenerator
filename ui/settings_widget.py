import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QCheckBox, QComboBox, QSpinBox, \
    QDoubleSpinBox, QPushButton, QFileDialog

from ui.message_box import MessageBox

KEY_GLOBAL = 0
KEY_LOCAL = 1
KEY_SMART = 2


class _Widget(QWidget):
    def __init__(self, key=None, key_type=None, default=None):
        super().__init__()
        self._tm = None
        self._sm = None
        self._key = key
        self._key_type = key_type
        self._default = default
        self._children = dict()

    def set_sm(self, sm):
        self._sm = sm
        for item in self._children.values():
            for el in item:
                if hasattr(el, 'set_sm'):
                    el.set_sm(sm)

    def set_tm(self, tm):
        self._tm = tm
        for item in self._children.values():
            for el in item:
                if hasattr(el, 'set_tm'):
                    el.set_tm(tm)

    def set_key_type(self, key_type):
        if self._key_type is None:
            self._key_type = key_type
        for item in self._children.values():
            for el in item:
                if hasattr(el, 'set_key_type'):
                    el.set_key_type(key_type)

    def _get(self):
        if self._key is None:
            return
        if self._key_type == KEY_GLOBAL or self._key_type is None:
            return self._sm.get_general(self._key, self._default)
        if self._key_type == KEY_LOCAL:
            return self._sm.get(self._key, self._default)
        return self._sm.get_smart(self._key, self._default)

    def _set(self, value):
        if self._key is None:
            return
        if self._key_type == KEY_GLOBAL or self._key_type is None:
            return self._sm.set_general(self._key, value)
        return self._sm.set(self._key, value)

    def _del(self):
        if self._key_type == KEY_GLOBAL or self._key_type is None:
            self._sm.remove_general(self._key)
        else:
            self._sm.remove(self._key)

    def delete_value(self):
        self._del()
        for item in self._children.values():
            for el in item:
                if hasattr(el, 'delete_value'):
                    el.delete_value()

    def set_value(self, value):
        pass

    def show_children(self):
        for item in self._children.values():
            for el in item:
                el.show()

    def load_value(self):
        self.set_value(self._get())
        self.show_children()
        for item in self._children.values():
            for el in item:
                if el.isHidden():
                    if hasattr(el, 'delete_value'):
                        el.delete_value()
                else:
                    if hasattr(el, 'load_value'):
                        el.load_value()

    def set_theme(self):
        pass


class LineEdit(_Widget):
    STD_WIDTH = 150

    def __init__(self, name='', text='', key=None, key_type=None, width=None, check_func=None):
        super().__init__(key, key_type, text)
        self._check_func = check_func
        self._last_value = text

        layout = QHBoxLayout() if width is None or width <= LineEdit.STD_WIDTH else QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel(name)
        layout.addWidget(self._label)

        self._line_edit = QLineEdit()
        self._line_edit.setText(text)
        self._line_edit.editingFinished.connect(self._on_editing_finished)
        self._line_edit.setMaximumWidth(width if width is not None else LineEdit.STD_WIDTH)
        layout.addWidget(self._line_edit)

    def _on_editing_finished(self):
        if self._check_func is None or self._check_func(self._line_edit.text()):
            self._last_value = self._line_edit.text()
            self._set(self._line_edit.text())
        else:
            MessageBox(MessageBox.Warning, "Ошибка", "Некорректное значение", self._tm)
            self._line_edit.setText(self._last_value)

    def set_value(self, text):
        self._last_value = str(text)
        self._set(str(text))
        self._line_edit.setText(str(text))

    def set_theme(self):
        self._tm.auto_css(self._line_edit)
        self._tm.auto_css(self._label)


class CheckBox(_Widget):
    def __init__(self, name, state=False, key=None, key_type=None, children: dict = None):
        super().__init__(key, key_type=None, default=state)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)

        if children is not None:
            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(0, 0, 0, 0)
            self.setLayout(main_layout)
            main_layout.addLayout(layout)
        else:
            self.setLayout(layout)

        self._checkbox = QCheckBox()
        self._checkbox.stateChanged.connect(self._on_state_changed)
        layout.addWidget(self._checkbox)

        self._label = QLabel(name)
        layout.addWidget(self._label)

        if children is not None:
            children_layout = QVBoxLayout()
            children_layout.setContentsMargins(20, 0, 0, 0)
            main_layout.addLayout(children_layout)
            for key, item in children.items():
                self._children[key] = []
                if isinstance(item, list):
                    for el in item:
                        self._children[key].append(el)
                        children_layout.addWidget(el)
                else:
                    self._children[key].append(item)
                    children_layout.addWidget(item)
        if key_type is not None:
            self.set_key_type(key_type)

    def _on_state_changed(self):
        self._set(self._checkbox.isChecked())
        self.load_value()

    def show_children(self):
        for key, item in self._children.items():
            for el in item:
                if key == self._checkbox.isChecked():
                    el.show()
                else:
                    el.hide()

    def set_value(self, value):
        if not value or value == 'false' or value == 'False':
            value = 0
        else:
            value = 1
        self._set(value)
        self._checkbox.setChecked(bool(value))

    def set_theme(self):
        self._tm.auto_css(self._checkbox)
        self._tm.auto_css(self._label)
        for item in self._children.values():
            for el in item:
                el.set_theme()


class ComboBox(_Widget):
    STD_WIDTH = 150

    def __init__(self, name: str, values: list[str], key=None, key_type=None, width=None, text_mode=False,
                 on_state_changed=None):
        super().__init__(key, key_type, 0)
        self._text_mode = text_mode
        self._on_state_changed = on_state_changed

        layout = QHBoxLayout() if width is None or width <= ComboBox.STD_WIDTH else QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel(name)
        layout.addWidget(self._label)

        self._combo_box = QComboBox()
        self._combo_box.addItems(values)
        self._combo_box.currentIndexChanged.connect(self._on_index_changed)
        self._combo_box.setFixedWidth(width if width is not None else ComboBox.STD_WIDTH)
        layout.addWidget(self._combo_box)

    def _on_index_changed(self, index):
        if self._text_mode:
            self._set(self._combo_box.currentText())
        else:
            self._set(index)
        if self._on_state_changed:
            self._on_state_changed()

    def set_value(self, value):
        if self._text_mode:
            self._set(str(value))
            self._combo_box.setCurrentText(str(value))
            return
        if not isinstance(value, int):
            self.set_value(0)
            return
        self._set(value)
        self._combo_box.setCurrentIndex(value)

    def set_theme(self):
        self._tm.auto_css(self._combo_box)
        self._tm.auto_css(self._label)


class SpinBox(_Widget):
    STD_WIDTH = 80

    def __init__(self, name: str, min_value=0, max_value=100, key=None, key_type=None, width=None, double=False):
        super().__init__(key, key_type, 0)
        self._double = double
        self._type = float if double else int

        layout = QHBoxLayout() if width is None or width <= SpinBox.STD_WIDTH else QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel(name)
        layout.addWidget(self._label)

        self._spin_box = QDoubleSpinBox() if double else QSpinBox()
        self._spin_box.setMinimum(min_value)
        self._spin_box.setMaximum(max_value)
        self._spin_box.valueChanged.connect(self._on_value_changed)
        self._spin_box.setFixedWidth(width if width is not None else SpinBox.STD_WIDTH)
        layout.addWidget(self._spin_box)

    def _on_value_changed(self, value):
        self._set(value)

    def set_value(self, value):
        self._set(self._type(value))
        self._spin_box.setValue(self._type(value))

    def set_theme(self):
        self._tm.auto_css(self._spin_box)
        self._tm.auto_css(self._label)


class FileEdit(_Widget):
    MODE_OPEN = 0
    MODE_SAVE = 1
    MODE_DIR = 2

    def __init__(self, name='', mode=MODE_OPEN, default='', key=None, key_type=None):
        super().__init__(key, key_type)
        self._last_value = default
        self._mode = mode

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel(name)
        layout.addWidget(self._label)

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(h_layout)

        self._line_edit = QLineEdit()
        self._line_edit.editingFinished.connect(self._on_editing_finished)
        h_layout.addWidget(self._line_edit)

        self._button = QPushButton("Обзор")
        self._button.setFixedSize(70, 22)
        h_layout.addWidget(self._button)

    def _on_editing_finished(self):
        if self._mode == FileEdit.MODE_OPEN and os.path.isfile(self._line_edit.text()):
            self._last_value = self._line_edit.text()
            self._set(self._line_edit.text())
        elif self._mode == FileEdit.MODE_SAVE and os.path.isdir(os.path.split(self._line_edit.text())[0]):
            self._last_value = self._line_edit.text()
            self._set(self._line_edit.text())
        elif self._mode == FileEdit.MODE_DIR and os.path.isdir(self._line_edit.text()):
            self._last_value = self._line_edit.text()
            self._set(self._line_edit.text())
        else:
            # MessageBox(MessageBox.Warning, "Ошибка", "Некорректное значение", self._tm)
            self._line_edit.setText(self._last_value)

    def _on_button_clicked(self):
        path = None
        if self._mode == FileEdit.MODE_OPEN:
            path = QFileDialog.getOpenFileName()
        elif self._mode == FileEdit.MODE_SAVE:
            path = QFileDialog.getSaveFileName()
        elif self._mode == FileEdit.MODE_DIR:
            path = QFileDialog.getExistingDirectory()
        if path:
            self.set_value(path)

    def set_value(self, text):
        self._last_value = str(text)
        self._set(str(text))
        self._line_edit.setText(str(text))

    def set_theme(self):
        self._tm.auto_css(self._line_edit)
        self._tm.auto_css(self._label)
        self._tm.auto_css(self._button)


class SwitchBox(_Widget):
    def __init__(self, condition, children: dict, key_type=None):
        super().__init__()
        self._condition = condition

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        for key, item in children.items():
            self._children[key] = []
            if isinstance(item, list):
                for el in item:
                    self._children[key].append(el)
                    layout.addWidget(el)
            else:
                self._children[key].append(item)
                layout.addWidget(item)
        if key_type is not None:
            self.set_key_type(key_type)

    def show_children(self):
        value = self._condition()
        for key, item in self._children.items():
            if key == value:
                for el in item:
                    el.show()
            else:
                for el in item:
                    el.hide()

    def set_theme(self):
        for item in self._children.values():
            for el in item:
                el.set_theme()


class SettingsWidget(QWidget):
    def __init__(self, sm, tm, *args, key_type=None):
        super().__init__()
        self._sm = sm
        self._tm = tm
        self._widgets = []

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        for el in args:
            self._widgets.append(el)
            layout.addWidget(el)
            if isinstance(el, _Widget):
                el.set_sm(self._sm)
                el.set_tm(self._tm)

        if key_type is not None:
            for el in self._widgets:
                if hasattr(el, 'set_key_type'):
                    el.set_key_type(key_type)
        self.load_values()

    def load_values(self):
        for el in self._widgets:
            if hasattr(el, 'load_value'):
                el.load_value()

    def set_theme(self):
        for el in self._widgets:
            if hasattr(el, 'set_theme'):
                el.set_theme()
