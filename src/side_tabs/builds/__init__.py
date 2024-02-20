from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QComboBox, QPushButton

from src.backend.backend_types.build import Build
from src.backend.managers import BackendManager
from src.side_tabs.builds.build_edit import BuildEdit
from src.ui.button import Button
from src.ui.custom_dialog import CustomDialog
from src.ui.side_bar_window import SideBarWindow


class BuildWindow(SideBarWindow):
    def __init__(self, bm: BackendManager, sm, tm):
        super().__init__(bm, sm, tm)

        self.setFixedSize(720, 480)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 0, 10)
        self.setLayout(layout)

        right_layout = QVBoxLayout()
        layout.addLayout(right_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addLayout(buttons_layout)

        self.button_add = Button(self.tm, 'buttons/plus', css='Main')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(40)
        self.button_add.clicked.connect(self.new_build)
        buttons_layout.addWidget(self.button_add, 1)

        self.button_delete = Button(self.tm, 'buttons/delete', css='Main')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(40)
        self.button_delete.clicked.connect(self._on_delete_pressed)
        buttons_layout.addWidget(self.button_delete, 1)

        self._list_widget = QListWidget()
        self._list_widget.currentItemChanged.connect(self._on_build_selected)
        self._list_widget.setFixedWidth(225)
        right_layout.addWidget(self._list_widget)

        self._build_edit = BuildEdit(self.bm, self.sm, self.tm)
        self._build_edit.nameChanged.connect(self._update_item_text)
        layout.addWidget(self._build_edit)

        self.bm.builds.onLoad.connect(lambda builds: [self.add_build(el) for el in builds])
        self.bm.builds.onAdd.connect(self.add_build)
        self.bm.builds.onDelete.connect(self.delete_build)
        self.bm.builds.onClear.connect(self.clear)

    def add_build(self, build):
        self._list_widget.addItem(ListWidgetItem(self.tm, build))

    def clear(self):
        self._list_widget.clear()
        self._build_edit.open(None)

    def delete_build(self, build):
        for i in range(self._list_widget.count()):
            if self._list_widget.item(i).build == build:
                self._list_widget.takeItem(i)
                break

    def _on_build_selected(self):
        item = self._list_widget.currentItem()
        if not isinstance(item, ListWidgetItem):
            return
        self._build_edit.open(item.build)

    def _update_item_text(self, text):
        item = self._list_widget.currentItem()
        if not isinstance(item, ListWidgetItem):
            return
        item.build['name'] = text
        self.bm.builds.onRename.emit(item.build)
        item.setText(text)

    def new_build(self):
        dialog = BuildTypeDialog(self.tm)
        if dialog.exec():
            build = self.bm.builds.new(dialog.value())

    def _on_delete_pressed(self):
        item = self._list_widget.currentItem()
        if not isinstance(item, ListWidgetItem):
            return
        self.bm.builds.delete(item.build.id)

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        self._build_edit.set_theme()
        for el in [self.button_add, self.button_delete, self._list_widget]:
            self.tm.auto_css(el)

    def closeEvent(self, a0) -> None:
        self._build_edit.store_build()


class BuildTypeDialog(CustomDialog):
    ITEMS = {'C': "Сборка C", 'C-lib': "Библиотека C", 'C++': "Сборка C++",
             "python": "Python", "python_coverage": "Python Coverage",
             'script': "Сценарий командной строки", 'bash': "Скрипт Bash", 'command': "Команда", 'report': "Отчет"}
    ITEMS_REVERSED = {item: key for key, item in ITEMS.items()}
    IMAGES = {'C': 'files/c',
              'C-lib': 'files/c',
              'C++': 'files/cpp',
              'python': 'files/py',
              'python_coverage': 'files/py',
              'bash': 'files/sh',
              'script': 'files/bat',
              'command': 'files/cmd',
              'report': 'files/md'}

    def __init__(self, tm):
        super().__init__(tm, "Новая конфигурация")

        self.setFixedSize(250, 120)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        self.setLayout(layout)

        self._combo_box = QComboBox()
        self._combo_box.addItems(BuildTypeDialog.ITEMS.values())
        for i, item in enumerate(self.IMAGES.values()):
            self._combo_box.setItemIcon(i, QIcon(self.tm.get_image(item)))
        layout.addWidget(self._combo_box)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(4)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(buttons_layout)

        self._button_ok = QPushButton("Создать")
        self._button_ok.setFixedSize(80, 22)
        self._button_ok.clicked.connect(self.accept)
        buttons_layout.addWidget(self._button_ok)

        self._button_cancel = QPushButton("Отмена")
        self._button_cancel.setFixedSize(80, 22)
        self._button_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(self._button_cancel)

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        self.set_theme()

    def value(self):
        return BuildTypeDialog.ITEMS_REVERSED[self._combo_box.currentText()]

    def set_theme(self):
        super().set_theme()
        for el in [self._button_cancel, self._button_ok, self._combo_box]:
            self.tm.auto_css(el)


class ListWidgetItem(QListWidgetItem):
    def __init__(self, tm, build: Build):
        super().__init__()
        self.tm = tm
        self.build = build
        self.set_theme()

    def update_name(self):
        self.setText(self.build.get('name', '-'))

    def set_theme(self):
        self.update_name()
        self.setFont(self.tm.font_medium)
        self.setIcon(QIcon(self.tm.get_image(BuildTypeDialog.IMAGES.get(self.build.type), 'icons/unknown_file')))
