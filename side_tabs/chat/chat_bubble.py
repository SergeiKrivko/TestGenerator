from time import sleep

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QTextEdit


class ChatBubble(QWidget):
    SIDE_LEFT = 0
    SIDE_RIGHT = 1

    _BORDER_RADIUS = 10

    def __init__(self, bm, tm, text, side):
        super().__init__()
        self._tm = tm
        self._bm = bm
        self._side = side
        self._text = text

        layout = QHBoxLayout()
        layout.setDirection(QHBoxLayout.Direction.LeftToRight if self._side == ChatBubble.SIDE_LEFT
                            else QHBoxLayout.Direction.RightToLeft)
        layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft if self._side == ChatBubble.SIDE_LEFT else Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        # font_metrics = QFontMetrics(self._tm.font_medium)

        self._text_edit = QTextEdit()
        self._text_edit.setMarkdown(text)
        self._text_edit.setReadOnly(True)
        # self._text_edit.setMaximumWidth(font_metrics.size(0, self._text).width() + 20)
        self._text_edit.textChanged.connect(self._resize)
        layout.addWidget(self._text_edit, 10)

        widget = QWidget()
        layout.addWidget(widget, 1)

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self._resize()

    def _resize(self):
        self._text_edit.setFixedHeight(10)
        self._text_edit.setFixedHeight(10 + self._text_edit.verticalScrollBar().maximum())

    def add_text(self, text: str):
        self._text += text
        self._text_edit.setMarkdown(self._text)

    def text(self):
        return self._text

    def set_theme(self):
        css = f"""color: {self._tm['TextColor']}; 
            background-color: {self._tm['BgColor']};
            border: 1px solid {self._tm['BorderColor']};
            border-top-left-radius: {ChatBubble._BORDER_RADIUS}px;
            border-top-right-radius: {ChatBubble._BORDER_RADIUS}px;
            border-bottom-left-radius: {0 if self._side == ChatBubble.SIDE_LEFT else ChatBubble._BORDER_RADIUS}px;
            border-bottom-right-radius: {0 if self._side == ChatBubble.SIDE_RIGHT else ChatBubble._BORDER_RADIUS}px;
            padding: 4px;"""
        self._text_edit.setStyleSheet(css)
        self._text_edit.setFont(self._tm.font_medium)
