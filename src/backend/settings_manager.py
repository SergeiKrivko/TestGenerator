import appdirs
from PyQt6.QtCore import QSettings, pyqtSignal, QObject

from src.backend.backend_types.project import Project


class SettingsManager(QObject):
    searching_complete = pyqtSignal()
    projectChanged = pyqtSignal()
    mainProjectChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        # self.q_settings = QSettings('settings.ini', QSettings.IniFormat)
        self.q_settings = QSettings()
        self.app_data_dir = appdirs.user_data_dir("TestGenerator", "SergeiKrivko").replace('\\', '/')

        self.project: Project | None = None

        line_sep = self.get_general('line_sep')
        if line_sep not in [0, 1, 2]:
            line_sep = 0
        self.line_sep = ['\n', '\r\n', '\r'][line_sep]

    def get_general(self, key, default=None):
        return self.q_settings.value(key, default)

    def get_bool(self, key: str, default=False):
        res = self.q_settings.value(key, default)
        if isinstance(res, bool):
            return res
        if isinstance(res, int):
            return bool(res)
        return str(res).lower() == 'true'

    def remove_general(self, key):
        self.q_settings.remove(key)

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

    def remove(self, key):
        if self.project is not None:
            self.project.pop(key)

    def get_data(self, key, default=None):
        if self.project is not None:
            return self.project.get_data(key, default)
        return default

    def set_data(self, key, value):
        if self.project is not None:
            self.project.set_data(key, value)

    def temp_dir(self):
        return f"{self.app_data_dir}/temp_files"
