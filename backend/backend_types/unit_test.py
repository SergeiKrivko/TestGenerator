import json
import os
from uuid import uuid4, UUID

from PyQt6.QtCore import QObject, pyqtSignal

from backend.commands import read_json


class UnitTest(QObject):
    nameChanged = pyqtSignal()
    statusChanged = pyqtSignal()

    PASSED = 0
    FAILED = 1
    CHANGED = 2

    def __init__(self, directory, test_id=None):
        super().__init__()
        self._directory = directory
        if test_id is None:
            self.id = uuid4()
        else:
            self.id = UUID(test_id)
        self._path = f"{self._directory}/{self.id}.json"
        self._data = None

        if not os.path.isfile(self._path):
            self.store()
        else:
            self.load()

    def path(self):
        return self._path

    def load(self):
        self._data = read_json(self._path)

    def store(self):
        if self._data is None:
            return
        os.makedirs(os.path.split(self._path)[0], exist_ok=True)
        with open(self._path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._data))

    def delete(self):
        try:
            os.remove(self._path)
        except FileNotFoundError:
            pass

    def set_path(self, new_path):
        self._path = new_path

    def unload(self):
        self._data = None

    def __getitem__(self, item):
        res = self._data[item]
        return res

    def get(self, key, default=None):
        res = self._data.get(key, default)
        return res

    def __setitem__(self, key, value):
        if key == 'name' or key == 'desc':
            self.nameChanged.emit()
        if key == 'status':
            self.statusChanged.emit()

        self._data[key] = value
        self.store()

