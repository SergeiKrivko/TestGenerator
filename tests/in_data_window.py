from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel, \
    QScrollArea, QCheckBox

from ui.button import Button

HEIGHT = 22
BUTTON_WIDTH = HEIGHT
LINE_EDIT_WIDTH = 100


class InDataWindow(QDialog):
    def __init__(self, sm, tm):
        super().__init__()
        self._sm = sm
        self._tm = tm

        layout = QVBoxLayout()
        self.setLayout(layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(buttons_layout)

        self._button_plus = Button(self._tm, 'plus')
        self._button_plus.setFixedSize(24, 24)
        self._button_plus.clicked.connect(self.add_elem)
        buttons_layout.addWidget(self._button_plus)

        self._scroll_area = QScrollArea()
        layout.addWidget(self._scroll_area)
        scroll_widget = QWidget()
        self._scroll_area.setWidget(scroll_widget)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_layout = QVBoxLayout()
        self._scroll_layout.setAlignment(Qt.AlignTop)
        scroll_widget.setLayout(self._scroll_layout)

        self._widgets = []

    def add_elem(self, data=None):
        widget = _DataEdit(self._tm)
        widget.set_theme()
        widget.closeRequested.connect(self.delete_elem)
        if isinstance(data, dict):
            widget.load(data)
        self._widgets.append(widget)
        self._scroll_layout.addWidget(widget)

    def save(self):
        self._sm.set_task('in_data_list', [el.save() for el in self._widgets])

    def load(self):
        self._widgets.clear()
        for i in range(self._scroll_layout.count()):
            self._scroll_layout.itemAt(0).widget().setParent(None)
        for el in self._sm.get_task('in_data_list', []):
            self.add_elem(el)

    def delete_elem(self, elem):
        self._widgets.remove(elem)
        elem.setParent(None)

    def exec(self) -> int:
        self.load()
        self.set_theme()
        res = super().exec()
        self.save()
        return res

    def set_theme(self):
        self.setStyleSheet(self._tm.bg_style_sheet)
        self._tm.auto_css(self._button_plus)
        self._tm.auto_css(self._button_plus, palette='Bg')
        for el in self._widgets:
            el.set_theme()


class _RangeEdit(QWidget):
    def __init__(self, tm, desc=''):
        super().__init__()
        self._tm = tm
        self._min = "-inf"
        self._max = "+inf"

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        font_metrics = QFontMetrics(self._tm.font_small)
        self._name_label = QLabel(desc)
        self._name_label.setFixedWidth(font_metrics.size(0, desc).width())
        layout.addWidget(self._name_label)

        self._button_open_1 = QPushButton("(")
        self._button_open_1.setFixedSize(BUTTON_WIDTH, HEIGHT)
        self._button_open_1.clicked.connect(lambda: (self._button_open_1.hide(), self._button_open_2.show()))
        layout.addWidget(self._button_open_1)

        self._button_open_2 = QPushButton("[")
        self._button_open_2.setFixedSize(BUTTON_WIDTH, HEIGHT)
        self._button_open_2.hide()
        self._button_open_2.clicked.connect(lambda: (self._button_open_2.hide(), self._button_open_1.show()))
        layout.addWidget(self._button_open_2)

        self._line_edit_min = QLineEdit()
        self._line_edit_min.setFixedSize(LINE_EDIT_WIDTH, HEIGHT)
        self._line_edit_min.editingFinished.connect(self._on_min_changed)
        layout.addWidget(self._line_edit_min)

        self._label = QLabel(";")
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setFixedWidth(6)
        layout.addWidget(self._label)

        self._line_edit_max = QLineEdit()
        self._line_edit_max.setFixedSize(LINE_EDIT_WIDTH, HEIGHT)
        self._line_edit_max.editingFinished.connect(self._on_max_changed)
        layout.addWidget(self._line_edit_max)

        self._button_close_1 = QPushButton(")")
        self._button_close_1.setFixedSize(BUTTON_WIDTH, HEIGHT)
        self._button_close_1.clicked.connect(lambda: (self._button_close_1.hide(), self._button_close_2.show()))
        layout.addWidget(self._button_close_1)

        self._button_close_2 = QPushButton("]")
        self._button_close_2.setFixedSize(BUTTON_WIDTH, HEIGHT)
        self._button_close_2.hide()
        self._button_close_2.clicked.connect(lambda: (self._button_close_2.hide(), self._button_close_1.show()))
        layout.addWidget(self._button_close_2)

    def _on_min_changed(self):
        text = self._line_edit_min.text()
        if not text.strip() or text.strip() == '-inf':
            self._min = text
        try:
            float(text)
            self._min = text
        except ValueError:
            self._line_edit_min.setText(self._min)

    def _on_max_changed(self):
        text = self._line_edit_max.text()
        if not text.strip() or text.strip() == '+inf' or text.strip() == 'inf':
            self._max = text
        try:
            float(text)
            self._max = text
        except ValueError:
            self._line_edit_max.setText(self._max)

    @staticmethod
    def _convert_value(text):
        if text.strip() in ('-inf', 'inf', '+inf', ''):
            return None
        try:
            return int(text)
        except ValueError:
            try:
                return float(text)
            except ValueError:
                return None

    def save(self):
        return {'min': self._convert_value(self._line_edit_min.text()),
                'max': self._convert_value(self._line_edit_max.text()),
                'open_brace': '[' if self._button_open_1.isHidden() else '(',
                'close_brace': ']' if self._button_open_1.isHidden() else ')'}

    def load(self, data: dict):
        if data.get('min') is None:
            self._line_edit_min.setText("")
        else:
            self._line_edit_min.setText(str(data.get('min', '')))
        if data.get('max') is None:
            self._line_edit_max.setText("")
        else:
            self._line_edit_max.setText(str(data.get('max', '')))

        if data.get('open_brace', '(') == '(':
            self._button_open_1.show()
            self._button_open_2.hide()
        else:
            self._button_open_2.show()
            self._button_open_1.hide()
        if data.get('close_brace', ')') == '(':
            self._button_close_1.show()
            self._button_close_2.hide()
        else:
            self._button_close_2.show()
            self._button_close_1.hide()

    def set_theme(self):
        for el in [self._button_open_1, self._button_open_2, self._line_edit_min, self._label,
                   self._line_edit_max, self._button_close_1, self._button_close_2, self._name_label]:
            self._tm.auto_css(el)


class _StrEdit(QWidget):
    def __init__(self, tm):
        super().__init__()
        self._tm = tm

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._range_edit = _RangeEdit(self._tm, "Длина:")
        layout.addWidget(self._range_edit)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setAlignment(Qt.AlignLeft)
        layout.addLayout(bottom_layout)

        self._checkbox = QCheckBox()
        bottom_layout.addWidget(self._checkbox)

        self._label = QLabel("Пробелы")
        bottom_layout.addWidget(self._label)

    def load(self, data: dict):
        self._checkbox.setChecked(bool(data.get('spaces', False)))
        self._range_edit.load(data)

    def save(self):
        return {'spaces': self._checkbox.isChecked(), **self._range_edit.save()}

    def set_theme(self):
        self._tm.auto_css(self._label)
        self._tm.auto_css(self._checkbox)
        self._range_edit.set_theme()


class _DataEdit(QWidget):
    _TYPE_WIDGETS = {'int': lambda tm: _RangeEdit(tm, "Диапазон:"),
                     'float': lambda tm: _RangeEdit(tm, "Диапазон:"),
                     'str': _StrEdit,
                     'struct': _RangeEdit,
                     'array': _RangeEdit, }
    closeRequested = pyqtSignal(object)

    def __init__(self, tm):
        super().__init__()
        self._tm = tm

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addLayout(top_layout)

        self._combo_box = QComboBox()
        self._combo_box.addItems(['int', 'float', 'str', 'struct', 'array'])
        self._combo_box.currentIndexChanged.connect(self._on_type_changed)
        top_layout.addWidget(self._combo_box)

        self._line_edit = QLineEdit()
        top_layout.addWidget(self._line_edit)

        self._button = Button(self._tm, "delete")
        self._button.setFixedSize(BUTTON_WIDTH, HEIGHT)
        self._button.clicked.connect(lambda: self.closeRequested.emit(self))
        top_layout.addWidget(self._button)

        self._type_edit = _RangeEdit(self._tm, "Диапазон:")
        self._layout.addWidget(self._type_edit)

    def _on_type_changed(self):
        self._type_edit.setParent(None)
        self._type_edit = _DataEdit._TYPE_WIDGETS[self._combo_box.currentText()](self._tm)
        self._layout.addWidget(self._type_edit)
        self._type_edit.set_theme()

    def save(self):
        return {'type': self._combo_box.currentText(), 'name': self._line_edit.text(), **self._type_edit.save()}

    def load(self, data: dict):
        self._combo_box.setCurrentText(data.get('type'))
        self._line_edit.setText(data.get('name'))
        self._type_edit.load(data)

    def set_theme(self):
        for el in [self._line_edit, self._combo_box, self._button]:
            self._tm.auto_css(el)
        self._type_edit.set_theme()
