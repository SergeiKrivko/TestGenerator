import asyncio

from PyQt6.QtCore import Qt
from PyQtUIkit.core import KitFont
from PyQtUIkit.widgets import *
from qasync import asyncSlot

from src.backend.language.language import FastRunFunction, FastRunAsyncFunction
from src.backend.managers import BackendManager


class FastRunDialog(KitDialog):
    def __init__(self, parent, bm: BackendManager, path: str, fast_run_option: FastRunFunction | FastRunAsyncFunction):
        super().__init__(parent)
        self.button_close = False
        self._bm: BackendManager = bm
        self._path = path
        self._fast_run_option = fast_run_option
        self.setFixedSize(340, 160)

        main_layout = KitVBoxLayout()
        main_layout.alignment = Qt.AlignmentFlag.AlignCenter
        main_layout.padding = 20
        main_layout.spacing = 10
        self.setWidget(main_layout)

        self._label = KitLabel(self._fast_run_option.name)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.font_size = KitFont.Size.BIG
        main_layout.addWidget(self._label)

        self._spinner = KitHBoxLayout()
        main_layout.addWidget(self._spinner, 10)

        spinner = KitSpinner()
        spinner.width = 2
        spinner.size = 40
        self._spinner.addWidget(spinner)

        self._status_label = KitLabel('Готово')
        self._status_label.main_palette = 'Success'
        self._status_label.setWordWrap(True)
        self._status_label.hide()
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self._status_label, 10)

        self._button_cancel = KitButton('Отмена')
        self._button_cancel.clicked.connect(self._on_canceled)
        main_layout.addWidget(self._button_cancel)

        if isinstance(self._fast_run_option, FastRunFunction):
            self._thread = self._bm.processes.run(self._run, 'fast-run', self._path)
            self._thread.finished.connect(lambda: self._on_finished())
        else:
            self._thread = None
        self._error = ''

    @asyncSlot()
    async def _on_thread_finished(self):
        await self._on_finished()

    async def _on_finished(self):
        self._spinner.hide()
        self._status_label.show()
        if self._error:
            self._status_label.text = self._error
            self._status_label.main_palette = 'Danger'
            self._apply_theme()
        else:
            await asyncio.sleep(1)
            self.accept()

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        if isinstance(self._fast_run_option, FastRunAsyncFunction):
            self._run_async()

    @asyncSlot()
    async def _run_async(self):
        try:
            await self._fast_run_option(self._path, self._bm)
        except Exception as ex:
            self._error = f"{ex.__class__.__name__}: {ex}"
        await self._on_finished()

    def _run(self):
        try:
            self._fast_run_option(self._path, self._bm)
        except Exception as ex:
            self._error = f"{ex.__class__.__name__}: {ex}"

    def _on_canceled(self):
        if self._thread:
            self._thread.terminate()
        self.reject()
