from time import sleep

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QHBoxLayout, QTextEdit, QLabel, QApplication

from src.side_tabs.chat import gpt
from src.side_tabs.chat.reply_widget import ReplyList
from src.side_tabs.chat.chat import GPTChat
from src.side_tabs.chat.chat_bubble import ChatBubble
from src.side_tabs.chat.settings_window import ChatSettingsWindow
from src.side_tabs.chat.message import GPTMessage
from src.ui.button import Button
from src.ui.message_box import MessageBox


class ChatWidget(QWidget):
    buttonBackPressed = pyqtSignal(int)
    updated = pyqtSignal()

    def __init__(self, bm, tm, chat: GPTChat):
        super().__init__()
        self._bm = bm
        self._tm = tm
        self._chat = chat

        self._bubbles = dict()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 10, 0)
        self.setLayout(layout)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(top_layout)

        self._button_back = Button(self._tm, 'buttons/button_back', css='Bg')
        self._button_back.setFixedSize(36, 36)
        self._button_back.clicked.connect(lambda: self.buttonBackPressed.emit(self._chat.id))
        top_layout.addWidget(self._button_back)

        self._name_label = QLabel(chat.name if chat.name and chat.name.strip() else 'Диалог')
        top_layout.addWidget(self._name_label)

        self._button_settings = Button(self._tm, 'buttons/generate', css='Bg')
        self._button_settings.setFixedSize(36, 36)
        self._button_settings.clicked.connect(self._open_settings)
        top_layout.addWidget(self._button_settings)

        self._scroll_area = ScrollArea()
        layout.addWidget(self._scroll_area, 1)

        self._scroll_widget = _ScrollWidget()
        self._scroll_widget.resized.connect(self._scroll)
        self._scroll_area.setWidget(self._scroll_widget)
        self._scroll_area.verticalScrollBar().valueChanged.connect(self._on_scrolled)
        self._scroll_area.setWidgetResizable(True)

        scroll_layout = QVBoxLayout()
        self._scroll_area.setLayout(scroll_layout)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._scroll_layout = QVBoxLayout()
        self._scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._scroll_layout.setContentsMargins(0, 0, 0, 0)
        self._scroll_widget.setLayout(scroll_layout)
        scroll_layout.addLayout(self._scroll_layout)

        self._progress_marker = QLabel("GPT печатает...")
        scroll_layout.addWidget(self._progress_marker)
        self._progress_marker.hide()

        self._reply_list = ReplyList(self._tm, self._chat)
        self._reply_list.hide()
        self._reply_list.scrollRequested.connect(self.scroll_to_message)
        layout.addWidget(self._reply_list)

        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)

        self._text_edit = ChatInputArea()
        self._text_edit.returnPressed.connect(self.send_message)
        bottom_layout.addWidget(self._text_edit, 1)

        self._button = Button(self._tm, "buttons/button_send", css='Bg')
        self._button.setFixedSize(30, 30)
        self._button.clicked.connect(self.send_message)
        bottom_layout.addWidget(self._button)

        self._button_scroll = Button(self._tm, 'buttons/down_arrow', css='Bg')
        self._button_scroll.setFixedSize(36, 36)
        self._scroll_area.resized.connect(
            lambda: self._button_scroll.move(self._scroll_area.width() - 51, self._scroll_area.height() - 46))
        self._button_scroll.clicked.connect(lambda: self._scroll(True))
        self._button_scroll.setParent(self._scroll_area)

        self.looper = None
        self._last_bubble = None
        self._last_message = None
        self._to_bottom = True
        self._last_maximum = 0
        self._want_to_scroll = None
        self._messages_is_loaded = False
        self._loading_messages = False

    def _load_messages(self, to_message=None):
        self._loading_messages = True
        self._messages_is_loaded = True
        loader = MessageLoader(list(self._chat.load_messages(to_message=to_message)))
        loader.messageLoaded.connect(self.insert_bubble)
        loader.finished.connect(self._on_load_finished)
        self._bm.processes.run(loader, 'GPT', f"load-{self._chat.id}")

    def _on_load_finished(self):
        self._loading_messages = False
        if self._want_to_scroll is not None:
            self.scroll_to_message(self._want_to_scroll)
            self._want_to_scroll = None

    def send_message(self):
        if not ((text := self._text_edit.toPlainText()).strip()):
            return
        self.add_bubble(self._chat.add_message('user', text, tuple(self._reply_list.messages)))
        self._text_edit.setText("")

        messages = self._chat.messages_to_prompt(list(self._reply_list.messages))
        for el in self._reply_list.messages:
            self._chat.get_message(el).replied_count += 1
        self._reply_list.clear()

        self.looper = Looper(messages, self._chat, model=self._chat.model, temperature=self._chat.temperature)
        if isinstance(self.looper, Looper) and not self.looper.isFinished():
            self.looper.terminate()
        self._last_message = None
        self._progress_marker.show()
        self.looper.sendMessage.connect(self.add_text)
        self.looper.exception.connect(self._on_gpt_error)
        self.looper.finished.connect(self._progress_marker.hide)
        self.looper.start()

    def add_bubble(self, message: GPTMessage):
        bubble = ChatBubble(self._bm._sm, self._tm, self._chat, message)
        self._add_bubble(bubble)
        return bubble

    def insert_bubble(self, message: GPTMessage):
        bubble = ChatBubble(self._bm._sm, self._tm, self._chat, message)
        self._add_bubble(bubble, 0)
        return bubble

    def set_top_hidden(self, hidden):
        for el in [self._name_label, self._button_settings, self._button_back]:
            el.setHidden(hidden)

    def _add_bubble(self, bubble, index=None):
        bubble.deleteRequested.connect(lambda: self._delete_message(bubble.message.id))
        bubble.replyRequested.connect(lambda: self._reply_list.add_message(bubble.message))
        bubble.scrollRequested.connect(self.scroll_to_message)
        if index is None:
            self.updated.emit()
            self._scroll_layout.addWidget(bubble)
            self._bubbles[bubble.message.id] = bubble
        else:
            self._scroll_layout.insertWidget(index, bubble)
            self._bubbles[bubble.message.id] = bubble
        bubble.set_theme()

    def _delete_message(self, message_id):
        self._chat.delete_message(message_id)
        self._bubbles.pop(message_id).setParent(None)

    def add_text(self, text):
        if self._last_message is None:
            self._last_message = self._chat.add_message('assistant', text)
            self._last_bubble = self.add_bubble(self._last_message)
        else:
            self._last_bubble.add_text(text)

    def scroll_to_message(self, message_id):
        if message_id not in self._bubbles:
            if not self._chat.get_message(message_id).deleted:
                self._want_to_scroll = message_id
                self._load_messages(to_message=message_id)
            return
        self._scroll_area.verticalScrollBar().setValue(self._bubbles[message_id].pos().y() - 5)

    def _on_scrolled(self):
        self._to_bottom = abs(self._scroll_area.verticalScrollBar().maximum() -
                              self._scroll_area.verticalScrollBar().value()) < 20
        self._button_scroll.setHidden(abs(self._scroll_area.verticalScrollBar().maximum() -
                                          self._scroll_area.verticalScrollBar().value()) < 300)
        self._chat.scrolling_pos = self._scroll_area.verticalScrollBar().value()
        if self._scroll_area.verticalScrollBar().value() <= 100 and not self._loading_messages:
            self._load_messages()

    def _scroll(self, to_bottom=False):
        self._button_scroll.setHidden(self._to_bottom)
        if to_bottom or self._to_bottom:
            self._to_bottom = True
            self._scroll_area.verticalScrollBar().setValue(self._scroll_area.verticalScrollBar().maximum())
            if self._scroll_area.verticalScrollBar().value() < self._scroll_area.verticalScrollBar().maximum():
                self._scroll_area.verticalScrollBar().setValue(self._scroll_area.verticalScrollBar().maximum())
            self._button_scroll.setHidden(True)
        elif self._loading_messages:
            self._scroll_area.verticalScrollBar().setValue(self._scroll_area.verticalScrollBar().value() +
                                                           self._scroll_area.verticalScrollBar().maximum() -
                                                           self._last_maximum)
        self._last_maximum = self._scroll_area.verticalScrollBar().maximum()

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        if not self._messages_is_loaded:
            self._load_messages()
        # self._scroll_area.verticalScrollBar().setValue(self._chat.scrolling_pos)

    def hideEvent(self, a0) -> None:
        super().hideEvent(a0)
        lst = list(self._bubbles.keys())
        lst.sort(reverse=False)
        ind = 0
        for i, el in enumerate(lst):
            if self._bubbles[el].pos().y() < self._scroll_area.verticalScrollBar().value():
                ind = i
        ind -= 5
        if ind > 0:
            for el in self._chat.drop_messages(self._bubbles[lst[ind]].message.id):
                bubble: ChatBubble = self._bubbles.pop(el.id)
                bubble.setParent(None)
                bubble.disconnect()

    def _open_settings(self):
        dialog = ChatSettingsWindow(self._bm._sm, self._tm, self._chat)
        dialog.exec()
        dialog.save()
        self._name_label.setText(self._chat.name if self._chat.name.strip() else 'Диалог')
        self._chat._db.commit()

    def _on_gpt_error(self, ex):
        MessageBox(MessageBox.Icon.Warning, "Ошибка", f"{ex.__class__.__name__}: {ex}", self._tm)

    def set_theme(self):
        self._scroll_widget.setStyleSheet(self._tm.base_css(palette='Main', border=False))
        for el in [self._scroll_area, self._text_edit, self._button, self._button_back, self._name_label,
                   self._button_settings, self._button_scroll]:
            self._tm.auto_css(el)

        css = f"""
        QPushButton {{
            background-color: {self._tm['BgColor']};  
            border: 1px solid {self._tm['BorderColor']}; 
            border-radius: {self._button_scroll.width() // 2}px; 
        }}
        QPushButton:hover {{
            background-color: {self._tm['BgHoverColor']};
        }}
        """
        self._button_scroll.setStyleSheet(css)

        for el in self._bubbles:
            el.set_theme()


