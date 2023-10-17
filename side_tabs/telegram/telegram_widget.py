import datetime
import os

from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QDialog, QLineEdit, QPushButton, QFileDialog

import config
from other.chat_widget import ChatWidget, ChatInputArea
from side_tabs.telegram.chat_bubble import TelegramChatBubble
from side_tabs.telegram.chat_list_widget import TelegramListWidget
from side_tabs.telegram.telegram_api import types
from side_tabs.telegram.telegram_manager import TelegramManager
from ui.button import Button
from ui.side_panel_widget import SidePanelWidget


enabled = config.secret_data and os.name != 'posix'


class TelegramWidget(SidePanelWidget):
    def __init__(self, sm, tm):
        super().__init__(sm, tm, "Telegram", [])

        if not enabled:
            return

        self._manager = TelegramManager(self.sm)
        self._manager.newChat.connect(self.add_chat)
        self._manager.addMessage.connect(self.add_message)
        self._manager.insertMessage.connect(self.insert_message)
        self._manager.loadingFinished.connect(self.loading_finished)
        self._manager.authorization.connect(self.get_authentication_data)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._list_widget = TelegramListWidget(self.tm, self._manager)
        self._list_widget.currentItemChanged.connect(self.show_chat)
        layout.addWidget(self._list_widget)

        self._chats_layout = QVBoxLayout()
        self._chats_layout.setSpacing(0)
        self._chats_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self._chats_layout)

        self._top_panel = TelegramTopWidget(self.tm, self._manager)
        self._top_panel.hide()
        self._top_panel.buttonBackPressed.connect(lambda: self.show_chat(None))
        self._chats_layout.addWidget(self._top_panel)

        self._chat_widgets = dict()
        self._current_chat = None

        self._manager_started = False
        # self._manager.start()

    def show(self):
        if enabled and not self._manager_started:
            self._manager.start()
            self._manager_started = True
        super().show()

    def add_message(self, message: types.TgMessage):
        self._chat_widgets[message.chat_id].add_message(message)

    def insert_message(self, message: types.TgMessage):
        self._chat_widgets[message.chat_id].insert_message(message)

    def loading_finished(self, chat: types.TgChat):
        self._chat_widgets[chat.id].check_if_need_to_load()

    def add_chat(self, chat):
        self._list_widget.add_item(chat)

        chat_widget = TelegramChatWidget(self.sm, self.tm, chat, self._manager)
        chat_widget.hide()
        chat_widget.set_theme()
        self._chat_widgets[chat.id] = chat_widget
        self._chats_layout.addWidget(chat_widget)

    def show_chat(self, chat_id):
        if isinstance(chat_id, str):
            chat_id = int(chat_id)
        if chat_id in self._chat_widgets:
            if self._current_chat in self._chat_widgets:
                self._chat_widgets[self._current_chat].hide()
            self._list_widget.hide()
            self._top_panel.show()
            self._top_panel.set_chat(self._manager.get_chat(chat_id))
            self._chat_widgets[chat_id].show()
            self._current_chat = chat_id
            self._manager.open_chat(chat_id)
            # self._manager.get_messages(chat_id)
        else:
            if self._current_chat in self._chat_widgets:
                self._chat_widgets[self._current_chat].hide()
            self._list_widget.show()
            self._top_panel.hide()
            self._list_widget.set_current_id(None)
            self._current_chat = None

    def get_authentication_data(self, state):
        dialog = PasswordWidget(self.tm, state)
        if dialog.exec():
            self._manager.authenticate_user(dialog.get_str1(), dialog.get_str2())

    def finish_work(self):
        if enabled:
            self._manager.terminate()

    def set_theme(self):
        super().set_theme()
        if not enabled:
            return
        self._top_panel.set_theme()
        self._list_widget.set_theme()
        for el in self._chat_widgets.values():
            el.set_theme()


