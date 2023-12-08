from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


class EmojiLabel(QLabel):
    def __init__(self, tm, emoji: str):
        super().__init__()
        self._tm = tm
        self._emoji = emoji
        self._pixmap = QPixmap(self._tm.get_image('emoji/' + self._emoji))
        self.setPixmap(self._pixmap)

    def set_theme(self):
        self.setStyleSheet("border: none;")

