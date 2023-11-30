from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from side_tabs.telegram.telegram_api import tg


class PhotoLabel(QLabel):
    MAX_HEIGHT = 600

    def __init__(self, tm, file: tg.File):
        super().__init__()
        self._tm = tm
        self._photo = file
        self._pixmap = None
        if self._photo.local.is_downloading_completed:
            self._pixmap = QPixmap(self._photo.local.path)
            self.resize_pixmap()
        else:
            tg.downloadFile(self._photo.id, 1)

    def update_image(self, image: tg.File):
        if isinstance(self._photo, tg.File) and image.id == self._photo.id:
            self._photo = image
            if self._photo.local.is_downloading_completed:
                self._pixmap = QPixmap(self._photo.local.path)
                self.resize_pixmap()

    def resize_pixmap(self):
        if isinstance(self._pixmap, QPixmap):
            pixmap = self._pixmap
            if self._pixmap.width() > self.maximumWidth() or self._pixmap.height() > self.MAX_HEIGHT:
                pixmap = self._pixmap.scaled(self.maximumWidth(), PhotoLabel.MAX_HEIGHT,
                                             Qt.AspectRatioMode.KeepAspectRatio)
            self.setPixmap(pixmap)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.resize_pixmap()

