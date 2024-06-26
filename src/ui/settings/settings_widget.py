import json
import os.path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QSizePolicy
from PyQtUIkit.widgets import *

from src.backend.backend_types.program import Program
from src.backend.managers import BackendManager
from src.ui.widgets.program_box import ProgramBox

KEY_GLOBAL = 0
KEY_LOCAL: int = 1
KEY_DICT = 2
KEY_DATA = 3


class _Widget(KitVBoxLayout):
    valueChanged = pyqtSignal(object)

    def __init__(self, bm: BackendManager, key=None, key_type=None, default=None, not_delete_keys=False):
        super().__init__()
        self._bm = bm
        self._sm = bm.sm
        self._key = key
        self._delete_keys = not not_delete_keys
        self._key_type = key_type
        self._default = default
        self._children = dict()
        self._dict = dict()

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
        if self._key_type == KEY_DICT:
            return self._dict.get(self._key, self._default)
        if self._key_type == KEY_GLOBAL or self._key_type is None:
            return self._sm.get_general(self._key, self._default)
        if self._key_type == KEY_LOCAL:
            return self._sm.get(self._key, self._default)
        if self._key_type == KEY_DATA:
            return self._sm.get_data(self._key, self._default)

    def _set(self, value):
        if self._key is None:
            return
        if self._key_type == KEY_DICT:
            self._dict[self._key] = value
        elif self._key_type == KEY_GLOBAL or self._key_type is None:
            self._sm.set_general(self._key, value)
        elif self._key_type == KEY_DATA:
            self._sm.set_data(self._key, value)
        else:
            self._sm.set(self._key, value)
        self.valueChanged.emit(value)

    def _del(self):
        if self._key is None:
            return
        if self._key_type == KEY_DICT:
            if self._key in self._dict:
                self._dict.pop(self._key)
        elif self._key_type == KEY_GLOBAL or self._key_type is None:
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
        self.load_children()

    def load_children(self):
        for item in self._children.values():
            for el in item:
                if el.isHidden():
                    if hasattr(el, 'delete_value') and self._delete_keys:
                        el.delete_value()
                else:
                    if hasattr(el, 'load_value'):
                        el.load_value()

    def set_theme(self):
        pass


class LineEdit(_Widget):
    STD_WIDTH = 150

    def __init__(self, bm: BackendManager, name='', text='', key=None, key_type=None, width=None,
                 check_func=None, one_line=False):
        super().__init__(bm, key, key_type, text)
        self._check_func = check_func
        self._last_value = text

        if one_line:
            layout = KitHBoxLayout()
            self.addWidget(layout)
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        else:
            layout = self
        layout.spacing = 6

        self._label = KitLabel(name)
        self._label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(self._label)

        self._line_edit = KitLineEdit()
        self._line_edit.setText(text)
        self._line_edit.editingFinished.connect(self._on_editing_finished)
        self._line_edit.setMaximumWidth(width if width is not None else LineEdit.STD_WIDTH)
        layout.addWidget(self._line_edit)

    def _on_editing_finished(self):
        if self._check_func is None or self._check_func(self._line_edit.text):
            self._last_value = self._line_edit.text
            self._set(self._line_edit.text)
        else:
            KitDialog.danger(self, "Ошибка", "Некорректное значение")
            self._line_edit.setText(self._last_value)

    def set_value(self, text):
        self._last_value = str(text)
        self._set(str(text))
        self._line_edit.setText(str(text))


class TextEdit(_Widget):
    STD_WIDTH = 150

    def __init__(self, bm, name='', text='', key=None, key_type=None):
        super().__init__(bm, key, key_type, text)
        self._last_value = text

        self.spacing = 6

        self._label = KitLabel(name)
        self._label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.addWidget(self._label)

        self._text_edit = KitTextEdit()
        self._text_edit.setText(text)
        self._text_edit.textChanged.connect(self._on_text_changed)
        self.addWidget(self._text_edit)

    def _on_text_changed(self):
        self._set(self._text_edit.toPlainText())

    def set_value(self, text):
        self._last_value = str(text)
        self._set(str(text))
        self._text_edit.setText(str(text))


class CheckBox(_Widget):
    def __init__(self, bm: BackendManager, name, state=False, key=None, key_type=None, children: dict = None, not_delete_keys=False):
        super().__init__(bm, key, key_type=None, default=state, not_delete_keys=not_delete_keys)

        self._checkbox = KitCheckBox(name)
        self._checkbox.stateChanged.connect(self._on_state_changed)
        self.addWidget(self._checkbox)

        if children is not None:
            children_layout = KitVBoxLayout()
            children_layout.setContentsMargins(20, 0, 0, 0)
            self.addWidget(children_layout)
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
        if not value or value in {'false', 'False', '0'}:
            value = 0
        else:
            value = 1
        self._set(value)
        self._checkbox.setChecked(bool(value))


