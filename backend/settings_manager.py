import os

from PyQt5.QtCore import QSettings, pyqtSignal, QObject
from json import dumps, loads, JSONDecodeError
import appdirs

from backend.types.project import Project
from backend.search import Searcher


class SettingsManager(QObject):
    searching_complete = pyqtSignal()
    projectChanged = pyqtSignal()
    mainProjectChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.q_settings = QSettings('settings.ini', QSettings.IniFormat)
        # self.q_settings = QSettings()
        self.app_data_dir = appdirs.user_data_dir("TestGenerator", "SergeiKrivko").replace('\\', '/')

        self.projects = dict()
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
        self.load_programs()
        if self.get_general('search_after_start', True):
            self.start_search()

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

    def set_main_project(self, project: Project):
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
        self.set_project(project.children()[project.get('selected_project')])
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

    def temp_dir(self):
        return f"{self.app_data_dir}/temp_files"

    def store_projects_list(self):
        self.set_general('projects', dumps(list(self.projects.keys())))
        self.set_general('project', None if self.main_project is None else self.main_project.path())

    def store(self):
        self.store_projects_list()
        for item in self.projects.values():
            item.save_settings()

    def add_project(self, name, path, temp=False):
        if name in self.projects:
            print(f"Project \"{name}\" already exists!")
            return
        project = Project(name, path, temp=temp, data_path=f"{self.app_data_dir}/projects")
        self.projects[name] = project
        project.create_gitignore()

    def delete_project(self, name=None, main_dir=False):
        if name is None:
            name = self.project
        if name not in self.projects:
            return
        self.projects[name].delete(main_dir)
        self.projects.pop(name)
        if name == self.project:
            self.project = ''
            self.current_project = None
        self.store_projects_list()

    def rename_project(self, new_name: str, name=None):
        if name is None:
            name = self.project
        project = self.projects[name]
        project.rename(new_name)
        self.projects.pop(name)
        self.projects[new_name] = project
        self.project = new_name
        self.store_projects_list()

    def load_programs(self):
        try:
            with open(f'{self.app_data_dir}/programs.json', encoding='utf-8') as f:
                self.programs = loads(f.read())
                if not isinstance(self.programs, dict):
                    raise TypeError
        except JSONDecodeError:
            self.start_search()
        except TypeError:
            self.start_search()
        except FileNotFoundError:
            self.start_search()

    def start_search(self):
        if self.searcher and not self.searcher.isFinished():
            return
        self.searcher = Searcher()
        self.searcher.finished.connect(self.search_finish)
        self.searcher.start()

    def search_finish(self):
        self.programs = self.searcher.res
        self.searching_complete.emit()
        with open(f'{self.app_data_dir}/programs.json', 'w', encoding='utf-8') as f:
            f.write(dumps(self.programs))
