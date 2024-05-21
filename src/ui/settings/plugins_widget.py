import asyncio

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
from PyQtUIkit.core import KitFont, KitIcon
from PyQtUIkit.widgets import *
from qasync import asyncSlot

from src.backend.managers import BackendManager


class PluginsWidget(KitHBoxLayout):
    def __init__(self, bm: BackendManager):
        super().__init__()
        self._bm = bm
        self._remote_downloaded = False

        self.padding = 10
        self.spacing = 12

        self._installed_layout = KitVBoxLayout()
        self._installed_layout.spacing = 6
        self.addWidget(self._installed_layout, 1)

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

        self._button_remote = _Button('line-cloud-download')
        self._button_remote.on_click = self._show_remote
        top_layout.addWidget(self._button_remote)

        self._list_widget = KitListWidget()
        self._list_widget.currentItemChanged.connect(self._on_item_selected)
        self._installed_layout.addWidget(self._list_widget)

        self._remote_layout = KitVBoxLayout()
        self._remote_layout.spacing = 6
        self._remote_layout.hide()
        self.addWidget(self._remote_layout, 1)

        top_layout = KitHBoxLayout()
        top_layout.alignment = Qt.AlignmentFlag.AlignLeft
        top_layout.spacing = 6
        self._remote_layout.addWidget(top_layout)

        self._button_back = _Button('line-arrow-back')
        self._button_back.on_click = self._show_installed
        top_layout.addWidget(self._button_back)

        self._button_download = _Button('line-download')
        self._button_download.on_click = self._on_download_button_clicked
        top_layout.addWidget(self._button_download)

        self._button_refresh = _Button('line-refresh')
        self._button_refresh.on_click = lambda: self._refresh_remote()
        top_layout.addWidget(self._button_refresh)

        self._remote_list_widget = KitListWidget()
        self._remote_list_widget.currentItemChanged.connect(self._on_remote_selected)
        self._remote_layout.addWidget(self._remote_list_widget)

        self._progress_layout = KitVBoxLayout()
        self._progress_layout.spacing = 12
        self._progress_layout.hide()
        self.addWidget(self._progress_layout, 1)

        self._progress_layout.addWidget(KitVBoxLayout(), 10)
        layout = KitHBoxLayout()
        layout.alignment = Qt.AlignmentFlag.AlignCenter
        self._progress_layout.addWidget(layout)

        self._spinner = KitSpinner()
        self._spinner.size = 72
        self._spinner.width = 5
        layout.addWidget(self._spinner)

        self._success_icon = KitIconWidget('line-checkmark-circle')
        self._success_icon.main_palette = 'Success'
        self._success_icon.setFixedSize(72, 72)
        self._success_icon.hide()
        layout.addWidget(self._success_icon)

        self._progress_label = KitLabel()
        self._progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._progress_label.font_size = KitFont.Size.BIG
        self._progress_layout.addWidget(self._progress_label)
        self._progress_layout.addWidget(KitVBoxLayout(), 10)

        self._text_area = KitTextBrowser()
        self._text_area.main_palette = 'Transparent'
        self._text_area.border = 0
        self._text_area.setReadOnly(True)
        self.addWidget(self._text_area, 1)

    def showEvent(self, a0):
        super().showEvent(a0)
        self.update_list()

    def _show_remote(self):
        self._installed_layout.hide()
        self._remote_layout.show()
        if not self._remote_downloaded:
            self._refresh_remote()

    def _show_installed(self):
        self._remote_layout.hide()
        self._installed_layout.show()

    def update_list(self):
        self._list_widget.clear()
        self._list_widget.addItems(self._bm.plugins.all)

    def _on_item_selected(self, item: KitListWidgetItem):
        if not item:
            self._text_area.setText('')
        else:
            plugin = self._bm.plugins.get(item.text())
            self._text_area.setMarkdown(f"# {plugin.name}\n### Версия {plugin.version}\n---\n\n{plugin.description}")

    def _on_remote_selected(self, item: KitListWidgetItem):
        if not item:
            self._text_area.setText('')
        else:
            plugin = self._bm.plugins.remote.get(item.text())
            self._text_area.setMarkdown(f"# {plugin.name}\n### Версия {plugin.version}\n---\n\n{plugin.description}")

    def _on_install_button_clicked(self):
        path, _ = QFileDialog.getOpenFileName(filter='TestGenerator plugins (*.TGPlugin.zip)')
        if path:
            self._bm.plugins.install(path)
            self.update_list()

    @asyncSlot()
    async def _refresh_remote(self):
        self._remote_layout.hide()
        self._progress_layout.show()
        self._progress_label.text = "Обновление"

        self._remote_list_widget.clear()
        await self._bm.plugins.update_remote()
        self._remote_list_widget.addItems(self._bm.plugins.remote)

        self._progress_layout.hide()
        self._remote_layout.show()

    def _on_remove_button_clicked(self):
        item = self._list_widget.currentItem()
        plugin = self._bm.plugins.get(item.text())
        if KitDialog.question(self, f"Вы уверены, что хотите удалить расширение \"{plugin.name}\"?") == 'Yes':
            self._bm.plugins.remove(plugin.name)
            self.update_list()
            KitDialog.info(self, "Удаление расширения",
                           "Для полного удаления расширения необходим перезапуск приложения.")

    def _on_download_button_clicked(self):
        item = self._remote_list_widget.currentItem()
        if not item:
            return
        plugin = self._bm.plugins.remote.get(item.text())

        if KitDialog.question(
                self, f"{'Обновить' if plugin.name in self._bm.plugins.all else 'Установить'} расширение"
                      f"\"{plugin.name}\"?") == 'Yes':
            self._download()

    @asyncSlot()
    async def _download(self):
        item = self._remote_list_widget.currentItem()
        if not item:
            return

        self._remote_layout.hide()
        self._progress_layout.show()
        self._progress_label.text = "Загрузка расширения"

        plugin = self._bm.plugins.remote.get(item.text())
        path = await self._bm.plugins.download_plugin(plugin)

        self._progress_label.text = "Установка расширения"
        if plugin.name in self._bm.plugins.all:
            self._bm.plugins.remove(plugin.name)
        await self._bm.processes.run_async(lambda: self._bm.plugins.install(path), 'plugins', 'installing')

        await self._show_success()
        self._progress_layout.hide()
        self._remote_layout.show()

    async def _show_success(self):
        self._spinner.hide()
        self._success_icon.show()
        await asyncio.sleep(1.5)
        self._success_icon.hide()
        self._spinner.show()


class _Button(KitIconButton):
    def __init__(self, icon):
        super().__init__(icon)
        self.setFixedSize(32, 24)
