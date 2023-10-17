import json
import os.path
import shutil
from typing import Literal

from PyQt6.QtCore import QObject, pyqtSignal

from backend.commands import write_file, read_json, get_sorted_jsons
from backend.types.unit_test import UnitTest


class UnitTestsSuite(QObject):
    addTest = pyqtSignal(UnitTest, int)
    deleteTest = pyqtSignal(int)
    nameChanged = pyqtSignal()

    def __init__(self, name):
        super().__init__()
        self._name = name
        self._tests = []
        self._code = ""

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name
        self.nameChanged.emit()

    def tests(self):
        for el in self._tests:
            yield el

    def code(self):
        return self._code

    def set_code(self, code):
        self._code = code

    def add_test(self, test: UnitTest):
        self._tests.append(test)
        self.addTest.emit(test, len(self._tests) - 1)

    def insert_test(self, test: UnitTest, index: int):
        self._tests.insert(index, test)
        self.addTest.emit(test, index)

    def delete_test(self, index):
        self._tests.pop(index)
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

    def load(self, path: str):
        self._tests.clear()
        if not os.path.isdir(path):
            return
        dct = read_json(os.path.join(path, "code.txt"))
        self.set_code(dct.get('code'))
        self.set_name(dct.get('name'))
        for el in get_sorted_jsons(path):
            self.add_test(UnitTest(os.path.join(path, el)))

    def store(self, path):
        path = os.path.join(path, self._name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path)
        write_file(os.path.join(path, "code.txt"), json.dumps({'name': self._name, 'code': self._code}))

        for i, test in enumerate(self._tests):
            test.set_path(f"{path}/{i}.json")
            test.store()
