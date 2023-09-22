import json
import os


class UnitTest:
    def __init__(self, path):
        self._path = path
        self._data = None
        self._loaded_count = 0

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
            f.write(self._data)
        self.unload(forced)

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
        self.load()
        res = self._data[item]
        self.unload()
        return res

    def get(self, key, default):
        self.load()
        res = self._data.get(key, default)
        self.unload()
        return res

    def __setitem__(self, key, value):
        self.load()
        self._data[key] = value
        self.store()

