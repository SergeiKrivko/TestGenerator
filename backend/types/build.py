import json
import os.path

from backend.commands import read_json

import language.testing.c as c


class Build:
    def __init__(self, id, path=None):
        self._data = dict() if path is None else read_json(path)
        self.id = id

    def get(self, key, default=None):
        return self._data.get(key, default)

    def store(self, path):
        os.makedirs(os.path.split(path)[0], exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._data))

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def pop(self, key):
        self._data.pop(key)

    def compile(self, project, sm, coverage):
        match self.get('type', 'C'):
            case 'C':
                return c.c_compile(project, self, sm, coverage)

    def run_preproc(self):
        pass

    def run(self, project, args, coverage=False):
        match self.get('type', 'C'):
            case 'C':
                return c.c_run(project, self, args)

    def run_postproc(self):
        pass
