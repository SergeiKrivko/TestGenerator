import os.path

import pylottie
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QLabel

from side_tabs.telegram.telegram_api import tg
from ui.themes import ThemeManager


class StickerWidget(QLabel):
    MAX_HEIGHT = 400

    def __init__(self, tm: ThemeManager, manager, sticker: tg.Sticker):
        super().__init__()
        self._manager = manager
        self._tm = tm
        self._sticker = sticker
        self._movie = None
        if self._sticker.sticker.local.is_downloading_completed:
            self._activate()
        else:
            tg.downloadFile(self._sticker.sticker.id, 1)
        self.setStyleSheet("border: none;")

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._resize()

    def _resize(self):
        print(self._movie)
        if not isinstance(self._movie, QMovie):
            return
        width = min(200, self._sticker.width)
        height = min(StickerWidget.MAX_HEIGHT, width * self._sticker.height // self._sticker.width)
        self._movie.setScaledSize(QSize(width, height))

    def download(self):
        if not self._sticker.sticker.local.is_downloading_completed and \
                not self._sticker.sticker.local.is_downloading_active:
            tg.downloadFile(self._sticker.sticker.id, 1)

    def on_downloaded(self, file: tg.File):
        if file.id == self._sticker.sticker.id:
            self._sticker.sticker = file
            self._activate()

    def _activate(self):
        path = f"{self._manager.temp_path}/{os.path.basename(self._sticker.sticker.local.path)[:-4]}.gif"
        if not os .path.isfile(path):
            pylottie.convertMultLottie2GIF([self._sticker.sticker.local.path], [path])
        self._movie = QMovie(path)
        self.setMovie(self._movie)
        self._movie.start()
        self._resize()
