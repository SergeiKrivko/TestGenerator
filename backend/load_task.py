import os
import shutil
from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal

from backend.commands import get_sorted_jsons
from backend.backend_types.build import Build
from backend.backend_types.func_test import FuncTest
from backend.backend_types.project import Project
from backend.backend_types.unit_tests_module import UnitTestsModule
from backend.backend_types.util import Util
from language.languages import languages
from language.utils import get_files


class Loader(QThread):
    updateProgress = pyqtSignal(int, int)
    loadingStart = pyqtSignal(Project)

    def __init__(self, manager, project: Project, main=False):
        super().__init__()
        if not isinstance(project, Project) and project is not None:
            raise Exception
        self._manager = manager
        self._sm = manager.sm
        self._project = project
        self._main_project = main

        if self._sm.project:
            self._old_data_path = self._sm.project.data_path()
        else:
            self._old_data_path = None
        self._new_data_path = ""
        self.progress = 0

    def store_task(self):
        self.store_func_tests()
        self.next_step()
        self.store_builds()
        self.next_step()
        self.store_unit_tests()
        self.next_step()

    def store_func_tests(self):
        pass
        # if os.path.isdir(data_path := f"{self._old_data_path}/func_tests"):
        #     pass
        #     shutil.rmtree(data_path)
        # for pos in ['pos', 'neg']:
        #     for i, el in enumerate(self._manager.func_tests[pos]):
        #         path = f"{data_path}/{pos}/{i}.json"
        #         el.set_path(path)
        #         el.store()

    def store_unit_tests(self):
        self._manager.convert_unit_tests()
        path = f"{self._old_data_path}/unit_tests"
        for module in self._manager.unit_tests_modules:
            module.store(path)

    def store_builds(self):
        if os.path.isdir(data_path := f"{self._old_data_path}/scenarios"):
            shutil.rmtree(data_path)
        for key, item in self._manager.builds.items():
            path = f"{data_path}/{key}.json"
            item.store(path)

    def store_utils(self):
        if os.path.isdir(data_path := f"{self._sm.app_data_dir}/utils"):
            shutil.rmtree(data_path)
        for key, item in self._manager.utils.items():
            path = f"{data_path}/{key}.json"
            item.store(path)

    def clear_all(self):
        self._manager.clear_func_tests()
        self._manager.clear_builds()
        self._manager.clear_unit_tests()
        self.next_step()

    def load_task(self):
        self.load_func_tests()
        self.next_step()
        self.load_builds()
        self.next_step()
        self.load_unit_tests()
        self.next_step()

    def load_func_tests(self):
        for test_type in ['pos', 'neg']:
            if isinstance(lst := self._sm.project.get(f'{test_type}_func_tests'), str):
                for test_id in lst.split(';'):
                    if test_id:
                        self._manager.add_func_test(FuncTest(
                            f"{self._new_data_path}/func_tests/{test_type}", test_id, test_type=test_type))
            else:
                for i, el in enumerate(get_sorted_jsons(f"{self._new_data_path}/func_tests/{test_type}")):
                    self._manager.add_func_test(FuncTest.from_file(
                        f"{self._new_data_path}/func_tests/{test_type}/{el}", test_type))

    def load_unit_tests(self):
        modules = dict()
        path = f"{self._new_data_path}/unit_tests"
        if os.path.isdir(path):
            for el in os.listdir(path):
                if os.path.isdir(os.path.join(path, el)):
                    self._manager.add_module(module := UnitTestsModule(el))
                    modules[el] = module
                    module.load(f"{path}/{el}")

        try:
            for el in get_files(self._sm.project.path(), languages[self._sm.project.get('language', 'C')].get(
                    'files')[0]):
                el = os.path.basename(el)
                if el not in modules:
                    module = UnitTestsModule(el)
                    modules[el] = module
                    self._manager.add_module(module)
        except KeyError:
            pass

    def load_builds(self):
        path = f"{self._new_data_path}/scenarios"
        if not os.path.isdir(path):
            return
        for el in get_sorted_jsons(path):
            build_path = os.path.join(path, el)
            self._manager.add_build(Build(int(el.rstrip('.json')), build_path))

    def load_utils(self):
        path = f"{self._sm.app_data_dir}/utils"
        if not os.path.isdir(path):
            return
        for el in get_sorted_jsons(path):
            util_path = os.path.join(path, el)
            self._manager.add_util(Util(int(el.rstrip('.json')), util_path))

    def next_step(self):
        self.progress += 1
        self.updateProgress.emit(self.progress, 7)

    def run(self) -> None:
        self.progress = -1
        self.next_step()

        if self._old_data_path:
            self.store_task()
        else:
            self.load_utils()

        self.clear_all()

        if self._project:
            self.loadingStart.emit(self._project)
            if isinstance(self._main_project, Project):
                self._sm.set_main_project(self._main_project, self._project)
            elif self._main_project:
                self._sm.set_main_project(self._project)
            else:
                self._sm.set_project(self._project)
            self.next_step()

            if self._sm.project and self._sm.project.path() in self._sm.all_projects:
                self._new_data_path = self._sm.project.data_path()
                self.load_task()

        elif self._sm.project:
            self._sm.project.save_settings()
            self.store_utils()
