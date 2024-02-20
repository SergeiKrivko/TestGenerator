import json
import os.path
from uuid import uuid4, UUID

from src.backend.commands import read_json


class FuncTest:
    IN_PROGRESS = 0
    PASSED = 1
    FAILED = 2
    TERMINATED = 3
    TIMEOUT = 4

    def __init__(self, directory='', test_id=None, test_type='pos'):
        if test_id:
            self.id = UUID(test_id)
        else:
            self.id = uuid4()

        self._directory = directory
        self._path = f"{self._directory}/{self.id}.json"
        self._name = ''
        self._test_type = test_type
        self._data = None

        self.in_data = dict()
        self.out_data = dict()
        self.prog_out = dict()
        self.utils_output = dict()

        self.load()
        self._status = FuncTest.IN_PROGRESS

        self.exit = 0
        self.time = 0
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
        if self._path is None or not os.path.isfile(self._path):
            self._data = dict()
            return
        try:
            with open(self._path, encoding='utf-8') as f:
                self._data = json.loads(f.read())
                self.load_testing_data()
        except json.JSONDecodeError:
            self._data = dict()

    def load_testing_data(self):
        self.in_data = {'STDIN': self.get('in', '')}
        self.out_data = {'STDOUT': self.get('out', '')}
        for i, el in enumerate(self.get('in_files', [])):
            self.in_data[f"in_file_{i + 1}.{el['type']}"] = el['text']
            if 'check' in el:
                self.out_data[f"check_file_{i + 1}.{el['type']}"] = el['check']
        for i, el in enumerate(self.get('out_files', [])):
            self.out_data[f"out_file_{i + 1}.{el['type']}"] = el['text']

    def clear_output(self):
        self.prog_out.clear()
        self.results.clear()
        self.utils_output.clear()

    def unload(self):
        self._data = None
        self.in_data.clear()
        self.out_data.clear()

    def delete(self):
        try:
            os.remove(self._path)
        except FileNotFoundError:
            pass

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
        self.store()

    def pop(self, key):
        self._data.pop(key)
        self.store()

    @staticmethod
    def from_file(path: str, test_type):
        test = FuncTest(os.path.split(path)[0], test_type=test_type)
        test._data = read_json(path)
        test.load_testing_data()
        test.store()
        return test

    def to_dict(self):
        return self._data

    def from_dict(self, data: dict):
        self._data = data
        self.load_testing_data()
        self.store()
