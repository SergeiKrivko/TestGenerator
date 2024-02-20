from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal, Qt, QPoint
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QMenu

from src.side_tabs.chat.chat import GPTChat


class Widget(QWidget):
    mouseMove = pyqtSignal(QPoint)

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

    def mouseMoveEvent(self, a0) -> None:
        super().mouseMoveEvent(a0)
        self.mouseMove.emit(a0.pos())


class GPTListWidget(QScrollArea):
    currentItemChanged = pyqtSignal(int)
    deleteItem = pyqtSignal(int)

    def __init__(self, tm):
        super().__init__()
        self._tm = tm
        self.setMinimumWidth(240)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_widget = Widget()
        scroll_widget.mouseMove.connect(self._on_mouse_move)
        self.setWidget(scroll_widget)
        self.setWidgetResizable(True)

        self._layout = QVBoxLayout()
        self._layout.setSpacing(5)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.setContentsMargins(5, 5, 5, 5)
        scroll_widget.setLayout(self._layout)

        self._items = dict()

    def _on_mouse_move(self, point: QPoint):
        for i in range(len(self._items)):
            item = self._layout.itemAt(i).widget()
            if isinstance(item, GPTListWidgetItem):
                item.set_hover(0 <= point.x() - item.pos().x() <= item.width() and
                               0 <= point.y() - item.pos().y() <= item.height())

    def _on_item_hover(self, chat_id):
        if isinstance(chat_id, str):
            chat_id = int(chat_id)
        for key, item in self._items.items():
            if key != chat_id:
                item.set_hover(False)

    def deselect(self, chat_id):
        self._items[chat_id].set_selected(False)

    def select(self, chat_id):
        self._items[chat_id].set_selected(True)

    def sort_chats(self):
        for el in self._items.values():
            el.setParent(None)
        items = sorted(self._items.values(), key=lambda item: item.chat.get_sort_key(), reverse=True)
        for el in items:
            self._layout.addWidget(el)

    def move_to_top(self, chat_id):
        self.sort_chats()
        # item = self._items[chat_id]
        # item.setParent(None)
        # item.update_name()
        # self._layout.insertWidget(0, item)

    def update_item_name(self, chat_id):
        self._items[chat_id].update_name()

    def _on_item_selected(self, chat_id: int):
        for key, item in self._items.items():
            if key != chat_id:
                item.set_selected(False)
        self.currentItemChanged.emit(chat_id)

    def set_current_id(self, chat_id: int):
        for key, item in self._items.items():
            if key != chat_id:
                item.set_selected(False)
        if chat_id in self._items:
            self._items[chat_id].set_selected(True)

    def add_item(self, chat: GPTChat):
        item = GPTListWidgetItem(self._tm, chat)
        item.selected.connect(self._on_item_selected)
        item.hover.connect(self._on_item_hover)
        item.deleteRequested.connect(self.deleteItem)
        item.pinRequested.connect(self.pin_chat)
        chat_id = chat.id
        item.set_theme()
        self._items[chat_id] = item
        self._layout.addWidget(item)
        self._set_items_width()

    def pin_chat(self, chat_id):
        self.sort_chats()

    def delete_item(self, chat_id):
        self._items[chat_id].setParent(None)
        self._items.pop(chat_id)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self._set_items_width()

    def _set_items_width(self):
        width = self.width() - 15
        if self.verticalScrollBar().maximum():
            width -= 8
        for el in self._items.values():
            el.setFixedWidth(width)

    def set_theme(self):
        self._tm.auto_css(self, palette='Bg', border=False)
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


