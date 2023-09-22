from PyQt5.QtCore import pyqtSignal, Qt, QPoint
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton

from settings.lab_widget import LabWidget
from ui.button import Button


class MainMenu(QWidget):
    TAB_CODE = 0
    TAB_TESTS = 1
    TAB_TESTING = 2
    TAB_UNIT_TESTING = 3
    tab_changed = pyqtSignal(int)
    closeButtonClicked = pyqtSignal()
    moveWindow = pyqtSignal(QPoint)
    maximize = pyqtSignal()
    minimize = pyqtSignal()
    hideWindow = pyqtSignal()

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
        buttons_layout.setSpacing(5)
        layout.addLayout(buttons_layout)

        self.button_code = QPushButton("Код")
        # self.button_code.setFixedSize(50, 24)
        self.button_code.setCheckable(True)
        self.button_code.clicked.connect(lambda flag: self.select_tab(self.TAB_CODE, flag))
        buttons_layout.addWidget(self.button_code, 1, Qt.AlignLeft)

        self.button_tests = QPushButton("Тесты")
        # self.button_tests.setFixedSize(60, 24)
        self.button_tests.setCheckable(True)
        self.button_tests.clicked.connect(lambda flag: self.select_tab(self.TAB_TESTS, flag))
        buttons_layout.addWidget(self.button_tests, 1, Qt.AlignLeft)

        self.button_testing = QPushButton("Тестирование")
        # self.button_testing.setFixedSize(115, 24)
        self.button_testing.setCheckable(True)
        self.button_testing.clicked.connect(lambda flag: self.select_tab(self.TAB_TESTING, flag))
        buttons_layout.addWidget(self.button_testing, 1, Qt.AlignLeft)

        self.button_unit_testing = QPushButton("Модульное тестирование")
        # self.button_testing.setFixedSize(115, 24)
        self.button_unit_testing.setCheckable(True)
        self.button_unit_testing.clicked.connect(lambda flag: self.select_tab(self.TAB_UNIT_TESTING, flag))
        buttons_layout.addWidget(self.button_unit_testing, 1, Qt.AlignLeft)

        self.lab_widget = LabWidget(self.tm, self.sm)
        layout.addWidget(self.lab_widget)

        self._widget = QWidget()
        layout.addWidget(self._widget, 1000)

        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)
        layout.addLayout(right_layout)

        self.button_settings = Button(self.tm, 'generate', css='Menu', color='TextColor')
        self.button_settings.setFixedSize(30, 30)
        right_layout.addWidget(self.button_settings)

        self.button_hide = Button(self.tm, 'button_hide_window', css='Menu', color='TextColor')
        self.button_hide.clicked.connect(self.hideWindow.emit)
        self.button_hide.setFixedSize(30, 30)
        right_layout.addWidget(self.button_hide)

        self.button_minimize = Button(self.tm, 'button_minimize_window', css='Menu', color='TextColor')
        self.button_minimize.hide()
        self.button_minimize.clicked.connect(self._on_minimize_clicked)
        self.button_minimize.setFixedSize(30, 30)
        right_layout.addWidget(self.button_minimize)

        self.button_maximize = Button(self.tm, 'button_maximize_window', css='Menu', color='TextColor')
        self.button_maximize.setFixedSize(30, 30)
        self.button_maximize.clicked.connect(self._on_maximize_clicked)
        right_layout.addWidget(self.button_maximize)

        self.button_close = Button(self.tm, 'button_close', css='Menu', color='TextColor')
        self.button_close.setFixedSize(30, 30)
        self.button_close.clicked.connect(self.closeButtonClicked.emit)
        right_layout.addWidget(self.button_close)

        self.current_tab = self.TAB_CODE
        self.last_pos = None
        self.moving = False
        self.maximized = False

    def mouseDoubleClickEvent(self, a0) -> None:
        if a0.button() == Qt.LeftButton:
            if self.maximized:
                self._on_minimize_clicked()
            else:
                self._on_maximize_clicked()

    def _on_minimize_clicked(self):
        self.maximized = False
        self.button_minimize.hide()
        self.button_maximize.show()
        self.minimize.emit()

    def _on_maximize_clicked(self):
        self.maximized = True
        self.button_maximize.hide()
        self.button_minimize.show()
        self.maximize.emit()

    def mousePressEvent(self, a0) -> None:
        if a0.button() == Qt.LeftButton and not self.maximized:
            self.moving = True
            self.last_pos = a0.pos()

    def mouseReleaseEvent(self, a0) -> None:
        if a0.button() == Qt.LeftButton:
            self.moving = False
            self.last_pos = None

    def mouseMoveEvent(self, a0) -> None:
        if self.moving:
            self.moveWindow.emit(a0.pos() - self.last_pos)

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
        if index != self.TAB_UNIT_TESTING:
            self.button_unit_testing.setChecked(False)
        elif not flag:
            self.button_unit_testing.setChecked(True)
        self.tab_changed.emit(index)

    def set_theme(self):
        self.setStyleSheet(f"background-color: {self.tm['MenuColor']}; "
                           f"border-bottom: 1px solid {self.tm['BorderColor']};")
        self._widget.setStyleSheet("border: none;")
        for el in [self.button_code, self.button_tests, self.button_testing, self.button_unit_testing]:
            el.setStyleSheet(self.tm.button_css(palette='Menu', border=False, padding=True))
            el.setFont(self.tm.font_medium)
        self.lab_widget.set_theme()
        for el in [self.button_minimize, self.button_maximize, self.button_settings, self.button_close,
                   self.button_hide]:
            el.set_theme()
