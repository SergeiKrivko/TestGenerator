import os.path
import random
from time import sleep
from uuid import UUID

import py7zr
from PyQt6.QtCore import QObject, pyqtSignal

from src.backend.managers._processes import CustomThread
from src.backend.backend_types.func_test import FuncTest
from src.backend.backend_types.project import Project
from src.backend.backend_types.unit_test import UnitTest
from src.backend.backend_types.unit_tests_suite import UnitTestsSuite
from src.backend.backend_types.util import Util
from src.backend.check_converter import CheckConverter
from src.backend.commands import *
from src.backend.func_testing import TestingLooper
from src.backend.load_task import Loader
from src.backend.managers._builds import BuildsManager
from src.backend.managers._func_tests import FuncTestsManager
from src.backend.managers._processes import ProcessManager
from src.backend.settings_manager import SettingsManager


class BackendManager(QObject):
    startChangingProject = pyqtSignal()
    finishChangingProject = pyqtSignal()
    loadingStart = pyqtSignal(Project)
    updateProgress = pyqtSignal(int, int)

    addUnitTestSuite = pyqtSignal(UnitTestsSuite)
    deleteSuite = pyqtSignal(int)
    clearUnitTests = pyqtSignal()
    unitTestingError = pyqtSignal(str)

    startTesting = pyqtSignal(list)
    testingError = pyqtSignal(str)
    testingUtilError = pyqtSignal(str)
    endTesting = pyqtSignal(object, object)

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
        self._sm = SettingsManager()

        self.func_tests = FuncTestsManager(self._sm, self)
        self.builds = BuildsManager(self._sm, self)
        self.processes = ProcessManager(self._sm, self)
        self.utils = dict()
        self.unit_tests_suites: list[UnitTestsSuite] = []

        self.func_test_completed = 0

        self._testing_looper = None
        self._loader = None

        self.changing_project = False

    # ------------------------- SETTINGS ------------------------------

    def open_project(self, project: Project | str):
        if isinstance(project, str):
            if project not in self._sm.projects:
                return
            project = self._sm.projects[project]
        if project == self._sm.project:
            return
        self.changing_project = True
        self.startChangingProject.emit()
        self.func_tests.run_macros_converter()
        self._run_loader(project)

    def close_project(self):
        self.changing_project = True
        self.startChangingProject.emit()
        self._run_loader(None)

    def open_main_project(self, project: Project, subproject: Project = None):
        if isinstance(project, str):
            project = os.path.abspath(project)
            if project not in self._sm.projects:
                return
            project = self._sm.projects[project]
        if project == self._sm.project:
            return
        self.changing_project = True
        self.startChangingProject.emit()
        self.func_tests.run_macros_converter()
        if subproject:
            self._run_loader(subproject, main=project)
        else:
            self._run_loader(project, main=True)

    def _run_loader(self, project: Project | None, main=False):
        self._loader = Loader(self, project, main)
        self._loader.finished.connect(self._on_loader_finished)
        self._loader.updateProgress.connect(self.updateProgress.emit)
        self._loader.loadingStart.connect(self.loadingStart.emit)
        self.processes.run(self._loader, 'load', None if project is None else project.path())

    def _on_loader_finished(self):
        if self.changing_project:
            self.changing_project = False
            self.finishChangingProject.emit()

    # -------------------------- TESTING --------------------------------

    def start_testing(self, verbose=False):
        self.func_tests.run_macros_converter()
        self.startTesting.emit(self.func_tests.all_tests)
        self.func_test_completed = 0
        self._testing_looper = TestingLooper(self._sm, self._sm.project, self,
                                             self.func_tests.all_tests, verbose=verbose)
        self._testing_looper.testStatusChanged.connect(self.func_test_set_status)
        self._testing_looper.finished.connect(lambda: self.endTesting.emit(self._testing_looper.coverage,
                                                                           self._testing_looper.coverage_html))
        self._testing_looper.compileFailed.connect(self.testingError.emit)
        self._testing_looper.utilFailed.connect(self.testingUtilError.emit)
        self.processes.run(self._testing_looper, 'testing', 'main')
        return self._testing_looper

    def stop_testing(self):
        if isinstance(self._testing_looper, TestingLooper) and self._testing_looper.isRunning():
            self._testing_looper.terminate()

    def func_test_set_status(self, test: FuncTest, status):
        if status in [FuncTest.PASSED, FuncTest.FAILED, FuncTest.TIMEOUT, FuncTest.TERMINATED]:
            self.func_test_completed += 1
        test.set_status(status)
        self.func_tests.onStatusChanged.emit(test)

    # --------------------------- BUILDS --------------------------------

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
        self._sm.set_data('unit_tests', ';'.join(str(test.id) for test in self.unit_tests_suites))
        self.addUnitTestSuite.emit(suite)

    def delete_suite(self, index):
        suite = self.unit_tests_suites[index]
        suite.delete()
        self.unit_tests_suites.pop(index)
        self._sm.set_data('unit_tests', ';'.join(str(test.id) for test in self.unit_tests_suites))
        self.deleteSuite.emit(index)

    def new_suite(self, data=None):
        suite = UnitTestsSuite(f"{self._sm.project.data_path()}/unit_tests")
        if data:
            suite.from_dict(data)
        self.add_suite(suite)
        return suite

    def convert_unit_tests(self):
        converter = CheckConverter(self._sm.project.unit_tests_path(), self._sm.project,
                                   self.unit_tests_suites.copy())
        converter.convert()

    def run_unit_tests(self):
        self.processes.run(lambda: self._unit_testing(self._sm.project), 'unit_testing', self._sm.project.path())

    def _unit_testing(self, project):
        self.convert_unit_tests()

        items = []
        for suite in self.unit_tests_suites:
            for el in suite.tests():
                el['status'] = UnitTest.CHANGED
                items.append(el)

        build_id = UUID(project.get('unit_build'))
        if build_id is None:
            self.unitTestingError.emit("Build not found!")
            return
        build = self.builds.get(build_id)

        res, errors = self.compile_build(build_id, project)
        if not res:
            self.unitTestingError.emit(errors)
            return

        i = 0
        try:
            for line in cmd_command_pipe(build.run(project, self._sm), shell=True):
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

    def clear_build_data(self, build_id: UUID):
        self.builds.get(build_id).clear(self._sm)

    def compile_build(self, build_id: UUID, project=None):
        if project is None:
            project = self._sm.project
        return self.builds.get(build_id).compile(project, self)

    def run_build_preproc(self, build_id: UUID, project=None):
        if project is None:
            project = self._sm.project
        return self.builds.get(build_id).run_preproc(project, self)

    def run_build_postproc(self, build_id: UUID, project=None):
        if project is None:
            project = self._sm.project
        return self.builds.get(build_id).run_postproc(project, self)

    def run_build(self, build_id, args='', in_data=None, project=None):
        if project is None:
            project = self._sm.project
        build = self.builds.get(build_id)
        command = build.run(project, self._sm, args)
        cwd = build.get('cwd', '.') if os.path.isabs(build.get('cwd', '.')) else \
            os.path.join(project.path(), build.get('cwd', '.'))
        if in_data is not None:
            return cmd_command(command, timeout=float(self._sm.get('time_limit', 3)), shell=True, input=in_data, cwd=cwd)
        return cmd_command(command, timeout=float(self._sm.get('time_limit', 3)), shell=True, cwd=cwd)

    def build_running_command(self, build_id, args='', project=None):
        if project is None:
            project = self._sm.project
        build = self.builds.get(build_id)
        command = build.run(project, self._sm, args)
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
            project = self._sm.project
        build = self.builds.get(build_id)
        cov = build.collect_coverage(project, self._sm)
        html_page = build.coverage_html(project, self._sm)
        build.clear_coverage(self._sm)
        return cov, html_page

    # ---------------------- ZIP ----------------------------

    def project_to_zip(self, path=None):
        if path is None:
            path = f"{self._sm.temp_dir()}/{self._sm.project.name()}.TGProject.7z"
        return self.processes.run(lambda: self._project_to_zip(path), 'zip', 'store')

    def project_from_zip(self, zip_path, path, open_after_load=False):
        self.processes.run(lambda: self._project_from_zip(zip_path, path, open_after_load), 'zip', 'load')

    def _project_to_zip(self, path):
        with py7zr.SevenZipFile(path, mode='w') as archive:
            archive.writeall(self._sm.project.path(), arcname='')

    def _project_from_zip(self, zip_path, path, open_after_load=False):
        path = os.path.abspath(path)
        with py7zr.SevenZipFile(zip_path, mode='r') as archive:
            archive.extractall(path)
        self._sm.add_main_project(path)
        if open_after_load:
            self.open_main_project(self._sm.all_projects[path])

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
            main_project, subproject = self._sm.find_main_project(
                path, temp=self._sm.get_general('open_file_temp_project'))
            lst = subproject.get('opened_files', [])
            lst.append(os.path.abspath(args[1]))
            subproject.set('opened_files', lst)
            subproject.save_settings()
            self.open_main_project(main_project, subproject)
        elif args.directory:
            path = args.directory
            self.open_main_project(*self._sm.find_main_project(path, temp=self._sm.get_general('open_dir_temp_project')))
        else:
            self.open_main_project(self._sm.get_general('project'))

        if self._loader:
            while not self._loader.isFinished():
                sleep(0.1)

        if not args.build and not args.testing:
            return

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
            command = build.run(self._sm.project, self._sm, args)
            if isinstance(util, Util):
                command = util['command'].format(app=command, args='')
            cwd = build.get('cwd', '.') if os.path.isabs(build.get('cwd', '.')) else \
                os.path.join(self._sm.project.path(), build.get('cwd', '.'))
            subprocess.run(command, cwd=cwd)

        if args.testing:
            self.start_testing(verbose=True)
            while not self._testing_looper.isFinished():
                sleep(0.1)

        self.close_program()

    def notification(self, title, message):
        self.showNotification.emit(title, message)

    def close_program(self):
        for project in list(self._sm.all_projects.values()):
            try:
                if project.get('temp', False):
                    self._sm.delete_project(project)
            except KeyError:
                pass
