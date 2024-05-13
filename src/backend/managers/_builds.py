import os.path
from typing import Type
from uuid import uuid4, UUID

from PyQt6.QtCore import pyqtSignal

from src.backend.backend_types.build import Build
from src.backend.builds.c import BuildCExecutable, BuildCLibrary
from src.backend.builds.python import BuildPython
from src.backend.builds.shell import BuildBash, BuildCommand
from src.backend.commands import read_json
from src.backend.managers.manager import AbstractManager
from src.backend.settings_manager import SettingsManager


class BuildsManager(AbstractManager):
    onAdd = pyqtSignal(Build)
    onDelete = pyqtSignal(Build)
    onRename = pyqtSignal(Build)
    onClear = pyqtSignal()
    onLoad = pyqtSignal(list)

    def __init__(self, sm: SettingsManager, bm):
        super().__init__(bm)
        self._sm = sm
        self._bm = bm
        self._builds = dict()

    def add(self, build: Build):
        self._builds[build.id] = build
        self.onAdd.emit(build)

    def new(self, type: str):
        build = _select(type)(build_id := uuid4(), self._bm, self._sm.project,
                              f"{self._sm.project.data_path()}/scenarios/{build_id}.json")
        build['type'] = type
        self.add(build)
        return build

    def delete(self, build_id: UUID):
        build = self._builds.pop(build_id)
        build.remove()
        self.onDelete.emit(build)

    def clear(self):
        self._builds.clear()
        self.onClear.emit()

    def get(self, build_id: UUID | str) -> Build:
        if not isinstance(build_id, UUID):
            build_id = UUID(build_id)
        return self._builds.get(build_id)

    def _load(self, file: str):
        if not file.endswith('.json'):
            return
        build_id = UUID(os.path.basename(file)[:-5])
        dct = read_json(file)
        build = _select(dct.get('type'))(build_id, self._bm, self._sm.project, file)
        self._builds[build_id] = build
        return build

    def add_some(self, files: list[str]):
        self._builds.clear()
        builds = []
        for file in files:
            builds.append(self._load(file))
        self.onLoad.emit(builds)

    @property
    def all(self):
        return self._builds

    def _load_builds(self):
        path = self._sm.project.data_path()
        path = f"{path}/scenarios"
        if not os.path.isdir(path):
            return
        self.add_some([os.path.join(path, el) for el in os.listdir(path)])

    async def load(self):
        await self._bm.processes.run_async(self._load_builds, 'loading', 'builds')


def _select(build_type: str) -> Type:
    match build_type:
        case Build.Type.C_EXE:
            return BuildCExecutable
        case Build.Type.C_LIB:
            return BuildCLibrary
        case Build.Type.PYTHON:
            return BuildPython
        case Build.Type.BASH:
            return BuildBash
        case Build.Type.COMMAND:
            return BuildCommand
        case _:
            return Build
