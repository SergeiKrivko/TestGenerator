import os
import shutil
from time import time, sleep
from uuid import UUID

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QMenu, QPushButton

from side_tabs.chat import gpt
from side_tabs.chat.chat_widget import ChatWidget
from side_tabs.chat.chats_list import GPTListWidget
from side_tabs.chat.gpt_dialog import GPTDialog
from side_tabs.chat.settings_window import ChatSettingsWindow
from ui.button import Button
from ui.side_panel_widget import SidePanelWidget


class ChatPanel(SidePanelWidget):
    def __init__(self, sm, bm, tm):
        super().__init__(sm, tm, "Чат", [])
        self.bm = bm
        self._data_path = self.sm.get_general('gpt_dialogs_path', '').strip()
        if not self._data_path:
            self._data_path = f"{self.sm.app_data_dir}/GPT/dialogs"

        self._layout = QHBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._layout.setContentsMargins(3, 3, 3, 3)
        self.setLayout(self._layout)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addLayout(main_layout, 0)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(top_layout)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        top_layout.addLayout(layout)

        self._button_add = Button(self.tm, 'plus', css='Main')
        self._button_add.setFixedSize(36, 36)
        self._button_add.clicked.connect(lambda: self._new_dialog())
        layout.addWidget(self._button_add)

        self._button_add_special = QPushButton()
        self._button_add_special.setFixedSize(20, 36)
        self._button_add_special.setMenu(NewChatMenu(self.tm, self._new_dialog))
        layout.addWidget(self._button_add_special)

        self._button_settings = Button(self.tm, 'generate', css='Main')
        self._button_settings.setFixedSize(36, 36)
        self._button_settings.clicked.connect(self._open_settings)
        top_layout.addWidget(self._button_settings)

        self._list_widget = GPTListWidget(tm)
        main_layout.addWidget(self._list_widget)
        self._list_widget.deleteItem.connect(self._delete_dialog)
        self._list_widget.currentItemChanged.connect(self._select_dialog)

        self.dialogs = dict()
        self.chat_widgets = dict()
        self.current = None

        try:
            self._last_dialog = UUID(self.sm.get('current_dialog', ''))
        except ValueError:
            self._last_dialog = None
        self._loading_started = False

    def _open_settings(self):
        dialog = None if self.current is None else self.dialogs[self.current]
        window = ChatSettingsWindow(self.sm, self.tm, dialog)
        window.exec()
        window.save()
        if dialog:
            dialog.store()

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        if not self._loading_started:
            self._loading_started = True
            self._load_dialogs()

    def _load_dialogs(self):
        self._loader = DialogLoader(self._data_path, str(self._last_dialog))
        self._loader.addDialog.connect(self._on_dialog_loaded)
        self._loader.finished.connect(lambda: (self._list_widget.sort_dialogs(), self._resize()))
        self.bm.run_process(self._loader, 'GPT', 'loading')

    def _on_dialog_loaded(self, dialog: GPTDialog):
        self._add_dialog(dialog)
        if dialog.id == self._last_dialog:
            self._list_widget.select(dialog.id)

    def _new_dialog(self, dialog_type=GPTDialog.SIMPLE):
        dialog = GPTDialog(self._data_path)
        dialog.time = time()
        dialog.type = dialog_type

        match dialog_type:
            case GPTDialog.TRANSLATE:
                dialog.data['language1'] = 'russian'
                dialog.data['language2'] = 'english'
                dialog.name = f"{dialog.data['language1'].capitalize()} ↔ {dialog.data['language2'].capitalize()}"
                dialog.used_messages = 1
            case GPTDialog.SUMMARY:
                dialog.name = f"Краткое содержание"
                dialog.used_messages = 1

        self._add_dialog(dialog)

    def _add_dialog(self, dialog):
        self.dialogs[dialog.id] = dialog

        chat_widget = ChatWidget(self.sm, self.bm, self.tm, dialog)
        chat_widget.buttonBackPressed.connect(self._close_dialog)
        chat_widget.hide()
        chat_widget.updated.connect(lambda: self._list_widget.move_to_top(dialog.id))
        self._layout.addWidget(chat_widget, 2)
        self.chat_widgets[dialog.id] = chat_widget
        chat_widget.set_theme()

        self._list_widget.add_item(dialog)

    def _delete_dialog(self, dialog_id):
        if dialog_id == self.current:
            self._close_dialog(dialog_id)
        self.dialogs[dialog_id].delete()
        self.chat_widgets.pop(dialog_id)
        self._list_widget.delete_item(dialog_id)
        self.dialogs.pop(dialog_id)

    def _select_dialog(self, dialog_id):
        if self.current is not None:
            self._close_dialog(self.current)
        self.sm.set('current_dialog', str(dialog_id))
        self.chat_widgets[dialog_id].show()
        self.current = dialog_id
        self._resize()

    def _close_dialog(self, dialog_id):
        self.chat_widgets[dialog_id].hide()
        self.set_list_hidden(False)
        self.current = None
        self._resize()
        self._list_widget.deselect(dialog_id)
        self._list_widget.update_item_name(dialog_id)
        self.sm.set('current_dialog', '')

    def set_list_hidden(self, hidden):
        for el in [self._button_add, self._button_add_special, self._button_settings, self._list_widget]:
            el.setHidden(hidden)

    def _resize(self):
        if self.width() > 550:
            self.set_list_hidden(False)
            if self.current is not None:
                self.chat_widgets[self.current].set_top_hidden(True)
            self._list_widget.setFixedWidth(max(220, self.width() // 4))
            # else:
            #     self._list_widget.setMaximumWidth(10000)
        elif self.current is not None:
            self.set_list_hidden(True)
            self.chat_widgets[self.current].set_top_hidden(False)
        else:
            self.set_list_hidden(False)
            self._list_widget.setMaximumWidth(10000)

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self._resize()

    def finish_work(self):
        if os.path.isdir(path := f"{self.sm.app_data_dir}/GPT/temp"):
            shutil.rmtree(path)

    def set_theme(self):
        super().set_theme()
        self._button_add.set_theme()
        self._button_settings.set_theme()
        self.tm.auto_css(self._button_add_special, palette='Main', border=False)
        self._list_widget.set_theme()
        for el in self.chat_widgets.values():
            el.set_theme()


class NewChatMenu(QMenu):
    def __init__(self, tm, func):
        super().__init__()
        self.tm = tm
        self.func = func

        action = self.addAction(QIcon(self.tm.get_image('simple_chat')), "Обычный диалог")
        action.triggered.connect(lambda: func(GPTDialog.SIMPLE))

        action = self.addAction(QIcon(self.tm.get_image('translate')), "Переводчик")
        action.triggered.connect(lambda: func(GPTDialog.TRANSLATE))

        action = self.addAction(QIcon(self.tm.get_image('summary')), "Краткое содержание")
        action.triggered.connect(lambda: func(GPTDialog.SUMMARY))

        self.tm.auto_css(self)


class DialogLoader(QThread):
    addDialog = pyqtSignal(GPTDialog)

    def __init__(self, data_path, first=None):
        super().__init__()
        self._data_path = data_path
        self._first = first

    def run(self) -> None:
        os.makedirs(self._data_path, exist_ok=True)
        if self._first:
            try:
                dialog = GPTDialog(self._data_path, self._first)
                dialog.load()
                self.addDialog.emit(dialog)
                sleep(0.1)
            except Exception as ex:
                pass
        for el in os.listdir(self._data_path):
            if el.endswith('.json') and el[:-len('.json')] != self._first:
                dialog = GPTDialog(self._data_path, el[:-len('.json')])
                dialog.load()
                self.addDialog.emit(dialog)
                sleep(0.1)