class ComboBox(_Widget):
    STD_WIDTH = 150

    def __init__(self, bm: BackendManager, name: str, values: list[str], key=None, key_type=None, width=None, text_mode=False,
                 on_state_changed=None, children: dict = None):
        super().__init__(bm, key, key_type=None, default=0)
        self._text_mode = text_mode
        self._on_state_changed = on_state_changed

        layout = KitHBoxLayout()
        layout.spacing = 6
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addWidget(layout)

        self._label = KitLabel(name)
        self._label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(self._label)

        self._combo_box = KitComboBox()
        self._combo_box.addItems(values)
        self._combo_box.currentIndexChanged.connect(self._on_index_changed)
        self._combo_box.setFixedWidth(width if width is not None else ComboBox.STD_WIDTH)
        layout.addWidget(self._combo_box)

        if children is not None:
            children_layout = KitVBoxLayout()
            children_layout.setContentsMargins(20, 0, 0, 0)
            self.addWidget(children_layout)
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

    def show_children(self):
        for key, item in self._children.items():
            for el in item:
                if key == (self._combo_box.currentValue() if self._text_mode else self._combo_box.currentIndex()):
                    el.show()
                else:
                    el.hide()

    def _on_index_changed(self, index):
        if self._text_mode:
            self._set(self._combo_box.currentValue())
        else:
            self._set(index)
        if self._on_state_changed:
            self._on_state_changed()
        self.show_children()
        self.load_children()

    def set_value(self, value):
        # print(f"{self._label.text}: set value {value}")
        if self._text_mode:
            self._combo_box.setCurrentValue(str(value))
            self._set(self._combo_box.currentValue())
            return
        if not isinstance(value, int):
            self.set_value(0)
            return
        self._set(value)
        self._combo_box.setCurrentIndex(value)


class SpinBox(_Widget):
    STD_WIDTH = 80

    def __init__(self, bm, name: str, min_value=0, max_value=100, key=None, key_type=None, width=None, double=False):
        super().__init__(bm, key, key_type, 0)
        self._double = double
        self._type = float if double else int

        layout = KitHBoxLayout()
        self.addWidget(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.spacing = 6

        self._label = KitLabel(name)
        self._label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(self._label)

        self._spin_box = KitSpinBox(float if double else int)
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


class FileEdit(_Widget):
    MODE_OPEN = 0
    MODE_SAVE = 1
    MODE_DIR = 2

    def __init__(self, bm, name='', mode=MODE_OPEN, default='', key=None, key_type=None):
        super().__init__(bm, key, key_type)
        self._last_value = default
        self._mode = mode

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
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
        if self._mode == FileEdit.MODE_OPEN and os.path.isfile(self._line_edit.text):
            self._last_value = self._line_edit.text
            self._set(self._line_edit.text)
        elif self._mode == FileEdit.MODE_SAVE and os.path.isdir(os.path.split(self._line_edit.text)[0]):
            self._last_value = self._line_edit.text
            self._set(self._line_edit.text)
        elif self._mode == FileEdit.MODE_DIR and os.path.isdir(self._line_edit.text):
            self._last_value = self._line_edit.text
            self._set(self._line_edit.text)
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


class SwitchBox(_Widget):
    def __init__(self, bm, condition, children: dict, key_type=None, not_delete_keys=False):
        super().__init__(bm, not_delete_keys=not_delete_keys)
        self._condition = condition
        self.spacing = 6

        for key, item in children.items():
            self._children[key] = []
            if isinstance(item, list):
                for el in item:
                    self._children[key].append(el)
                    self.addWidget(el)
            else:
                self._children[key].append(item)
                self.addWidget(item)
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


class ProgramEdit(_Widget):
    def __init__(self, bm: BackendManager, desc, program: Program, key_type=None):
        super().__init__(bm, program.key(), key_type, program.basic().to_json())
        self.bm = bm
        self.spacing = 6

        self.label = KitLabel(desc)
        self.addWidget(self.label)

        self.program_box = ProgramBox(self.bm, program)
        self.addWidget(self.program_box)
        self._connected = False

    def set_value(self, value):
        self.program_box.set_value(value)
        if not self._connected:
            self.program_box.currentChanged.connect(lambda prog: self._set(prog.to_json()))
            self._connected = True


class SettingsWidget(KitScrollArea):
    def __init__(self, sm, *args, key_type=None):
        super().__init__()
        self._sm = sm
        self._widgets = []
        self.main_palette = 'Bg'

        self.__scroll_layout = KitVBoxLayout()
        self.__scroll_layout.padding = 0, 0, 20, 0
        self.__scroll_layout.spacing = 10
        self.__scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(self.__scroll_layout)

        for el in args:
            self._widgets.append(el)
            self.__scroll_layout.addWidget(el)

        if key_type is not None:
            for el in self._widgets:
                if hasattr(el, 'set_key_type'):
                    el.set_key_type(key_type)
        self.load_values()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.__scroll_layout.setMaximumWidth(a0.size().width())
        super().resizeEvent(a0)

    def load_values(self):
        for el in self._widgets:
            if hasattr(el, 'load_value'):
                el.load_value()

    def showEvent(self, a0):
        super().showEvent(a0)
        super()._apply_theme()
