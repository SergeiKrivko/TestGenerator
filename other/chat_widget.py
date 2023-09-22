from random import randint
from time import sleep

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFontMetrics, QKeyEvent
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QScrollArea, QWidget, QHBoxLayout, QTextEdit, QSizePolicy

from ui.button import Button
from ui.side_panel_widget import SidePanelWidget


class ChatPanel(SidePanelWidget):
    def __init__(self, sm, tm):
        super().__init__(sm, tm, "Чат", [])

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._chat_widget = ChatWidget(self.sm, self.tm)
        layout.addWidget(self._chat_widget)

    def set_theme(self):
        super().set_theme()
        self._chat_widget.set_theme()


class ChatWidget(QWidget):
    def __init__(self, sm, tm):
        super().__init__()
        self._sm = sm
        self._tm = tm

        self._bubbles = []

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._scroll_area = QScrollArea()
        layout.addWidget(self._scroll_area, 1)

        scroll_widget = QWidget()
        self._scroll_area.setWidget(scroll_widget)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_layout = QVBoxLayout()
        self._scroll_layout.setAlignment(Qt.AlignTop)
        # self._scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_widget.setLayout(self._scroll_layout)

        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)

        self._button_document = Button(self._tm, "telegram_document")
        self._button_document.setFixedSize(30, 30)
        bottom_layout.addWidget(self._button_document)

        self._button_tg_project = Button(self._tm, "button_to_zip")
        self._button_tg_project.setFixedSize(30, 30)
        bottom_layout.addWidget(self._button_tg_project)

        self._text_edit = ChatInputArea()
        self._text_edit.returnPressed.connect(self.send_message)
        bottom_layout.addWidget(self._text_edit, 1)

        self._button = Button(self._tm, "button_send")
        self._button.setFixedSize(30, 30)
        self._button.clicked.connect(self.send_message)
        bottom_layout.addWidget(self._button)

        self.looper = None

    def send_message(self):
        if not (text := self._text_edit.toPlainText()):
            return
        self.add_bubble(text, ChatBubble.SIDE_RIGHT)
        self._text_edit.setText("")
        self.looper = Looper(text)
        if isinstance(self.looper, Looper) and not self.looper.isFinished():
            self.looper.terminate()
        self.looper.sendMessage.connect(lambda answer: self.add_bubble(answer, ChatBubble.SIDE_LEFT))
        self.looper.start()

    def add_bubble(self, text, side):
        bubble = ChatBubble(self._tm, text, side)
        self._add_buble(bubble)

    def _add_buble(self, bubble):
        self._scroll_layout.addWidget(bubble)
        self._bubbles.append(bubble)
        bubble.set_theme()

    def _insert_bubble(self, bubble):
        self._scroll_layout.insertWidget(0, bubble)
        self._bubbles.insert(0, bubble)
        bubble.set_theme()

    def set_theme(self):
        for el in [self._scroll_area, self._text_edit, self._button, self._button_document, self._button_tg_project]:
            self._tm.auto_css(el)
        for el in self._bubbles:
            el.set_theme()


class Looper(QThread):
    sendMessage = pyqtSignal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        sleep(randint(1, 5))
        self.sendMessage.emit(self.text)


class ChatBubble(QWidget):
    SIDE_LEFT = 0
    SIDE_RIGHT = 1

    _BORDER_RADIUS = 10

    def __init__(self, tm, text, side):
        super().__init__()
        self._tm = tm
        self._side = side
        self._text = text

        layout = QHBoxLayout()
        layout.setDirection(QHBoxLayout.LeftToRight if self._side == ChatBubble.SIDE_LEFT else QHBoxLayout.RightToLeft)
        layout.setAlignment(Qt.AlignLeft if self._side == ChatBubble.SIDE_LEFT else Qt.AlignRight)
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        font_metrics = QFontMetrics(self._tm.font_medium)

        self._label = QLabel(self._text)
        self._label.setWordWrap(True)
        self._label.setMaximumWidth(font_metrics.size(0, self._text).width() + 20)
        self._label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        layout.addWidget(self._label, 10)

        widget = QWidget()
        layout.addWidget(widget, 1)

    def set_theme(self):
        css = f"""color: {self._tm['TextColor']}; 
            background-color: {self._tm['BgColor']};
            border: 1px solid {self._tm['BorderColor']};
            border-top-left-radius: {ChatBubble._BORDER_RADIUS}px;
            border-top-right-radius: {ChatBubble._BORDER_RADIUS}px;
            border-bottom-left-radius: {0 if self._side == ChatBubble.SIDE_LEFT else ChatBubble._BORDER_RADIUS}px;
            border-bottom-right-radius: {0 if self._side == ChatBubble.SIDE_RIGHT else ChatBubble._BORDER_RADIUS}px;
            padding: 4px;"""
        self._label.setStyleSheet(css)
        self._label.setFont(self._tm.font_medium)


class ChatInputArea(QTextEdit):
    returnPressed = pyqtSignal()
    resize = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        self.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self):
        height = self.verticalScrollBar().maximum()
        if not height:
            self.setFixedHeight(30)
            height = self.verticalScrollBar().maximum()
        self.setFixedHeight(min(300, self.height() + height))

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            self.returnPressed.emit()
        else:
            super().keyPressEvent(e)
