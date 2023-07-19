import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QComboBox, QDialog, QLineEdit, \
    QPushButton

from ui.button import Button


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

        self.combo_box = QComboBox()
        self.combo_box.setFixedSize(200, 24)
        self.combo_box.currentIndexChanged.connect(self.subproject_changed)
        main_layout.addWidget(self.combo_box)

        self.button_plus = Button(self.tm, 'plus', css='Menu')
        self.button_plus.setFixedSize(24, 24)
        self.button_plus.clicked.connect(self.new_subproject)
        main_layout.addWidget(self.button_plus)

        self.setLayout(main_layout)

        self.signals = True
        self.sm.project_changed.connect(self.open_task)

    def lab_changed(self):
        if self.sm.get('struct') != 0:
            return
        if signals := self.signals:
            self.sm.start_change_task.emit()
            self.signals = False
        self.sm.set('lab', self.lab_spin_box.value())
        if signals:
            self.find_variant()
            self.signals = True
            self.sm.finish_change_task.emit()

    def subproject_changed(self):
        if self.sm.get('struct') != 2:
            return
        if signals := self.signals:
            self.sm.start_change_task.emit()
            self.signals = False
        self.sm.set('lab', self.combo_box.currentIndex())
        if signals:
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

    def new_subproject(self):
        dialog = NewSubProjectDialog(self.tm)
        if dialog.exec():
            lst = self.sm.get('subprojects', [])
            if dialog.line_edit.text() in lst:
                return
            lst.append(dialog.line_edit.text())
            self.sm.set('subprojects', lst)
            self.combo_box.addItems([dialog.line_edit.text()])

    def open_task(self):
        struct = self.sm.get('struct')
        if struct == 0:
            self.show()
            self.combo_box.hide()
            self.button_plus.hide()
            for el in self.labels:
                el.show()
            self.lab_spin_box.show()
            self.task_spin_box.show()
            self.var_spin_box.show()
        elif struct == 1:
            self.hide()
        elif struct == 2:
            self.show()
            for el in self.labels:
                el.hide()
            self.lab_spin_box.hide()
            self.task_spin_box.hide()
            self.var_spin_box.hide()
            self.combo_box.show()
            self.button_plus.show()

        if signals := self.signals:
            self.sm.start_change_task.emit()
            self.signals = False
        self.lab_spin_box.setValue(self.sm.get('lab', 1))
        self.task_spin_box.setValue(self.sm.get('task', 1))
        self.var_spin_box.setValue(self.sm.get('var', 0))
        self.combo_box.clear()
        self.combo_box.addItems(self.sm.get('subprojects', []))
        self.combo_box.setCurrentIndex(self.sm.get('lab', 1))
        if signals:
            self.signals = True
            self.sm.finish_change_task.emit()

    def set_theme(self):
        for label in self.labels:
            self.tm.auto_css(label)
        for label in [self.lab_spin_box, self.task_spin_box, self.var_spin_box, self.combo_box]:
            self.tm.auto_css(label, palette='Bg')
        self.button_plus.set_theme()


class NewSubProjectDialog(QDialog):
    def __init__(self, tm):
        super().__init__()
        self.tm = tm

        layout = QVBoxLayout()

        self.label = QLabel("Название подпроекта:")
        layout.addWidget(self.label)

        self.line_edit = QLineEdit()
        self.line_edit.setMinimumSize(200, 24)
        layout.addWidget(self.line_edit)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)
        layout.addLayout(buttons_layout)

        self.button_ok = QPushButton("Ок")
        self.button_ok.setFixedSize(80, 22)
        self.button_ok.clicked.connect(self.accept)
        buttons_layout.addWidget(self.button_ok)

        self.button_cancel = QPushButton("Отмена")
        self.button_cancel.setFixedSize(80, 22)
        self.button_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(self.button_cancel)

        self.setLayout(layout)
        self.set_theme()

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        for el in [self.label, self.line_edit, self.button_cancel, self.button_ok]:
            self.tm.auto_css(el)

