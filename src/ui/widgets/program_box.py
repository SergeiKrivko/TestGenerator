from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQtUIkit.widgets import *

from src.backend.backend_types.program import Program, ProgramInstance
from src.backend.managers import BackendManager


class ProgramBox(KitHBoxLayout):
    currentChanged = pyqtSignal(ProgramInstance)

    def __init__(self, bm: BackendManager, program: Program):
        super().__init__()
        self._program = program
        self._bm = bm
        self._sm = bm.sm
        self._creation_mode = 0

        self.setSpacing(3)

        self.combo_box = KitComboBox()
        self.combo_box.currentValueChanged.connect(self.currentChanged.emit)
        self.addWidget(self.combo_box)

        self.line_edit = KitLineEdit()
        self.line_edit.hide()
        self.line_edit.returnPressed.connect(self._on_return_pressed)
        self.addWidget(self.line_edit)

        self.button_return = KitButton()
        # self.button_return.hide()
        self.button_return.clicked.connect(self._on_return_pressed)
        self.addWidget(self.button_return)
        self.button_return.setFixedSize(1, 22)

        self.button_update = KitIconButton('line-refresh')
        self.addWidget(self.button_update)
        self.button_update.setFixedSize(24, 22)

        self.button_add = KitIconButton('line-add')
        self.addWidget(self.button_add)
        self.button_add.on_click = self._on_plus_clicked
        self.button_add.setFixedSize(24, 22)

        self.button_more = KitIconButton('line-chevron-down')
        self.addWidget(self.button_more)
        self.button_more.setFixedSize(20, 22)

        self.menu = Menu(self)
        self.menu.typeSelected.connect(self.select_program)
        self.button_more.setMenu(self.menu)

        self.button_update.clicked.connect(lambda: self._sm.start_search(forced=True))
        self._sm.searching_complete.connect(self.update_items)
        self.update_items()

    def current(self):
        return self.combo_box.currentValue()

    def set_items(self, items: list[ProgramInstance], delete_current=False):
        last_value = self.combo_box.currentValue()

        self.combo_box.clear()
        if not delete_current and last_value:
            self.combo_box.addItem(KitComboBoxItem(last_value.name, last_value))

        for prog in items:
            self.combo_box.addItem(KitComboBoxItem(prog.name, prog, '' if prog.valid else 'line-close'))

    def add_item(self, item: ProgramInstance):
        item.program.add_existing(item)
        self.combo_box.addItem(KitComboBoxItem(item.name, item, '' if item.valid else 'line-close'))
        self._bm.programs.store_programs()

    def _on_plus_clicked(self):
        self.select_program(0)

    def select_program(self, type=0):
        self._creation_mode = type
        self.combo_box.hide()
        self.line_edit.show()

        self.button_update.hide()
        self.button_return.show()
        self.button_add.hide()
        self.button_more.hide()

        self.line_edit.setText(self.combo_box.currentValue()._path)
        self.line_edit.selectAll()
        self.line_edit.setFocus()

    def _on_return_pressed(self):
        if text := self.line_edit.text().strip():
            self.set_value(ProgramInstance(self._program, text, self._creation_mode))

        self.button_update.show()
        # self.button_return.hide()
        self.button_add.show()
        self.button_more.show()

        self.line_edit.hide()
        self.combo_box.show()

    def _on_editing_finished(self):
        self.line_edit.hide()
        self.combo_box.show()

    def update_items(self, forced=False):
        self.set_items(list(self._program.existing()), delete_current=False)

    def set_value(self, program: ProgramInstance | dict | str):
        if isinstance(program, (dict, str)):
            program = ProgramInstance.from_json(program)
        self.combo_box.setCurrentValue(program)
        if self.combo_box.currentValue() != program:
            self.add_item(program)
            self.combo_box.setCurrentIndex(self.combo_box.count() - 1)


class Menu(KitMenu):
    typeSelected = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)

        action = self.addAction('Программа')
        action.triggered.connect(lambda: self.typeSelected.emit(0))

        action = self.addAction('WSL')
        action.triggered.connect(lambda: self.typeSelected.emit(Program.WSL))
