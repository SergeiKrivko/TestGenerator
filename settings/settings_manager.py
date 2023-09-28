import os
import shutil

from PyQt5.QtCore import QSettings, pyqtSignal, QObject
from json import dumps, loads, JSONDecodeError
import appdirs

from settings.search import Searcher


class SettingsManager(QObject):
    searching_complete = pyqtSignal()
    project_changed = pyqtSignal()
    startChangeTask = pyqtSignal()
    finishChangeTask = pyqtSignal()

    def __init__(self):
        super().__init__()
        # self.q_settings = QSettings('settings.ini', QSettings.IniFormat)
        self.q_settings = QSettings()
        self.app_data_dir = appdirs.user_data_dir("TestGenerator", "SergeiKrivko").replace('\\', '/')

        self.project = ''
        try:
            s = self.get_general('projects')
            self.projects = loads(s)
            if not isinstance(self.projects, dict):
                raise TypeError
            for key, item in self.projects.items():
                self.projects[key] = Project(key, item)
        except JSONDecodeError:
            self.projects = dict()
        except TypeError:
            self.projects = dict()

        self.current_project = None
        self.path = ''
        self.data_path = ''

        line_sep = self.get_general('line_sep')
        if line_sep not in [0, 1, 2]:
            line_sep = 0
        self.line_sep = ['\n', '\r\n', '\r'][line_sep]

        self.set_project(self.get_general('project'))

        self.programs = dict()
        self.searcher = None
        self.load_programs()
        if self.get_general('search_after_start', True):
            self.start_search()

    def get_general(self, key, default=None):
        return self.q_settings.value(key, default)

    def get(self, key, default=None, project=None):
        if project is None or project == self.project:
            if self.current_project is not None:
                return self.current_project.get(key, default)
            return default
        return self.projects.get(project, dict()).get(key, default)

    def __getitem__(self, item):
        return self.get(item)

    def get_smart(self, key, default=None):
        if self.current_project is not None and self.current_project.have_key(key):
            return self.current_project.get(key, default)
        return self.get_general(key, default)

    def get_task(self, key, default=None):
        if self.current_project is None:
            return default
        return self.current_project.get_task(key, default)

    def remove_general(self, key):
        self.q_settings.remove(key)

    def remove(self, key):
        if self.current_project is not None:
            self.current_project.remove(key)

    def set_project(self, project):
        if project == self.project:
            return
        print(1)
        self.start_change_task()
        print(2)

        if project is None or project not in self.projects:
            self.project = ''
            self.current_project = None
            self.store_projects_list()
            return

        if isinstance(self.current_project, Project):
            self.current_project.store()

        self.project = project
        self.current_project = self.projects.get(self.project)
        self.path = self.current_project.path()
        self.data_path = self.current_project.data_path()
        self.current_project.load()

        self.project_changed.emit()
        self.finishChangeTask.emit()

    def start_change_task(self):
        if isinstance(self.current_project, Project):
            self.startChangeTask.emit()
            self.current_project.store_task()

    def finish_change_task(self):
        self.finishChangeTask.emit()

    def lab_path(self, lab=None, task=None, var=None, project=None):
        if project is None and isinstance(self.current_project, Project):
            return self.current_project.lab_path(lab, task, var)
        if project not in self.projects:
            raise Exception
        return self.projects[project].lab_path(lab, task, var)

    def data_lab_path(self, lab=None, task=None, var=None, project=None):
        if project is None and isinstance(self.current_project, Project):
            return self.current_project.data_lab_path(lab, task, var)
        if project not in self.projects:
            raise Exception
        return self.projects[project].data_lab_path(lab, task, var)

    def set_general(self, key, value):
        if key == 'line_sep':
            self.line_sep = ['\n', '\r\n', '\r'][value]
        self.q_settings.setValue(key, value)

    def set_task(self, key, value):
        if self.current_project is None:
            return
        return self.current_project.set_task(key, value)

    def set(self, key, value, project=None):
        if project is None or project == self.project:
            if self.current_project is not None:
                return self.current_project.set(key, value)
            return
        return self.projects.get(project, dict()).set(key, value)

    def __setitem__(self, key, value):
        self.set(key, value)

    def temp_dir(self):
        return f"{self.app_data_dir}/temp_files"

    def test_in_path(self, test_type, number, lab=(None, None, None), project=None):
        if not self.get('func_tests_in_project', True):
            return f"{self.data_lab_path(*lab, project=project)}/func_tests_data/{test_type}_{number}_in.txt"
        return os.path.join(self.lab_path(*lab, project=project), self.get(
            'stdin_pattern', "func_tests/data/{test_type}_{number:0>2}_in.txt").format(
            test_type=test_type, number=number + 1))

    def test_out_path(self, test_type, number, lab=(None, None, None), project=None):
        if not self.get('func_tests_in_project', True):
            return f"{self.data_lab_path(*lab, project=project)}/func_tests_data/{test_type}_{number}_out.txt"
        return os.path.join(self.lab_path(*lab, project=project), self.get(
            'stdout_pattern', "func_tests/data/{test_type}_{number:0>2}_out.txt").format(
            test_type=test_type, number=number + 1))

    def test_args_path(self, test_type, number, lab=(None, None, None), project=None):
        if not self.get('func_tests_in_project', True):
            return f"{self.data_lab_path(*lab, project=project)}/func_tests_data/{test_type}_{number}_args.txt"
        return os.path.join(self.lab_path(*lab, project=project), self.get(
            'args_pattern', "func_tests/data/{test_type}_{number:0>2}_args.txt").format(
            test_type=test_type, number=number + 1))

    def test_in_file_path(self, test_type, number, file_number=1, binary=False, lab=(None, None, None), project=None):
        if not self.get('func_tests_in_project', True):
            return f"{self.app_data_dir}/temp_files/{test_type}_{number}_fin{file_number}.{'bin' if binary else 'txt'}"
        return os.path.join(self.lab_path(*lab, project=project), self.get(
            'fin_pattern', "func_tests/data_files/{test_type}_{number:0>2}_in{index}.{extension}").format(
            test_type=test_type, number=number + 1, index=file_number + 1, extension=('bin' if binary else 'txt')))

    def test_out_file_path(self, test_type, number, file_number=1, binary=False, lab=(None, None, None), project=None):
        if not self.get('func_tests_in_project', True):
            return f"{self.app_data_dir}/temp_files/{test_type}_{number}_fout{file_number}.{'bin' if binary else 'txt'}"
        return os.path.join(self.lab_path(*lab, project=project), self.get(
            'fout_pattern', "func_tests/data_files/{test_type}_{number:0>2}_out{index}.{extension}").format(
            test_type=test_type, number=number + 1, index=file_number + 1, extension=('bin' if binary else 'txt')))

    def test_check_file_path(self, test_type, number, file_number=1, binary=False, lab=(None, None, None),
                             project=None):
        if not self.get('func_tests_in_project', True):
            return f"{self.app_data_dir}/temp_files/{test_type}_{number}_fcheck{file_number}.{'bin' if binary else 'txt'}"
        return os.path.join(self.lab_path(*lab, project=project), self.get(
            'fcheck_pattern', "func_tests/data_files/{test_type}_{number:0>2}_check{index}.{extension}").format(
            test_type=test_type, number=number + 1, index=file_number + 1, extension=('bin' if binary else 'txt')))

    def readme_path(self, lab=(None, None, None), project=None):
        if not self.get('func_tests_in_project', True):
            return f"{self.data_lab_path(*lab, project=project)}/func_tests_readme.md"
        return os.path.join(self.lab_path(*lab, project=project), self.get('readme_pattern', "func_tests/readme.md"))

    def store_projects_list(self):
        self.set_general('projects', dumps({key: item.path() for key, item in self.projects.items()}))
        self.set_general('project', self.project)

    def store(self):
        self.store_projects_list()
        if isinstance(self.current_project, Project):
            self.current_project.store()

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
        print('start_search')
        self.searcher = Searcher()
        self.searcher.finished.connect(self.search_finish)
        self.searcher.start()

    def search_finish(self):
        self.programs = self.searcher.res
        self.searching_complete.emit()
        with open(f'{self.app_data_dir}/programs.json', 'w', encoding='utf-8') as f:
            f.write(dumps(self.programs))


