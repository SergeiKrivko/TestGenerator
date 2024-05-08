from PyQt6.QtCore import Qt
from PyQtUIkit.core import KitFont
from PyQtUIkit.widgets import *
from qasync import asyncSlot

from src.backend.managers import BackendManager


class OpeningDialog(KitHBoxLayout):
    def __init__(self, parent, bm: BackendManager):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.border = 1
        self.main_palette = 'Bg'
        self._parent = parent
        self._bm = bm
        self.button_close = False
        self._bm.projects.finishOpening.connect(lambda: self._close())
        self._bm.projects.updateProgress.connect(self._update_progress)
        self.setFixedWidth(400)

        main_layout = KitVBoxLayout()
        main_layout.padding = 20
        main_layout.spacing = 10
        self.addWidget(main_layout)

        self._title_label = KitLabel("Открытие проекта")
        self._title_label.font_size = KitFont.Size.BIG
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self._title_label)

        self._project_label = KitLabel(self._bm.projects.current.name())
        self._project_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self._project_label)

        self._progress_bar = KitProgressBar()
        main_layout.addWidget(self._progress_bar)

    def showEvent(self, a0):
        self._set_tm(self._parent.theme_manager)
        super().showEvent(a0)

    def _update_progress(self, value, max_value):
        self._progress_bar.setValue(value)
        self._progress_bar.setMaximum(max_value)

    @asyncSlot()
    async def _close(self):
        self.close()
