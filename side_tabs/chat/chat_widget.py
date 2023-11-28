from time import sleep
from uuid import UUID

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QHBoxLayout, QTextEdit, QLabel

from side_tabs.chat import gpt
from side_tabs.chat.gpt_dialog import GPTDialog
from side_tabs.chat.chat_bubble import ChatBubble
from side_tabs.chat.settings_window import ChatSettingsWindow
from ui.button import Button
from ui.message_box import MessageBox


class ChatWidget(QWidget):
    buttonBackPressed = pyqtSignal(UUID)
    updated = pyqtSignal()

    def __init__(self, sm, bm, tm, dialog: GPTDialog):
        super().__init__()
        self._sm = sm
        self._bm = bm
        self._tm = tm
        self._dialog = dialog

        self._bubbles = []

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 10, 0)
        self.setLayout(layout)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(top_layout)

        self._button_back = Button(self._tm, 'button_back', css='Main')
        self._button_back.setFixedSize(36, 36)
        self._button_back.clicked.connect(lambda: self.buttonBackPressed.emit(self._dialog.id))
        top_layout.addWidget(self._button_back)

        self._name_label = QLabel(dialog.name if dialog.name.strip() else 'Диалог')
        top_layout.addWidget(self._name_label)

        self._button_settings = Button(self._tm, 'generate', css='Main')
        self._button_settings.setFixedSize(36, 36)
        self._button_settings.clicked.connect(self._open_settings)
        top_layout.addWidget(self._button_settings)

        self._scroll_area = QScrollArea()
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

        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)

        self._text_edit = ChatInputArea()
        self._text_edit.returnPressed.connect(self.send_message)
        bottom_layout.addWidget(self._text_edit, 1)

        self._button = Button(self._tm, "button_send", css='Main')
        self._button.setFixedSize(30, 30)
        self._button.clicked.connect(self.send_message)
        bottom_layout.addWidget(self._button)

        self.looper = None
        self._last_bubble = None
        self._last_message = None
        self._to_bottom = True
        self._messages_is_loaded = False

    def _load_messages(self):
        self._messages_is_loaded = True
        loader = MessageLoader(self._dialog)
        loader.messageLoaded.connect(self.insert_bubble)
        self._bm.run_process(loader, 'GPT', f"load-{self._dialog.id}")

    def send_message(self):
        if not ((text := self._text_edit.toPlainText()).strip()):
            return
        self.add_bubble(text, ChatBubble.SIDE_RIGHT)
        self._text_edit.setText("")
        self._dialog.append_message('user', text)

        messages = self._dialog.system_prompts()
        messages.extend(self._dialog.messages[-self._dialog.used_messages:])

        self.looper = Looper(messages, self._dialog, temperature=self._dialog.temperature)
        if isinstance(self.looper, Looper) and not self.looper.isFinished():
            self.looper.terminate()
        self._last_message = None
        self._progress_marker.show()
        self.looper.sendMessage.connect(self.add_text)
        self.looper.exception.connect(self._on_gpt_error)
        self.looper.finished.connect(self._progress_marker.hide)
        self._bm.run_process(self.looper, 'GPT', f'message-{self._dialog.id}')

    def add_bubble(self, text, side):
        bubble = ChatBubble(self._sm, self._bm, self._tm, text, side)
        self._add_bubble(bubble)
        return bubble

    def insert_bubble(self, text, side):
        bubble = ChatBubble(self._sm, self._bm, self._tm, text, side)
        self._add_bubble(bubble, 0)
        return bubble

    def set_top_hidden(self, hidden):
        for el in [self._name_label, self._button_settings, self._button_back]:
            el.setHidden(hidden)

    def _add_bubble(self, bubble, index=None):
        bubble.deleteRequested.connect(lambda: self._delete_message(bubble))
        if index is None:
            self.updated.emit()
            self._scroll_layout.addWidget(bubble)
            self._bubbles.append(bubble)
        else:
            self._scroll_layout.insertWidget(index, bubble)
            self._bubbles.insert(index, bubble)
        bubble.set_theme()

    def _insert_bubble(self, bubble):
        self._scroll_layout.insertWidget(0, bubble)
        self._bubbles.insert(0, bubble)
        bubble.set_theme()

    def _delete_message(self, bubble):
        for i, b in enumerate(self._bubbles):
            if b == bubble:
                self._bubbles.pop(i)
                self._dialog.pop_message(i)
                bubble.setParent(None)
                break

    def add_text(self, text):
        if self._last_message is None:
            self._last_bubble = self.add_bubble('', ChatBubble.SIDE_LEFT)
            self._last_message = self._dialog.append_message('assistant', text)
        else:
            self._last_message['content'] += text
            self._dialog.store()
        self._last_bubble.add_text(text)

    def _on_scrolled(self):
        self._to_bottom = abs(self._scroll_area.verticalScrollBar().maximum() -
                              self._scroll_area.verticalScrollBar().value()) < 5
        self._dialog.scrolling_pos = self._scroll_area.verticalScrollBar().value()

    def _scroll(self):
        if self._to_bottom:
            self._scroll_area.verticalScrollBar().setValue(self._scroll_area.verticalScrollBar().maximum())

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        if not self._messages_is_loaded:
            self._load_messages()
        self._scroll_area.verticalScrollBar().setValue(self._dialog.scrolling_pos)

    def _open_settings(self):
        dialog = ChatSettingsWindow(self._sm, self._tm, self._dialog)
        dialog.exec()
        dialog.save()
        self._dialog.store()
        self._name_label.setText(self._dialog.name if self._dialog.name.strip() else 'Диалог')

    def _on_gpt_error(self, ex):
        MessageBox(MessageBox.Icon.Warning, "Ошибка", f"{ex.__class__.__name__}: {ex}", self._tm)

    def set_theme(self):
        self._scroll_widget.setStyleSheet(self._tm.base_css(palette='Main', border=False))
        for el in [self._scroll_area, self._text_edit, self._button, self._button_back, self._name_label,
                   self._button_settings]:
            self._tm.auto_css(el)
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
            for el in gpt.stream_response(self.text, model=self.chat.model, **self.kwargs):
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
        if (e.key() == Qt.Key.Key_Return or e.key() == Qt.Key.Key_Enter) and not self._shift_pressed:
            self.returnPressed.emit()
        elif e.key() == Qt.Key.Key_Shift:
            self._shift_pressed = True
            super().keyPressEvent(e)
        else:
            super().keyPressEvent(e)

    def keyReleaseEvent(self, e) -> None:
        if e.key() == Qt.Key.Key_Shift:
            self._shift_pressed = False
        super().keyPressEvent(e)


class _ScrollWidget(QWidget):
    resized = pyqtSignal()

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self.resized.emit()


class MessageLoader(QThread):
    messageLoaded = pyqtSignal(str, int)

    def __init__(self, dialog):
        super().__init__()
        self._dialog = dialog

    def run(self) -> None:
        for el in reversed(self._dialog.messages):
            self.messageLoaded.emit(el.get('content', ''),
                                    ChatBubble.SIDE_RIGHT if el.get('role') == 'user' else ChatBubble.SIDE_LEFT)
            sleep(0.1)
