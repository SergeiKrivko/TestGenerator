from PyQtUIkit.widgets import *

from src import config
from src.backend.backend_types.build import Build
from src.backend.managers import BackendManager
from src.ui.side_tabs.builds.build_edit import BuildEdit
from src.ui.side_tabs.builds.build_icons import ITEMS, IMAGES
from src.ui.widgets.side_bar_window import SideBarDialog


class BuildWindow(SideBarDialog):

    def __init__(self, parent, bm: BackendManager):
        super().__init__(parent, bm)

        self.name = f"{config.APP_NAME} - Конфигурации сборки"
        self.setFixedSize(720, 480)

        layout = KitHBoxLayout()
        layout.padding = 10, 10, 0, 10
        layout.spacing = 6
        self.setWidget(layout)

        right_layout = KitVBoxLayout()
        right_layout.setFixedWidth(225)
        right_layout.spacing = 6
        layout.addWidget(right_layout)

        buttons_layout = KitHBoxLayout()
        buttons_layout.spacing = 6
        right_layout.addWidget(buttons_layout)

        self.button_add = KitIconButton('line-add')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(40)
        self.button_add.on_click = self.new_build
        buttons_layout.addWidget(self.button_add, 1)

        self.button_delete = KitIconButton('line-trash')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(40)
        self.button_delete.on_click = self._on_delete_pressed
        buttons_layout.addWidget(self.button_delete, 1)

        self._list_widget = KitListWidget()
        self._list_widget.currentItemChanged.connect(self._on_build_selected)
        right_layout.addWidget(self._list_widget)

        self._build_edit = BuildEdit(self.bm)
        self._build_edit.nameChanged.connect(self._update_item_text)
        layout.addWidget(self._build_edit)

        self.bm.builds.onLoad.connect(lambda builds: [self.add_build(el) for el in builds])
        self.bm.builds.onAdd.connect(self.add_build)
        self.bm.builds.onDelete.connect(self.delete_build)
        self.bm.builds.onClear.connect(self.clear)

    def add_build(self, build):
        self._list_widget.addItem(ListWidgetItem(build))

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
        dialog = KitFormDialog(self,
                               KitForm.ComboField('', [KitComboBoxItem(item, key, IMAGES[key])
                                                    for key, item in ITEMS.items()]))
        if dialog.exec():
            build = self.bm.builds.new(dialog.res()[0])

    def _on_delete_pressed(self):
        item = self._list_widget.currentItem()
        if not isinstance(item, ListWidgetItem):
            return
        self.bm.builds.delete(item.build.id)

    def hideEvent(self, a0) -> None:
        super().hideEvent(a0)
        self._build_edit.store_build()
        self._build_edit.clear()


class ListWidgetItem(KitListWidgetItem):
    def __init__(self, build: Build):
        super().__init__('')
        self.build = build
        self.icon = IMAGES.get(self.build.type, 'line-help')
        self.update_name()

    def update_name(self):
        self.setText(self.build.get('name', '-'))