class TelegramChatWidget(ChatWidget):
    sendMessage = pyqtSignal(str)
    SB_VALUE_TO_LOAD = 20

    def __init__(self, sm, tm, chat: types.TgChat, manager: TelegramManager):
        super().__init__(sm, tm)
        self._chat = chat
        self._manager = manager

        self._scroll_bar = self._scroll_area.verticalScrollBar()
        self._scroll_bar.valueChanged.connect(self._on_scroll_bar_value_changed)

        self._messages_to_load = 50

        if not self._chat.permissions.can_send_messages:
            self._text_edit.hide()
            self._button.hide()

        self._button_document.clicked.connect(self._sending_document)

    def show(self) -> None:
        if self.isHidden():
            self._scroll_bar.setValue(self._scroll_bar.maximum())
            self.check_if_need_to_load()
        super().show()

    def _sending_document(self):
        path, _ = QFileDialog.getOpenFileName(caption="Выберите файл для отправки")
        if path:
            dialog = SendFileDialog(self._tm, path, self._text_edit.toPlainText())
            if dialog.exec():
                self._manager.send_file_message(dialog.text_area.toPlainText(), dialog.file_name_line.text(),
                                                self._chat.id)

    def check_if_need_to_load(self):
        if self._chat.message_count() < self._messages_to_load:
            self._manager.load_messages(self._chat)

    def _on_scroll_bar_value_changed(self):
        for el in self._bubbles:
            if 0 < el.y() - self._scroll_bar.value() + el.height() < self.height():
                el.set_read()

    def add_messages_to_load(self):
        self._messages_to_load = self._chat.message_count() + 50

    def add_message(self, message: types.TgMessage):
        self.add_bubble(message)

    def insert_message(self, message: types.TgMessage):
        self.insert_bubble(message)

    def insert_bubble(self, message: types.TgMessage):
        bubble = TelegramChatBubble(self._tm, message, self._manager)
        bubble.set_max_width(int(self.width() * 0.8))
        if isinstance(self._chat.type, types.TgChatTypePrivate):
            bubble.hide_sender()
        self._insert_bubble(bubble)

    def add_bubble(self, message: types.TgMessage, *args):
        bubble = TelegramChatBubble(self._tm, message, self._manager)
        bubble.set_max_width(int(self.width() * 0.8))
        if isinstance(self._chat.type, types.TgChatTypePrivate):
            bubble.hide_sender()
        self._add_buble(bubble)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        for el in self._bubbles:
            el.set_max_width(min(500, int(self.width() * 0.7)))

    def send_message(self):
        if not (text := self._text_edit.toPlainText()):
            return
        # self.sendMessage.emit(text)
        self._manager.send_message(text, self._chat.id)
        self._text_edit.setText("")


class TelegramTopWidget(QWidget):
    buttonBackPressed = pyqtSignal()

    def __init__(self, tm, manager: TelegramManager):
        super().__init__()
        self._tm = tm
        self._manager = manager
        self._chat = None

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(3, 3, 3, 3)
        self.setLayout(layout)

        self._button_back = Button(self._tm, 'button_back')
        self._button_back.setFixedSize(36, 36)
        self._button_back.clicked.connect(self.buttonBackPressed.emit)
        layout.addWidget(self._button_back)

        labels_layout = QVBoxLayout()
        layout.addLayout(labels_layout)

        self._name_label = QLabel()
        labels_layout.addWidget(self._name_label)

        self._status_label = QLabel()
        labels_layout.addWidget(self._status_label)

        self._manager.updateUserStatus.connect(self._on_user_status_updated)

    def set_chat(self, chat: types.TgChat):
        self._chat = chat
        self._name_label.setText(chat.title)
        if isinstance(chat.type, types.TgChatTypePrivate):
            self._status_label.show()
            user = self._manager.get_user(chat.type.user_id)
            if isinstance(user.status, types.TgUserStatusOnline):
                self._status_label.setText("В сети")
            else:
                self._status_label.setText(f"Был(а) в {self.get_time(user.status.was_online)}")
        else:
            self._status_label.hide()

    @staticmethod
    def get_time(t: int):
        return datetime.datetime.fromtimestamp(t).strftime("%H:%M")

    def _on_user_status_updated(self, user_id: str | int):
        if not isinstance(self._chat, types.TgChat):
            return
        user_id = int(user_id)
        if isinstance(self._chat.type, types.TgChatTypePrivate):
            self._status_label.show()
            user = self._manager.get_user(self._chat.type.user_id)
            if isinstance(user.status, types.TgUserStatusOnline):
                self._status_label.setText("В сети")
            else:
                self._status_label.setText(f"Был(а) в {self.get_time(user.status.was_online)}")

    def set_theme(self):
        for el in [self._name_label]:
            self._tm.auto_css(el)
        self._button_back.set_theme()


