import os

from PyQt6.QtCore import QSettings, pyqtSignal, QObject
from json import dumps, loads, JSONDecodeError
import appdirs

from backend.backend_types.program import PROGRAMS, ProgramInstance
from backend.backend_types.project import Project
from backend.search import Searcher


class SettingsManager(QObject):
    searching_complete = pyqtSignal()
    projectChanged = pyqtSignal()
    mainProjectChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        # self.q_settings = QSettings('settings.ini', QSettings.IniFormat)
        self.q_settings = QSettings()
        self.app_data_dir = appdirs.user_data_dir("TestGenerator", "SergeiKrivko").replace('\\', '/')

        self.projects: dict[str: Project] = dict()
        self.all_projects = dict()
        self.project: Project | None = None
        self.main_project: Project | None = None
        self._load_projects()

        line_sep = self.get_general('line_sep')
        if line_sep not in [0, 1, 2]:
            line_sep = 0
        self.line_sep = ['\n', '\r\n', '\r'][line_sep]

        self.programs = dict()
        self.searcher = None
        self.start_search(self.get_general('search_after_start', True), wait=True)

    def _load_projects(self):
        self.projects = dict()
        try:
            s = self.get_general('projects')
            projects = loads(s)
            if not isinstance(projects, list):
                raise TypeError
            for item in projects:
                try:
                    self.projects[os.path.abspath(item)] = Project(item, self)
                except FileNotFoundError:
                    pass
        except JSONDecodeError:
            pass
        except TypeError:
            pass

    def get_general(self, key, default=None):
        return self.q_settings.value(key, default)

    def remove_general(self, key):
        self.q_settings.remove(key)

    def remove(self, key):
        if self.project is not None:
            self.project.pop(key)

    def set_main_project(self, project: Project, subproject: Project = None):
        if project == self.main_project:
            return

        if project is None or project.path() not in self.projects:
            self.project = None
            self.main_project = None
            self.store_projects_list()
            return

        if isinstance(self.project, Project):
            self.project.save_settings()
        self.main_project = project
        project.load_projects()
        self.mainProjectChanged.emit()
        if subproject:
            self.set_project(subproject)
        elif project.has_item('selected_project') and project.get('selected_project') in self.all_projects:
            self.set_project(self.all_projects[project.get('selected_project')])
        else:
            self.set_project(project)
        self.store_projects_list()

    def set_project(self, project: Project):
        if project == self.project:
            return

        if self.main_project is None or project is None or project.path() not in self.all_projects:
            self.project = None
            self.main_project = None
            self.store_projects_list()
            return

        if isinstance(self.project, Project):
            self.project.save_settings()

        self.main_project['selected_project'] = project.path()
        self.project = project
        self.project.load_settings()
        self.projectChanged.emit()

    def set_general(self, key, value):
        if key == 'line_sep':
            self.line_sep = ['\n', '\r\n', '\r'][value]
        self.q_settings.setValue(key, value)

    def get(self, key, default=None):
        if self.project is not None:
            return self.project.get(key, default)
        return default

    def set(self, key, value):
        if self.project is not None:
            self.project.set(key, value)

    def get_data(self, key, default=None):
        if self.project is not None:
            return self.project.get_data(key, default)
        return default

    def set_data(self, key, value):
        if self.project is not None:
            self.project.set_data(key, value)

    def temp_dir(self):
        return f"{self.app_data_dir}/temp_files"

    def store_projects_list(self):
        self.set_general('projects', dumps(list(self.projects.keys())))
        if self.main_project is not None:
            self.set_general('project', self.main_project.path())

    def store(self):
        self.store_projects_list()
        for item in self.projects.values():
            item.save_settings()

    def find_project(self, path):
        while True:
            path, name = os.path.split(path)
            if not name:
                break
            if os.path.isdir(os.path.join(path, Project.TEST_GENERATOR_DIR)):
                if path in self.all_projects:
                    return self.all_projects[path]
                else:
                    project = Project(path, self, load=True)
                    return project

    def find_main_project(self, path, temp=False):
        first_path = path
        first_project = None
        while True:
            if os.path.isdir(os.path.join(path, Project.TEST_GENERATOR_DIR)):
                if first_project is None:
                    first_project = path
                if path in self.projects:
                    main_project = self.projects[path]
                    main_project.load_projects()
                    first_project = main_project if first_project not in self.all_projects else \
                        self.all_projects[first_project]
                    return main_project, first_project

            path, name = os.path.split(path)
            if not name:
                break

        if first_project is None:
            first_project = first_path

        main_project = self.add_main_project(first_project, temp=temp)
        return main_project, main_project

    def add_main_project(self, path, temp=False):
        path = os.path.abspath(path)
        if path in self.projects:
            return self.projects[path]
        if path in self.all_projects:
            self.projects[path] = self.all_projects[path]
            return self.all_projects[path]
        else:
            project = Project(path, self, makedirs=True, load=True)
            project.set('default_struct', True)
            project.set('default_compiler_settings', True)
            project.set('default_testing_settings', True)
            if temp:
                project.set('temp', True)
            self.projects[path] = project
            return project

    def add_project(self, path):
        path = os.path.abspath(path)
        if path in self.all_projects:
            return self.all_projects[path]
        project = Project(path, self, makedirs=True)
        project.set('default_struct', True)
        project.set('default_compiler_settings', True)
        project.set('default_testing_settings', True)
        return project

    def delete_main_project(self, project=None, directory=False, data=False):
        if project is None:
            project = self.main_project

        if project.path() not in self.projects:
            return

        if data or directory:
            project.delete(directory)
        self.projects.pop(project.path())
        if project == self.main_project:
            self.main_project = None
            self.project = None

    def delete_project(self, project: Project, directory=False):
        project.delete(directory)
        self.all_projects.pop(project.path())
        if project.path() in self.projects:
            self.projects.pop(project.path())
        if project == self.project:
            self.project = None
            self.set_project(self.main_project)

    def rename_project(self, new_name: str, name=None):
        if name is None:
            name = self.project
        project = self.projects[name]
        project.rename(new_name)
        self.projects.pop(name)
        self.projects[new_name] = project
        self.project = new_name
        self.store_projects_list()

    def start_search(self, forced=False, wait=False):
        if self.searcher and not self.searcher.isFinished():
            return
        self.searcher = Searcher(self, forced, wait)
        self.searcher.finished.connect(self.search_finish)
        self.searcher.start()

    def search_finish(self):
        self.programs = self.searcher.res
        self.searching_complete.emit()
        self.store_programs()

    def store_programs(self):
        with open(f'{self.app_data_dir}/programs.json', 'w', encoding='utf-8') as f:
            f.write(dumps({key: list(map(ProgramInstance.to_json, item.existing())) for key, item in PROGRAMS.items()}))
