import asyncio
import sys
from typing import Callable, Any

from PyQt6.QtCore import QObject, pyqtSignal, QThread
if sys.platform == 'win32':
    import PyTaskbar

from src.backend.settings_manager import SettingsManager


class ProcessManager(QObject):
    allFinished = pyqtSignal()
    statusChanged = pyqtSignal(str, str)

    def __init__(self, sm: SettingsManager, bm):
        super().__init__()
        self._sm = sm
        self._bm = bm

        self._win_id = None

        self._background_processes: dict[str: dict[str: QThread]] = dict()
        self._background_process_count = 0

        self._taskbar_progress = None

        self._process_with_progress = None

    def set_win_id(self, win_id):
        self._win_id = win_id

    def run(self, thread: Callable[[], Any] | QThread, group: str, name: str) -> QThread:
        if not isinstance(thread, QThread):
            thread = _Looper(thread)
        if group not in self._background_processes:
            self._background_processes[group] = dict()

        if name in self._background_processes[group]:
            self._background_processes[group][name].terminate()
        self._background_processes[group][name] = thread
        self._background_process_count += 1
        thread.finished.connect(lambda: self._on_thread_finished(group, name, thread))
        if isinstance(thread, CustomThread) and sys.platform == 'win32' and self._win_id:
            if self._taskbar_progress is None:
                self._taskbar_progress = PyTaskbar.Progress(int(self._win_id))
                self._taskbar_progress.init()
                self._taskbar_progress.setState('normal')
            self._set_process_with_progress(group, name)
            thread.progressChanged.connect(lambda v: self._on_process_changed(group, name, v))
        thread.start()
        self.statusChanged.emit(group, name)
        return thread

    async def run_async(self, thread: Callable[[], Any] | QThread, group: str, name: str):
        thread = self.run(thread, group, name)
        while not thread.isFinished():
            await asyncio.sleep(0.5)
        if isinstance(thread, _Looper):
            return thread.res
        return None

    def _on_thread_finished(self, group, name, process):
        self._background_process_count -= 1
        if self._background_processes[group][name] == process:
            self._background_processes[group].pop(name)
            if (group, name) == self._process_with_progress:
                self._taskbar_progress.setProgress(0)
                self._process_with_progress = None
        self.statusChanged.emit(group, name)
        if self._background_process_count == 0:
            self.allFinished.emit()

    def _set_process_with_progress(self, group, name):
        self._process_with_progress = group, name

    def _on_process_changed(self, group, name, value):
        if isinstance(self._process_with_progress, tuple) and \
                group == self._process_with_progress[0] and name == self._process_with_progress[1]:
            self._taskbar_progress.setProgress(value)

    @property
    def all_finished(self):
        return self._background_process_count == 0

    @property
    def groups(self):
        return self._background_processes.keys()

    @property
    def all(self):
        for group_name, group in self._background_processes.items():
            for process_name, process in group.items():
                yield group_name, process_name, process

    def get_processes(self, group: str):
        return self._background_processes.get(group, dict()).keys()

    def terminate_all(self):
        for item in self._background_processes.values():
            for el in list(item.values()):
                el.terminate()


class _Looper(QThread):
    def __init__(self, func):
        super().__init__()
        self._func = func
        self.res = None

    def run(self) -> None:
        self.res = self._func()


class CustomThread(QThread):
    progressChanged = pyqtSignal(int)

    def __init__(self, max_progress=100):
        super().__init__()
        self._progress = 0
        self._max_progress = max_progress

    @property
    def max_progress(self):
        return self._max_progress

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.progressChanged.emit(int(self._progress))

    def set_progress(self, value):
        self._progress = value
        self.progressChanged.emit(int(self._progress))
