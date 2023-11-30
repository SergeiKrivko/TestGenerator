from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

from side_tabs.telegram.telegram_api import tg
from ui.button import Button


class VoicePlayer(QWidget):
    def __init__(self, tm, voice_message: tg.VoiceNote):
        super().__init__()
        self._tm = tm
        self._voice = voice_message

        self.media_player = QMediaPlayer()
        self._audio = QAudioOutput()
        self.media_player.setAudioOutput(self._audio)
        self.media_player.setSource(QUrl.fromLocalFile(self._voice.voice.local.path))
        self.media_player.errorOccurred.connect(print)
        self.media_player.mediaStatusChanged.connect(self._on_media_status_changed)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)

        self._button_play = Button(self._tm, 'button_run', css='Menu')
        self._button_play.setFixedSize(30, 30)
        self._button_play.clicked.connect(self.play)
        layout.addWidget(self._button_play)

        self._button_pause = Button(self._tm, 'button_pause', css='Menu')
        self._button_pause.hide()
        self._button_pause.setFixedSize(30, 30)
        self._button_pause.clicked.connect(self.pause)
        layout.addWidget(self._button_pause)

        self._duration_label = QLabel(f"{voice_message.duration // 60:0>2}:{voice_message.duration % 60:0>2}")
        layout.addWidget(self._duration_label)

    def play(self):
        if self._voice.voice.local.is_downloading_completed:
            self.media_player.play()
            self._button_pause.show()
            self._button_play.hide()
        else:
            tg.downloadFile(self._voice.voice.id, 1)

    def pause(self):
        self.media_player.pause()
        self._button_pause.hide()
        self._button_play.show()

    def on_downloaded(self, voice: tg.File):
        self._voice.voice = voice
        self.media_player.setSource(QUrl.fromLocalFile(self._voice.voice.local.path))
        self.media_player.play()
        self._button_pause.show()
        self._button_play.hide()

    def _on_media_status_changed(self, status):
        match status:
            case QMediaPlayer.MediaStatus.EndOfMedia:
                self._button_pause.hide()
                self._button_play.show()

    def set_theme(self):
        for el in [self._button_play, self._button_pause, self._duration_label]:
            self._tm.auto_css(el)
