import datetime
from uuid import UUID

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QHBoxLayout, QTextEdit, QLabel, QLineEdit, QSpinBox, \
    QDoubleSpinBox

from side_tabs.chat import gpt, GPTDialog
from side_tabs.chat.chat_bubble import ChatBubble
from ui.button import Button
from ui.custom_dialog import CustomDialog


class ChatWidget(QWidget):
    buttonBackPressed = pyqtSignal(UUID)

    def __init__(self, sm, bm, tm, dialog: GPTDialog):
        super().__init__()
        self._sm = sm
        self._bm = bm
        self._tm = tm
        self._dialog = dialog

        self._bubbles = []

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(top_layout)

        self._button_back = Button(self._tm, 'button_back')
        self._button_back.setFixedSize(36, 36)
        self._button_back.clicked.connect(lambda: self.buttonBackPressed.emit(self._dialog.id))
        top_layout.addWidget(self._button_back)

        self._name_label = QLabel(dialog.name if dialog.name.strip() else 'Диалог')
        top_layout.addWidget(self._name_label)

        self._button_settings = Button(self._tm, 'generate')
        self._button_settings.setFixedSize(36, 36)
        self._button_settings.clicked.connect(self._open_settings)
        top_layout.addWidget(self._button_settings)

        self._scroll_area = QScrollArea()
        layout.addWidget(self._scroll_area, 1)

        scroll_widget = _ScrollWidget()
        scroll_widget.resized.connect(self._scroll)
        self._scroll_area.setWidget(scroll_widget)
        self._scroll_area.verticalScrollBar().valueChanged.connect(self._on_scrolled)
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
        self._to_bottom = True

        for el in self._dialog.messages:
            self.add_bubble(el.get('content', ''),
                            ChatBubble.SIDE_RIGHT if el.get('role') == 'user' else ChatBubble.SIDE_LEFT)

    def send_message(self):
        if not ((text := self._text_edit.toPlainText()).strip()):
            return
        self.add_bubble(text, ChatBubble.SIDE_RIGHT)
        self._text_edit.setText("")
        self._dialog.append_message('user', text)
        self.looper = Looper(self._dialog.messages[-self._dialog.used_messages:], temperature=self._dialog.temperature)
        if isinstance(self.looper, Looper) and not self.looper.isFinished():
            self.looper.terminate()
        self._last_bubble = self.add_bubble('', ChatBubble.SIDE_LEFT)
        self._last_message = None
        self.looper.sendMessage.connect(self.add_text)
        self._bm.run_process(self.looper, 'GPT_chat', str(self._dialog.id))

    def add_bubble(self, text, side):
        bubble = ChatBubble(self._bm, self._tm, text, side)
        self._add_buble(bubble)
        return bubble

    def _add_buble(self, bubble):
        bubble.deleteRequested.connect(lambda: self._delete_message(bubble))
        self._scroll_layout.addWidget(bubble)
        self._bubbles.append(bubble)
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
        self._last_bubble.add_text(text)
        if self._last_message is None:
            self._last_message = self._dialog.append_message('assistant', text)
        else:
            self._last_message['content'] += text
            self._dialog.store()

    def _on_scrolled(self):
        self._to_bottom = abs(self._scroll_area.verticalScrollBar().maximum() -
                              self._scroll_area.verticalScrollBar().value()) < 5
        self._dialog.scrolling_pos = self._scroll_area.verticalScrollBar().value()

    def _scroll(self):
        if self._to_bottom:
            self._scroll_area.verticalScrollBar().setValue(self._scroll_area.verticalScrollBar().maximum())

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        self._scroll_area.verticalScrollBar().setValue(self._dialog.scrolling_pos)

    def _open_settings(self):
        dialog = ChatSettingsWindow(self._tm, self._dialog)
        dialog.exec()
        dialog.save()
        self._dialog.store()
        self._name_label.setText(self._dialog.name if self._dialog.name.strip() else 'Диалог')

    def set_theme(self):
        for el in [self._scroll_area, self._text_edit, self._button, self._button_back, self._name_label,
                   self._button_settings]:
            self._tm.auto_css(el)
        for el in self._bubbles:
            el.set_theme()


class Looper(QThread):
    sendMessage = pyqtSignal(str)

    def __init__(self, text, **kwargs):
        super().__init__()
        self.text = text
        self.kwargs = kwargs

    def run(self):
        for el in gpt.stream_response(self.text, **self.kwargs):
            self.sendMessage.emit(el)


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


class ChatSettingsWindow(CustomDialog):
    def __init__(self, tm, dialog: GPTDialog):
        super().__init__(tm, "Настройки диалога", True, True)
        self._dialog = dialog

        self._labels = []
        self.setFixedWidth(300)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        label = QLabel("Название диалога")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._name_label = QLineEdit()
        self._name_label.setText(self._dialog.name)
        main_layout.addWidget(self._name_label)

        self._time_label = QLabel()
        self._time_label.setText(f"Создан: {datetime.datetime.fromtimestamp(self._dialog.time).strftime('%D %H:%M')}")
        self._labels.append(self._time_label)
        main_layout.addWidget(self._time_label)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(layout)

        label = QLabel("Используемые сообщения:")
        self._labels.append(label)
        layout.addWidget(label)

        self._used_messages_box = QSpinBox()
        self._used_messages_box.setMinimum(0)
        self._used_messages_box.setMaximum(20)
        self._used_messages_box.setValue(self._dialog.used_messages)
        layout.addWidget(self._used_messages_box)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(layout)

        label = QLabel("Максимум сообщений:")
        self._labels.append(label)
        layout.addWidget(label)

        self._saved_messages_box = QSpinBox()
        self._saved_messages_box.setMinimum(0)
        self._saved_messages_box.setMaximum(200)
        self._saved_messages_box.setValue(self._dialog.saved_messages)
        layout.addWidget(self._saved_messages_box)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(layout)

        label = QLabel("Temperature:")
        self._labels.append(label)
        layout.addWidget(label)

        self._temperature_box = QDoubleSpinBox()
        self._temperature_box.setMinimum(0)
        self._temperature_box.setMaximum(1)
        self._temperature_box.setSingleStep(0.01)
        self._temperature_box.setValue(self._dialog.temperature)
        layout.addWidget(self._temperature_box)

    def save(self):
        self._dialog.name = self._name_label.text()
        self._dialog.used_messages = self._used_messages_box.value()
        self._dialog.saved_messages = self._saved_messages_box.value()
        self._dialog.temperature = self._temperature_box.value()

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        self.set_theme()

    def set_theme(self):
        super().set_theme()
        for el in self._labels:
            self.tm.auto_css(el)
        for el in [self._name_label, self._used_messages_box, self._saved_messages_box, self._temperature_box]:
            self.tm.auto_css(el)


class _ScrollWidget(QWidget):
    resized = pyqtSignal()

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self.resized.emit()
