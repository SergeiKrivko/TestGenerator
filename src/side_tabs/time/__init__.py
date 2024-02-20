from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QComboBox, QTextEdit, QLabel, QSpinBox, QDoubleSpinBox, \
    QLineEdit

from src.side_tabs.builds.commands_list import ScenarioBox
from src.ui.custom_dialog import CustomDialog
from src.ui.side_panel_widget import SidePanelWidget


class TimePanel(SidePanelWidget):
    def __init__(self, sm, bm, tm):
        super().__init__(sm, tm, "Замеры времени", [])
        self.bm = bm

        mail_layout = QVBoxLayout()
        mail_layout.setContentsMargins(0, 0, 0, 0)
        mail_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(mail_layout)

        self._build_edit = ScenarioBox(self.sm, self.bm, self.tm)
        mail_layout.addWidget(self._build_edit)

        self._x_edit = QPushButton()
        self._x_edit.clicked.connect(self._on_x_edit_clicked)
        mail_layout.addWidget(self._x_edit)

        self._x_field = Field(**self.sm.get('time_measure_x', dict()))

    def _on_x_edit_clicked(self):
        dialog = FieldEditDialog(self.tm)
        dialog.open_field(self._x_field)
        if dialog.exec():
            self._x_field = dialog.store()
            self._x_edit.setText(self._x_field.to_text())
            self.sm.set('time_measure_x', dialog.store().to_dict())

    def set_theme(self):
        super().set_theme()
        for el in [self._x_edit]:
            self.tm.auto_css(el)
        self._build_edit.set_theme()


class Field:
    INT = 0
    FLOAT = 1
    INT_RANGE = 2
    FLOAT_RANGE = 3
    LIST = 4

    def __init__(self, **kwargs):
        print(kwargs)
        self.type = Field.INT if kwargs.get('type', 0) is None else kwargs.get('type', 0)
        self.name = kwargs.get('name', '')
        self.min = kwargs.get('min', 0)
        self.max = kwargs.get('max', 100)
        self.step = kwargs.get('step', 1)
        self.values = kwargs.get('values', [])

    def to_dict(self):
        dct = {'type': self.type}
        if self.type == Field.INT_RANGE or self.type == Field.FLOAT_RANGE:
            dct['min'] = self.min
            dct['max'] = self.max
            dct['step'] = self.step
        if self.type in [Field.INT, Field.FLOAT, Field.INT_RANGE, Field.FLOAT_RANGE]:
            dct['name'] = self.name
        if self.type in [Field.INT, Field.FLOAT, Field.LIST]:
            dct['values'] = self.values

    def to_text(self):
        if self.type in [Field.INT, Field.FLOAT, Field.INT_RANGE, Field.FLOAT_RANGE]:
            return self.name
        return '; '.join(self.values)

    @staticmethod
    def from_dict(data: dict):
        return Field(**data)

    def get_values(self):
        if self.type == Field.INT_RANGE:
            return range(int(self.min), int(self.max), int(self.step))
        if self.type == Field.FLOAT_RANGE:
            a = self.min
            while a < self.max + self.step / 2:
                yield a
                a += self.step
            return
        return self.values


