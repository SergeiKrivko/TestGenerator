from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QHBoxLayout, QTextEdit

from ui.button import Button


class ChatWidget(QWidget):
    loadRequested = pyqtSignal()

    def __init__(self, sm, tm):
        super().__init__()
        self._sm = sm
        self._tm = tm

        self._bubbles = []

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._scroll_area = _ScrollArea()
        self._scroll_area.loadRequested.connect(self.loadRequested.emit)
        layout.addWidget(self._scroll_area, 1)

        scroll_widget = _ScrollWidget()
        self._scroll_area.setWidget(scroll_widget)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_layout = QVBoxLayout()
        self._scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
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

        self._last_pos = 0
        self._last_max = 0

    def send_message(self):
        pass

    def add_bubble(self, text, side):
        pass

    def _add_buble(self, bubble):
        self._scroll_layout.addWidget(bubble)
        self._bubbles.append(bubble)
        bubble.set_theme()

    def _insert_bubble(self, bubble):
        self._scroll_layout.insertWidget(0, bubble)
        self._bubbles.insert(0, bubble)
        bubble.set_theme()

    def _delete_bubbles(self, message_ids):
        message_ids = set(message_ids)
        i = 0
        while i < len(self._bubbles):
            if self._bubbles[i]._message.id in message_ids:
                self._bubbles[i].setParent(None)
                self._bubbles.pop(i)

            i += 1

    def set_theme(self):
        for el in [self._scroll_area, self._text_edit, self._button, self._button_document, self._button_tg_project]:
            self._tm.auto_css(el)
        for el in self._bubbles:
            el.set_theme()


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


class _ScrollArea(QScrollArea):
    loadRequested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._last_pos = 0
        self._last_max = 0
        self.verticalScrollBar().valueChanged.connect(self._on_scrolled)

    def setWidget(self, w: '_ScrollWidget') -> None:
        super().setWidget(w)
        w.resized.connect(self._on_resized)

    def _on_scrolled(self, pos):
        if pos < 50:
            self.loadRequested.emit()

    def _on_resized(self) -> None:
        self._last_pos = self.verticalScrollBar().value()
        if self._last_pos > self._last_max - 10:
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        elif self._last_pos < 50:
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum() -
                                              self._last_max + self._last_pos)

        self._last_max = self.verticalScrollBar().maximum()


class _ScrollWidget(QWidget):
    resized = pyqtSignal()

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self.resized.emit()
