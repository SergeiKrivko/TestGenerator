import json
import os.path
from enum import Enum
from typing import Literal
from uuid import uuid4, UUID

from src.backend.commands import read_json, write_file
from src.other.binary_redactor.convert_binary import convert_bytes


class FuncTest:
    class Status(Enum):
        NONE = 0
        IN_PROGRESS = 1
        PASSED = 2
        FAILED = 3
        TERMINATED = 4
        TIMEOUT = 5

    class Comparator(Enum):
        DEFAULT = 0
        NONE = 1
        NUMBERS = 2
        NUMBERS_AS_STRING = 3
        TEXT_AFTER = 4
        WORDS_AFTER = 5
        TEXT = 6
        WORDS = 7

    class Type(Enum):
        POS = 'pos'
        NEG = 'neg'

    class InFile:
        def __init__(self, type: Literal['txt', 'bin'], data: str, check: str | None = None):
            self.type = type
            self.data = data
            self.check = check

        def bytes(self):
            if self.type == 'txt':
                return self.data
            return convert_bytes(self.data)

        def check_bytes(self):
            if self.type == 'txt':
                return self.check
            return convert_bytes(self.check)

        def to_dict(self):
            return {'type': self.type, 'text': self.data, 'check': self.check}

    class OutFile:
        def __init__(self, type: Literal['txt', 'bin'], data: str):
            self.type = type
            self.data = data

        def bytes(self):
            if self.type == 'txt':
                return self.data
            return convert_bytes(self.data)

        def to_dict(self):
            return {'type': self.type, 'text': self.data}

    class Result:
        def __init__(self, test: 'FuncTest'):
            self._test = test

            self.args = test.args

            self._code = 0
            self._time = 0
            self._results: dict[str: bool] = dict()
            self._files: dict[str: str] = dict()
            self._utils_output = dict()

        @property
        def results(self):
            return self._results

        @property
        def code(self):
            return self._code

        @code.setter
        def code(self, value):
            self._code = value

        @property
        def files(self):
            return self._files

        @property
        def utils_output(self):
            return self._utils_output

        @property
        def time(self):
            return self._time

        @time.setter
        def time(self, value):
            self._time = value

    def __init__(self, directory: str, test_type: Type, test_id=None):
        if test_id:
            self.id = UUID(test_id)
        else:
            self.id = uuid4()

        if not isinstance(test_type, FuncTest.Type):
            raise TypeError('test_type must be of type FuncTest.Type')

        self._directory = directory
        self._path = f"{self._directory}/{self.id}.json"

        self._type = test_type
        self._desc = ''
        self._stdin = ''
        self._stdout = ''
        self._in_files: list[FuncTest.InFile] = []
        self._out_files: list[FuncTest.OutFile] = []
        self._args = ''
        self._exit = None
        self._current_in = 0
        self._current_out = 0
        self.load()

        self._res = FuncTest.Result(self)

        self._status = FuncTest.Status.NONE

    def load(self, data=None):
        if data is None:
            data = read_json(self._path)
        self._desc = data.get('desc', '')
        self._stdin = data.get('in', '')
        self._stdout = data.get('out', '')

        for el in data.get('in_files', []):
            self._in_files.append(FuncTest.InFile(el.get('type'), el.get('text'), el.get('check')))
        for el in data.get('out_files', []):
            self._out_files.append(FuncTest.OutFile(el.get('type'), el.get('text')))

        self._args = data.get('args', '')
        self._exit = data.get('exit', '')
        self._current_in = data.get('current_in', 0)
        self._current_out = data.get('current_out', 0)

    def to_dict(self):
        return {
            'desc': self._desc,
            'in': self._stdin,
            'out': self._stdout,
            'in_files': [el.to_dict() for el in self._in_files],
            'out_files': [el.to_dict() for el in self._out_files],
            'args': self._args,
            'exit': self._exit,
            'current_in': self._current_in,
            'current_out': self._current_out,
        }

    def save(self):
        write_file(self._path, json.dumps(self.to_dict()))

    @property
    def type(self) -> Type:
        return self._type

    @property
    def description(self) -> str:
        return self._desc

    @description.setter
    def description(self, value: str):
        self._desc = value
        self.save()

    @property
    def stdin(self) -> str:
        return self._stdin

    @stdin.setter
    def stdin(self, value):
        self._stdin = value
        self.save()

    @property
    def stdout(self):
        return self._stdout

    @stdout.setter
    def stdout(self, value):
        self._stdout = value
        self.save()

    @property
    def in_files(self) -> list[InFile]:
        return self._in_files

    @property
    def out_files(self) -> list[OutFile]:
        return self._out_files

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value
        self.save()

    @property
    def exit(self):
        return self._exit

    @exit.setter
    def exit(self, value):
        self._exit = value
        self.save()

    @property
    def current_in(self):
        return self._current_in

    @current_in.setter
    def current_in(self, value):
        self._current_in = value
        self.save()

    @property
    def current_out(self):
        return self._current_out

    @current_out.setter
    def current_out(self, value):
        self._current_out = value
        self.save()

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, status: Status):
        if not isinstance(status, FuncTest.Status):
            raise TypeError('status must be of type FuncTest.Status')
        self._status = status
        self.save()

    @property
    def res(self):
        return self._res

    @staticmethod
    def from_file(path: str, test_type):
        test = FuncTest.from_dict(os.path.split(path)[0], test_type, read_json(path))
        os.remove(path)
        return test

    @staticmethod
    def from_dict(path, test_type, data: dict):
        test = FuncTest(path, test_type)
        test.load(data)
        test.save()
        return test

    def delete(self):
        if os.path.isfile(self._path):
            os.remove(self._path)
