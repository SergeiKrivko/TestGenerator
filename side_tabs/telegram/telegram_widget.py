import datetime
import os

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTabBar

import config
from side_tabs.telegram.chat_list_widget import TelegramListWidget
from side_tabs.telegram.chat_widget import TelegramChatWidget
from side_tabs.telegram.send_message_dialog import SendMessageDialog
from side_tabs.telegram.telegram_api import tg
from side_tabs.telegram.telegram_manager import TelegramManager, TgChat
from ui.button import Button
from ui.custom_dialog import CustomDialog
from ui.side_panel_widget import SidePanelWidget

enabled = config.secret_data and os.name != 'posix'


class TelegramWidget(SidePanelWidget):
    def __init__(self, sm, bm, tm):
        super().__init__(sm, tm, "Telegram", [])
        self.bm = bm

        if not enabled:
            return

        self._manager = TelegramManager(self.sm, self.bm)
        self._manager.chatsLoaded.connect(self.update_chats)
        self._manager.addMessage.connect(self.add_message)
        self._manager.insertMessage.connect(self.insert_message)
        self._manager.loadingFinished.connect(self.loading_finished)
        self._manager.threadLoaded.connect(self._jump)
        self._manager.authorization.connect(self.get_authentication_data)
        self._manager.updateFolders.connect(self.update_folders)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)
        layout.addLayout(list_layout)

        self._tab_bar = QTabBar()
        self._tab_bar.setFixedHeight(26)
        self._tab_bar.currentChanged.connect(self._on_folder_selected)
        list_layout.addWidget(self._tab_bar)

        self._list_widget = TelegramListWidget(self.tm, self._manager)
        self._list_widget.currentItemChanged.connect(self.show_chat)
        list_layout.addWidget(self._list_widget)

        self._chats_layout = QVBoxLayout()
        self._chats_layout.setSpacing(0)
        self._chats_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self._chats_layout)

        self._top_panel = TelegramTopWidget(self.tm, self._manager)
        self._top_panel.hide()
        self._top_panel.buttonBackPressed.connect(self.hide_chat)
        self._chats_layout.addWidget(self._top_panel)

        self._chat_widgets = dict()
        self._current_chat = None
        self._last_chats = []

        self._manager_started = False
        self._folders = []
        # self._manager.start()

    def command(self, text, file=None, image=None, *args, **kwargs):
        dialog = SelectChatDialog(self.tm, self._manager)
        if dialog.exec():
            chat = self._manager.get_chat(dialog.chat)
            dialog2 = SendMessageDialog(self.tm, chat, text, SendMessageDialog.TEXT_ONLY)
            if dialog2.exec():
                tg.sendMessage(dialog.chat, input_message_content=tg.InputMessageText(
                    text=tg.FormattedText(text=dialog2.text_area.toPlainText())))

    def show(self):
        if enabled and not self._manager_started:
            self._manager.start()
            self._manager_started = True
        super().show()

    def update_folders(self, folders):
        self._folders = list(folders.values())
        for key in folders:
            self._tab_bar.addTab(key)

    def update_chats(self, chat_ids):
        self._list_widget.clear()
        for el in chat_ids:
            self.add_chat(self._manager.get_chat(el))

    def _on_folder_selected(self):
        tg.getChats(self._folders[self._tab_bar.currentIndex()], 100)

    def add_message(self, message: tg.Message):
        if (message.chat_id, message.message_thread_id) not in self._chat_widgets:
            return
        self._chat_widgets[(message.chat_id, message.message_thread_id)].add_message(message)

    def insert_message(self, message: tg.Message):
        self._chat_widgets[(message.chat_id, message.message_thread_id)].insert_message(message)

    def loading_finished(self, chat: TgChat, thread=0):
        self._chat_widgets[(chat.id, thread)].loading = False
        self._chat_widgets[(chat.id, thread)].check_if_need_to_load()

    def add_chat(self, chat, thread=0, messages=None):
        if thread == 0:
            self._list_widget.add_item(chat)
        if (chat.id, thread) in self._chat_widgets:
            return

        chat_widget = TelegramChatWidget(self.sm, self.tm, self._manager, chat, thread)
        chat_widget.hide()
        chat_widget.set_theme()
        chat_widget.jumpRequested.connect(self._jump)
        self._chat_widgets[(chat.id, thread)] = chat_widget
        self._chats_layout.addWidget(chat_widget)

    def _jump(self, thread_info: tg.MessageThreadInfo):
        self.add_chat(self._manager.get_chat(thread_info.chat_id), thread_info.message_thread_id,
                      messages=thread_info.messages)
        self.show_chat(thread_info.chat_id, thread_info.message_thread_id)

    def show_chat(self, chat_id, thread=0):
        if isinstance(chat_id, str):
            chat_id = int(chat_id)
        if chat_id is None:
            self.hide_chat()
            return
        if (chat_id, thread) not in self._chat_widgets:
            return
        if self._current_chat in self._chat_widgets:
            if len(self._last_chats) > 1 and (chat_id, thread) == self._last_chats[-1]:
                self._last_chats.pop(-1)
            else:
                self._last_chats.append(self._current_chat)
            self._chat_widgets[self._current_chat].hide()
        self._list_widget.hide()
        self._tab_bar.hide()
        self._top_panel.show()
        self._top_panel.set_chat(self._manager.get_chat(chat_id))
        self._chat_widgets[(chat_id, thread)].show()
        self._current_chat = (chat_id, thread)
        tg.openChat(chat_id)
        # self._manager.get_messages(chat_id)

    def hide_chat(self):
        if self._current_chat in self._chat_widgets:
            self._chat_widgets[self._current_chat].hide()
        self._current_chat = None
        if self._last_chats:
            self.show_chat(*self._last_chats.pop(-1))
        else:
            self._list_widget.show()
            self._tab_bar.show()
            self._top_panel.hide()
            self._list_widget.set_current_id(None)

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
        self.tm.auto_css(self._tab_bar)
        self._top_panel.set_theme()
        self._list_widget.set_theme()
        for el in self._chat_widgets.values():
            el.set_theme()


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

        self._button_back = Button(self._tm, 'buttons/button_back')
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

    def set_chat(self, chat: TgChat):
        self._chat = chat
        self._name_label.setText(chat.title)
        if isinstance(chat.type, tg.ChatTypePrivate):
            self._status_label.show()
            user = self._manager.get_user(chat.type.user_id)
            if isinstance(user.status, tg.UserStatusOnline):
                self._status_label.setText("В сети")
            else:
                self._status_label.setText(f"Был(а) в {self.get_time(user.status.was_online)}")
        else:
            self._status_label.hide()

    @staticmethod
    def get_time(t: int):
        return datetime.datetime.fromtimestamp(t).strftime("%H:%M")

    def _on_user_status_updated(self, user_id: str | int):
        if not isinstance(self._chat, TgChat):
            return
        user_id = int(user_id)
        if isinstance(self._chat.type, tg.ChatTypePrivate):
            self._status_label.show()
            user = self._manager.get_user(self._chat.type.user_id)
            if isinstance(user.status, tg.UserStatusOnline):
                self._status_label.setText("В сети")
            else:
                self._status_label.setText(f"Был(а) в {self.get_time(user.status.was_online)}")

    def set_theme(self):
        for el in [self._name_label]:
            self._tm.auto_css(el)
        self._button_back.set_theme()


