from uuid import UUID

from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea

from side_tabs.chat.gpt_dialog import GPTDialog
from ui.button import Button


class GPTListWidget(QScrollArea):
    currentItemChanged = pyqtSignal(UUID)
    deleteItem = pyqtSignal(UUID)

    def __init__(self, tm):
        super().__init__()
        self._tm = tm

        scroll_widget = QWidget()
        self.setWidget(scroll_widget)
        self.setWidgetResizable(True)

        self._layout = QVBoxLayout()
        self._layout.setSpacing(5)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.setContentsMargins(5, 5, 5, 5)
        scroll_widget.setLayout(self._layout)

        self._items = dict()

    def _on_item_hover(self, chat_id):
        if isinstance(chat_id, str):
            chat_id = int(chat_id)
        for key, item in self._items.items():
            if key != chat_id:
                item.set_hover(False)

    def deselect(self, chat_id):
        self._items[chat_id].set_selected(False)

    def update_item_name(self, dialog_id):
        self._items[dialog_id].update_name()

    def _on_item_selected(self, chat_id: UUID):
        for key, item in self._items.items():
            if key != chat_id:
                item.set_selected(False)
        self.currentItemChanged.emit(chat_id)

    def set_current_id(self, chat_id: UUID):
        for key, item in self._items.items():
            if key != chat_id:
                item.set_selected(False)
        if chat_id in self._items:
            self._items[chat_id].set_selected(True)

    def add_item(self, chat: GPTDialog):
        item = GPTListWidgetItem(self._tm, chat)
        item.selected.connect(self._on_item_selected)
        item.hover.connect(self._on_item_hover)
        item.deleteRequested.connect(self.deleteItem)
        chat_id = chat.id
        item.set_theme()
        self._items[chat_id] = item
        self._layout.addWidget(item)

    def delete_item(self, chat_id):
        self._items[chat_id].setParent(None)
        self._items.pop(chat_id)

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


class GPTListWidgetItem(QWidget):
    PALETTE = 'Main'
    selected = pyqtSignal(UUID)
    hover = pyqtSignal(UUID)
    deleteRequested = pyqtSignal(UUID)

    def __init__(self, tm, chat: GPTDialog):
        super().__init__()
        self._tm = tm
        self._chat = chat
        self._chat_id = chat.id
        self._selected = False
        self._hover = False

        self.setFixedHeight(44)

        strange_layout = QVBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)
        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(7, 7, 7, 7)
        strange_widget.setLayout(main_layout)

        self._name_label = Label()
        self.update_name()
        self._name_label.mouseMoving.connect(lambda: self.set_hover(True))
        main_layout.addWidget(self._name_label)

        self._button_delete = Button(self._tm, 'delete', css='Menu')
        self._button_delete.setFixedSize(30, 30)
        self._button_delete.clicked.connect(lambda: self.deleteRequested.emit(self._chat_id))
        main_layout.addWidget(self._button_delete)

    def update_name(self):
        if self._chat.name.strip():
            self._name_label.setText(self._chat.name)
        elif self._chat.messages:
            self._name_label.setText(self._chat.messages[-1].get('content', ''))
        else:
            self._name_label.setText('<Новый диалог>')

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
        self._button_delete.set_theme()
