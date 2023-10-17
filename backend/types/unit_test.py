import json
import os

from PyQt6.QtCore import QObject, pyqtSignal


class UnitTest(QObject):
    nameChanged = pyqtSignal()
    statusChanged = pyqtSignal()

    PASSED = 0
    FAILED = 1
    CHANGED = 2

    def __init__(self, path):
        super().__init__()
        self._path = path
        self._data = None
        self._loaded_count = 0

        self.load()

    def path(self):
        return self._path

    def load(self, forced=False):
        if not self._loaded_count or forced:
            try:
                with open(self._path, encoding='utf-8') as f:
                    self._data = json.loads(f.read())
            except FileNotFoundError:
                self._data = dict()
            except json.JSONDecodeError:
                self._data = dict()
        self._loaded_count += 1

    def store(self, forced=False):
        if self._data is None:
            return
        os.makedirs(os.path.split(self._path)[0], exist_ok=True)
        with open(self._path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._data))
        # self.unload(forced)

    def set_path(self, new_path):
        self._path = new_path

    def unload(self, forced=False):
        if self._data is None:
            return
        if forced:
            self._loaded_count = 0
        else:
            self._loaded_count = max(self._loaded_count - 1, 0)
        if not self._loaded_count:
            self._data = None

    def __getitem__(self, item):
        # self.load()
        res = self._data[item]
        # self.unload()
        return res

    def get(self, key, default):
        # self.load()
        res = self._data.get(key, default)
        # self.unload()
        return res

    def __setitem__(self, key, value):
        if key == 'name' or key == 'desc':
            self.nameChanged.emit()
        if key == 'status':
            self.statusChanged.emit()

        # self.load()
        self._data[key] = value
        # self.store()

