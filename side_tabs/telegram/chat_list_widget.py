from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea

from side_tabs.telegram.telegram_api import tg
from side_tabs.telegram.telegram_manager import TelegramManager, TgChat


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
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.setContentsMargins(2, 2, 2, 2)
        scroll_widget.setLayout(self._layout)

        self._items = dict()

    def clear(self):
        for el in self._items.values():
            el.setParent(None)
            el.disabled = True
            el.hide()
        self._items.clear()

    def _on_chat_updated(self, chat_id):
        for el in self._items.values():
            el.update_chat(chat_id)

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

    def add_item(self, chat: TgChat):
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
        width = self.width() - 19
        for el in self._items.values():
            el.setFixedWidth(width)

    def set_theme(self):
        self._tm.auto_css(self, border_radius=False)
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

    def __init__(self, tm, chat: TgChat, manager: TelegramManager):
        super().__init__()
        self._tm = tm
        self._chat = chat
        self._chat_id = chat.id
        self._selected = False
        self._hover = False
        self._manager = manager
        self.disabled = False

        self.setFixedHeight(54)

        strange_layout = QVBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)
        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(2, 2, 2, 2)
        strange_widget.setLayout(main_layout)

        self._icon_label = Label()
        self._icon_label.mouseMoving.connect(lambda: self.set_hover(True))
        self._icon_label.setFixedWidth(54)
        self._photo = None
        if chat.photo is not None:
            self._photo = chat.photo.small
            if self._photo.local.can_be_downloaded:
                tg.downloadFile(self._photo.id, 1)
            # manager.updateFile.connect(self.update_icon)
            if self._photo.local.is_downloading_completed:
                self._icon_label.setPixmap(QPixmap(self._photo.local.path).scaled(48, 48))
        main_layout.addWidget(self._icon_label)

        layout = QVBoxLayout()
        main_layout.addLayout(layout)

        self._name_label = Label(self._chat.title)
        self._name_label.mouseMoving.connect(lambda: self.set_hover(True))
        layout.addWidget(self._name_label)

        last_message_layout = QHBoxLayout()
        last_message_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(last_message_layout)

        self._last_message_label = LastMessageWidget(self._tm)
        self._last_message_label.mouseMoving.connect(lambda: self.set_hover(True))
        self.update_last_message(self._chat.last_message)
        last_message_layout.addWidget(self._last_message_label, 10)

        self._unread_count_label = Label(str(self._chat.unread_count))
        self._unread_count_label.mouseMoving.connect(lambda: self.set_hover(True))
        self._unread_count_label.setMinimumWidth(30)
        self._unread_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        last_message_layout.addWidget(self._unread_count_label, 1)
        if self._chat.unread_count == 0:
            self._unread_count_label.hide()

    def update_last_message(self, message):
        if message is not None and (isinstance(self._chat.type, tg.ChatTypeBasicGroup) or
                                    isinstance(self._chat.type, tg.ChatTypeSupergroup) and hasattr(
                    message.sender_id, 'user_id')):
            sender = self._manager.get_user(message.sender_id.user_id)
        else:
            sender = None
        self._last_message_label.open_message(message, sender)

    def update_chat(self, chat_id: str):
        if int(chat_id) != self._chat.id or self.disabled:
            return
        message = self._chat.last_message
        if isinstance(message, tg.Message):
            self.update_last_message(message)

        self._unread_count_label.setText(str(self._chat.unread_count))
        if self._chat.unread_count == 0:
            self._unread_count_label.hide()
        else:
            self._unread_count_label.show()

    def update_icon(self, image: tg.File):
        if isinstance(self._photo, tg.File) and image.id == self._photo.id and \
                self._photo.local.is_downloading_completed:
            self._icon_label.setPixmap(QPixmap(self._photo.local.path).scaled(44, 44))

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.set_selected(True)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if 0 < a0.pos().x() < self.width() and 0 < a0.pos().y() < self.height():
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
        self._name_label.setFont(self._tm.font_medium)
        self._last_message_label.set_theme()
        self._unread_count_label.setStyleSheet(f"background-color: {self._tm['MenuColor']};"
                                               f"border: 0px solid black;"
                                               f"border-radius: 8px;"
                                               f"padding: 3px;")
        self._unread_count_label.setFont(self._tm.font_medium)


class LastMessageWidget(QWidget):
    mouseMoving = pyqtSignal()

    def __init__(self, tm):
        super().__init__()
        self._tm = tm

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setMinimumWidth(0)

        self._icon_label = Label()
        self._icon_label.hide()
        self._icon_label.setFixedSize(20, 20)
        self._icon_label.mouseMoving.connect(self.mouseMoving.emit)
        layout.addWidget(self._icon_label)

        v_layout = QVBoxLayout()
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        v_layout.setSpacing(1)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(v_layout)

        # self._sender_label = Label()
        # self._sender_label.setWordWrap(True)
        # self._sender_label.setFixedHeight(12)
        # self._sender_label.mouseMoving.connect(self.mouseMoving.emit)
        # v_layout.addWidget(self._sender_label)

        self._text_label = Label()
        self._text_label.setWordWrap(True)
        self._text_label.setFixedHeight(26)
        self._text_label.mouseMoving.connect(self.mouseMoving.emit)
        v_layout.addWidget(self._text_label)

    def set_theme(self):
        self._text_label.setFont(self._tm.font_small)
        # self._sender_label.setFont(self._tm.font_small)
        # self._sender_label.setStyleSheet(f"color: {self._tm['TestPassed'].name()}")

    def open_message(self, message: tg.Message, sender: tg.User = None):
        text = ""
        icon = None

        if sender:
            # self._sender_label.show()
            text += sender.first_name + ': '

        if message is not None:
            match message.content.__class__:
                case tg.MessageText:
                    text += message.content.text.text
                case tg.MessagePhoto:
                    icon = message.content.photo.minithumbnail
                    if message.content.caption.text:
                        text += message.content.caption.text
                    else:
                        text += "Фотография"

        self._text_label.setText(text[:80])
        if isinstance(icon, tg.Minithumbnail):
            self._icon_label.show()
            # self._icon_label.setPixmap(QPixmap(icon.load()))
        else:
            self._icon_label.hide()