class Looper(QThread):
    sendMessage = pyqtSignal(str)
    exception = pyqtSignal(Exception)

    def __init__(self, text, chat, **kwargs):
        super().__init__()
        self.text = text
        self.chat = chat
        self.kwargs = kwargs

    def run(self):
        try:
            for el in gpt.stream_response(self.text, **self.kwargs):
                self.sendMessage.emit(el)
        except Exception as ex:
            self.exception.emit(ex)


class ChatInputArea(QTextEdit):
    returnPressed = pyqtSignal()
    resize = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        self.textChanged.connect(self._on_text_changed)

        self._shift_pressed = False

    def _on_text_changed(self):
        height = self.verticalScrollBar().maximum()
        if not height:
            self.setFixedHeight(30)
            height = self.verticalScrollBar().maximum()
        self.setFixedHeight(min(300, self.height() + height))

    def keyPressEvent(self, e: QKeyEvent) -> None:
        modifiers = QApplication.keyboardModifiers()
        if (e.key() == Qt.Key.Key_Return or e.key() == Qt.Key.Key_Enter) and \
                modifiers != Qt.KeyboardModifier.ShiftModifier:
            self.returnPressed.emit()
        else:
            super().keyPressEvent(e)


class _ScrollWidget(QWidget):
    resized = pyqtSignal()

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self.resized.emit()


class MessageLoader(QThread):
    messageLoaded = pyqtSignal(GPTMessage)

    def __init__(self, messages):
        super().__init__()
        self._messages = messages

    def run(self) -> None:
        for el in self._messages:
            self.messageLoaded.emit(el)
            sleep(0.1)


class ScrollArea(QScrollArea):
    resized = pyqtSignal()

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self.resized.emit()
