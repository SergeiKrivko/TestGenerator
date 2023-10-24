import os.path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QScrollArea

from ui.custom_dialog import CustomDialog


class CompilerErrorWindow(CustomDialog):
    def __init__(self, text: str, tm, mask='', name="Ошибка компиляции"):
        super().__init__(name, True)
        super().set_theme()
        if isinstance(mask, str) and '{file}' in mask and '{line}' in mask:
            self._mask = mask
            self._prefix = self._mask[:self._mask.index("{file}")]
            self._sep = self._mask[self._mask.index("{file}") + len("{file}"):self._mask.index("{line}")]
            if '{symbol}' in mask:
                self._sep2 = self._mask[self._mask.index("{line}") + len("{line}"):self._mask.index("{symbol}")]
                self._suffix = self._mask[self._mask.index("{symbol}") + len("{symbol}"):]
            else:
                self._sep2 = None
                self._suffix = self._mask[self._mask.index("{line}") + len("{line}"):]
        else:
            self._mask = ''

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 0, 10)

        self.scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.scroll_area.setWidget(scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.tm.auto_css(self.scroll_area, palette='Bg', border=False)
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setSpacing(1)
        # self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_widget.setLayout(self.scroll_layout)
        main_layout.addWidget(self.scroll_area)

        for line in text.split('\n'):
            if self._mask:
                file, n, m, new_line = self.parse_line(line)
                if file:
                    button = LinkButton(self.tm, file, n, m if self._sep2 is not None else None)
                    button.pressed.connect(self.button_triggered)
                    self.scroll_layout.addWidget(button)
                    self.add_label(new_line)
                else:
                    self.add_label(line)
            else:
                self.add_label(line)

        # QBtn = QDialogButtonBox.StandardButton.Ok
        # self.buttonBox = QDialogButtonBox(QBtn)
        # self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setStyleSheet(tm.button_css('Main'))
        # self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setFont(tm.font_small)
        # self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setFixedSize(80, 20)
        # main_layout.addWidget(self.buttonBox)

        self.setLayout(main_layout)
        self.resize(600, 520)
        self.goto = None

    def parse_line(self, text: str):
        if not text.startswith(self._prefix):
            return
        old_text = text
        file = ''
        line = 0
        symbol = 0
        try:
            text = text[len(self._prefix):]
            file = text[:text.index(self._sep)]
            if not os.path.isfile(file):
                file = ''
            else:
                text = text[text.index(self._sep) + len(self._sep):]
                if self._sep2 is None:
                    line = int(text[:text.index(self._suffix)])
                    text = text[text.index(self._suffix) + len(self._suffix):]
                else:
                    line = int(text[:text.index(self._sep2)])
                    text = text[text.index(self._sep2):]
                    symbol = int(text[len(self._sep2):text.index(self._suffix)])
                    text = text[text.index(self._suffix) + len(self._suffix):]
            return file, line, symbol, text
        except IndexError:
            return '', 0, 0, old_text
        except ValueError:
            # text = text[text.index(self._suffix):]
            return '', 0, 0, old_text

    def add_label(self, text):
        label = QLabel(text)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse |
                                      Qt.TextInteractionFlag.TextSelectableByKeyboard)
        label.setWordWrap(True)
        label.setFont(self.tm.code_font)
        self.scroll_layout.addWidget(label)

    def connect_button(self, widget, file, pos):
        widget.clicked.connect(lambda: self.button_triggered(file, pos))

    def button_triggered(self, file, line, symbol):
        self.goto = file, line, symbol
        self.accept()


class LinkButton(QPushButton):
    pressed = pyqtSignal(str, int, int)

    def __init__(self, tm, file, line, symbol=None):
        super().__init__()

        self.file = file
        self.line = line
        self.symbol = symbol

        self.setText(f"{file} {line}{f':{self.symbol}' if self.symbol is not None else ''}")
        tm.auto_css(self)
        self.clicked.connect(lambda: self.pressed.emit(self.file, self.line, self.symbol))

        self.setFixedSize(QFontMetrics(tm.font_medium).size(0, self.text()).width() + 22, 22)
