from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFontMetrics, QKeyEvent
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QScrollArea, QWidget, QHBoxLayout, QTextEdit

from side_tabs.chat import gpt
from side_tabs.chat.chat_bubble import ChatBubble
from ui.button import Button
from ui.side_panel_widget import SidePanelWidget


class ChatPanel(SidePanelWidget):
    def __init__(self, sm, bm, tm):
        super().__init__(sm, tm, "Чат", [])
        self.bm = bm

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._chat_widget = ChatWidget(self.sm, self.bm, self.tm)
        layout.addWidget(self._chat_widget)

    def set_theme(self):
        super().set_theme()
        self._chat_widget.set_theme()


class ChatWidget(QWidget):
    def __init__(self, sm, bm, tm):
        super().__init__()
        self._sm = sm
        self._bm = bm
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
        self._scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self._scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_widget.setLayout(self._scroll_layout)

        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)

        self._text_edit = ChatInputArea()
        self._text_edit.returnPressed.connect(self.send_message)
        bottom_layout.addWidget(self._text_edit, 1)

        self._button = Button(self._tm, "button_send")
        self._button.setFixedSize(30, 30)
        self._button.clicked.connect(self.send_message)
        bottom_layout.addWidget(self._button)

        self.looper = None
        self._last_bubble = None
        self._last_message = None
        self.messages = []

    def send_message(self):
        if not (text := self._text_edit.toPlainText()):
            return
        self.add_bubble(text, ChatBubble.SIDE_RIGHT)
        self._text_edit.setText("")
        self.messages.append({'role': 'user', 'content': text})
        self.looper = Looper(self.messages.copy())
        if isinstance(self.looper, Looper) and not self.looper.isFinished():
            self.looper.terminate()
        self._last_bubble = self.add_bubble('', ChatBubble.SIDE_LEFT)
        self._last_message = None
        self.looper.sendMessage.connect(self.add_text)
        self._bm.run_process(self.looper, 'GPT_chat', '1')

    def add_bubble(self, text, side):
        bubble = ChatBubble(self._bm, self._tm, text, side)
        self._add_buble(bubble)
        return bubble

    def _add_buble(self, bubble):
        self._scroll_layout.addWidget(bubble)
        self._bubbles.append(bubble)
        bubble.set_theme()

    def _insert_bubble(self, bubble):
        self._scroll_layout.insertWidget(0, bubble)
        self._bubbles.insert(0, bubble)
        bubble.set_theme()

    def add_text(self, text):
        self._last_bubble.add_text(text)
        if self._last_message is None:
            self._last_message = {'role': 'assistant', 'content': text}
            self.messages.append(self._last_message)
        else:
            self._last_message['content'] = self._last_bubble.text()

    def set_theme(self):
        for el in [self._scroll_area, self._text_edit, self._button]:
            self._tm.auto_css(el)
        for el in self._bubbles:
            el.set_theme()


class Looper(QThread):
    sendMessage = pyqtSignal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        for el in gpt.simple_response(self.text):
            self.sendMessage.emit(el)


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
        if e.key() == Qt.Key.Key_Return or e.key() == Qt.Key.Key_Enter:
            self.returnPressed.emit()
        else:
            super().keyPressEvent(e)
