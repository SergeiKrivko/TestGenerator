from uuid import uuid4, UUID

from PyQt6.QtCore import QObject, pyqtSignal

from backend.backend_types.build import Build
from backend.settings_manager import SettingsManager


class BuildsManager(QObject):
    onAdd = pyqtSignal(Build)
    onDelete = pyqtSignal(Build)
    onRename = pyqtSignal(Build)
    onClear = pyqtSignal()
    onLoad = pyqtSignal(list)

    def __init__(self, sm: SettingsManager, bm):
        super().__init__()
        self._sm = sm
        self._bm = bm
        self._builds = dict()

    def add(self, build: Build):
        self._builds[build.id] = build
        self.onAdd.emit(build)

    def new(self, type: str):
        build = Build(build_id := uuid4(), f"{self._sm.project.data_path()}/scenarios/{build_id}.json")
        build['type'] = type
        self.add(build)
        return build

    def delete(self, id: UUID):
        build = self._builds[id]
        self._builds.pop(id)
        self.onDelete.emit(build)

    def clear(self):
        self._builds.clear()
        self.onClear.emit()

    def get(self, id: UUID) -> Build:
        return self._builds.get(id)

    def load(self, builds: list[Build]):
        print(builds)
        self._builds.clear()
        for build in builds:
            self._builds[build.id] = build
        self.onLoad.emit(builds)

    @property
    def all(self):
        return self._builds
