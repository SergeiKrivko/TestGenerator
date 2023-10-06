import json
import os.path
import shutil

from backend.commands import read_json

from language.testing.c import *
from language.testing.python import *


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

    def clear(self, sm):
        temp_dir = f"{sm.temp_dir()}/build{self.id}"
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)

    def compile(self, project, sm):
        match self.get('type'):
            case 'C':
                return c_compile(project, self, sm)
            case _:
                return True, ''

    def run_preproc(self):
        pass

    def run(self, project, sm, args):
        match self.get('type'):
            case 'C':
                return c_run(project, self, args)
            case 'python':
                return python_run(project, self, args)
            case 'python_coverage':
                return python_run_coverage(project, sm, self, args)
            case 'bash':
                return f"{sm.get_general('bash', 'usr/bin/bash')} \"{self.get('file')}\" {args}"
            case 'script':
                return f"{self.get('file')} {args}"
            case 'command':
                return self.get('command')
            case _:
                return ""

    def collect_coverage(self, project, sm):
        match self.get('type', 'C'):
            case 'C':
                print(c_collect_coverage(sm, self))
                return c_collect_coverage(sm, self)
            case 'python_coverage':
                return python_collect_coverage(sm, self)
            case _:
                return None

    def run_postproc(self):
        pass
