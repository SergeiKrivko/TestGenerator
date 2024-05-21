import importlib
import os.path
import shutil
import sys
import time
from urllib.parse import quote

import aiohttp
from PyQt6.QtCore import QObject, pyqtSignal
from TestGeneratorPluginLib._built_plugin import BuiltPlugin

from src.backend.language.languages import LANGUAGES
from src.backend.settings_manager import SettingsManager


class RemotePlugin:
    def __init__(self, user_id, data: dict):
        self.user_id = user_id
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.author = data.get('author', '')
        self.url = data.get('url', '')

        versions = data.get('versions', dict())

        all_version = versions.get('all')
        this_version = versions.get(sys.platform)
        self.version = all_version or this_version
        self.platform = 'all' if all_version else sys.platform


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
        self._remote: dict[str: RemotePlugin] = dict()

        self._file_create_options = dict()

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

    def _import_plugin(self, path: str):
        path = os.path.abspath(path)
        sys.path.insert(0, path)
        sys.path.insert(1, os.path.join(path, '__packages__'))

        module = importlib.import_module('__plugin__')

        plugin: BuiltPlugin = module.__plugin__
        self._plugins[plugin.name] = plugin
        plugin.init(self._bm)
        for key, item in plugin.main_tabs.items():
            self.newMainTab.emit(key, item(self._bm))
        for key, item in plugin.side_tabs.items():
            self.newSideTab.emit(key, item(self._bm))
        for key, item in plugin.fast_run_options.items():
            LANGUAGES[key].fast_run.extend(item)
        for key, item in plugin._plugin.files_create_options.items():
            if key not in self._file_create_options:
                self._file_create_options[key] = []
            self._file_create_options[key].append(item)

        sys.modules.pop('__plugin__')
        sys.path.pop(0)
        sys.path.pop(0)
        return plugin

    def install(self, path: str):
        temp_path = f"{self._sm.temp_dir()}/plugin"
        if os.path.isdir(temp_path):
            shutil.rmtree(temp_path)
        shutil.unpack_archive(path, temp_path)

        with open(os.path.join(temp_path, '__plugin__.py'), encoding='utf-8') as f:
            text = f.read()
            substr = '__plugin__ = BuiltPlugin(Plugin, '
            text = text[text.index(substr) + len(substr):]
            if text.startswith('"'):
                text = text[1:]
                name = text[:text.index('"')]
            elif text.startswith("'"):
                text = text[1:]
                name = text[:text.index("'")]
            else:
                raise Exception("Can not find plugin name")

        dst_path = os.path.join(self._path, name)
        if os.path.isdir(dst_path):
            shutil.rmtree(dst_path)
        os.makedirs(self._path, exist_ok=True)
        os.rename(temp_path, dst_path)

        self._import_plugin(dst_path)

        return name

    def remove(self, name):
        plugin: BuiltPlugin = self._plugins[name]
        plugin.terminate()
        time.sleep(0.1)
        for el in plugin.main_tabs:
            self.removeMainTab.emit(el)
        for el in plugin.side_tabs:
            self.removeSideTab.emit(el)
        for key, item in plugin.fast_run_options.items():
            for el in item:
                LANGUAGES[key].fast_run.remove(el)
        for key, item in plugin._plugin.files_create_options.items():
            self._file_create_options[key].remove(item)

        self._plugins.pop(name)
        shutil.rmtree(os.path.join(self._path, name))

    def file_create_options(self, extension: str):
        return self._file_create_options.get(extension, [])

    async def update_remote(self):
        self._remote.clear()
        try:
            url = f"https://testgenerator-bf37c-default-rtdb.europe-west1.firebasedatabase.app/plugins.json"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.ok:
                        data = await resp.json()
                        for user_id, data in data.items():
                            for plugin_name, plugin_data in data.items():
                                self._remote[plugin_name] = RemotePlugin(user_id=user_id, data=plugin_data)
        except aiohttp.ClientError:
            pass

    async def download_plugin(self, plugin: RemotePlugin):
        url = f"https://firebasestorage.googleapis.com/v0/b/testgenerator-bf37c.appspot.com/o/" \
              f"{quote(f'plugins/{plugin.user_id}/{plugin.name}/{plugin.platform}.TGPlugin.zip', safe='')}?alt=media"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if not resp.ok:
                    raise aiohttp.ClientError
                dst_path = os.path.join(self._sm.temp_dir(), 'plugin.TGPlugin.zip')
                os.makedirs(self._sm.temp_dir(), exist_ok=True)
                with open(dst_path, 'bw') as f:
                    while not resp.closed:
                        chunk = await resp.content.readany()
                        f.write(chunk)
        print('finished downloading plugin')
        return dst_path

    @property
    def all(self):
        return list(self._plugins.keys())

    @property
    def remote(self):
        return self._remote
