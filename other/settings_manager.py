from PyQt5.QtCore import QSettings


class SettingsManager:
    def __init__(self):
        self.q_settings = QSettings()
        self.path = self.get_general('__project__')

    def get_general(self, key, default=None):
        return self.q_settings.value(key, default)

    def get(self, key, default=None):
        return self.q_settings.value(self.path, dict()).get(key, default)

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
            if not isinstance(self.get('compiler'), str):
                self.set('compiler', 'gcc -std=c99 -Wall -Werror')
            if not isinstance(self.get('-lm'), bool):
                self.set('-lm', True)
            if not isinstance(self.get('lab'), int):
                self.set('lab', 1)
            if not isinstance(self.get('task'), int):
                self.set('task', 1)
            if not isinstance(self.get('var'), int):
                self.set('var', 0)
            if not isinstance(self.get('pos_comparator'), int):
                self.set('pos_comparator', 0)
            if not isinstance(self.get('neg_comparator'), int):
                self.set('neg_comparator', 0)
            if not isinstance(self.get('line_sep'), str):
                self.set('line_sep', '\n')
