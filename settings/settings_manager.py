import os
import shutil

from PyQt5.QtCore import QSettings, pyqtSignal, QObject
from json import dumps, loads, JSONDecodeError
import appdirs

from settings.search import Searcher


class SettingsManager(QObject):
    searching_complete = pyqtSignal()
    project_changed = pyqtSignal()
    start_change_task = pyqtSignal()
    finish_change_task = pyqtSignal()

    def __init__(self):
        super().__init__()
        # self.q_settings = QSettings('settings.ini', QSettings.IniFormat)
        self.q_settings = QSettings()
        self.app_data_dir = appdirs.user_data_dir("TestGenerator", "SergeiKrivko").replace('\\', '/')

        self.project = ''
        try:
            s = self.get_general('projects')
            self.projects = loads(s)
        except JSONDecodeError:
            self.projects = dict()
        except TypeError:
            self.projects = dict()
        self.path = ''
        self.data_path = ''
        self.data_path_old = ''
        line_sep = self.get_general('line_sep')
        if line_sep not in [0, 1, 2]:
            line_sep = 0
        self.line_sep = ['\n', '\r\n', '\r'][line_sep]
        self.project_settings = dict()
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
            dct = self.project_settings
        else:
            path = self.projects.get(project)
            data_path = f"{path}/.TestGenerator"
            data_path_old = f"{self.app_data_dir}/projects/{project}"
            if not os.path.isdir(data_path) and os.path.isdir(data_path_old):
                try:
                    os.rename(data_path_old, data_path)
                    with open(f"{data_path}/.gitignore", 'w', encoding='utf-8') as f:
                        f.write('# Created by TestGenerator\n*\n')
                except Exception as ex:
                    print(f"{ex.__class__.__name__}: {ex}")

            try:
                with open(f"{data_path}/TestGeneratorSettings.json", encoding='utf-8') as f:
                    dct = loads(f.read())
            except FileNotFoundError:
                return default
            except JSONDecodeError:
                return default
        return dct.get(key, self.get_general(key, default))

    def __getitem__(self, item):
        return self.get(item)

    def get_smart(self, key, default=None):
        if key in self.project_settings:
            return self.project_settings[key]
        return self.get_general(key, default)

    def remove_general(self, key):
        self.q_settings.remove(key)

    def remove(self, key):
        if key in self.project_settings:
            self.project_settings.pop(key)

    def set_project(self, project):
        self.start_change_task.emit()
        if project is None:
            self.project = ''
            self.set_general('projects', dumps(self.projects))
            return
        self.store()
        self.project = project

        self.path = self.projects.get(self.project)
        self.data_path = f"{self.path}/.TestGenerator"
        self.data_path_old = f"{self.app_data_dir}/projects/{self.project}"

        if not os.path.isdir(self.data_path) and os.path.isdir(self.data_path_old):
            try:
                os.rename(self.data_path_old, self.data_path)
                with open(f"{self.data_path}/.gitignore", 'w', encoding='utf-8') as f:
                    f.write('# Created by TestGenerator\n*\n')
            except Exception as ex:
                print(f"{ex.__class__.__name__}: {ex}")
        elif os.path.isdir(self.data_path_old):
            try:
                shutil.rmtree(self.data_path_old)
            except Exception as ex:
                print(f"{ex.__class__.__name__}: {ex}")

        try:
            with open(f"{self.data_path}/TestGeneratorSettings.json", encoding='utf-8') as f:
                self.project_settings = loads(text := f.read())
                # print(f"read from {self.data_path}/TestGeneratorSettings.json:\n{text}")
        except FileNotFoundError:
            self.project_settings = dict()
        except JSONDecodeError:
            self.project_settings = dict()

        self.project_changed.emit()
        self.finish_change_task.emit()

    def lab_path(self, lab=None, task=None, var=None, project=None):
        struct = self.get('struct', project=project)
        if struct == 1:
            return self.path

        elif struct == 2:
            if lab is None:
                lab = self.get('lab', project=project)
            try:
                return f"{self.path}/{self.get('subprojects', [])[lab]}"
            except IndexError:
                return self.path
            except TypeError:
                return self.path

        if lab is None:
            lab = self.get('lab', project=project)
        if task is None:
            task = self.get('task', project=project)
        if var is None:
            var = self.get('var', project=project)
        if project is None:
            path = self.path
        else:
            path = self.projects[project]

        if var == -1:
            return os.path.join(path, self.get('dir_no_var_pattern', 'lab_{lab:0>2}_{task:0>2}').format(
                lab=lab, task=task))
        return os.path.join(path, self.get('dir_pattern', 'lab_{lab:0>2}_{task:0>2}_{var:0>2}').format(
            lab=lab, task=task, var=var))

    def data_lab_path(self, lab=None, task=None, var=None, project=None):
        if self.get('struct', project=project) == 1:
            return f"{self.data_path}/data"
        if project in self.projects:
            project = f"{self.app_data_dir}/projects/{project}"
        else:
            project = self.data_path
        if lab is None:
            lab = self.get('lab')
        if task is None:
            task = self.get('task')
        if var is None:
            var = self.get('var')
        return f"{project}/{lab}/{task}/{var}"

    def set_general(self, key, value):
        if key == 'line_sep':
            self.line_sep = ['\n', '\r\n', '\r'][value]
        self.q_settings.setValue(key, value)

    def set(self, key, value, project=None):
        if project is None or project == self.project:
            self.project_settings[key] = value
        else:
            path = self.projects.get(project)
            data_path = f"{path}/.TestGenerator"
            data_path_old = f"{self.app_data_dir}/projects/{project}"
            if not os.path.isdir(data_path) and os.path.isdir(data_path_old):
                try:
                    os.rename(data_path_old, data_path)
                    with open(f"{data_path}/.gitignore", 'w', encoding='utf-8') as f:
                        f.write('# Created by TestGenerator\n*\n')
                except Exception as ex:
                    print(f"{ex.__class__.__name__}: {ex}")

            try:
                with open(f"{data_path}/TestGeneratorSettings.json", encoding='utf-8') as f:
                    dct = loads(f.read())
            except FileNotFoundError:
                dct = dict()
            except JSONDecodeError:
                dct = dict()
            dct[key] = value
            os.makedirs(data_path, exist_ok=True)
            with open(f"{data_path}/TestGeneratorSettings.json", 'w', encoding='utf-8') as f:
                # print(f"write \"{dumps(dct)}\" to {self.app_data_dir}/projects/{project}/TestGeneratorSettings.json")
                f.write(dumps(dct))

    def __setitem__(self, key, value):
        self.set(key, value)

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

    def repair_settings(self):
        if self.data_path:
            # if self.q_settings.value(self.data_path) is None:
            #     self.q_settings.setValue(self.data_path, '{}')

            if not isinstance(self.get('lab'), int) or self.get('struct') == 1:
                self.set('lab', 1)
            if not isinstance(self.get('task'), int) or self.get('struct') == 1:
                self.set('task', 1)
            if not isinstance(self.get('var'), int) or self.get('struct') == 1:
                self.set('var', 0)

            if self.get('default_testing_settings', True):
                if not isinstance(self.get_general('compiler'), str):
                    self.set_general('compiler', 'gcc -std=c99 -Wall -Werror')
                if not isinstance(self.get_general('-lm'), int):
                    self.set_general('-lm', 1)
                if not isinstance(self.get_general('pos_comparator'), int):
                    self.set_general('pos_comparator', 0)
                if not isinstance(self.get_general('neg_comparator'), int):
                    self.set_general('neg_comparator', 0)
                if not isinstance(self.get_general('pos_substring'), str):
                    self.set_general('pos_substring', 'Result:')
                if not isinstance(self.get_general('neg_substring'), str):
                    self.set_general('neg_substring', 'Result:')
                if not isinstance(self.get_general('line_sep'), int):
                    self.set_general('line_sep', 0)
                if not isinstance(self.get_general('memory_testing'), int):
                    self.set_general('memory_testing', 0)
                if not isinstance(self.get_general('coverage'), int):
                    self.set_general('coverage', 0)
                if not isinstance(self.get_general('time_limit'), (float, int, str)):
                    self.set_general('time_limit', '10.0')
                if 'compiler' in self.project_settings:
                    self.project_settings.pop('compiler')
                if '-lm' in self.project_settings:
                    self.project_settings.pop('-lm')
                if 'pos_comparator' in self.project_settings:
                    self.project_settings.pop('pos_comparator')
                if 'neg_comparator' in self.project_settings:
                    self.project_settings.pop('neg_comparator')
                if 'pos_substring' in self.project_settings:
                    self.project_settings.pop('pos_substring')
                if 'neg_substring' in self.project_settings:
                    self.project_settings.pop('neg_substring')
                if 'epsilon' in self.project_settings:
                    self.project_settings.pop('epsilon')
                if 'memory_testing' in self.project_settings:
                    self.project_settings.pop('memory_testing')
                if 'coverage' in self.project_settings:
                    self.project_settings.pop('coverage')
                if 'time_limit' in self.project_settings:
                    self.project_settings.pop('time_limit')
            else:
                if not isinstance(self.get('compiler'), str):
                    self.set('compiler', self.get_general('compiler', 'gcc -std=c99 -Wall -Werror'))
                if not isinstance(self.get('-lm'), int):
                    self.set('-lm', self.get_general('-lm', 1))
                if not isinstance(self.get('pos_comparator'), int):
                    self.set('pos_comparator', self.get_general('pos_comparator', 0))
                if not isinstance(self.get('neg_comparator'), int):
                    self.set('neg_comparator', self.get_general('neg_comparator', 0))
                if not isinstance(self.get('pos_substring'), str):
                    self.set('pos_substring', self.get_general('pos_substring', 'Result:'))
                if not isinstance(self.get('neg_substring'), str):
                    self.set('neg_substring', self.get_general('neg_substring', 'Result:'))
                if not isinstance(self.get('memory_testing'), int):
                    self.set('memory_testing', self.get_general('memory_testing', 0))
                if not isinstance(self.get('coverage'), int):
                    self.set('coverage', self.get_general('coverage', 0))
                if not isinstance(self.get('time_limit'), (float, int)):
                    self.set('time_limit', self.get_general('time_limit', 10))

    def store(self):
        if self.project not in self.projects:
            return
        if self.data_path:
            os.makedirs(self.data_path, exist_ok=True)
            with open(f"{self.data_path}/TestGeneratorSettings.json", 'w', encoding='utf-8') as f:
                # print(f"write \"{dumps(self.project_settings)}\" to {self.data_path}/TestGeneratorSettings.json")
                f.write(dumps(self.project_settings))
            self.set_general('projects', dumps(self.projects))
            self.set_general('project', self.project)

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
