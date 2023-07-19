import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox


class LabWidget(QWidget):
    def __init__(self, tm, sm, vertical=False):
        super().__init__()
        self.tm = tm
        self.sm = sm

        main_layout = QVBoxLayout() if vertical else QHBoxLayout()
        main_layout.setAlignment(Qt.AlignTop if vertical else Qt.AlignLeft)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.labels = []

        main_layout.addWidget(label := QLabel("Лаба:"))
        self.labels.append(label)

        self.lab_spin_box = QSpinBox()
        self.lab_spin_box.setMinimum(1)
        self.lab_spin_box.setMaximum(10000)
        self.lab_spin_box.setFixedWidth(50)
        self.lab_spin_box.setValue(self.sm.get('lab', 1))
        self.lab_spin_box.valueChanged.connect(self.lab_changed)
        main_layout.addWidget(self.lab_spin_box)

        main_layout.addWidget(label := QLabel("Задание:"))
        self.labels.append(label)

        self.task_spin_box = QSpinBox()
        self.task_spin_box.setMinimum(1)
        self.task_spin_box.setMaximum(10000)
        self.task_spin_box.setFixedWidth(50)
        self.task_spin_box.setValue(self.sm.get('task', 1))
        self.task_spin_box.valueChanged.connect(self.task_changed)
        main_layout.addWidget(self.task_spin_box)

        main_layout.addWidget(label := QLabel("Вариант:"))
        self.labels.append(label)

        self.var_spin_box = QSpinBox()
        self.var_spin_box.setMinimum(-1)
        self.var_spin_box.setMaximum(10000)
        self.var_spin_box.setFixedWidth(50)
        self.var_spin_box.setValue(self.sm.get('var', 0))
        self.var_spin_box.valueChanged.connect(self.var_changed)
        main_layout.addWidget(self.var_spin_box)

        self.setLayout(main_layout)

        self.signals = True

    def lab_changed(self):
        if signals := self.signals:
            self.sm.start_change_task.emit()
            self.signals = False
        self.sm.set('lab', self.lab_spin_box.value())
        if signals:
            self.find_variant()
            self.signals = True
            self.sm.finish_change_task.emit()

    def task_changed(self):
        if signals := self.signals:
            self.sm.start_change_task.emit()
            self.signals = False
        self.sm.set('task', self.task_spin_box.value())
        if signals:
            self.find_variant()
            self.signals = True
            self.sm.finish_change_task.emit()

    def var_changed(self):
        if signals := self.signals:
            self.sm.start_change_task.emit()
            self.signals = False
        self.sm.set('var', self.var_spin_box.value())
        if signals:
            self.signals = True
            self.sm.finish_change_task.emit()

    def find_variant(self):
        for i in range(-1, 100):
            if os.path.isdir(self.sm.lab_path(var=i)):
                self.var_spin_box.setValue(i)
                return True

    def open_task(self):
        if self.sm.get('struct') == 1:
            self.hide()
        else:
            self.show()

        if signals := self.signals:
            self.sm.start_change_task.emit()
            self.signals = False
        self.lab_spin_box.setValue(self.sm.get('lab', 1))
        self.task_spin_box.setValue(self.sm.get('task', 1))
        self.var_spin_box.setValue(self.sm.get('var', 0))
        if signals:
            self.signals = True
            self.sm.finish_change_task.emit()

    def set_theme(self):
        for label in self.labels:
            self.tm.auto_css(label)
        for label in [self.lab_spin_box, self.task_spin_box, self.var_spin_box]:
            self.tm.auto_css(label)
