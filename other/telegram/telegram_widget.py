from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QScrollArea, QDialog, QLineEdit, QPushButton, \
    QFileDialog

import config
from other.chat_widget import ChatWidget, ChatBubble, ChatInputArea
from other.telegram.chat_bubble import TelegramChatBubble
from other.telegram.telegram_api import types
from other.telegram.telegram_manager import TelegramManager
from ui.button import Button
from ui.side_panel_widget import SidePanelWidget


class TelegramWidget(SidePanelWidget):
    def __init__(self, sm, tm):
        super().__init__(sm, tm, "Telegram", [])

        if config.secret_data:
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

        self._top_panel = TelegramTopWidget(self.tm)
        self._top_panel.hide()
        self._top_panel.buttonBackPressed.connect(lambda: self.show_chat(None))
        self._chats_layout.addWidget(self._top_panel)

        self._chat_widgets = dict()
        self._current_chat = None

        self._manager_started = False
        # self._manager.start()

    def show(self):
        if not self._manager_started and config.secret_data:
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
            self._top_panel.set_chat_name(self._manager.get_chat(chat_id).title)
            self._chat_widgets[chat_id].show()
            self._current_chat = chat_id
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
        if config.secret_data:
            self._manager.terminate()

    def set_theme(self):
        super().set_theme()
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
        self.check_if_need_to_load()

    def add_messages_to_load(self):
        self._messages_to_load = self._chat.message_count() + 50

    def add_message(self, message: types.TgMessage):
        self.add_bubble(message)

    def insert_message(self, message: types.TgMessage):
        self.insert_bubble(message)

    def insert_bubble(self, message: types.TgMessage):
        bubble = TelegramChatBubble(self._tm, message, self._manager)
        bubble.set_max_width(int(self.width() * 0.8))
        self._insert_bubble(bubble)

    def add_bubble(self, message: types.TgMessage, *args):
        bubble = TelegramChatBubble(self._tm, message, self._manager)
        bubble.set_max_width(int(self.width() * 0.8))
        self._add_buble(bubble)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        for el in self._bubbles:
            el.set_max_width(min(300, int(self.width() * 0.7)))

    def send_message(self):
        if not (text := self._text_edit.toPlainText()):
            return
        # self.sendMessage.emit(text)
        self._manager.send_message(text, self._chat.id)
        self._text_edit.setText("")


class TelegramListWidget(QScrollArea):
    currentItemChanged = pyqtSignal(str)

    def __init__(self, tm, manager: TelegramManager):
        super().__init__()
        self._tm = tm
        self._manager = manager

        scroll_widget = QWidget()
        self.setWidget(scroll_widget)
        self.setWidgetResizable(True)

        self._layout = QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        scroll_widget.setLayout(self._layout)

        self._items = dict()

    def _on_item_hover(self, chat_id):
        if isinstance(chat_id, str):
            chat_id = int(chat_id)
        for key, item in self._items.items():
            if key != chat_id:
                item.set_hover(False)

    def _on_item_selected(self, chat_id):
        if isinstance(chat_id, str):
            chat_id = int(chat_id)
        for key, item in self._items.items():
            if key != chat_id:
                item.set_selected(False)
        self.currentItemChanged.emit(str(chat_id))

    def set_current_id(self, chat_id):
        for key, item in self._items.items():
            if key != chat_id:
                item.set_selected(False)
        if chat_id in self._items:
            self._items[chat_id].set_selected(True)

    def add_item(self, chat: types.TgChat):
        item = TelegramListWidgetItem(self._tm, chat, self._manager)
        item.selected.connect(self._on_item_selected)
        item.hover.connect(self._on_item_hover)
        chat_id = chat.id
        item.set_theme()
        self._items[chat_id] = item
        self._layout.addWidget(item)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self._set_items_width()

    def _set_items_width(self):
        width = self.width() - 15
        for el in self._items.values():
            el.setFixedWidth(width)

    def set_theme(self):
        self._tm.auto_css(self)
        for item in self._items.values():
            item.set_theme()


class Label(QLabel):
    mouseMoving = pyqtSignal()

    def __init__(self, text=''):
        super().__init__(text)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.mouseMoving.emit()
        super().mouseMoveEvent(ev)


class TelegramListWidgetItem(QWidget):
    PALETTE = 'Main'
    selected = pyqtSignal(str)
    hover = pyqtSignal(str)

    def __init__(self, tm, chat: types.TgChat, manager: TelegramManager):
        super().__init__()
        self._tm = tm
        self._chat = chat
        self._chat_id = chat.id
        self._selected = False
        self._hover = False

        self.setFixedHeight(50)

        strange_layout = QVBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)
        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(3, 3, 3, 3)
        strange_widget.setLayout(main_layout)

        self._icon_label = Label()
        self._icon_label.mouseMoving.connect(lambda: self.set_hover(True))
        self._icon_label.setFixedWidth(50)
        self._photo = None
        if chat.photo is not None:
            self._photo = chat.photo.small
            if self._photo.local.can_be_downloaded:
                self._photo.download()
            manager.updateFile.connect(self.update_icon)
            if self._photo.local.is_downloading_completed:
                self._icon_label.setPixmap(QPixmap(self._photo.local.path).scaled(44, 44))
        main_layout.addWidget(self._icon_label)

        layout = QVBoxLayout()
        main_layout.addLayout(layout)

        self._name_label = Label(self._chat.title)
        self._name_label.mouseMoving.connect(lambda: self.set_hover(True))
        layout.addWidget(self._name_label)

    def update_icon(self, image: types.TgFile):
        if isinstance(self._photo, types.TgFile) and image.id == self._photo.id and \
                self._photo.local.is_downloading_completed:
            self._icon_label.setPixmap(QPixmap(self._photo.local.path).scaled(44, 44))

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self.set_selected(True)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if 0 < a0.x() < self.width() and 0 < a0.y() < self.height():
            self.set_hover(True)
        else:
            self.set_hover(False)

    def set_selected(self, status):
        if self._selected == bool(status):
            return
        self._selected = bool(status)
        self.set_theme()
        if status:
            self.selected.emit(str(self._chat_id))

    def set_hover(self, hover):
        hover = bool(hover)
        if self._hover == hover:
            return
        self._hover = hover
        self.set_theme()
        if hover:
            self.hover.emit(str(self._chat_id))

    def set_theme(self):
        if self._selected:
            suffix = "Selected"
        elif self._hover:
            suffix = "Hover"
        else:
            suffix = ""
        self.setStyleSheet(f"""background-color: {self._tm[f'{TelegramListWidgetItem.PALETTE}{suffix}Color']};
                               border: 0px solid {self._tm[f'{TelegramListWidgetItem.PALETTE}BorderColor']};
                               color: {self._tm['TextColor']};""")
        self._name_label.setStyleSheet("border: none;")
        self._name_label.setFont(self._tm.font_small)


class TelegramTopWidget(QWidget):
    buttonBackPressed = pyqtSignal()

    def __init__(self, tm):
        super().__init__()
        self._tm = tm

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
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

    def set_chat_name(self, name):
        self._name_label.setText(name)

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
        buttons_layout.setAlignment(Qt.AlignRight)
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


