import os
import shutil
from typing import Literal

from PyQt6.QtCore import QObject, pyqtSignal

from backend.backend_types.unit_tests_suite import UnitTestsSuite


class UnitTestsModule(QObject):
    addSuite = pyqtSignal(UnitTestsSuite, int)
    deleteSuite = pyqtSignal(int)

    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self._suits = []

    def name(self):
        return self._name

    def suits(self):
        for el in self._suits:
            yield el

    def add_suite(self, suite: UnitTestsSuite):
        self._suits.append(suite)
        self.addSuite.emit(suite, len(self._suits) - 1)

    def insert_suite(self, suite: UnitTestsSuite, index: int):
        self._suits.insert(index, suite)
        self.addSuite.emit(suite, index)

    def delete_suite(self, index):
        self._suits.pop(index)
        self.deleteSuite.emit(index)

    def move_suite(self, direction: Literal['up', 'down'], index: int):
        match direction:
            case 'up':
                if index <= 0:
                    return
                test = self._suits[index]
                self.delete_suite(index)
                index -= 1
                self.insert_suite(test, index)
            case 'down':
                if index >= len(self._suits) - 1:
                    return
                test = self._suits[index]
                self.delete_suite(index)
                index += 1
                self.insert_suite(test, index)

    def has_suits(self):
        return bool(len(self._suits))

    def load(self, path: str):
        self._suits.clear()
        if not os.path.isdir(path):
            return
        for el in os.listdir(path):
            if os.path.isdir(os.path.join(path, el)):
                self.add_suite(suite := UnitTestsSuite(el))
                suite.load(os.path.join(path, el))

    def store(self, path):
        path = os.path.join(path, self._name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path)

        for i, suite in enumerate(self._suits):
            suite.store(path)

