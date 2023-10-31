import os
from time import time
from uuid import UUID

from PyQt6.QtWidgets import QHBoxLayout

from side_tabs.chat import gpt
from side_tabs.chat.gpt_dialog import GPTDialog
from side_tabs.chat.chat_widget import ChatWidget
from side_tabs.chat.chats_list import GPTListWidget
from ui.side_panel_widget import SidePanelWidget


class ChatPanel(SidePanelWidget):
    def __init__(self, sm, bm, tm):
        super().__init__(sm, tm, "Чат", ['add'])
        self.bm = bm
        self._data_path = f"{self.sm.app_data_dir}/GPT/dialogs"

        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._list_widget = GPTListWidget(tm)
        self._layout.addWidget(self._list_widget)
        self._list_widget.deleteItem.connect(self._delete_dialog)
        self._list_widget.currentItemChanged.connect(self._select_dialog)

        self.dialogs = dict()
        self.chat_widgets = dict()
        self.current = None
        self.buttons['add'].clicked.connect(self._new_dialog)

        self._load_dialogs()
        try:
            if (dialog_id := UUID(self.sm.get_general('gpt_current_dialog', ''))) in self.dialogs:
                self._select_dialog(dialog_id)
        except ValueError:
            pass

    def _load_dialogs(self):
        os.makedirs(self._data_path, exist_ok=True)
        for el in os.listdir(self._data_path):
            if el.endswith('.json'):
                dialog = GPTDialog(self._data_path, el[:-len('.json')])
                dialog.load()
                self._add_dialog(dialog)

    def _new_dialog(self):
        dialog = GPTDialog(self._data_path)
        dialog.time = time()
        self._add_dialog(dialog)

    def _add_dialog(self, dialog):
        self.dialogs[dialog.id] = dialog

        chat_widget = ChatWidget(self.sm, self.bm, self.tm, dialog)
        chat_widget.buttonBackPressed.connect(self._close_dialog)
        chat_widget.hide()
        self._layout.addWidget(chat_widget)
        self.chat_widgets[dialog.id] = chat_widget
        chat_widget.set_theme()

        self._list_widget.add_item(dialog)

    def _delete_dialog(self, dialog_id):
        self.dialogs[dialog_id].delete()
        self.chat_widgets.pop(dialog_id)
        self._list_widget.delete_item(dialog_id)
        self.dialogs.pop(dialog_id)

    def _select_dialog(self, dialog_id):
        self.sm.set_general('gpt_current_dialog', str(dialog_id))
        self._list_widget.hide()
        self.chat_widgets[dialog_id].show()
        self.current = dialog_id

    def _close_dialog(self, dialog_id):
        self._list_widget.show()
        self.chat_widgets[dialog_id].hide()
        self._list_widget.deselect(dialog_id)
        self._list_widget.update_item_name(dialog_id)
        self.current = None

    def set_theme(self):
        super().set_theme()
        self._list_widget.set_theme()
        for el in self.chat_widgets.values():
            el.set_theme()

