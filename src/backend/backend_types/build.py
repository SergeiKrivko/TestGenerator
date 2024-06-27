import json
import os.path
import shutil
from uuid import UUID

from src.backend.backend_types.program import ProgramInstance, PROGRAMS
from src.backend.commands import read_json, cmd_command


class Build:
    class Type:
        C_EXE = 'C'
        C_LIB = 'C-lib'
        CPP_EXE = 'C++'
        CPP_LIB = 'C++lib'
        C_SHARP = 'C#'
        PYTHON = 'python'
        BASH = 'bash'
        COMMAND = 'command'

    def __init__(self, id: UUID, bm, project, path=None):
        self._data = dict() if path is None else read_json(path)
        self._id = id
        self._path = path
        self.__deleted = False

        self._bm = bm
        self._project = project

    @property
    def type(self):
        return self.get('type')

    @property
    def name(self):
        return self.get('name')

    @property
    def id(self):
        return self._id

    def get(self, key, default=None):
        return self._data.get(key, default)

    def store(self):
        if self.__deleted:
            return
        os.makedirs(os.path.split(self._path)[0], exist_ok=True)
        with open(self._path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._data))

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value
        self.store()

    def program(self, program) -> ProgramInstance:
        return PROGRAMS[program].get(self._bm.sm, self)

    def pop(self, key):
        self._data.pop(key)

    def temp_dir(self):
        return f"{self._bm.sm.temp_dir()}/build-{self.id}"

    def clear(self):
        temp_dir = self.temp_dir()
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)

    def compile(self):
        return True, ''

    def run_preproc(self):
        res, errors = True, ''
        for el in self.get('preproc', []):
            match el['type']:
                case 0:
                    build = self._bm.builds.get(el['data'])
                    res, errors = build.execute()
            if not res:
                break
        return res, errors

    def run_postproc(self):
        res, errors = True, ''
        for el in self.get('postproc', []):
            match el['type']:
                case 0:
                    build = self._bm.builds.get(el['data'])
                    res, errors = build.execute()
            if not res:
                break
        return res, errors

    def command(self, args=''):
        return ""

    def coverage(self):
        return None

    def coverage_html(self):
        return None

    def clear_coverage(self):
        pass

    def execute(self):
        res, errors = self.run_preproc()
        if not res:
            return res, errors

        res, errors = self.compile()
        if not res:
            return res, errors

        if command := self.command():
            run_res = cmd_command(command)
            res = not run_res.returncode
            errors = run_res.stdout + run_res.stderr
        if not res:
            return res, errors
        res, errors = self.run_postproc()

        return res, errors

    def remove(self):
        if os.path.isfile(self._path):
            os.remove(self._path)
        self.__deleted = True
