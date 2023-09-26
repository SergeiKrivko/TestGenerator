import os

from PyQt5.QtCore import QThread


def find(path, dct):
    res = {key: list() for key in dct.keys()}
    for root, dirs, files in os.walk(path):
        for file in files:
            if file in dct and (not dct[file] or dct[file](os.path.join(root, file))):
                res[file].append(os.path.join(root, file))
    return res


class Searcher(QThread):
    def __init__(self):
        super().__init__()
        self.res = dict()

    def run(self):
        if os.name == 'nt':
            self.res = find('C:\\', {
                'gcc.exe': None,
                'gcov.exe': None,
                'python.exe': None,
                'coverage.exe': None
            })
        else:
            self.res = find('/', {
                'gcc.exe': None,
                'gcov.exe': None,
                'python.exe': None,
                'coverage.exe': None
            })
