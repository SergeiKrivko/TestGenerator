from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QListWidgetItem

from ui.button import Button
from unit_testing.unit_test import UnitTest

BUTTONS_MAX_WIDTH = 40


class UnitTestingWidget(QWidget):
    def __init__(self, sm, cm, tm):
        super().__init__()
        self.sm = sm
        self.cm = cm
        self.tm = tm

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(left_layout, 1)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addLayout(buttons_layout)

        self.button_add = Button(self.tm, 'plus', css='Bg')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_add.clicked.connect(self.add_test)
        buttons_layout.addWidget(self.button_add)

        self.button_delete = Button(self.tm, 'delete', css='Bg')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(BUTTONS_MAX_WIDTH)
        buttons_layout.addWidget(self.button_delete)

        self.button_up = Button(self.tm, 'button_up', css='Bg')
        self.button_up.setFixedHeight(22)
        self.button_up.setMaximumWidth(BUTTONS_MAX_WIDTH)
        buttons_layout.addWidget(self.button_up)

        self.button_down = Button(self.tm, 'button_down', css='Bg')
        self.button_down.setFixedHeight(22)
        self.button_down.setMaximumWidth(BUTTONS_MAX_WIDTH)
        buttons_layout.addWidget(self.button_down)

        self.button_copy = Button(self.tm, 'copy', css='Bg')
        self.button_copy.setFixedHeight(22)
        self.button_copy.setMaximumWidth(BUTTONS_MAX_WIDTH)
        buttons_layout.addWidget(self.button_copy)

        self._list_widget = QListWidget()
        left_layout.addWidget(self._list_widget)

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(right_layout, 2)

        self._code_edit = QTextEdit()
        right_layout.addWidget(self._code_edit)

        self.data_dir = ""
        self.temp_file_index = 0

    def open_task(self):
        self.data_dir = f"{self.sm.data_lab_path()}/unit_tests"
        self.temp_file_index = 0

    def add_test(self):
        self._list_widget.addItem(ListWidgetItem(self.tm, UnitTest(self.create_temp_file())))

    def create_temp_file(self):
        path = f"{self.data_dir}/temp_{self.temp_file_index}"
        self.temp_file_index += 1
        return path

    def set_theme(self):
        for el in [self._list_widget, self._code_edit, self.button_add, self.button_delete, self.button_down,
                   self.button_up, self.button_copy]:
            self.tm.auto_css(el)
        self._code_edit.setFont(self.tm.code_font)


class ListWidgetItem(QListWidgetItem):
    def __init__(self, tm, test: UnitTest):
        super().__init__()
        self._tm = tm
        self.test = test
        self.setText(self.test.get('desc', '-'))
        self.set_theme()

    def set_theme(self):
        self.setFont(self._tm.font_medium)