class Project:
    DATA_DIR = ".TestGenerator"
    SETTINGS_FILE = "TestGeneratorSettings.json"
    TASK_SETTINGS_FILE = "settings.json"
    NO_STRUCT_PROJECT_DATA_DIR = "data"

    def __init__(self, name, path, temp=False, data_path=''):
        self._name = name
        self._path = path
        self._dict = None
        self._task_settings = None
        self._is_temp_project = temp
        if temp:
            self._data_dir = os.path.join(data_path, self._name)
        else:
            self._data_dir = os.path.join(self._path, Project.DATA_DIR)

    def load(self):
        try:
            with open(os.path.join(self._data_dir, Project.SETTINGS_FILE), encoding='utf-8') as f:
                self._dict = loads(f.read())
            if not isinstance(self._dict, dict):
                self._dict = dict()
        except FileNotFoundError:
            self._dict = dict()
        except JSONDecodeError:
            self._dict = dict()

    def store(self):
        if self._dict is None:
            return
        try:
            os.makedirs(self._path, exist_ok=True)
            with open(os.path.join(self._data_dir, Project.SETTINGS_FILE), 'w', encoding='utf-8') as f:
                f.write(dumps(self._dict))
            self._dict = None
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")

    def get(self, key, default=None):
        if self._dict is not None:
            return self._dict.get(key, default)
        self.load()
        if isinstance(self._dict, dict):
            res = self._dict.get(key, default)
            self._dict = None
            return res
        return default

    def set(self, key, value):
        if self._dict is not None:
            self._dict[key] = value
            return
        self.load()
        if isinstance(self._dict, dict):
            self._dict[key] = value
            self.store()
        if key in ['lab', 'task', 'var']:
            self.load_task()

    def remove(self, key):
        if self._dict is not None:
            if key in self._dict:
                self._dict.pop(key)
            return
        self.load()
        if isinstance(self._dict, dict) and key in self._dict:
            self._dict.pop(key)
            self.store()

    def load_task(self):
        self.store_task()
        try:
            with open(os.path.join(self.data_lab_path(), Project.TASK_SETTINGS_FILE), encoding='utf-8') as f:
                self._task_settings = loads(f.read())
            if not isinstance(self._dict, dict):
                self._task_settings = dict()
        except FileNotFoundError:
            self._task_settings = dict()
        except JSONDecodeError:
            self._task_settings = dict()

    def store_task(self):
        if self._task_settings is None:
            return
        if set(self._task_settings.keys()).issubset({'in_data', 'out_data', 'in_data_list'}):
            if self.get_task('in_data') in ['', '-'] and self.get_task('out_data') in ['', '-'] and \
                    not self.get_task('in_data_list'):
                return
        try:
            os.makedirs(path := self.data_lab_path(), exist_ok=True)
            with open(os.path.join(path, Project.TASK_SETTINGS_FILE), 'w', encoding='utf-8') as f:
                f.write(dumps(self._task_settings))
            self._task_settings = None
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")

    def get_task(self, key, default=None):
        if not isinstance(self._task_settings, dict):
            self.load_task()
        return self._task_settings.get(key, default)

    def set_task(self, key, value):
        if not isinstance(self._task_settings, dict):
            self.load_task()
        self._task_settings[key] = value

    def lab_path(self, lab=None, task=None, var=None):
        if self.get('struct', 0) == 1:
            return self._path

        elif self.get('struct', 0) == 2:
            if lab is None:
                lab = self.get('lab')
            try:
                return f"{self._path}/{self.get('subprojects', [])[lab]}"
            except IndexError:
                return self._path
            except TypeError:
                return self._path

        if lab is None:
            lab = self.get('lab', 1)
        if task is None:
            task = self.get('task', 1)
        if var is None:
            var = self.get('var', 0)
        if var == -1:
            return os.path.join(self._path, self.get('dir_no_var_pattern', 'lab_{lab:0>2}_{task:0>2}').format(
                lab=lab, task=task, var=var))
        return os.path.join(self._path, self.get('dir_pattern', 'lab_{lab:0>2}_{task:0>2}_{var:0>2}').format(
            lab=lab, task=task, var=var))

    def data_lab_path(self, lab=None, task=None, var=None, project=None):
        if self.get('struct', 0) == 1:
            return os.path.join(self._data_dir, Project.NO_STRUCT_PROJECT_DATA_DIR)

        if lab is None:
            lab = self.get('lab', 1)
        if task is None:
            task = self.get('task', 1)
        if var is None:
            var = self.get('var', 0)
        return f"{self._data_dir}/{lab}/{task}/{var}"

    def path(self):
        return self._path

    def name(self):
        return self._name

    def data_path(self):
        return self._data_dir

    def have_key(self, key):
        return key in self._dict

    def delete(self, main_dir=False):
        try:
            if main_dir:
                shutil.rmtree(self._path)
            if os.path.isdir(self._data_dir):
                shutil.rmtree(self._data_dir)
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")

    def rename(self, new_name):
        self._name = new_name

    def move(self, new_path):
        try:
            os.rename(self._path, new_path)
            self._path = new_path
            if not self._is_temp_project:
                self._data_dir = os.path.join(self._path, Project.DATA_DIR)
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")

    def create_gitignore(self):
        os.makedirs(self._data_dir, exist_ok=True)
        with open(os.path.join(self._data_dir, ".gitignore"), 'w', encoding='utf-8') as f:
            f.write('# Created by TestGenerator\n*\n')
