import os.path

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QWidget, QPushButton, QLabel, QScrollArea


class CompilerErrorWindow(QDialog):
    def __init__(self, text: str, tm, mask=''):
        super().__init__()
        self.setWindowTitle("Ошибка компиляции")
        self.setStyleSheet(tm.bg_style_sheet)
        self.tm = tm
        if '{file}' in mask and '{line}' in mask:
            self._mask = mask
            self._prefix = self._mask[:self._mask.index("{file}")]
            self._sep = self._mask[self._mask.index("{file}") + len("{file}"):self._mask.index("{line}")]
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
        self.scroll_layout.setAlignment(Qt.AlignTop)
        scroll_widget.setLayout(self.scroll_layout)
        main_layout.addWidget(self.scroll_area)

        for line in text.split('\n'):
            if self._mask:
                file, n, new_line = self.parse_line(line)
                if file:
                    button = LinkButton(self.tm, file, n)
                    button.pressed.connect(self.button_triggered)
                    self.scroll_layout.addWidget(button)
                    self.add_label(new_line)
                else:
                    self.add_label(line)
            else:
                self.add_label(line)

        # QBtn = QDialogButtonBox.Ok
        # self.buttonBox = QDialogButtonBox(QBtn)
        # self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.button(QDialogButtonBox.Ok).setStyleSheet(tm.button_css('Main'))
        # self.buttonBox.button(QDialogButtonBox.Ok).setFont(tm.font_small)
        # self.buttonBox.button(QDialogButtonBox.Ok).setFixedSize(80, 20)
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
        try:
            text = text[len(self._prefix):]
            file = text[:text.index(self._sep)]
            if not os.path.isfile(file):
                file = ''
            else:
                text = text[text.index(self._sep) + len(self._sep):]
                line = int(text[:text.index(self._suffix)])
                text = text[text.index(self._suffix):]
            return file, line, text
        except IndexError:
            return '', 0, old_text
        except ValueError:
            # text = text[text.index(self._suffix):]
            return '', 0, old_text

    def add_label(self, text):
        label = QLabel(text)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        label.setWordWrap(True)
        label.setFont(self.tm.code_font)
        self.scroll_layout.addWidget(label)

    def connect_button(self, widget, file, pos):
        widget.clicked.connect(lambda: self.button_triggered(file, pos))

    def button_triggered(self, file, pos):
        self.goto = file, pos
        self.accept()


class LinkButton(QPushButton):
    pressed = pyqtSignal(str, int)

    def __init__(self, tm, file, line):
        super().__init__()

        self.file = file
        self.line = line

        self.setText(f"{file}: line {line}")
        tm.auto_css(self)
        self.clicked.connect(lambda: self.pressed.emit(self.file, self.line))

        self.setFixedSize(QFontMetrics(tm.font_small).size(0, self.text()).width() + 22, 22)
