from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
from PyQtUIkit.widgets import *

from src.backend.managers import BackendManager


class PluginsWidget(KitHBoxLayout):
    def __init__(self, bm: BackendManager):
        super().__init__()
        self._bm = bm

        self.padding = 10
        self.spacing = 12

        self._installed_layout = KitVBoxLayout()
        self._installed_layout.spacing = 6
        self.addWidget(self._installed_layout)

        top_layout = KitHBoxLayout()
        top_layout.alignment = Qt.AlignmentFlag.AlignLeft
        top_layout.spacing = 6
        self._installed_layout.addWidget(top_layout)

        self._button_install = _Button('line-add')
        self._button_install.on_click = self._on_install_button_clicked
        top_layout.addWidget(self._button_install)

        self._button_remove = _Button('line-trash')
        self._button_remove.on_click = self._on_remove_button_clicked
        top_layout.addWidget(self._button_remove)

        self._list_widget = KitListWidget()
        self._list_widget.currentItemChanged.connect(self._on_item_selected)
        self._installed_layout.addWidget(self._list_widget)

        self._text_area = KitTextBrowser()
        self._text_area.main_palette = 'Transparent'
        self._text_area.border = 0
        self._text_area.setReadOnly(True)
        self.addWidget(self._text_area)

    def showEvent(self, a0):
        super().showEvent(a0)
        self.update_list()

    def update_list(self):
        self._list_widget.clear()
        self._list_widget.addItems(self._bm.plugins.all)

    def _on_item_selected(self, item: KitListWidgetItem):
        if not item:
            self._text_area.setText('')
        else:
            plugin = self._bm.plugins.get(item.text())
            self._text_area.setMarkdown(f"# {plugin.name}\n### Версия {plugin.version}\n---\n\n{plugin.description}")

    def _on_install_button_clicked(self):
        path, _ = QFileDialog.getOpenFileName(filter='TestGenerator plugins (*.TGPlugin.zip)')
        if path:
            self._bm.plugins.install(path)
            self.update_list()

    def _on_remove_button_clicked(self):
        item = self._list_widget.currentItem()
        plugin = self._bm.plugins.get(item.text())
        if KitDialog.question(self, f"Вы уверены, что хотите удалить расширение \"{plugin.name}\"?") == 'Yes':
            self._bm.plugins.remove(plugin.name)
            self.update_list()
            KitDialog.info(self, "Удаление расширения",
                           "Для полного удаления расширения необходим перезапуск приложения.")


class _Button(KitIconButton):
    def __init__(self, icon):
        super().__init__(icon)
        self.setFixedSize(32, 24)