class PasswordWidget(QDialog):
    def __init__(self, tm, state):
        super().__init__()

        if isinstance(state, types.TgAuthorizationStateWaitPhoneNumber):
            self._text = "Пожалуйста, введите свой номер телефона:"
            self._password_mode = False
            self._2_lines = False
        elif isinstance(state, types.TgAuthorizationStateWaitCode):
            self._text = "Пожалуйста, введите полученный вами код аутентификации:"
            self._password_mode = True
            self._2_lines = False
        elif isinstance(state, types.TgAuthorizationStateWaitEmailAddress):
            self._text = "Пожалуйста, введите свой адрес электронной почты:"
            self._password_mode = False
            self._2_lines = False
        elif isinstance(state, types.TgAuthorizationStateWaitEmailCode):
            self._text = "Пожалуйста, введите полученный вами по электронной почте код аутентификации:"
            self._password_mode = True
            self._2_lines = False
        elif isinstance(state, types.TgAuthorizationStateWaitRegistration):
            self._text = "Пожалуйста, введите имя и фамилию:"
            self._password_mode = True
            self._2_lines = True
        elif isinstance(state, types.TgAuthorizationStateWaitPassword):
            self._text = "Пожалуйста, введите свой пароль:"
            self._password_mode = True
            self._2_lines = False

        layout = QVBoxLayout()
        self.setLayout(layout)

        self._label = QLabel(self._text)
        layout.addWidget(self._label)

        self._line_edit = QLineEdit()
        if self._password_mode:
            self._line_edit.setEchoMode(QLineEdit.Password)
        self._line_edit.returnPressed.connect(self.accept)
        layout.addWidget(self._line_edit)

        self._line_edit2 = QLineEdit()
        if self._password_mode:
            self._line_edit2.setEchoMode(QLineEdit.Password)
        self._line_edit2.returnPressed.connect(self.accept)
        if not self._2_lines:
            self._line_edit2.hide()
        layout.addWidget(self._line_edit2)

        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        self._button = QPushButton("OK")
        self._button.clicked.connect(self.accept)
        buttons_layout.addWidget(self._button)

        self.setStyleSheet(tm.bg_style_sheet)
        for el in [self._label, self._line_edit, self._button, self._line_edit2]:
            tm.auto_css(el)

    def get_str1(self):
        return self._line_edit.text()

    def get_str2(self):
        return self._line_edit2.text()


class SendFileDialog(QDialog):
    def __init__(self, tm, file, text=''):
        super().__init__()
        self._tm = tm
        self.setWindowTitle("Отправка файла")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.file_name_line = QLineEdit()
        self.file_name_line.setText(file)
        self.file_name_line.setReadOnly(True)
        layout.addWidget(self.file_name_line)

        self.text_area = ChatInputArea()
        self.text_area.setText(text)
        layout.addWidget(self.text_area)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(buttons_layout)

        self._button_cancel = QPushButton("Отмена")
        self._button_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(self._button_cancel)

        self._button_send = QPushButton("Отправить")
        self._button_send.clicked.connect(self.accept)
        buttons_layout.addWidget(self._button_send)

        for el in [self.file_name_line, self.text_area, self._button_send, self._button_cancel]:
            self._tm.auto_css(el)
