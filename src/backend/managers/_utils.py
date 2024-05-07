from uuid import UUID

from PyQt6.QtCore import QObject, pyqtSignal

from src.backend.backend_types.util import Util
from src.backend.settings_manager import SettingsManager


class UtilsManager(QObject):
    addUtil = pyqtSignal(Util)
    deleteUtil = pyqtSignal(Util)
    renameUtil = pyqtSignal(Util)
    clearUtils = pyqtSignal()

    def __init__(self, bm):
        super().__init__()
        self._bm = bm
        self._utils = dict()

    def add(self, util: Util):
        self._utils[util.id] = util
        self.addUtil.emit(util)

    def delete(self, id: UUID):
        util = self._utils[id]
        self._utils.pop(id)
        self.deleteUtil.emit(util)

    def clear(self):
        self._utils.clear()
        self.clearUtils.emit()

    def get(self, id: UUID):
        return self._utils.get(id)

    @property
    def all(self):
        return self._utils

