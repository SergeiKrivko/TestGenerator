from typing import Literal

from PyQt6.QtCore import QObject, pyqtSignal

from src.backend.backend_types.func_test import FuncTest
from src.backend.commands import get_jsons
from src.backend.func_testing import TestingLooper
from src.backend.history_manager import EMPTY_RECORD, HistoryManager
from src.backend.macros_converter import MacrosConverter
from src.backend.managers.manager import AbstractManager
from src.backend.settings_manager import SettingsManager


class FuncTestsManager(AbstractManager):
    onAdd = pyqtSignal(FuncTest, int)
    onDelete = pyqtSignal(FuncTest, int)
    onClear = pyqtSignal()
    onStatusChanged = pyqtSignal(FuncTest)

    startTesting = pyqtSignal(list)
    testingError = pyqtSignal(str)
    testingUtilError = pyqtSignal(str)
    endTesting = pyqtSignal(object, object)

    def __init__(self, sm: SettingsManager, bm):
        super().__init__(bm)
        self._sm = sm
        self._bm = bm
        self._func_tests = {FuncTest.Type.POS: [], FuncTest.Type.NEG: []}

        self._func_tests_history = HistoryManager()

        self.tests_completed = 0
        self._testing_looper = None

    def add(self, test: FuncTest, index=None, record=None):
        if record is None:
            record = EMPTY_RECORD
        record.add_data(('add', test, index))
        if index is None:
            index = len(self._func_tests[test.type])
        self._func_tests[test.type].insert(index, test)
        self._sm.set_data(f'{test.type}_func_tests',
                          ';'.join(str(test.id) for test in self._func_tests[test.type]))
        self.onAdd.emit(test, index)

    def new(self, test_type: FuncTest.Type, index=None, record=None):
        if record is None:
            record = self._func_tests_history.add_record('new')
        path = f"{self._sm.project.data_path()}/func_tests/{test_type.value}"
        test = FuncTest(path, test_type=test_type)
        self.add(test, index, record=record)
        return test

    def from_data(self, test_type: FuncTest.Type, index=None, data=None, record=None):
        if record is None:
            record = self._func_tests_history.add_record('new')
        path = f"{self._sm.project.data_path()}/func_tests/{test_type.value}"
        test = FuncTest.from_dict(path, test_type=test_type, data=data)
        self.add(test, index, record=record)
        return test

    def delete(self, type: FuncTest.Type, index: int, record=None):
        test = self._func_tests[type][index]
        if record is None:
            record = self._func_tests_history.add_record('delete_group')
        record.add_data(('delete', test, index))
        self._func_tests[type].pop(index)
        test.delete()
        self._sm.set_data(f'{type}_func_tests', ';'.join(str(test.id) for test in self._func_tests[type]))
        self.onDelete.emit(test, index)

    def add_some(self, type: FuncTest.Type, tests: list[int] | dict[int: dict]):
        record = self._func_tests_history.add_record('add_group')
        if isinstance(tests, list):
            for i in tests:
                self.new(type, i, record=record)
        else:
            for i, data in tests.items():
                self.from_data(type, i, data, record=record)

    def delete_some(self, type: FuncTest.Type, indexes: list[int]):
        record = self._func_tests_history.add_record('delete_tests')
        for ind in sorted(indexes, reverse=True):
            self.delete(type, ind, record=record)

    def clear(self):
        for test_type in FuncTest.Type:
            self._func_tests[test_type].clear()
            # self.sm.set_data(f'{test_type}_func_tests', ';'.join(str(test.id) for test in self.func_tests[test_type]))
        self.onClear.emit()

    def get(self, type: FuncTest.Type = None, index: int = 0):
        if type is None:
            if index >= len(self._func_tests[FuncTest.Type.POS]):
                index -= len(self._func_tests[FuncTest.Type.POS])
                type = FuncTest.Type.NEG
            else:
                type = FuncTest.Type.POS
        return self._func_tests[type][index]

    def move(self, type: FuncTest.Type, direction: Literal['up', 'down'], index: int):
        record = self._func_tests_history.add_record('move')
        match direction:
            case 'up':
                if index <= 0:
                    return
                test = self.get(type, index)
                self.delete(type, index, record=record)
                index -= 1
                self.add(test, index, record=record)
            case 'down':
                if index >= len(self._func_tests[type]) - 1:
                    return
                test = self.get(type, index)
                self.delete(type, index, record=record)
                index += 1
                self.add(test, index, record=record)
        self._sm.project.set_data(f'{type.value}_func_tests', ';'.join(str(test.id) for test in self._func_tests[type]))

    def count(self, type: FuncTest.Type = None):
        match type:
            case FuncTest.Type.POS:
                return len(self._func_tests[FuncTest.Type.POS])
            case FuncTest.Type.NEG:
                return len(self._func_tests[FuncTest.Type.NEG])
            case None:
                return len(self._func_tests[FuncTest.Type.POS]) + len(self._func_tests[FuncTest.Type.NEG])

    def macros_converter(self):
        if self._sm.project is None:
            return
        if not self._func_tests[FuncTest.Type.POS] and not self._func_tests[FuncTest.Type.NEG]:
            return
        looper = MacrosConverter(self._sm.project, {FuncTest.Type.POS: self._func_tests[FuncTest.Type.POS].copy(),
                                                    FuncTest.Type.NEG: self._func_tests[FuncTest.Type.NEG].copy()}, self._sm)
        self._bm.processes.run(looper, 'macros_converter', self._sm.project.path())

    async def macros_converter_async(self):
        if self._sm.project is None:
            return
        if not self._func_tests[FuncTest.Type.POS] and not self._func_tests[FuncTest.Type.NEG]:
            return
        looper = MacrosConverter(self._sm.project, {FuncTest.Type.POS: self._func_tests[FuncTest.Type.POS].copy(),
                                                    FuncTest.Type.NEG: self._func_tests[FuncTest.Type.NEG].copy()}, self._sm)
        await self._bm.processes.run_async(looper, 'macros_converter', self._sm.project.path())

    def undo(self, redo=False):
        if redo:
            record = self._func_tests_history.get_redo()
        else:
            record = self._func_tests_history.get_undo()
        if record is None:
            return
        actions = list(record)
        record.clear()
        for action_type, test, index in actions:
            if action_type == 'delete':
                self.add(test, index, record=record)
            else:
                self.delete(test.type(), index, record=record)

    @property
    def all_tests(self):
        return self._func_tests[FuncTest.Type.POS] + self._func_tests[FuncTest.Type.NEG]

    def testing(self, verbose=False):
        return self._bm.processes.run(self._testing(verbose), 'testing', 'main')

    async def testing_async(self, verbose=False):
        return self._bm.processes.run_async(self._testing(verbose), 'testing', 'main')

    def _testing(self, verbose=False):
        # self.macros_converter()
        self.startTesting.emit(self.all_tests)
        self.tests_completed = 0
        self._testing_looper = TestingLooper(self._bm, self._sm.project, self.all_tests, verbose=verbose)
        self._testing_looper.testStatusChanged.connect(self._func_test_set_status)
        self._testing_looper.finished.connect(lambda: self.endTesting.emit(self._testing_looper.coverage,
                                                                           self._testing_looper.coverage_html))
        self._testing_looper.compileFailed.connect(self.testingError.emit)
        self._testing_looper.utilFailed.connect(self.testingUtilError.emit)
        return self._testing_looper

    def stop_testing(self):
        if isinstance(self._testing_looper, TestingLooper) and self._testing_looper.isRunning():
            self._testing_looper.terminate()

    def _func_test_set_status(self, test: FuncTest, status):
        if status in [FuncTest.Status.PASSED, FuncTest.Status.FAILED, FuncTest.Status.TIMEOUT, FuncTest.Status.TERMINATED]:
            self.tests_completed += 1
        test.status = status
        self.onStatusChanged.emit(test)

    def _load_func_tests(self):
        path = self._sm.project.path()
        for test_type in FuncTest.Type:
            if isinstance(lst := self._sm.project.get_data(f'{test_type.value}_func_tests'), str):
                for test_id in lst.split(';'):
                    if test_id:
                        self.add(FuncTest(
                            f"{path}/func_tests/{test_type.value}", test_type, test_id))
            else:
                for i, el in enumerate(get_jsons(f"{path}/func_tests/{test_type.value}")):
                    self.add(FuncTest.from_file(
                        f"{path}/func_tests/{test_type.value}/{el}", test_type))

    async def load(self):
        await self._bm.processes.run_async(self._load_func_tests, 'loading', 'func_tests')
