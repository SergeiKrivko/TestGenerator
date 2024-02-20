import json
import os.path
import shutil
from typing import Literal
from uuid import uuid4, UUID

from PyQt6.QtCore import QObject, pyqtSignal

from src.backend.commands import write_file, read_json
from src.backend.backend_types.unit_test import UnitTest


class UnitTestsSuite(QObject):
    addTest = pyqtSignal(UnitTest, int)
    deleteTest = pyqtSignal(int)
    nameChanged = pyqtSignal()
    moduleChanged = pyqtSignal()

    def __init__(self, directory, suite_id=None):
        super().__init__()
        if suite_id is None:
            self.id = uuid4()
        else:
            self.id = UUID(suite_id)
        self._directory = directory
        self._path = os.path.join(self._directory, str(self.id))
        self._data_file = os.path.join(self._path, 'data.txt')

        self._removing = False

        self._name = ""
        self._module = ""
        self._tests = []
        self._code = ""
        self.load()

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name
        self.store()
        self.nameChanged.emit()

    def module(self):
        return self._module

    def set_module(self, module):
        self._module = module
        self.store()
        self.moduleChanged.emit()

    def tests(self):
        for el in self._tests:
            yield el

    def code(self):
        return self._code

    def set_code(self, code):
        self._code = code
        self.store()

    def add_test(self, test: UnitTest):
        self._tests.append(test)
        self.store()
        self.addTest.emit(test, len(self._tests) - 1)

    def new_test(self, index=None, data=None):
        if index is None:
            index = len(self._tests)
        test = UnitTest(self._path)
        if data:
            test.set_data(data)
        self.insert_test(test, index)

    def insert_test(self, test: UnitTest, index: int):
        self._tests.insert(index, test)
        self.store()
        self.addTest.emit(test, index)

    def delete_test(self, index):
        self._tests[index].delete()
        self._tests.pop(index)
        self.store()
        self.deleteTest.emit(index)

    def move_test(self, direction: Literal['up', 'down'], index: int):
        match direction:
            case 'up':
                if index <= 0:
                    return
                test = self._tests[index]
                self.delete_test(index)
                index -= 1
                self.insert_test(test, index)
            case 'down':
                if index >= len(self._tests) - 1:
                    return
                test = self._tests[index]
                self.delete_test(index)
                index += 1
                self.insert_test(test, index)

    def from_dict(self, dct):
        self.set_code(dct.get('code'))
        self.set_name(dct.get('name'))
        self.set_module(dct.get('module'))

    def load(self):
        self._tests.clear()
        if not os.path.isdir(self._path):
            return
        dct = read_json(self._data_file)
        self.from_dict(dct)
        for el in dct.get('tests', []):
            self.add_test(UnitTest(self._path, el))

    def to_dict(self):
        return {
            'name': self._name,
            'code': self._code,
            'module': self._module,
        }

    def store(self):
        if self._removing:
            return
        os.makedirs(self._path, exist_ok=True)
        write_file(self._data_file, json.dumps({
            **self.to_dict(),
            'tests': [str(test.id) for test in self._tests]
        }))

    def delete(self):
        self._removing = True
        try:
            shutil.rmtree(self._path)
        except FileNotFoundError:
            pass
        except PermissionError:
            pass
