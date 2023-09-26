import json
import os
import shutil


class UnitTest:
    def __init__(self, path):
        self._path = path
        self._data = None
        self._loaded_count = 0

    def path(self):
        return self._path

    def rename_file(self, new_name: str):
        os.rename(self._path, new_name)
        self._path = new_name

    def delete_file(self):
        try:
            os.remove(self._path)
        except FileNotFoundError:
            pass
        self.unload(True)

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
        self.unload(forced)

    def change_dir(self, new_path):
        self._path = os.path.join(new_path + os.path.basename(self._path))

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


class UnitTestSuite:
    def __init__(self, data_dir: str, module: str, name: str):
        super().__init__()
        self._data_dir = data_dir
        self._module = module
        self._name = name

        self._path = ''
        self._update_path()

    def _update_path(self):
        old_path = self._path
        self._path = os.path.join(self._data_dir, self._module, self._name)
        try:
            os.rename(old_path, self._path)
        except FileNotFoundError:
            pass

    def path(self):
        return self._path

    def set_name(self, name):
        self._name = name
        self._update_path()

    def name(self):
        return self._name

    def set_module(self, module):
        self._module = module
        self._update_path()

    def module(self):
        return self._module

    def delete_dir(self):
        try:
            shutil.rmtree(self._path)
        except FileNotFoundError:
            pass


