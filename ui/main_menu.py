from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton

from settings.lab_widget import LabWidget
from ui.button import Button


class MainMenu(QWidget):
    TAB_CODE = 0
    TAB_TESTS = 1
    TAB_TESTING = 2
    tab_changed = pyqtSignal(int)

    def __init__(self, sm, tm):
        super().__init__()
        self.sm = sm
        self.tm = tm

        self.setFixedHeight(44)

        strange_layout = QHBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)
        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(35)
        strange_widget.setLayout(layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(2)
        layout.addLayout(buttons_layout)

        self.button_code = QPushButton("Код")
        self.button_code.setFixedSize(40, 24)
        self.button_code.setCheckable(True)
        self.button_code.clicked.connect(lambda flag: self.select_tab(self.TAB_CODE, flag))
        buttons_layout.addWidget(self.button_code)

        self.button_tests = QPushButton("Тесты")
        self.button_tests.setFixedSize(50, 24)
        self.button_tests.setCheckable(True)
        self.button_tests.clicked.connect(lambda flag: self.select_tab(self.TAB_TESTS, flag))
        buttons_layout.addWidget(self.button_tests)

        self.button_testing = QPushButton("Тестирование")
        self.button_testing.setFixedSize(100, 24)
        self.button_testing.setCheckable(True)
        self.button_testing.clicked.connect(lambda flag: self.select_tab(self.TAB_TESTING, flag))
        buttons_layout.addWidget(self.button_testing)

        self.lab_widget = LabWidget(self.tm, self.sm)
        layout.addWidget(self.lab_widget)

        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setAlignment(Qt.AlignRight)
        layout.addLayout(right_layout)

        self.button_settings = Button(self.tm, 'generate', css='Menu', color='TextColor')
        self.button_settings.setFixedSize(30, 30)
        right_layout.addWidget(self.button_settings)

        self.current_tab = self.TAB_CODE

    def select_tab(self, index, flag):
        if index != self.TAB_CODE:
            self.button_code.setChecked(False)
        elif not flag:
            self.button_code.setChecked(True)
        if index != self.TAB_TESTS:
            self.button_tests.setChecked(False)
        elif not flag:
            self.button_tests.setChecked(True)
        if index != self.TAB_TESTING:
            self.button_testing.setChecked(False)
        elif not flag:
            self.button_testing.setChecked(True)
        self.tab_changed.emit(index)

    def set_theme(self):
        self.setStyleSheet(f"background-color: {self.tm['MenuColor']}; "
                           f"border-bottom: 1px solid {self.tm['BorderColor']};")
        # self.tm.auto_css(self.project_widget)
        for el in [self.button_code, self.button_tests, self.button_testing]:
            el.setStyleSheet(self.tm.button_css('Menu'))
            el.setFont(self.tm.font_small)
        self.lab_widget.set_theme()
        self.button_settings.set_theme(self.tm)
