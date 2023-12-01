import os.path
import random
import sys
import types
from time import sleep
from typing import Literal

import py7zr
from PyQt6.QtCore import QObject, pyqtSignal, QThread

from backend.backend_types.unit_tests_suite import UnitTestsSuite
from backend.func_testing import TestingLooper
from backend.history_manager import HistoryManager, EMPTY_RECORD
from backend.load_task import Loader
from backend.macros_converter import MacrosConverter
from backend.backend_types.build import Build
from backend.backend_types.project import Project
from backend.backend_types.unit_test import UnitTest
from backend.backend_types.util import Util
from backend.check_converter import CheckConverter
from backend.settings_manager import SettingsManager
from backend.backend_types.func_test import FuncTest
from backend.commands import *


class BackendManager(QObject):
    startChangingProject = pyqtSignal()
    finishChangingProject = pyqtSignal()
    allProcessFinished = pyqtSignal()
    loadingStart = pyqtSignal(Project)
    updateProgress = pyqtSignal(int, int)

    addFuncTest = pyqtSignal(FuncTest, int)
    deleteFuncTest = pyqtSignal(FuncTest, int)
    clearFuncTests = pyqtSignal()
    changeTestStatus = pyqtSignal(FuncTest)

    addUnitTestSuite = pyqtSignal(UnitTestsSuite)
    deleteSuite = pyqtSignal(int)
    clearUnitTests = pyqtSignal()
    unitTestingError = pyqtSignal(str)

    startTesting = pyqtSignal(list)
    testingError = pyqtSignal(str)
    testingUtilError = pyqtSignal(str)
    endTesting = pyqtSignal(object, object)

    addBuild = pyqtSignal(Build)
    deleteBuild = pyqtSignal(Build)
    renameBuild = pyqtSignal(Build)
    clearBuilds = pyqtSignal()

    addUtil = pyqtSignal(Util)
    deleteUtil = pyqtSignal(Util)
    renameUtil = pyqtSignal(Util)
    clearUtils = pyqtSignal()

    showMainTab = pyqtSignal(str)
    showSideTab = pyqtSignal(str)
    mainTabCommand = pyqtSignal(str, tuple, dict)
    sideTabCommand = pyqtSignal(str, tuple, dict)
    showNotification = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.sm = SettingsManager()

        self.func_tests = {'pos': [], 'neg': []}
        self.builds = dict()
        self.utils = dict()
        self.unit_tests_suites: list[UnitTestsSuite] = []

        self.func_test_completed = 0

        self._testing_looper = None
        self._loader = None

        self._background_processes: dict[str: dict[str: QThread]] = dict()
        self._background_process_count = 0

        self.changing_project = False

        self._func_tests_history = HistoryManager()

    # ------------------------- SETTINGS ------------------------------

    def open_project(self, project: Project | str):
        if isinstance(project, str):
            if project not in self.sm.projects:
                return
            project = self.sm.projects[project]
        if project == self.sm.project:
            return
        self.changing_project = True
        self.startChangingProject.emit()
        self.run_macros_converter()
        self._run_loader(project)

    def close_project(self):
        self.changing_project = True
        self.startChangingProject.emit()
        self._run_loader(None)

    def open_main_project(self, project: Project, subproject: Project = None):
        if isinstance(project, str):
            project = os.path.abspath(project)
            if project not in self.sm.projects:
                return
            project = self.sm.projects[project]
        if project == self.sm.project:
            return
        self.changing_project = True
        self.startChangingProject.emit()
        self.run_macros_converter()
        if subproject:
            self._run_loader(subproject, main=project)
        else:
            self._run_loader(project, main=True)

    def _run_loader(self, project: Project | None, main=False):
        self._loader = Loader(self, project, main)
        self._loader.finished.connect(self._on_loader_finished)
        self._loader.updateProgress.connect(self.updateProgress.emit)
        self._loader.loadingStart.connect(self.loadingStart.emit)
        self.run_process(self._loader, 'load', None if project is None else project.path())

    def _on_loader_finished(self):
        if self.changing_project:
            self.changing_project = False
            self.finishChangingProject.emit()

    # ------------------------ FUNC TESTS -----------------------------

    def add_func_test(self, test: FuncTest, index=None, record=None):
        if record is None:
            record = EMPTY_RECORD
        record.add_data(('add', test, index))
        if index is None:
            index = len(self.func_tests[test.type()])
        self.func_tests[test.type()].insert(index, test)
        self.sm.set_data(f'{test.type()}_func_tests', ';'.join(str(test.id) for test in self.func_tests[test.type()]))
        self.addFuncTest.emit(test, index)

    def new_func_test(self, test_type='pos', index=None, data=None, record=None):
        if record is None:
            record = self._func_tests_history.add_record('new')
        test = FuncTest(f"{self.sm.project.data_path()}/func_tests/{test_type}", test_type=test_type)
        if data:
            test.from_dict(data)
        self.add_func_test(test, index, record=record)
        return test

    def delete_func_test(self, type: Literal['pos', 'neg'], index: int, record=None):
        test = self.func_tests[type][index]
        if record is None:
            record = self._func_tests_history.add_record('delete_group')
        record.add_data(('delete', test, index))
        self.func_tests[type].pop(index)
        test.delete()
        self.sm.set_data(f'{type}_func_tests', ';'.join(str(test.id) for test in self.func_tests[type]))
        self.deleteFuncTest.emit(test, index)

    def add_some_func_tests(self, type: Literal['pos', 'neg'], tests: list[int] | dict[int: dict]):
        record = self._func_tests_history.add_record('add_group')
        if isinstance(tests, list):
            for i in tests:
                self.new_func_test(type, i, record=record)
        else:
            for i, data in tests.items():
                self.new_func_test(type, i, data, record=record)

    def delete_some_func_tests(self, type: Literal['pos', 'neg'], indexes: list[int]):
        record = self._func_tests_history.add_record('delete_tests')
        for ind in sorted(indexes, reverse=True):
            self.delete_func_test(type, ind, record=record)

    def clear_func_tests(self):
        for test_type in ['pos', 'neg']:
            self.func_tests[test_type].clear()
            # self.sm.set_data(f'{test_type}_func_tests', ';'.join(str(test.id) for test in self.func_tests[test_type]))
        self.clearFuncTests.emit()

    def get_func_test(self, type: Literal['pos', 'neg', 'all'], index: int):
        if type == 'all':
            if index >= len(self.func_tests['pos']):
                index -= len(self.func_tests['pos'])
                type = 'neg'
            else:
                type = 'pos'
        return self.func_tests[type][index]

    def move_func_test(self, type: Literal['pos', 'neg'], direction: Literal['up', 'down'], index: int):
        record = self._func_tests_history.add_record('move')
        match direction:
            case 'up':
                if index <= 0:
                    return
                test = self.get_func_test(type, index)
                self.delete_func_test(type, index, record=record)
                index -= 1
                self.add_func_test(test, index, record=record)
            case 'down':
                if index >= len(self.func_tests[type]) - 1:
                    return
                test = self.get_func_test(type, index)
                self.delete_func_test(type, index, record=record)
                index += 1
                self.add_func_test(test, index, record=record)
        self.sm.project.set_data(f'{type}_func_tests', ';'.join(str(test.id) for test in self.func_tests[type]))

    def func_tests_count(self, type: Literal['pos', 'neg', 'all'] = 'all'):
        match type:
            case 'pos':
                return len(self.func_tests['pos'])
            case 'neg':
                return len(self.func_tests['neg'])
            case 'all':
                return len(self.func_tests['pos']) + len(self.func_tests['neg'])

    def run_macros_converter(self):
        if self.sm.project is None:
            return
        if not self.func_tests['pos'] and not self.func_tests['neg']:
            return
        looper = MacrosConverter(self.sm.project, {'pos': self.func_tests['pos'].copy(),
                                                   'neg': self.func_tests['neg'].copy()}, self.sm)
        self.run_process(looper, 'macros_converter', self.sm.project.path())

    def undo_func_tests(self, redo=False):
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
                self.add_func_test(test, index, record=record)
            else:
                self.delete_func_test(test.type(), index, record=record)

    # -------------------------- TESTING --------------------------------

    def start_testing(self, verbose=False):
        self.run_macros_converter()
        self.startTesting.emit(self.func_tests['pos'] + self.func_tests['neg'])
        self.func_test_completed = 0
        self._testing_looper = TestingLooper(self.sm, self.sm.project, self,
                                             self.func_tests['pos'] + self.func_tests['neg'], verbose=verbose)
        self._testing_looper.testStatusChanged.connect(self.func_test_set_status)
        self._testing_looper.finished.connect(lambda: self.endTesting.emit(self._testing_looper.coverage,
                                                                           self._testing_looper.coverage_html))
        self._testing_looper.compileFailed.connect(self.testingError.emit)
        self._testing_looper.utilFailed.connect(self.testingUtilError.emit)
        self.run_process(self._testing_looper, 'testing', 'main')
        return self._testing_looper

    def stop_testing(self):
        if isinstance(self._testing_looper, TestingLooper) and self._testing_looper.isRunning():
            self._testing_looper.terminate()

    def func_test_set_status(self, test: FuncTest, status):
        if status in [FuncTest.PASSED, FuncTest.FAILED, FuncTest.TIMEOUT, FuncTest.TERMINATED]:
            self.func_test_completed += 1
        test.set_status(status)
        self.changeTestStatus.emit(test)

    # --------------------------- BUILDS --------------------------------

    def add_build(self, build: Build):
        self.builds[build.id] = build
        self.addBuild.emit(build)

    def generate_build_id(self):
        while (res := random.randint(0, 2**31)) in self.builds:
            pass
        return res

    def delete_build(self, id: int):
        build = self.builds[id]
        self.builds.pop(id)
        self.deleteBuild.emit(build)

    def clear_builds(self):
        self.builds.clear()
        self.clearBuilds.emit()

    def get_build(self, id: int) -> Build:
        return self.builds.get(id)

    # --------------------------- UTILS --------------------------------

    def add_util(self, util: Util):
        self.utils[util.id] = util
        self.addUtil.emit(util)

    def generate_util_id(self):
        while (res := random.randint(0, 2**31)) in self.utils:
            pass
        return res

    def delete_util(self, id: int):
        util = self.utils[id]
        self.utils.pop(id)
        self.deleteUtil.emit(util)

    def clear_utils(self):
        self.utils.clear()
        self.clearUtils.emit()

    def get_util(self, id: int):
        return self.utils.get(id)

    # ------------------- UNIT TESTING -------------------------

    def add_suite(self, suite: UnitTestsSuite):
        self.unit_tests_suites.append(suite)
        self.sm.set_data('unit_tests', ';'.join(str(test.id) for test in self.unit_tests_suites))
        self.addUnitTestSuite.emit(suite)

    def delete_suite(self, index):
        suite = self.unit_tests_suites[index]
        suite.delete()
        self.unit_tests_suites.pop(index)
        self.sm.set_data('unit_tests', ';'.join(str(test.id) for test in self.unit_tests_suites))
        self.deleteSuite.emit(index)

    def new_suite(self, data=None):
        suite = UnitTestsSuite(f"{self.sm.project.data_path()}/unit_tests")
        if data:
            suite.from_dict(data)
        self.add_suite(suite)
        return suite

    def convert_unit_tests(self):
        converter = CheckConverter(self.sm.project.unit_tests_path(), self.sm.project,
                                   self.unit_tests_suites.copy())
        converter.convert()

    def run_unit_tests(self):
        self.run_process(lambda: self._unit_testing(self.sm.project), 'unit_testing', self.sm.project.path())

    def _unit_testing(self, project):
        self.convert_unit_tests()

        items = []
        for suite in self.unit_tests_suites:
            for el in suite.tests():
                el['status'] = UnitTest.CHANGED
                items.append(el)

        build_id = project.get('unit_build')
        if build_id is None:
            self.unitTestingError.emit("Build not found!")
            return
        build = self.get_build(build_id)

        res, errors = self.compile_build(build_id, project)
        if not res:
            self.unitTestingError.emit(errors)
            return

        i = 0
        try:
            for line in cmd_command_pipe(build.run(project, self.sm), shell=True):
                if line.count(':') >= 6:
                    lst = line.split(':')
                    items[i]['status'] = UnitTest.PASSED if lst[2] == 'P' else UnitTest.FAILED
                    items[i]['test_res'] = ':'.join(lst[6:])
                    i += 1
        except subprocess.CalledProcessError as ex:
            self.unitTestingError.emit(str(ex))
            return

    def clear_unit_tests(self):
        self.unit_tests_suites.clear()
        self.clearUnitTests.emit()

    # --------------------- running ----------------------------

    def clear_build_data(self, build_id: int):
        self.builds[build_id].clear(self.sm)

    def compile_build(self, build_id: int, project=None):
        if project is None:
            project = self.sm.project
        return self.builds[build_id].compile(project, self)

    def run_build(self, build_id, args='', in_data=None, project=None):
        if project is None:
            project = self.sm.project
        build = self.builds[build_id]
        command = build.run(project, self.sm, args)
        cwd = build.get('cwd', '.') if os.path.isabs(build.get('cwd', '.')) else \
            os.path.join(project.path(), build.get('cwd', '.'))
        if in_data is not None:
            return cmd_command(command, timeout=float(self.sm.get('time_limit', 3)), shell=True, input=in_data, cwd=cwd)
        return cmd_command(command, timeout=float(self.sm.get('time_limit', 3)), shell=True, cwd=cwd)

    def build_running_command(self, build_id, args='', project=None):
        if project is None:
            project = self.sm.project
        build = self.builds[build_id]
        command = build.run(project, self.sm, args)
        return command

    def execute_build(self, build_id, args='', in_data=None, project=None):
        res, errors = self.compile_build(build_id, project)
        if not res:
            return res, errors
        return self.run_build(build_id, args, in_data, project)

    def run_scenarios(self, builds: list[int], args='', in_data=None, project=None):
        lst = []
        for el in builds:
            lst.append(self.execute_build(el, args, in_data, project))
        return lst

    def collect_coverage(self, build_id, project=None):
        if project is None:
            project = self.sm.project
        cov = self.builds[build_id].collect_coverage(project, self.sm)
        html_page = self.builds[build_id].coverage_html(project, self.sm)
        return cov, html_page

    # --------------------- process ----------------------------

    def run_process(self, thread: types.FunctionType | types.LambdaType | QThread, group: str, name: str):
        if not isinstance(thread, QThread):
            thread = Looper(thread)
        if group not in self._background_processes:
            self._background_processes[group] = dict()

        if name in self._background_processes[group]:
            self._background_processes[group][name].terminate()
        self._background_processes[group][name] = thread
        self._background_process_count += 1
        thread.finished.connect(lambda: self._on_thread_finished(group, name, thread))
        thread.start()
        return thread

    def _on_thread_finished(self, group, name, process):
        self._background_process_count -= 1
        if self._background_processes[group][name] == process:
            self._background_processes[group].pop(name)
        if self._background_process_count == 0:
            self.allProcessFinished.emit()

    def all_finished(self):
        return self._background_process_count == 0

    def terminate_all(self):
        for item in self._background_processes.values():
            for el in list(item.values()):
                el.terminate()

    # ---------------------- ZIP ----------------------------

    def project_to_zip(self, path=None):
        if path is None:
            path = f"{self.sm.temp_dir()}/{self.sm.project.name()}.TGProject.7z"
        return self.run_process(lambda: self._project_to_zip(path), 'zip', 'store')

    def project_from_zip(self, zip_path, path, open_after_load=False):
        self.run_process(lambda: self._project_from_zip(zip_path, path, open_after_load), 'zip', 'load')

    def _project_to_zip(self, path):
        with py7zr.SevenZipFile(path, mode='w') as archive:
            archive.writeall(self.sm.project.path(), arcname='')

    def _project_from_zip(self, zip_path, path, open_after_load=False):
        path = os.path.abspath(path)
        with py7zr.SevenZipFile(zip_path, mode='r') as archive:
            archive.extractall(path)
        self.sm.add_main_project(path)
        if open_after_load:
            self.open_main_project(self.sm.all_projects[path])

    # --------------------- tabs ----------------------------

    def main_tab_command(self, tab: str, *args, **kwargs):
        self.mainTabCommand.emit(tab, args, kwargs)

    def side_tab_command(self, tab: str, *args, **kwargs):
        self.sideTabCommand.emit(tab, args, kwargs)

    def main_tab_show(self, tab: str):
        self.showMainTab.emit(tab)

    def side_tab_show(self, tab: str):
        self.showSideTab.emit(tab)

    # ------------------- cmd args --------------------------

    def parse_cmd_args(self, args):
        if args.file:
            path = args.file
            main_project, subproject = self.sm.find_main_project(
                path, temp=self.sm.get_general('open_file_temp_project'))
            lst = subproject.get('opened_files', [])
            lst.append(os.path.abspath(args[1]))
            subproject.set('opened_files', lst)
            subproject.save_settings()
            self.open_main_project(main_project, subproject)
        elif args.directory:
            path = args.directory
            self.open_main_project(*self.sm.find_main_project(path, temp=self.sm.get_general('open_dir_temp_project')))
        else:
            self.open_main_project(self.sm.get_general('project'))

        if self._loader:
            while not self._loader.isFinished():
                sleep(0.1)

        util = None
        if args.util:
            try:
                util_id = int(args.util)
            except ValueError:
                for key, item in self.utils.items():
                    if item['name'] == args.util:
                        util_id = key
                        break
                else:
                    raise KeyError("Util not found")
            util = self.utils[util_id]

        if args.build:
            try:
                build_id = int(args.build)
            except ValueError:
                for key, item in self.builds.items():
                    if item['name'] == args.build:
                        build_id = key
                        break
                else:
                    raise KeyError("Build not found")
            build = self.builds[build_id]
            command = build.run(self.sm.project, self.sm, args)
            if isinstance(util, Util):
                command = util['command'].format(app=command, args='')
            cwd = build.get('cwd', '.') if os.path.isabs(build.get('cwd', '.')) else \
                os.path.join(self.sm.project.path(), build.get('cwd', '.'))
            subprocess.run(command, cwd=cwd)

        if args.testing:
            self.start_testing(verbose=True)
            while not self._testing_looper.isFinished():
                sleep(0.1)

        self.close_program()

    def notification(self, title, message):
        self.showNotification.emit(title, message)

    def close_program(self):
        for project in list(self.sm.all_projects.values()):
            try:
                if project.get('temp', False):
                    self.sm.delete_project(project)
            except KeyError:
                pass


class Looper(QThread):
    def __init__(self, func):
        super().__init__()
        self._func = func
        self.res = None

    def run(self) -> None:
        self.res = self._func()
