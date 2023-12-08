from PyQt6.QtCore import pyqtSignal, Qt, QPoint
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

from ui.lab_widget import LabWidget
from ui.button import Button


class MainMenu(QWidget):
    tab_changed = pyqtSignal(str)
    closeButtonClicked = pyqtSignal()
    moveWindow = pyqtSignal(QPoint)
    maximize = pyqtSignal()
    minimize = pyqtSignal()
    hideWindow = pyqtSignal()

    def __init__(self, sm, bm, tm):
        super().__init__()
        self.sm = sm
        self.bm = bm
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

        self._buttons = dict()
        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.setContentsMargins(0, 0, 0, 0)
        self._buttons_layout.setSpacing(5)
        layout.addLayout(self._buttons_layout)

        self.lab_widget = LabWidget(self.tm, self.sm, self.bm)
        layout.addWidget(self.lab_widget)

        self._widget = QWidget()
        layout.addWidget(self._widget, 1000)

        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)
        layout.addLayout(right_layout)

        self.button_settings = Button(self.tm, 'buttons/generate', css='Menu', color='TextColor')
        self.button_settings.setFixedSize(30, 30)
        right_layout.addWidget(self.button_settings)

        self.button_hide = Button(self.tm, 'buttons/button_hide_window', css='Menu', color='TextColor')
        self.button_hide.clicked.connect(self.hideWindow.emit)
        self.button_hide.setFixedSize(30, 30)
        right_layout.addWidget(self.button_hide)

        self.button_minimize = Button(self.tm, 'buttons/button_minimize_window', css='Menu', color='TextColor')
        self.button_minimize.hide()
        self.button_minimize.clicked.connect(self._on_minimize_clicked)
        self.button_minimize.setFixedSize(30, 30)
        right_layout.addWidget(self.button_minimize)

        self.button_maximize = Button(self.tm, 'buttons/button_maximize_window', css='Menu', color='TextColor')
        self.button_maximize.setFixedSize(30, 30)
        self.button_maximize.clicked.connect(self._on_maximize_clicked)
        right_layout.addWidget(self.button_maximize)

        self.button_close = Button(self.tm, 'buttons/button_close', css='Menu', color='TextColor')
        self.button_close.setFixedSize(30, 30)
        self.button_close.clicked.connect(self.closeButtonClicked.emit)
        right_layout.addWidget(self.button_close)

        self.current_tab = ''
        self.last_pos = None
        self.moving = False
        self.maximized = False

    def add_tab(self, identifier: str, name: str):
        button = QPushButton(name)
        button.setCheckable(True)
        button.clicked.connect(lambda flag: self.select_tab(identifier, flag))
        self._buttons_layout.addWidget(button, 1, Qt.AlignmentFlag.AlignLeft)

        self._buttons[identifier] = button

        button.setStyleSheet(self.tm.button_css(palette='Menu', border=False, padding=True))
        button.setFont(self.tm.font_medium)

    def mouseDoubleClickEvent(self, a0) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
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
        if a0.button() == Qt.MouseButton.LeftButton and not self.maximized:
            self.moving = True
            self.last_pos = a0.pos()

    def mouseReleaseEvent(self, a0) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.moving = False
            self.last_pos = None

    def mouseMoveEvent(self, a0) -> None:
        if self.moving:
            self.moveWindow.emit(a0.pos() - self.last_pos)

    def select_tab(self, triggered_key, flag):
        for key, item in self._buttons.items():
            if triggered_key != key:
                item.setChecked(False)
            elif not flag:
                item.setChecked(True)
        if triggered_key != self.current_tab:
            self.current_tab = triggered_key
            self.tab_changed.emit(triggered_key)

    def set_theme(self):
        self.setStyleSheet(f"background-color: {self.tm['MenuColor']}; "
                           f"border-bottom: 1px solid {self.tm['BorderColor']};")
        self._widget.setStyleSheet("border: none;")
        for el in self._buttons.values():
            el.setStyleSheet(self.tm.button_css(palette='Menu', border=False, padding=True))
            el.setFont(self.tm.font_medium)
        self.lab_widget.set_theme()
        for el in [self.button_minimize, self.button_maximize, self.button_settings, self.button_close,
                   self.button_hide]:
            el.set_theme()
