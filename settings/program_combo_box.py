import os

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton


class ProgramComboBox(QWidget):
    def __init__(self, sm, file, key, general=True):
        super().__init__()
        self.sm = sm
        self.file = file
        self.key = key
        self.general = general
        self.items = []

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        self.combo_box = QComboBox()
        layout.addWidget(self.combo_box)
        self.combo_box.currentTextChanged.connect(self.set_sm_value)

        self.button_update = QPushButton("↺")
        layout.addWidget(self.button_update)
        self.button_update.setFixedWidth(24)
        self.button_update.clicked.connect(self.sm.start_search)

        self.button_add = QPushButton("+")
        layout.addWidget(self.button_add)
        self.button_add.setFixedWidth(24)

        self.setLayout(layout)

        self.sm.searching_complete.connect(self.update_items)

        if os.name != 'nt':
            self.setDisabled(True)
        else:
            self.update_items()

    def set_items(self, items: list, delete_current=False):
        text = self.combo_box.currentText()
        if not delete_current and text not in items and text.strip():
            items.append(text)
        self.items = items
        self.combo_box.clear()
        self.combo_box.addItems(items)
        self.combo_box.setCurrentText(text)

    def add_item(self, item: str):
        self.items.append(item)
        self.combo_box.addItem(item, None)

    def update_items(self, forced=True):
        self.set_items(self.sm.programs.get(self.file, []), delete_current=forced)

    def set_value(self, text: str):
        if text not in self.items:
            self.add_item(text)
        self.combo_box.setCurrentText(text)

    def set_sm_value(self, text):
        if self.general:
            self.sm.set_general(self.key, text)
        else:
            self.sm.set(self.key, text)

    def set_theme(self, tm):
        tm.auto_css(self.combo_box)
        tm.auto_css(self.button_add)
        tm.auto_css(self.button_update)
