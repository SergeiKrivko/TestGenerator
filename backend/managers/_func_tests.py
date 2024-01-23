from typing import Literal

from PyQt6.QtCore import QObject, pyqtSignal

from backend.backend_types.func_test import FuncTest
from backend.history_manager import EMPTY_RECORD, HistoryManager
from backend.macros_converter import MacrosConverter
from backend.settings_manager import SettingsManager


class FuncTestsManager(QObject):
    onAdd = pyqtSignal(FuncTest, int)
    onDelete = pyqtSignal(FuncTest, int)
    onClear = pyqtSignal()
    onStatusChanged = pyqtSignal(FuncTest)

    def __init__(self, sm: SettingsManager, bm):
        super().__init__()
        self._sm = sm
        self._bm = bm
        self._func_tests = {'pos': [], 'neg': []}

        self._func_tests_history = HistoryManager()

    def add(self, test: FuncTest, index=None, record=None):
        if record is None:
            record = EMPTY_RECORD
        record.add_data(('add', test, index))
        if index is None:
            index = len(self._func_tests[test.type()])
        self._func_tests[test.type()].insert(index, test)
        self._sm.set_data(f'{test.type()}_func_tests',
                          ';'.join(str(test.id) for test in self._func_tests[test.type()]))
        self.onAdd.emit(test, index)

    def new(self, test_type='pos', index=None, data=None, record=None):
        if record is None:
            record = self._func_tests_history.add_record('new')
        test = FuncTest(f"{self._sm.project.data_path()}/func_tests/{test_type}", test_type=test_type)
        if data:
            test.from_dict(data)
        self.add(test, index, record=record)
        return test

    def delete(self, type: Literal['pos', 'neg'], index: int, record=None):
        test = self._func_tests[type][index]
        if record is None:
            record = self._func_tests_history.add_record('delete_group')
        record.add_data(('delete', test, index))
        self._func_tests[type].pop(index)
        test.delete()
        self._sm.set_data(f'{type}_func_tests', ';'.join(str(test.id) for test in self._func_tests[type]))
        self.onDelete.emit(test, index)

    def add_some(self, type: Literal['pos', 'neg'], tests: list[int] | dict[int: dict]):
        record = self._func_tests_history.add_record('add_group')
        if isinstance(tests, list):
            for i in tests:
                self.new(type, i, record=record)
        else:
            for i, data in tests.items():
                self.new(type, i, data, record=record)

    def delete_some(self, type: Literal['pos', 'neg'], indexes: list[int]):
        record = self._func_tests_history.add_record('delete_tests')
        for ind in sorted(indexes, reverse=True):
            self.delete(type, ind, record=record)

    def clear(self):
        for test_type in ['pos', 'neg']:
            self._func_tests[test_type].clear()
            # self.sm.set_data(f'{test_type}_func_tests', ';'.join(str(test.id) for test in self.func_tests[test_type]))
        self.onClear.emit()

    def get(self, type: Literal['pos', 'neg', 'all'], index: int):
        if type == 'all':
            if index >= len(self._func_tests['pos']):
                index -= len(self._func_tests['pos'])
                type = 'neg'
            else:
                type = 'pos'
        return self._func_tests[type][index]

    def move(self, type: Literal['pos', 'neg'], direction: Literal['up', 'down'], index: int):
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
        self._sm.project.set_data(f'{type}_func_tests', ';'.join(str(test.id) for test in self._func_tests[type]))

    def count(self, type: Literal['pos', 'neg', 'all'] = 'all'):
        match type:
            case 'pos':
                return len(self._func_tests['pos'])
            case 'neg':
                return len(self._func_tests['neg'])
            case 'all':
                return len(self._func_tests['pos']) + len(self._func_tests['neg'])

    def run_macros_converter(self):
        if self._sm.project is None:
            return
        if not self._func_tests['pos'] and not self._func_tests['neg']:
            return
        looper = MacrosConverter(self._sm.project, {'pos': self._func_tests['pos'].copy(),
                                                    'neg': self._func_tests['neg'].copy()}, self._sm)
        self._bm.processes.run(looper, 'macros_converter', self._sm.project.path())

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
        return self._func_tests['pos'] + self._func_tests['neg']