class GPTListWidgetItem(QWidget):
    PALETTE = 'Main'
    selected = pyqtSignal(int)
    hover = pyqtSignal(int)

    deleteRequested = pyqtSignal(int)
    pinRequested = pyqtSignal(int)

    def __init__(self, tm, chat: GPTChat):
        super().__init__()
        self._tm = tm
        self.chat = chat
        self._chat_id = chat.id
        self._selected = False
        self._hover = False
        self.setMouseTracking(True)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.run_context_menu)

        self.setFixedHeight(44)

        strange_layout = QVBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)
        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(7, 7, 7, 7)
        strange_widget.setLayout(main_layout)

        self._icon_label = Label()
        self._icon_label.setFixedSize(30, 30)
        self._icon_label.mouseMoving.connect(lambda: self.set_hover(True))
        main_layout.addWidget(self._icon_label)

        self._name_label = Label()
        self._name_label.setWordWrap(True)
        self.update_name()
        self._name_label.mouseMoving.connect(lambda: self.set_hover(True))
        main_layout.addWidget(self._name_label)

        # self._button_delete = Button(self._tm, 'delete', css='Main')
        # self._button_delete.setFixedSize(30, 30)
        # self._button_delete.clicked.connect(lambda: self.deleteRequested.emit(self._chat_id))
        # main_layout.addWidget(self._button_delete)

    def __str__(self):
        return f"ChatItem({self.chat.id}, {self.chat.get_sort_key()})"

    def update_name(self):
        icons = {
            GPTChat.SIMPLE: 'icons/simple_chat',
            GPTChat.TRANSLATE: 'icons/translate',
            GPTChat.SUMMARY: 'icons/summary',
        }
        self._icon_label.setPixmap(QPixmap(self._tm.get_image(
            icons.get(self.chat.type, 'icons/simple_chat'))).scaledToWidth(30))

        if self.chat.name and self.chat.name.strip():
            self._name_label.setText(self.chat.name)
        elif self.chat.last_message:
            self._name_label.setText(self.chat.last_message.content)
        else:
            self._name_label.setText('<Новый диалог>')

    def run_context_menu(self, pos):
        menu = ContextMenu(self._tm, self.chat)
        menu.move(self.mapToGlobal(pos))
        menu.exec()
        match menu.action:
            case ContextMenu.DELETE:
                self.deleteRequested.emit(self._chat_id)
            case ContextMenu.PIN:
                self.chat.pinned = True
                self.pinRequested.emit(self._chat_id)
            case ContextMenu.UNPIN:
                self.chat.pinned = False
                self.pinRequested.emit(self._chat_id)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.set_selected(True)

    def set_selected(self, status):
        if self._selected == bool(status):
            return
        self._selected = bool(status)
        self.set_theme()
        if status:
            self.selected.emit(self._chat_id)

    def set_hover(self, hover):
        hover = bool(hover)
        if self._hover == hover:
            return
        self._hover = hover
        self.set_theme()
        if hover:
            self.hover.emit(self._chat_id)

    def set_theme(self):
        if self._selected:
            suffix = "Selected"
        elif self._hover:
            suffix = "Hover"
        else:
            suffix = ""
        self.setStyleSheet(f"""background-color: {self._tm[f'{GPTListWidgetItem.PALETTE}{suffix}Color']};
                               border: 0px solid {self._tm[f'{GPTListWidgetItem.PALETTE}BorderColor']};
                               border-radius: 6px;
                               color: {self._tm['TextColor']};""")
        self._name_label.setStyleSheet("border: none;")
        self._name_label.setFont(self._tm.font_medium)


class ContextMenu(QMenu):
    DELETE = 0
    PIN = 1
    UNPIN = 2

    def __init__(self, tm, chat):
        super().__init__()
        self.tm = tm
        self._chat = chat
        self.action = None

        action = self.addAction(QIcon(self.tm.get_image('buttons/button_delete')), "Удалить")
        action.triggered.connect(lambda: self.set_action(ContextMenu.DELETE))

        if self._chat.pinned:
            action = self.addAction(QIcon(self.tm.get_image('buttons/unpin')), "Открепить")
            action.triggered.connect(lambda: self.set_action(ContextMenu.UNPIN))
        else:
            action = self.addAction(QIcon(self.tm.get_image('buttons/pin')), "Закрепить")
            action.triggered.connect(lambda: self.set_action(ContextMenu.PIN))

        self.tm.auto_css(self)

    def set_action(self, action):
        self.action = action
