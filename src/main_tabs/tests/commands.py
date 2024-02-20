import json
import os
from subprocess import run
import subprocess
from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal

from src.side_tabs.builds.commands_list import CommandsList
from src.language.languages import languages
from src.language.utils import get_files


class CommandManager:
    def __init__(self, sm):
        self.sm = sm
        self.path = ''

    @staticmethod
    def cmd_command(args, **kwargs):
        if os.name == 'nt':
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            return run(args, capture_output=True, text=True, startupinfo=si, **kwargs)
        else:
            return run(args, capture_output=True, text=True, **kwargs)

    def cmd_command_looper(self, args, **kwargs):
        return Looper(lambda: self.cmd_command(args, **kwargs))

    def run_code(self, path, args='', in_data=None, coverage=False, scip_timeout=False):
        for language in languages:
            for el in language.get('files', []):
                if path.endswith(el):
                    timeout = None if scip_timeout else float(self.sm.get_smart('time_limit', 3))
                    if in_data is not None:
                        return self.cmd_command(language['run'](path, self, args, coverage),
                                                input=in_data, timeout=timeout, shell=True)
                    return self.cmd_command(language['run'](path, self, args, coverage), timeout=timeout, shell=True)

    def update_path(self):
        self.path = self.sm.lab_path()

    def compile(self, data: dict | str, path: str = None, coverage=False):
        if path is None:
            path = self.sm.lab_path()
        if isinstance(data, str):
            try:
                data = json.loads(CommandManager.read_file(
                                f"{self.sm.data_lab_path()}/scenarios/make/{data}.json", ''))
            except json.JSONDecodeError:
                return False, "Invalid build data"
        return languages[self.sm.get('language', 'C')].get(
            'compile', lambda *args: (False, 'Can\'t compile this file'))(path, self, self.sm, data, coverage)

    def run_main_code(self, args='', in_data=None, file='', coverage=False):
        if in_data is not None:
            return self.cmd_command(languages[self.sm.get('language', 'C')].get('run')(
                f"{self.path}/{file}", self.sm, args, coverage), timeout=float(self.sm.get('time_limit', 3)),
                shell=True, input=in_data, cwd=self.sm.lab_path())
        return self.cmd_command(languages[self.sm.get('language', 'C')].get('run')(
            f"{self.path}/{file}", self.sm, args, coverage), timeout=float(self.sm.get('time_limit', 3)), shell=True,
            cwd=self.sm.lab_path())

    def collect_coverage(self):
        res = languages[self.sm.get('language', 'C')].get('coverage', lambda *args: 0)(self.path, self.sm, self)
        self.clear_coverage_files()
        return res

    def clear_coverage_files(self):
        self.path = self.sm.lab_path()
        languages[self.sm.get('language', 'C')].get('clear_coverage', lambda *args: 0)(self.path)

    def get_files_list(self, path=None):
        if path is None:
            path = self.sm.lab_path()
        for ex in languages.get(self.sm.get('language', 'C'), dict()).get('files', list()):
            for el in get_files(path, ex):
                yield el

    def run_scenarios(self, data: list | dict, cwd=None):
        if isinstance(data, dict):
            data = [data]
        if cwd is None:
            cwd = self.sm.lab_path()
        res = []
        for scenario in data:
            match scenario['type']:
                case CommandsList.TYPE_CMD:
                    res.append(self.cmd_command(scenario['data'], shell=True, cwd=cwd))
                case CommandsList.TYPE_BUILD:
                    res.append(self.compile(scenario['data'], cwd))
        return res

    def test_count(self):
        count = 0
        i = 1
        while os.path.isfile(self.sm.test_in_file_path('pos', i)):
            count += 1
        i = 1
        while os.path.isfile(self.sm.test_in_file_path('neg', i)):
            count += 1
        return count

    @staticmethod
    def after_second(func, time: int | float = 1):
        looper = Looper(lambda: sleep(time))
        looper.finished.connect(func)
        looper.start()
        return looper

    @staticmethod
    def read_file(path, default=''):
        try:
            file = open(path, encoding='utf-8')
            res = file.read()
            file.close()
            return res
        except Exception:
            return default

    @staticmethod
    def read_binary(path, default=None):
        if default is not None:
            try:
                file = open(path, 'br')
                res = file.read()
                file.close()
                return res
            except FileNotFoundError:
                return default
        with open(path, 'br') as f:
            return f.read()

    def list_of_tasks(self):
        res = []
        for file in os.listdir(self.sm['path']):
            if file.startswith(f"lab_{self.sm['lab']:0>2}_"):
                try:
                    res.append(int(file[7:9]))
                except Exception:
                    pass
        res.sort()
        return res

    def parse_todo_md(self):
        res = []
        try:
            with open(f"{self.sm.data_path}/TODO/lab_{self.sm['lab']:0>2}.md", encoding='utf-8') as file:
                task = -1
                for line in file:
                    if line.startswith('## Общее'):
                        task = 0
                    elif line.startswith('## Задание'):
                        task = int(line.split()[2])
                    elif line.startswith('- '):
                        res.append((task, line[1:].strip()))
                    res.sort()
        except FileNotFoundError:
            pass
        return res

    def parse_todo_in_code(self, current_task=False):
        res = []
        for folder in (
                os.listdir(self.sm['path']) if not current_task else
                (f"lab_{self.sm['lab']:0>2}_"
                 f"{self.sm['task']:0>2}_{self.sm['var']:0>2}",)):

            if os.path.isdir(f"{self.sm['path']}/{folder}"):
                for file in os.listdir(f"{self.sm['path']}/{folder}"):
                    if file.endswith(".c") or file.endswith(".h"):
                        i = 1
                        for line in (f := open(f"{self.sm['path']}/{folder}/{file}", encoding='utf-8')):
                            if "// TODO:" in line:
                                res.append((f"{folder}/{file}", i, line[line.index("// TODO:") + 8:].strip()))
                            i += 1
                        f.close()
        return res


class Looper(QThread):
    complete = pyqtSignal(object)

    def __init__(self, func):
        super(Looper, self).__init__()
        self.func = func
        self.res = None

    def run(self) -> None:
        self.res = self.func()
        self.complete.emit(self.res)
