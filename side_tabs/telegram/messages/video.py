from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget

from side_tabs.telegram.telegram_api import tg


class VideoPlayer(QVideoWidget):
    MAX_HEIGHT = 600

    def __init__(self, tm, video: tg.Video):
        super().__init__()
        self._tm = tm
        self._video = video

        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self)
        self.media_player.setLoops(QMediaPlayer.Loops.Infinite)
        self.media_player.setSource(QUrl.fromLocalFile(self._video.video.local.path))

        self._resize()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._resize()

    def _resize(self):
        self.setFixedHeight(min(VideoPlayer.MAX_HEIGHT, self.width() * self._video.height // self._video.width))

    def play(self):
        if self._video.video.local.is_downloading_completed:
            self.media_player.play()
        else:
            tg.downloadFile(self._video.video.id, 1)

    def pause(self):
        self.media_player.pause()

    def on_downloaded(self, video: tg.File):
        self._video.video = video
        self.media_player.setSource(QUrl.fromLocalFile(self._video.video.local.path))
        self.media_player.play()

