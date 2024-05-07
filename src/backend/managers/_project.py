import json
import os
import shutil
from uuid import UUID

from PyQt6.QtCore import QObject, pyqtSignal
from py7zr import py7zr

from src.backend.backend_types import FuncTest
from src.backend.backend_types.project import Project
from src.backend.backend_types.unit_tests_suite import UnitTestsSuite
from src.backend.backend_types.util import Util
from src.backend.commands import get_sorted_jsons, get_jsons
from src.backend.settings_manager import SettingsManager


class ProjectManager(QObject):
    startClosing = pyqtSignal(object)
    finishClosing = pyqtSignal(object)
    startOpening = pyqtSignal(Project)
    finishOpening = pyqtSignal(Project)

    updateProgress = pyqtSignal(int, int)
    recentChanged = pyqtSignal()

    def __init__(self, bm):
        super().__init__()
        self._bm = bm
        self._sm: SettingsManager = bm.sm

        self.__utils_loaded = False

        self.__recent_projects: list[str] = []
        self.__all_projects = dict()
        self.__current: Project | None = None

        self._load_projects()

    @property
    def current(self):
        return self.__current

    @property
    def all(self):
        return self.__all_projects

    @property
    def recent(self):
        for proj in self.__recent_projects:
            yield self.__all_projects[proj]

    def _get_project(self, path: str) -> Project | None:
        return self.__all_projects.get(os.path.abspath(path), None)

    async def open(self, project: Project | str):
        if isinstance(project, str):
            project = self._get_project(project)
            if project is None:
                return None

        if project != self._sm.project:
            await self.close()
            await self._open(project)
        return project

    async def close(self):
        project = self.__current
        self.startClosing.emit(project)
        await self._bm.processes.run_async(self._close_project, 'projects', 'close')

        self.__current = None
        self._sm.project = None

        self.finishClosing.emit(project)

    def _close_project(self):
        self._progress(0)
        if not self._sm.project:
            return
        self._store_builds()
        self._store_utils()

        self._bm.func_tests.clear()
        self._bm.builds.clear()
        # self._bm.unit_tests.clear()
        self._progress(1)

    def _store_builds(self):
        for key, item in self._bm.builds.all.items():
            item.store()

    def _store_utils(self):
        if os.path.isdir(data_path := f"{self._sm.app_data_dir}/utils"):
            shutil.rmtree(data_path)
        for key, item in self._bm.utils.all.items():
            path = f"{data_path}/{key}.json"
            item.store(path)

    async def _open(self, project: Project):
        self._progress(1)
        self.__current = project
        self._sm.project = project

        if self.__current.path() in self.__recent_projects:
            self.__recent_projects.remove(self.__current.path())
        self.__recent_projects.insert(0, self.__current.path())
        self._store_projects_list()

        if not self.__utils_loaded:
            await self._bm.processes.run_async(self._load_utils, 'projects', 'utils')

        self._progress(2)

        self.startOpening.emit(self.__current)
        await self._bm.processes.run_async(lambda: self._open_project(project), 'projects', 'opening')
        self.finishOpening.emit(self.__current)

    def _open_project(self, project: Project):
        self._load_func_tests(project.data_path())
        self._progress(3)
        self._load_builds(project.data_path())
        self._progress(4)
        self._load_unit_tests(project.data_path())
        self._progress(5)

    def _load_func_tests(self, path):
        for test_type in FuncTest.Type:
            if isinstance(lst := self._sm.project.get_data(f'{test_type.value}_func_tests'), str):
                for test_id in lst.split(';'):
                    if test_id:
                        self._bm.func_tests.add(FuncTest(
                            f"{path}/func_tests/{test_type.value}", test_type, test_id))
            else:
                for i, el in enumerate(get_jsons(f"{path}/func_tests/{test_type.value}")):
                    self._bm.func_tests.add(FuncTest.from_file(
                        f"{path}/func_tests/{test_type.value}/{el}", test_type))

    def _load_unit_tests(self, path):
        if isinstance(lst := self._sm.project.get_data(f'unit_tests'), str):
            for suite_id in lst.split(';'):
                if suite_id:
                    self._bm.unit_tests.add_suite(UnitTestsSuite(f"{path}/unit_tests", suite_id))

    def _load_builds(self, path):
        path = f"{path}/scenarios"
        if not os.path.isdir(path):
            return
        self._bm.builds.load([os.path.join(path, el) for el in os.listdir(path)])

    def _load_utils(self):
        path = f"{self._sm.app_data_dir}/utils"
        if not os.path.isdir(path):
            return
        for el in get_sorted_jsons(path):
            util_path = os.path.join(path, el)
            self._bm.utils.add(Util(UUID(el[:-5]), util_path))

    def _progress(self, value):
        self.updateProgress.emit(value, 6)

    def _load_projects(self):
        self.__recent_projects.clear()
        try:
            s = self._sm.get_general('recent_projects')
            projects = json.loads(s)
            if not isinstance(projects, list):
                raise TypeError
            for item in projects:
                if not os.path.isdir(item):
                    continue
                try:
                    self.__all_projects[os.path.abspath(item)] = Project(item, self)
                except FileNotFoundError:
                    pass
                else:
                    self.__recent_projects.append(os.path.abspath(item))
        except json.JSONDecodeError:
            pass
        except TypeError:
            pass
        self.recentChanged.emit()

    def _store_projects_list(self):
        self._sm.set_general('project', self.__current.path())
        self._sm.set_general('recent_projects', json.dumps(self.__recent_projects))
        self.recentChanged.emit()

    async def new(self, path, open_proj=True):
        path = os.path.abspath(path)
        if path in self.__all_projects:
            res = self.__all_projects[path]
        else:
            project = Project(path, self, makedirs=True)
            project.set('default_struct', True)
            project.set('default_compiler_settings', True)
            project.set('default_testing_settings', True)
            res = project
            self.__all_projects[res.path()] = res

        if open_proj:
            await self.open(res)
        else:
            self.__recent_projects.append(res)
            self._store_projects_list()
        return res

    async def find(self, path, temp=False):
        path = os.path.abspath(path)
        while True:
            if os.path.isdir(os.path.join(path, Project.TEST_GENERATOR_DIR)):
                await self.open(path)
                return

            path, name = os.path.split(path)
            if not name:
                break

        await self._add(path, temp=temp)

    async def forget(self, project: Project = None):
        if project is None:
            project = self.__current
        if project.path() not in self.__all_projects:
            return None

        if self.__current.path() == project.path():
            await self.close()
        if project in self.__recent_projects:
            self.__recent_projects.remove(project.path())
            self._store_projects_list()
        return project

    async def remove_data(self, project: Project = None):
        project = await self.forget(project)
        if not project:
            return None
        project.delete(dir=False)

    async def remove_folder(self, project: Project = None):
        project = await self.forget(project)
        if not project:
            return None
        project.delete(dir=True)

    async def project_to_zip(self, path=None):
        if path is None:
            path = f"{self._sm.temp_dir()}/{self._sm.project.name()}.TGProject.7z"
        await self._bm.processes.run_async(lambda: self._project_to_zip(path), 'zip', 'store')

    async def project_from_zip(self, zip_path, path, open_after_load=True):
        path = await self._bm.processes.run_async(lambda: self._project_from_zip(zip_path, path), 'zip', 'load')
        await self._add(path, open=open_after_load)

    def _project_to_zip(self, path):
        with py7zr.SevenZipFile(path, mode='w') as archive:
            archive.writeall(self._sm.project.path(), arcname='')

    def _project_from_zip(self, zip_path, path):
        path = os.path.abspath(path)
        with py7zr.SevenZipFile(zip_path, mode='r') as archive:
            archive.extractall(path)
        return path
