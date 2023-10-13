from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea

from side_tabs.telegram.telegram_api import types
from side_tabs.telegram.telegram_manager import TelegramManager


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

        last_message_layout = QHBoxLayout()
        last_message_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(last_message_layout)

        self._last_message_label = LastMessageWidget(self._tm)
        self._last_message_label.mouseMoving.connect(lambda: self.set_hover(True))
        self._last_message_label.open_message(self._chat.last_message)
        last_message_layout.addWidget(self._last_message_label, 10)

        self._unread_count_label = Label(str(self._chat.unread_count))
        self._unread_count_label.mouseMoving.connect(lambda: self.set_hover(True))
        self._unread_count_label.setMinimumWidth(30)
        self._unread_count_label.setAlignment(Qt.AlignCenter)
        last_message_layout.addWidget(self._unread_count_label, 1)
        if self._chat.unread_count == 0:
            self._unread_count_label.hide()

        manager.updateChat.connect(self.update_chat)

    def update_chat(self, chat_id: str):
        if int(chat_id) != self._chat.id:
            return
        message = self._chat.last_message
        if isinstance(message, types.TgMessage):
            self._last_message_label.open_message(message)

        self._unread_count_label.setText(str(self._chat.unread_count))
        if self._chat.unread_count == 0:
            self._unread_count_label.hide()
        else:
            self._unread_count_label.show()

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

        self._text_label = Label()
        self._text_label.setFixedHeight(12)
        self._text_label.mouseMoving.connect(self.mouseMoving.emit)
        layout.addWidget(self._text_label)

    def set_theme(self):
        self._text_label.setFont(self._tm.font_small)

    def open_message(self, message: types.TgMessage):
        text = ""
        icon = None
        if message is not None:
            match message.content.__class__:
                case types.TgMessageText:
                    text = message.content.text.text
                case types.TgMessagePhoto:
                    icon = message.content.photo.minithumbnail
                    if message.content.caption.text:
                        text = message.content.caption.text
                    else:
                        text = "Фотография"

        self._text_label.setText(text[:40])
        if isinstance(icon, types.TgMinithumbnail):
            self._icon_label.show()
            self._icon_label.setPixmap(QPixmap(icon.load()))
        else:
            self._icon_label.hide()
