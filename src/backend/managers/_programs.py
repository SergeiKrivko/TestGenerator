import json
import os
import sys

from PyQt6.QtCore import QObject, pyqtSignal, QThread

from src.backend.backend_types.program import ProgramInstance, PROGRAMS, Program
from src.backend.managers.manager import AbstractManager
from src.backend.settings_manager import SettingsManager


class ProgramsManager(AbstractManager):
    searchComplete = pyqtSignal()

    def __init__(self, sm: SettingsManager, bm):
        super().__init__(bm)
        self._sm = sm
        self._bm = bm

        self.programs = dict()
        self.searcher = None

        forced = self._sm.get_general('search_after_start', True)
        if forced in {'false', 'False', '0'}:
            forced = False
        self.start_search(forced, wait=True)

    def start_search(self, forced=False, wait=False):
        if self.searcher and not self.searcher.isFinished():
            return
        self.searcher = Searcher(self._sm, forced, wait)
        self.searcher.finished.connect(self.search_finish)
        self.searcher.start()

    def search_finish(self):
        self.programs = self.searcher.res
        self.searchComplete.emit()
        self.store_programs()

    def store_programs(self):
        with open(f'{self._sm.app_data_dir}/programs.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps({key: list(map(ProgramInstance.to_json, item.existing()))
                                for key, item in PROGRAMS.items()}))


def find(path, dct):
    res = {key: list() for key in dct.keys()}
    for root, dirs, files in os.walk(path):
        for file in files:
            if file in dct and (not dct[file] or dct[file](os.path.join(root, file))):
                res[file].append(os.path.join(root, file))
    return res


def find_programs(path, programs: dict[str: str], vs=0):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file in programs:
                print(os.path.join(root, file))
                prog = programs[file]
                prog.add_existing(ProgramInstance(prog, os.path.join(root, file), vs))


class Searcher(QThread):
    def __init__(self, sm, forced=False, wait=False):
        super().__init__()
        self.sm = sm
        self.forced = forced
        self.wait = wait
        self.res = dict()

    def load_programs(self):
        try:
            with open(f'{self.sm.app_data_dir}/programs.json', encoding='utf-8') as f:
                programs = {key: list(map(ProgramInstance.from_json, item)) for key, item in json.loads(f.read()).items()}
                for key, item in programs.items():
                    PROGRAMS[key].set_existing(item)
                if not isinstance(programs, dict):
                    raise TypeError
        except json.JSONDecodeError:
            return False
        except TypeError:
            return False
        except FileNotFoundError:
            return False
        return True

    def run(self):
        if self.forced or not self.load_programs():
            match sys.platform:
                case 'win32':
                    find_programs('C:\\', {item.win_name: item for item in PROGRAMS.values()})
                    if self.sm.get_general('use_wsl', False):
                        for prog in PROGRAMS.values():
                            prog.add_existing(ProgramInstance(prog, prog.linux_name, Program.WSL))
                case 'linux':
                    find_programs('/usr', {item.linux_name: item for item in PROGRAMS.values()})
                case 'darwin':
                    find_programs('/', {item.mac_name: item for item in PROGRAMS.values()})
