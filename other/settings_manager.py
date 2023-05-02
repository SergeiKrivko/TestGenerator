from PyQt5.QtCore import QSettings


class SettingsManager:
    def __init__(self):
        # self.q_settings = QSettings('settings.ini', QSettings.IniFormat)
        self.q_settings = QSettings()
        self.path = self.get_general('__project__')

    def get_general(self, key, default=None):
        return self.q_settings.value(key, default)

    def get(self, key, default=None):
        return self.q_settings.value(self.path, dict()).get(key, self.get_general(key, default))

    def __getitem__(self, item):
        return self.get(item)

    def remove(self, key):
        self.q_settings.remove(key)

    def lab_path(self, lab=None, task=None, var=None):
        if lab is None:
            lab = self.get('lab')
        if task is None:
            task = self.get('task')
        if var is None:
            var = self.get('var')
        if var == -1:
            return f"{self.path}/lab_{lab:0>2}_{task:0>2}"
        return f"{self.path}/lab_{lab:0>2}_{task:0>2}_{var:0>2}"

    def set_general(self, key, value):
        self.q_settings.setValue(key, value)
        if key == '__project__':
            self.path = value

    def set(self, key, value):
        dct = self.q_settings.value(self.path)
        dct[key] = value
        self.q_settings.setValue(self.path, dct)

    def __setitem__(self, key, value):
        self.set(key, value)

    def repair_settings(self):
        if self.path:
            if self.q_settings.value(self.path) is None:
                self.q_settings.setValue(self.path, dict())

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
                dlg = self.get_general(self.path)
                if 'compiler' in dlg:
                    dlg.pop('compiler')
                if '-lm' in dlg:
                    dlg.pop('-lm')
                if 'pos_comparator' in dlg:
                    dlg.pop('pos_comparator')
                if 'neg_comparator' in dlg:
                    dlg.pop('neg_comparator')
                if 'pos_substring' in dlg:
                    dlg.pop('pos_substring')
                if 'neg_substring' in dlg:
                    dlg.pop('neg_substring')
                if 'epsilon' in dlg:
                    dlg.pop('epsilon')
                if 'memory_testing' in dlg:
                    dlg.pop('memory_testing')
                if 'coverage' in dlg:
                    dlg.pop('coverage')
                if 'time_limit' in dlg:
                    dlg.pop('time_limit')
                self.set_general(self.path, dlg)
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
