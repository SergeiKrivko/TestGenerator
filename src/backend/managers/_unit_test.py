import subprocess
from uuid import UUID

from PyQt6.QtCore import QObject, pyqtSignal

from src.backend.backend_types.unit_test import UnitTest
from src.backend.backend_types.unit_tests_suite import UnitTestsSuite
from src.backend.check_converter import CheckConverter
from src.backend.commands import cmd_command_pipe


class UnitTestsManager(QObject):
    suiteAdded = pyqtSignal(UnitTestsSuite)
    suiteDeleted = pyqtSignal(int)
    cleared = pyqtSignal()
    errorOccurred = pyqtSignal(str)

    def __init__(self, bm):
        super().__init__()
        self._bm = bm
        self._sm = bm.sm
        self.unit_tests_suites: list[UnitTestsSuite] = []

    def add_suite(self, suite: UnitTestsSuite):
        self.unit_tests_suites.append(suite)
        self._sm.set_data('unit_tests', ';'.join(str(test.id) for test in self.unit_tests_suites))
        self.suiteAdded.emit(suite)

    def delete_suite(self, index):
        suite = self.unit_tests_suites[index]
        suite.delete()
        self.unit_tests_suites.pop(index)
        self._sm.set_data('unit_tests', ';'.join(str(test.id) for test in self.unit_tests_suites))
        self.suiteDeleted.emit(index)

    def new_suite(self, data=None):
        suite = UnitTestsSuite(f"{self._sm.project.data_path()}/unit_tests")
        if data:
            suite.from_dict(data)
        self.add_suite(suite)
        return suite

    def convert(self):
        converter = CheckConverter(self._sm.project.unit_tests_path(), self._sm.project,
                                   self.unit_tests_suites.copy())
        converter.convert()

    def run(self):
        self._bm.processes.run(lambda: self._unit_testing(self._sm.project), 'unit_testing', self._sm.project.path())

    async def run_async(self):
        await self._bm.processes.run_async(lambda: self._unit_testing(self._sm.project),
                                           'unit_testing', self._sm.project.path())

    def _unit_testing(self, project):
        self.convert()

        items = []
        for suite in self.unit_tests_suites:
            for el in suite.tests():
                el['status'] = UnitTest.CHANGED
                items.append(el)

        build_id = UUID(project.get('unit_build'))
        if build_id is None:
            self.errorOccurred.emit("Build not found!")
            return
        build = self._bm.builds.get(build_id)

        res, errors = build.compile(build_id, project)
        if not res:
            self.errorOccurred.emit(errors)
            return

        i = 0
        try:
            for line in cmd_command_pipe(build.command(project, self._sm), shell=True):
                if line.count(':') >= 6:
                    lst = line.split(':')
                    items[i]['status'] = UnitTest.PASSED if lst[2] == 'P' else UnitTest.FAILED
                    items[i]['test_res'] = ':'.join(lst[6:])
                    i += 1
        except subprocess.CalledProcessError as ex:
            self.errorOccurred.emit(str(ex))
            return

    def clear_unit_tests(self):
        self.unit_tests_suites.clear()
        self.cleared.emit()

