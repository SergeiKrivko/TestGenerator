import os
import shutil
from json import loads, JSONDecodeError
from subprocess import run, TimeoutExpired
import subprocess
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from tests.binary_decoder import decode, comparator as bytes_comparator
from tests.macros_converter import MacrosConverter, background_process_manager
from language.languages import languages


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

    def update_path(self):
        self.path = self.sm.lab_path()

    def compile(self, coverage=False):
        self.update_path()
        return languages[self.sm.get('language', 'C')].get(
            'compile', lambda *args: (False, 'Can\'t compile this file'))(self.path, self, self.sm, coverage)

    def run_code(self, args='', in_data='', file='', coverage=False):
        return languages[self.sm.get('language', 'C')].get('run')(f"{self.path}/{file}", self.sm, self, args, in_data,
                                                                  coverage)

    def collect_coverage(self):
        res = languages[self.sm.get('language', 'C')].get('coverage', lambda *args: 0)(self.path, self.sm, self)
        self.clear_coverage_files()
        return res

    def clear_coverage_files(self):
        self.path = self.sm.lab_path()
        languages[self.sm.get('language', 'C')].get('clear_coverage', lambda *args: 0)(self.path)

    def testing(self, pos_comparator, neg_comparator, memory_testing, coverage):
        self.update_path()
        if not os.path.isdir(self.path):
            raise FileNotFoundError
        self.looper = TestingLooper(
            self.sm, self,
            pos_comparator, neg_comparator, memory_testing, coverage)
        if f"{self.sm.data_lab_path()}/func_tests" in background_process_manager.dict:
            background_process_manager.dict[f"{self.sm.data_lab_path()}/func_tests"].finished.connect(self.looper.start)
        else:
            self.looper.start()

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