class PasswordWidget(CustomDialog):
    def __init__(self, tm, state):
        super().__init__(tm, config.APP_NAME, button_close=True)
        super().set_theme()

        self.setFixedWidth(300)

        if isinstance(state, tg.AuthorizationStateWaitPhoneNumber):
            self._text = "Пожалуйста, введите свой номер телефона:"
            self._password_mode = False
            self._2_lines = False
        elif isinstance(state, tg.AuthorizationStateWaitCode):
            self._text = "Пожалуйста, введите полученный вами код аутентификации:"
            self._password_mode = True
            self._2_lines = False
        elif isinstance(state, tg.AuthorizationStateWaitEmailAddress):
            self._text = "Пожалуйста, введите свой адрес электронной почты:"
            self._password_mode = False
            self._2_lines = False
        elif isinstance(state, tg.AuthorizationStateWaitEmailCode):
            self._text = "Пожалуйста, введите полученный вами по электронной почте код аутентификации:"
            self._password_mode = True
            self._2_lines = False
        elif isinstance(state, tg.AuthorizationStateWaitRegistration):
            self._text = "Пожалуйста, введите имя и фамилию:"
            self._password_mode = True
            self._2_lines = True
        elif isinstance(state, tg.AuthorizationStateWaitPassword):
            self._text = "Пожалуйста, введите свой пароль:"
            self._password_mode = True
            self._2_lines = False

        layout = QVBoxLayout()
        self.setLayout(layout)

        self._label = QLabel(self._text)
        self._label.setWordWrap(True)
        layout.addWidget(self._label)

        self._line_edit = QLineEdit()
        if self._password_mode:
            self._line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self._line_edit.returnPressed.connect(self.accept)
        layout.addWidget(self._line_edit)

        self._line_edit2 = QLineEdit()
        if self._password_mode:
            self._line_edit2.setEchoMode(QLineEdit.EchoMode.Password)
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


class SelectChatDialog(CustomDialog):
    def __init__(self, tm, manager: TelegramManager):
        super().__init__(tm, "Выберите чат", True, True)
        self._manager = manager
        self.chat = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        self._list_widget = TelegramListWidget(tm, manager)
        self._list_widget.currentItemChanged.connect(self._on_chat_selected)
        layout.addWidget(self._list_widget)

        for el in self._manager._chats.values():
            self._list_widget.add_item(el)
        self.set_theme()

    def _on_chat_selected(self, chat_id):
        chat_id = int(chat_id)
        self.chat = chat_id
        self.accept()

    def set_theme(self):
        super().set_theme()
        self._list_widget.set_theme()
