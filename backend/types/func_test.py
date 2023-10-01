import json
import os.path


class FuncTest:
    IN_PROGRESS = 0
    PASSED = 1
    FAILED = 2
    TERMINATED = 3
    TIMEOUT = 4

    def __init__(self, path=None, name='', test_type='pos'):
        self._path = path
        self._name = name
        self._test_type = test_type
        self._data = None

        self.in_data = dict()
        self.out_data = dict()
        self.prog_out = dict()
        self.utils_output = dict()

        self.load()
        self._status = FuncTest.IN_PROGRESS

        self.exit = 0
        self.args = ''
        self.results = dict()

    def status(self):
        return self._status

    def res(self):
        return all(self.results.values())

    def name(self):
        return self._name

    def set_status(self, status):
        self._status = status

    def type(self):
        return self._test_type

    def is_loaded(self):
        return self._data is not None

    def set_path(self, path):
        self._path = path

    def load(self):
        if self._path is None:
            return
        try:
            with open(self._path, encoding='utf-8') as f:
                self._data = json.loads(f.read())
                self.in_data = {'STDIN': self.get('in', '')}
                self.out_data = {'STDOUT': self.get('out', '')}
                for i, el in enumerate(self.get('in_files', [])):
                    self.in_data[f"in_file_{i + 1}.{el['type']}"] = el['text']
                    if 'check' in el:
                        self.out_data[f"check_file_{i + 1}.{el['type']}"] = el['check']
                for i, el in enumerate(self.get('out_files', [])):
                    self.out_data[f"out_file_{i + 1}.{el['type']}"] = el['text']
        except json.JSONDecodeError:
            self._data = dict()

    def unload(self):
        self._data = None
        self.in_data.clear()
        self.out_data.clear()

    def get(self, key, default=None):
        return self._data.get(key, default)

    def store(self):
        os.makedirs(os.path.split(self._path)[0], exist_ok=True)
        with open(self._path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._data))

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def pop(self, key):
        self._data.pop(key)

