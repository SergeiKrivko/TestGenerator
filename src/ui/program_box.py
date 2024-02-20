from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QMenu

from src.backend.backend_types.program import Program, ProgramInstance
from src.ui.button import Button


class ProgramBox(QWidget):
    currentChanged = pyqtSignal(ProgramInstance)

    def __init__(self, program: Program, sm=None, tm=None):
        super().__init__()
        self._program = program
        self._sm = sm
        self._tm = tm
        self._creation_mode = 0
        self._items = []

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        self.setLayout(layout)

        self.combo_box = QComboBox()
        layout.addWidget(self.combo_box)
        self.combo_box.currentIndexChanged.connect(self._on_index_changed)

        self.line_edit = QLineEdit()
        self.line_edit.hide()
        self.line_edit.returnPressed.connect(self._on_return_pressed)
        layout.addWidget(self.line_edit)

        self.button_return = QPushButton()
        # self.button_return.hide()
        self.button_return.clicked.connect(self._on_return_pressed)
        layout.addWidget(self.button_return)
        self.button_return.setFixedSize(1, 22)

        self.button_update = Button(None, 'buttons/update')
        layout.addWidget(self.button_update)
        self.button_update.setFixedSize(24, 22)

        self.button_add = Button(None, 'buttons/plus')
        layout.addWidget(self.button_add)
        self.button_add.clicked.connect(self._on_plus_clicked)
        self.button_add.setFixedSize(24, 22)

        self.button_more = QPushButton()
        layout.addWidget(self.button_more)
        self.button_more.setFixedSize(20, 22)

        self.menu = Menu()
        self.menu.typeSelected.connect(self.select_program)
        self.button_more.setMenu(self.menu)

        self.set_sm(sm)
        self.set_tm(tm)

    def set_sm(self, sm):
        self._sm = sm
        if self._sm is None:
            return
        self.button_update.clicked.connect(lambda: self._sm.start_search(forced=True))
        self._sm.searching_complete.connect(self.update_items)
        self.update_items()

    def set_tm(self, tm):
        self._tm = tm

    def current(self):
        return self._items[self.combo_box.currentIndex()]

    def set_items(self, items: list[ProgramInstance], delete_current=False):
        text = self.combo_box.currentText()
        if not delete_current and self._items:
            items.append(self._items[self.combo_box.currentIndex()])
        self._items = items
        self.combo_box.clear()
        self.combo_box.addItems([item.name() for item in items])
        for i, item in enumerate(self._items):
            if not item.valid:
                self.combo_box.setItemIcon(i, QIcon(self._tm.get_image('icons/failed', color=self._tm['TestFailed'])))
        self.combo_box.setCurrentText(text)

    def add_item(self, item: ProgramInstance):
        item.program.add_existing(item)
        self._items.append(item)
        self.combo_box.addItem(item.name(), None)
        if not item.valid:
            self.combo_box.setItemIcon(self.combo_box.count() - 1,
                                       QIcon(self._tm.get_image('icons/failed', color=self._tm['TestFailed'])))
            self._sm.store_programs()

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

        self.line_edit.setText(self.combo_box.currentText())
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
        for i in range(len(self._items)):
            if self._items[i].name() == program.name() and self._items[i].virtual_system == program.virtual_system:
                self.combo_box.setCurrentIndex(i)
                return
        self.add_item(program)
        self.combo_box.setCurrentIndex(self.combo_box.count() - 1)

    def _on_index_changed(self, ind):
        try:
            self.currentChanged.emit(self._items[ind])
        except IndexError:
            pass

    def set_theme(self):
        self._tm.auto_css(self.combo_box)
        self._tm.auto_css(self.button_add)
        self._tm.auto_css(self.button_update)
        self._tm.auto_css(self.button_return)
        self._tm.auto_css(self.line_edit)
        self._tm.auto_css(self.button_more)
        self._tm.auto_css(self.menu)


class Menu(QMenu):
    typeSelected = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        action = self.addAction('Программа')
        action.triggered.connect(lambda: self.typeSelected.emit(0))

        action = self.addAction('WSL')
        action.triggered.connect(lambda: self.typeSelected.emit(Program.WSL))