class TestingLooper(QThread):
    test_complete = pyqtSignal(bool, dict, int, bool, str)
    test_crash = pyqtSignal(dict, int, str)
    test_timeout = pyqtSignal()
    end_testing = pyqtSignal()
    testing_terminate = pyqtSignal(str)

    def __init__(self, sm, cm: CommandManager, pos_comparator, neg_comparator, memory_testing=False, coverage=False):
        super(TestingLooper, self).__init__()
        self.sm = sm
        self.cm = cm
        self.memory_testing = memory_testing
        self.data_path = f"{self.sm.data_lab_path()}/func_tests"
        self.pos_comparator = pos_comparator
        self.neg_comparator = neg_comparator
        self.coverage = coverage

    def run(self):
        code, errors = self.cm.compile(coverage=self.coverage)
        if not code:
            self.testing_terminate.emit(errors)
            return

        for pos in filter(lambda s: os.path.isdir(f"{self.data_path}/{s}"), ['pos', 'neg']):
            lst = list(filter(lambda s: s.rstrip('.json').isdigit(), os.listdir(f"{self.data_path}/{pos}")))
            lst.sort(key=lambda s: int(s.rstrip('.json')))
            for i, el in enumerate(lst):
                try:
                    dct = loads(CommandManager.read_file(f"{self.data_path}/{pos}/{el}"))
                    try:
                        if self.sm.get('func_tests_in_project'):
                            args = CommandManager.read_file(self.sm.test_args_path(pos, i))
                        else:
                            args = MacrosConverter.convert_args(
                                dct.get('args', ''), '', pos, i,
                                {j + 1: self.sm.test_in_file_path(pos, i, j, binary=d.get('type', 'txt') == 'bin')
                                 for j, d in enumerate(dct.get('in_files', []))},
                                {j + 1: self.sm.test_out_file_path(pos, i, j, binary=d.get('type', 'txt') == 'bin')
                                 for j, d in enumerate(dct.get('out_files', []))},
                                f"{self.sm.app_data_dir}/temp_files")
                            self.convert_test_files('in', dct, pos, i)
                            self.convert_test_files('out', dct, pos, i)
                            self.convert_test_files('check', dct, pos, i)
                        res = self.cm.run_code(args, dct.get('in', ''), coverage=self.coverage)
                    except TimeoutExpired:
                        self.test_timeout.emit()
                        continue
                    if res.stderr:
                        self.test_crash.emit({'STDOUT': res.stdout}, res.returncode, res.stderr)
                        continue
                    comparator = self.pos_comparator if pos == 'pos' else self.neg_comparator
                    comparator_res = comparator(dct.get('out', ''), res.stdout)
                    prog_out = {"STDOUT": res.stdout}

                    for j, file in enumerate(dct.get('out_files', [])):
                        path = "" if self.sm.get('func_tests_in_project') else f"{self.sm.app_data_dir}/temp_files/"
                        if file.get('type', 'txt') == 'txt':
                            text = CommandManager.read_file(f"{path}temp_{j + 1}.txt", '')
                            comparator_res = comparator_res and file.text == text
                            prog_out[f"out_file_{i}.txt"] = text
                        else:
                            text = CommandManager.read_binary(f"{path}temp_{j + 1}.bin", b'')
                            comparator_res = comparator_res and bytes_comparator(
                                text, file['text'],
                                CommandManager.read_binary(self.sm.test_out_file_path(pos, i, j, True), b''))
                            prog_out[f"out_file_{i}.bin"], _ = decode(file['text'], text)

                    for j, file in dct.get('check_files', dict()).items():
                        if file.get('type', 'txt') == 'txt':
                            text = CommandManager.read_file(self.sm.test_in_file_path(pos, i, j, False), '')
                            comparator_res = comparator_res and file['text'] == text
                            prog_out[f"in_file_{i}.txt"] = text
                        else:
                            text = CommandManager.read_binary(self.sm.test_in_file_path(pos, i, j, True), b'')
                            comparator_res = comparator_res and bytes_comparator(
                                text, file['text'], CommandManager.read_binary(
                                    self.sm.test_check_file_path(pos, i, j, True), b''))
                            prog_out[f"in_file_{i}.bin"], _ = decode(file['text'], text)


                    if self.memory_testing:
                        self.convert_test_files('in', dct, pos, i)

                        valgrind_out = CommandManager.cmd_command(
                            ["valgrind", "-q", "./app.exe", *args], input=dct.get('in', '')).stderr
                    else:
                        valgrind_out = ""

                    if self.sm.get('func_tests_in_project'):
                        self.convert_test_files('in', dct, pos, i)
                    elif os.path.isdir(f"{self.sm.app_data_dir}/temp_files"):
                        shutil.rmtree(f"{self.sm.app_data_dir}/temp_files")

                    expected_code = dct.get('exit', '')
                    if expected_code:
                        code_res = res.returncode == int(expected_code)
                    elif pos == 'pos':
                        code_res = res.returncode == 0
                    else:
                        code_res = res.returncode != 0
                    self.test_complete.emit(code_res and comparator_res, prog_out, res.returncode, not valgrind_out,
                                            valgrind_out)
                    sleep(0.01)
                    i += 1
                except JSONDecodeError:
                    pass

        self.end_testing.emit()

    def convert_test_files(self, in_out, dct, pos, i):
        if in_out == 'in':
            iterator = enumerate(dct.get('in_files', []))
        elif in_out == 'out':
            iterator = enumerate(dct.get('out_files', []))
        elif in_out == 'check':
            iterator = dct.get('check_files', []).items()
        else:
            raise ValueError(f'Unknown files type: "{in_out}". Can be only "in", "out" and "check" files')

        for j, file in iterator:
            if file.get('type', 'txt') == 'txt':
                MacrosConverter.convert_txt(file['text'], self.sm.test_in_file_path(pos, i, j, False),
                                            self.sm.get('line_sep'))
            else:
                MacrosConverter.convert_bin(file['text'], self.sm.test_in_file_path(pos, i, j, True))

    def terminate(self) -> None:
        sleep(0.1)
        self.cm.clear_coverage_files()
        super(TestingLooper, self).terminate()
