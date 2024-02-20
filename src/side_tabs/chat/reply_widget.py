from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton

from src.side_tabs.chat.chat import GPTChat
from src.side_tabs.chat.message import GPTMessage
from src.ui.button import Button


class ReplyList(QWidget):
    scrollRequested = pyqtSignal(int)

    def __init__(self, tm, chat: GPTChat, mode=1):
        super().__init__()
        self._tm = tm
        self._chat = chat
        self._mode = mode

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._messages = list()
        self._widgets = dict()

    def add_message(self, message: GPTMessage):
        message_id = message.id
        if message_id in self._messages:
            return

        index = 0
        if self._messages:
            for i in self._chat.message_ids:
                if i == message_id:
                    break
                if i == self._messages[index]:
                    index += 1
                    if index == len(self._messages):
                        break

        self._messages.insert(index, message_id)
        item = _ReplyItem(self._tm, message, can_be_deleted=self._mode == 1)

        item.deleteRequested.connect(self.delete_item)
        item.scrollRequested.connect(self.scrollRequested.emit)

        item.setMaximumWidth(self.width())
        item.setMinimumWidth(0)
        self._widgets[message_id] = item
        self._layout.insertWidget(index, item)
        self.show()

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        for el in self._widgets.values():
            el.setMaximumWidth(self.width())

    def delete_item(self, message_id):
        self._messages.remove(message_id)
        self._widgets[message_id].setParent(None)
        if not self._messages:
            self.hide()

    def clear(self):
        for el in self._widgets.values():
            el.setParent(None)
        self._widgets.clear()
        self._messages.clear()
        self.hide()

    @property
    def messages(self):
        for el in self._messages:
            yield el


class _ReplyItem(QPushButton):
    deleteRequested = pyqtSignal(int)
    scrollRequested = pyqtSignal(int)

    def __init__(self, tm, message: GPTMessage, can_be_deleted=True):
        super().__init__()
        self._message = message
        self._tm = tm
        self._can_be_deleted = can_be_deleted

        self.setIcon(QIcon(self._tm.get_image('buttons/reply')))
        self.setFixedHeight(26)
        self.clicked.connect(lambda: self.scrollRequested.emit(self._message.id))

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(36, 2, 2, 2)
        self.setLayout(main_layout)

        self._label = QLabel(self._message.content.split('\n')[0])
        self._label.setFixedHeight(16)
        self._label.setWordWrap(True)
        main_layout.addWidget(self._label)

        self._button = Button(self._tm, 'buttons/button_delete')
        self._button.clicked.connect(lambda: self.deleteRequested.emit(self._message.id))
        self._button.setFixedSize(22, 22)
        main_layout.addWidget(self._button, Qt.AlignmentFlag.AlignRight)
        if not self._can_be_deleted:
            self._button.hide()

        self.set_theme()

    def set_theme(self):
        self.setStyleSheet(self._tm.button_css(palette='Main', border=True, padding=True, align='left'))
        for el in [self._label, self._button]:
            self._tm.auto_css(el, palette='Main')
        self._label.setStyleSheet(f"background-color: #00000000; border: none;")
