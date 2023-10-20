import json
import os.path
import shutil

from backend.commands import read_json
from backend.backend_types.build import Build

from language.testing.c import *
from language.testing.python import *


class Util:
    BEFORE_TESTING = 0
    FOR_TEST = 1
    AFTER_TESTING = 2

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

    def run(self, project, build: Build, args=None, **kwargs):
        match self.get('type', 0):
            case Util.FOR_TEST:
                app_file = build.get('app_file', 'app.exe')
                if not os.path.isabs(app_file):
                    app_file = './' + app_file
                command = self.get('command', '').format(app=app_file, args='' if args is None else args)
                res = cmd_command(command, cwd=project.path(), shell=True, **kwargs)
            case _:
                return False, "Invalid util type"

        match self.get('output', 0):
            case 0:
                output = res.stdout
            case 1:
                output = res.stderr
            case _:
                output = ''

        if self.get('returncode_res', False) and res.returncode:
            return False, output
        if self.get('output_res', False) and output:
            return False, output
        return True, output

