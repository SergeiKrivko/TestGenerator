import os
import sys
from json import JSONDecodeError, loads

from PyQt6.QtCore import QThread

from src.backend.backend_types.program import PROGRAMS, Program, ProgramInstance


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
                programs = {key: list(map(ProgramInstance.from_json, item)) for key, item in loads(f.read()).items()}
                for key, item in programs.items():
                    PROGRAMS[key].set_existing(item)
                if not isinstance(programs, dict):
                    raise TypeError
        except JSONDecodeError:
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
