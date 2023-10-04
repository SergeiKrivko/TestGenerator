from typing import Literal

from PyQt5.QtCore import QObject, pyqtSignal, QThread

from backend.func_testing import TestingLooper
from backend.load_task import Loader
from backend.macros_converter import MacrosConverter
from backend.types.build import Build
from backend.types.project import Project
from backend.types.unit_tests_module import UnitTestsModule
from side_tabs.builds.commands_list import CommandsList
from language.languages import languages
from backend.settings_manager import SettingsManager
from backend.types.func_test import FuncTest
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

    addUnitTestModule = pyqtSignal(UnitTestsModule)
    clearUnitTests = pyqtSignal()

    startTesting = pyqtSignal(list)
    testingError = pyqtSignal(str)
    testingUtilError = pyqtSignal(str)
    endTesting = pyqtSignal()

    addBuild = pyqtSignal(Build)
    deleteBuild = pyqtSignal(Build)
    renameBuild = pyqtSignal(Build, str)
    clearBuilds = pyqtSignal()

    showMainTab = pyqtSignal(str)
    showSideTab = pyqtSignal(str)
    mainTabCommand = pyqtSignal(str, tuple, dict)
    sideTabCommand = pyqtSignal(str, tuple, dict)

    def __init__(self):
        super().__init__()
        self.sm = SettingsManager()

        self.func_tests = {'pos': [], 'neg': []}
        self.builds = dict()
        self.unit_tests_modules: list[UnitTestsModule] = []

        self.func_test_completed = 0

        self._testing_looper = None
        self._loader = None

        self._background_processes: dict[str: dict[str: QThread]] = dict()
        self._background_process_count = 0

        self.changing_project = False

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

    def open_main_project(self, project: Project):
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
        self._run_loader(project, main=True)

    def _run_loader(self, project: Project, main=False):
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

    def add_func_test(self, test: FuncTest, index=None):
        if index is None:
            index = len(self.func_tests[test.type()])
        self.func_tests[test.type()].insert(index, test)
        self.addFuncTest.emit(test, index)

    def delete_func_test(self, type: Literal['pos', 'neg'], index: int):
        test = self.func_tests[type][index]
        self.func_tests[type].pop(index)
        self.deleteFuncTest.emit(test, index)

    def clear_func_tests(self):
        self.func_tests['pos'].clear()
        self.func_tests['neg'].clear()
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
        match direction:
            case 'up':
                if index <= 0:
                    return
                test = self.get_func_test(type, index)
                self.delete_func_test(type, index)
                index -= 1
                self.add_func_test(test, index)
            case 'down':
                if index >= len(self.func_tests[type]) - 1:
                    return
                test = self.get_func_test(type, index)
                self.delete_func_test(type, index)
                index += 1
                self.add_func_test(test, index)

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

    # -------------------------- TESTING --------------------------------

    def start_testing(self):
        self.run_macros_converter()
        self.startTesting.emit(self.func_tests['pos'] + self.func_tests['neg'])
        self.func_test_completed = 0
        self._testing_looper = TestingLooper(self.sm, self.sm.project, self,
                                             self.func_tests['pos'] + self.func_tests['neg'])
        self._testing_looper.testStatusChanged.connect(self.func_test_set_status)
        self._testing_looper.finished.connect(self.endTesting.emit)
        self._testing_looper.compileFailed.connect(self.testingError.emit)
        self._testing_looper.utilFailed.connect(self.testingUtilError.emit)
        self.run_process(self._testing_looper, 'testing', 'main')

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
        self.builds[build.name] = build
        self.addBuild.emit(build)

    def delete_build(self, name: str):
        build = self.builds[name]
        self.builds.pop(name)
        self.deleteBuild.emit(build)

    def clear_builds(self):
        self.builds.clear()
        self.clearBuilds.emit()

    def rename_build(self, name: str, new_name: str):
        if new_name in self.builds:
            return
        build = self.builds[name]
        build.set_name(new_name)
        self.builds.pop(name)
        self.builds[new_name] = build
        self.renameBuild.emit(build, new_name)

    def get_build(self, name: str):
        return self.builds[name]

    # ------------------- UNIT TESTING -------------------------

    def add_module(self, module: UnitTestsModule):
        self.unit_tests_modules.append(module)
        self.addUnitTestModule.emit(module)

    def convert_unit_tests(self):
        pass

    def clear_unit_tests(self):
        self.unit_tests_modules.clear()
        self.clearUnitTests.emit()

    # --------------------- running ----------------------------

    def compile(self, build: Build | str, project: Project = None, coverage=False):
        if project is None:
            project = self.sm.project
        if isinstance(build, str):
            try:
                build = self.get_build(build)
            except KeyError:
                return False, "Invalid build data"
        return languages[self.sm.get('language', 'C')].get(
            'compile', lambda *args: (False, 'Can\'t compile this file'))(project, build, self.sm, coverage)

    def run_main_code(self, args='', in_data=None, project=None, coverage=False):
        if project is None:
            project = self.sm.project
        if in_data is not None:
            return cmd_command(languages[self.sm.get('language', 'C')].get('run')(
                project.path(), project, self.sm, args, coverage), timeout=float(self.sm.get('time_limit', 3)),
                shell=True, input=in_data, cwd=project.path())
        return cmd_command(languages[self.sm.get('language', 'C')].get('run')(
            project.path(), project, self.sm, args, coverage), timeout=float(self.sm.get('time_limit', 3)),
            shell=True, cwd=project.path())

    def collect_coverage(self):
        res = languages[self.sm.get('language', 'C')].get('coverage', lambda *args: 0)(self.path, self.sm, self)
        return res

    def run_scenarios(self, data: list | dict, cwd=None):
        if isinstance(data, dict):
            data = [data]
        if cwd is None:
            cwd = self.sm.lab_path()
        res = []
        for scenario in data:
            match scenario['type']:
                case CommandsList.TYPE_CMD:
                    res.append(self.cmd_command(scenario['data'], shell=True, cwd=cwd))
                case CommandsList.TYPE_BUILD:
                    res.append(self.compile(scenario['data'], cwd))
        return res

    # --------------------- process ----------------------------

    def run_process(self, thread, group: str, name: str):
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
            for el in item.values():
                el.terminate()

    # --------------------- tabs ----------------------------

    def main_tab_command(self, tab: str, *args, **kwargs):
        self.mainTabCommand.emit(tab, args, kwargs)

    def side_tab_command(self, tab: str, *args, **kwargs):
        self.sideTabCommand.emit(tab, args, kwargs)

    def main_tab_show(self, tab: str):
        self.showMainTab.emit(tab)

    def side_tab_show(self, tab: str):
        self.showSideTab.emit(tab)


class Looper(QThread):
    def __init__(self, func):
        super().__init__()
        self._func = func
        self.res = None

    def run(self) -> None:
        self.res = self._func()
