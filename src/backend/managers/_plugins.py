import importlib
import os.path
import shutil
import sys

from PyQt6.QtCore import QObject, pyqtSignal
from TestGeneratorPluginLib._built_plugin import BuiltPlugin

from src.backend.language.languages import LANGUAGES
from src.backend.settings_manager import SettingsManager


class PluginManager(QObject):
    newMainTab = pyqtSignal(str, object)
    newSideTab = pyqtSignal(str, object)
    removeMainTab = pyqtSignal(str)
    removeSideTab = pyqtSignal(str)

    def __init__(self, bm):
        super().__init__()
        self._bm = bm
        self._sm: SettingsManager = bm.sm

        self._path = f"{self._sm.app_data_dir}/plugins"
        self._plugins: dict[str: BuiltPlugin] = dict()

    def init(self):
        if not os.path.isdir(self._path):
            return
        for el in os.listdir(self._path):
            try:
                self.load(el)
            except Exception as e:
                print(f"Cannot load plugin {el}: {e.__class__.__name__}: {e}")

    def load(self, name: str):
        path = f"{self._path}/{name}"
        self._import_plugin(path)

    def get(self, name) -> BuiltPlugin:
        return self._plugins.get(name)

    def _import_plugin(self, path: str, add=True):
        path = os.path.abspath(path)
        sys.path.insert(0, path)
        sys.path.insert(1, os.path.join(path, '__packages__'))

        module = importlib.import_module('__plugin__')

        plugin: BuiltPlugin = module.__plugin__
        if add:
            self._plugins[plugin.name] = plugin
            plugin.init(self._bm)
            for key, item in plugin.main_tabs.items():
                self.newMainTab.emit(key, item(self._bm))
            for key, item in plugin.side_tabs.items():
                self.newSideTab.emit(key, item(self._bm))
            for key, item in plugin.fast_run_options.items():
                LANGUAGES[key].fast_run.extend(item)

        sys.modules.pop('__plugin__')
        sys.path.pop(0)
        sys.path.pop(0)
        return plugin

    def install(self, path: str):
        temp_path = f"{self._sm.temp_dir()}/plugin"
        if os.path.isdir(temp_path):
            shutil.rmtree(temp_path)
        shutil.unpack_archive(path, temp_path)

        plugin = self._import_plugin(temp_path)

        name = plugin.name
        dst_path = os.path.join(self._path, name)
        os.makedirs(self._path, exist_ok=True)
        os.rename(temp_path, dst_path)

        return name

    def remove(self, name):
        plugin = self._plugins[name]
        for el in plugin.main_tabs:
            self.removeMainTab.emit(el)
        for el in plugin.side_tabs:
            self.removeSideTab.emit(el)
        for key, item in plugin.fast_run_options.items():
            for el in item:
                LANGUAGES[key].fast_run.remove(el)

        self._plugins.pop(name)
        shutil.rmtree(os.path.join(self._path, name))

    @property
    def all(self):
        return list(self._plugins.keys())