class FieldEditDialog(CustomDialog):
    def __init__(self, tm):
        super().__init__(tm)
        super().set_theme()

        self.setFixedSize(250, 250)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self._type_box = QComboBox()
        main_layout.addWidget(self._type_box)
        self._type_box.addItems(['int', 'float', 'int range', 'float range', 'list'])

        self._name_edit = QLineEdit()
        main_layout.addWidget(self._name_edit)

        self.text_edit = QTextEdit()
        main_layout.addWidget(self.text_edit)

        self._labels = []

        label = QLabel("Начало:")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._start_box = QSpinBox()
        self._start_box.setMinimum(-1000000000)
        self._start_box.setMaximum(1000000000)
        main_layout.addWidget(self._start_box)

        self._start_float_box = QDoubleSpinBox()
        self._start_float_box.setMinimum(-1e300)
        self._start_float_box.setMaximum(1e300)
        self._start_float_box.setDecimals(6)
        main_layout.addWidget(self._start_float_box)

        label = QLabel("Конец:")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._stop_box = QSpinBox()
        self._stop_box.setMinimum(-1000000000)
        self._stop_box.setMaximum(1000000000)
        main_layout.addWidget(self._stop_box)

        self._stop_float_box = QDoubleSpinBox()
        self._stop_float_box.setMinimum(-1e300)
        self._stop_float_box.setMaximum(1e300)
        self._stop_float_box.setDecimals(6)
        main_layout.addWidget(self._stop_float_box)

        label = QLabel("Шаг:")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._step_box = QSpinBox()
        self._step_box.setMinimum(-1000000000)
        self._step_box.setMaximum(1000000000)
        main_layout.addWidget(self._step_box)

        self._step_float_box = QDoubleSpinBox()
        self._step_float_box.setMinimum(-1e300)
        self._step_float_box.setMaximum(1e300)
        self._step_float_box.setDecimals(6)
        main_layout.addWidget(self._step_float_box)

        self._button = QPushButton("OK")
        self._button.clicked.connect(self.accept)
        main_layout.addWidget(self._button)

        self._field = None
        self._type_box.currentIndexChanged.connect(self._on_type_changed)
        self._on_type_changed()

    def _on_type_changed(self):
        if isinstance(self._field, Field):
            self._field.type = self._type_box.currentIndex()
        for el in self._labels:
            el.hide()
        self._name_edit.hide()
        self.text_edit.hide()
        self._start_box.hide()
        self._stop_box.hide()
        self._step_box.hide()
        self._start_float_box.hide()
        self._stop_float_box.hide()
        self._step_float_box.hide()
        if not isinstance(self._field, Field):
            return

        if self._field.type != Field.LIST:
            self._name_edit.show()
            self._name_edit.setText(self._field.name)

        if self._field.type == Field.INT_RANGE:
            for el in self._labels:
                el.show()
            self._start_box.show()
            self._stop_box.show()
            self._step_box.show()
            self._start_box.setValue(self._field.min)
            self._stop_box.setValue(self._field.max)
            self._step_box.setValue(self._field.step)
        elif self._field.type == Field.FLOAT_RANGE:
            for el in self._labels:
                el.show()
            self._start_float_box.show()
            self._stop_float_box.show()
            self._step_float_box.show()
            self._start_float_box.setValue(self._field.min)
            self._stop_float_box.setValue(self._field.max)
            self._step_float_box.setValue(self._field.step)
        else:
            self.text_edit.show()
            self.text_edit.setText('\n'.join(map(str, self._field.values)))

    def open_field(self, field: Field):
        self._field = field
        flag = self._field.type != self._type_box.currentIndex()
        self._type_box.setCurrentIndex(self._field.type)
        if flag:
            self._on_type_changed()

    def store(self):
        if not isinstance(self._field, Field):
            return Field()

        self._field.name = self._name_edit.text()
        if self._field.type == Field.INT_RANGE:
            self._field.min = self._start_box.value()
            self._field.max = self._stop_box.value()
            self._field.step = self._step_box.value()
        elif self._field.type == Field.FLOAT_RANGE:
            self._field.min = self._start_float_box.value()
            self._field.max = self._stop_float_box.value()
            self._field.step = self._step_float_box.value()
        elif self._field.type == Field.INT:
            try:
                self._field.values = map(int, self.text_edit.toPlainText().split())
            except ValueError:
                self._field.values = tuple()
        elif self._field.type == Field.FLOAT:
            try:
                self._field.values = map(float, self.text_edit.toPlainText().split())
            except ValueError:
                self._field.values = tuple()
        elif self._field.type == Field.LIST:
            self._field.values = self.text_edit.toPlainText().split()

        return self._field

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        self.set_theme()

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        for el in self._labels:
            self.tm.auto_css(el)
        for el in [self._type_box, self._name_edit, self.text_edit, self._start_box, self._start_float_box,
                   self._stop_box, self._stop_float_box, self._step_box, self._step_float_box, self._button]:
            self.tm.auto_css(el)
