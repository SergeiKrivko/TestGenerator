import os
from PyQt5.QtCore import QSettings
from json import dumps, loads, JSONDecodeError
import appdirs


class SettingsManager:
    def __init__(self):
        # self.q_settings = QSettings('settings.ini', QSettings.IniFormat)
        self.q_settings = QSettings()
        self.app_data_dir = appdirs.user_data_dir("TestGenerator", "SergeiKrivko").replace('\\', '/')

        self.project = ''
        self.projects = dict()
        self.path = ''
        self.data_path = ''
        self.project_settings = dict()
        self.set_project(self.get_general('project'))

    def get_general(self, key, default=None):
        return self.q_settings.value(key, default)

    def get(self, key, default=None, project=None):
        if project is None:
            dct = self.project_settings
        else:
            dct = loads(self.get_general(project, '{}'))
        return dct.get(key, self.get_general(key, default))

    def __getitem__(self, item):
        return self.get(item)

    def remove(self, key):
        self.q_settings.remove(key)

    def set_project(self, project):
        self.store()
        self.project = project
        try:
            s = self.get_general('projects')
            self.projects = loads(s)
        except JSONDecodeError:
            self.projects = dict()
        except TypeError:
            self.projects = dict()

        self.path = self.projects.get(self.project)

        self.data_path = f"{self.app_data_dir}/projects/{self.project}"
        try:
            with open(f"{self.data_path}/TestGeneratorSettings.json", encoding='utf-8') as f:
                self.project_settings = loads(f.read())
        except FileNotFoundError:
            self.project_settings = dict()
        except JSONDecodeError:
            self.project_settings = dict()

    def lab_path(self, lab=None, task=None, var=None, appdata=False):
        if lab is None:
            lab = self.get('lab')
        if task is None:
            task = self.get('task')
        if var is None:
            var = self.get('var')
        if var == -1:
            return f"{self.data_path if appdata else self.path}/lab_{lab:0>2}_{task:0>2}"
        return f"{self.data_path if appdata else self.path}/lab_{lab:0>2}_{task:0>2}_{var:0>2}"

    def data_lab_path(self, lab=None, task=None, var=None):
        if lab is None:
            lab = self.get('lab')
        if task is None:
            task = self.get('task')
        if var is None:
            var = self.get('var')
        return f"{self.data_path}/{lab}/{task}/{var}"

    def set_general(self, key, value):
        self.q_settings.setValue(key, value)

    def set(self, key, value, project=None):
        if project is None:
            self.project_settings[key] = value
        else:       # TODO: изменить на файлы в АппДате
            dct = loads(self.get_general(project, '{}'))
            dct[key] = value
            self.q_settings.setValue(project, dumps(dct))

    def __setitem__(self, key, value):
        self.set(key, value)

    def repair_settings(self):
        if self.data_path:
            # if self.q_settings.value(self.data_path) is None:
            #     self.q_settings.setValue(self.data_path, '{}')

            if not isinstance(self.get('lab'), int):
                self.set('lab', 1)
            if not isinstance(self.get('task'), int):
                self.set('task', 1)
            if not isinstance(self.get('var'), int):
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
                if not isinstance(self.get_general('line_sep'), str):
                    self.set_general('line_sep', '\n')
                if not isinstance(self.get_general('memory_testing'), int):
                    self.set_general('memory_testing', 0)
                if not isinstance(self.get_general('coverage'), int):
                    self.set_general('coverage', 0)
                if not isinstance(self.get_general('time_limit'), (float, int)):
                    self.set_general('time_limit', 10)
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
                if not isinstance(self.get('line_sep'), str):
                    self.set('line_sep', self.get_general('line_sep', '\n'))
                if not isinstance(self.get('memory_testing'), int):
                    self.set('memory_testing', self.get_general('memory_testing', 0))
                if not isinstance(self.get('coverage'), int):
                    self.set('coverage', self.get_general('coverage', 0))
                if not isinstance(self.get('time_limit'), (float, int)):
                    self.set('time_limit', self.get_general('time_limit', 10))
                    
    def store(self):
        if self.project and self.data_path:
            os.makedirs(self.data_path, exist_ok=True)
            with open(f"{self.data_path}/TestGeneratorSettings.json", 'w', encoding='utf-8') as f:
                f.write(dumps(self.project_settings))
            self.set_general('projects', dumps(self.projects))
            self.set_general('project', self.project)

