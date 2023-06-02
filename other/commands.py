import os
from json import loads, JSONDecodeError
from subprocess import run, TimeoutExpired
import subprocess
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from other.macros_converter import MacrosConverter, background_process_manager


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
        old_dir = os.getcwd()
        os.chdir(self.path)

        compile_res = self.cmd_command(self.sm['compiler'].split() + ["-c"] +
                                       (['--coverage'] if coverage else []) +
                                       list(filter(lambda path: path.endswith('.c'), os.listdir(self.path))) + ["-g"] +
                                       (['-lm'] if self.sm['-lm'] else []))
        if compile_res.returncode:
            os.chdir(old_dir)
            return False, compile_res.stderr

        compile_res = self.cmd_command(self.sm['compiler'].split() +
                                       (['--coverage'] if coverage else []) + ['-o'] +
                                       [f"{self.path}/app.exe"] +
                                       list(filter(lambda path: path.endswith('.o'), os.listdir(self.path))) +
                                       (['-lm'] if self.sm['-lm'] else []))

        if compile_res.returncode:
            os.chdir(old_dir)
            return False, compile_res.stderr

        for file in os.listdir(self.path):
            if file.endswith('.o'):
                os.remove(f"{self.path}/{file}")

        os.chdir(old_dir)
        return True, ''

    def collect_coverage(self):
        total_count = 0
        count = 0

        self.update_path()
        for file in os.listdir(self.path):
            if file.endswith('.c'):
                res = self.cmd_command(["gcov", f"{self.path}/{file}"])
                for line in res.stdout.split('\n'):
                    if "Lines executed:" in line:
                        p, _, c = line.split(":")[1].split()
                        total_count += int(c)
                        count += round(float(p[:-1]) / 100 * int(c))
                        break

        self.clear_coverage_files()

        if total_count == 0:
            return 0
        return count / total_count * 100

    def clear_coverage_files(self):
        for file in os.listdir(self.path):
            if '.gcda' in file or '.gcno' in file or 'temp.txt' in file or '.gcov' in file:
                os.remove(f"{self.path}/{file}")

    def testing(self, pos_comparator, neg_comparator, memory_testing, coverage):
        self.update_path()
        self.looper = TestingLooper(
            self.sm, self.compile, self.sm.lab_path(), f"{self.sm.data_lab_path()}/func_tests",
            pos_comparator, neg_comparator, memory_testing, coverage, time_limit=self.sm.get('time_limit'))
        if f"{self.sm.data_lab_path()}/func_tests" in background_process_manager.dict:
            background_process_manager.dict[f"{self.sm.data_lab_path()}/func_tests"].finished.connect(self.looper.start)
        else:
            self.looper.start()

    def test_count(self):
        count = 0
        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt"):
            count += 1
        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt"):
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
        print(os.getcwd())
        self.res = self.func()
        self.complete.emit(self.res)


class TestingLooper(QThread):
    test_complete = pyqtSignal(bool, dict, int, bool, str)
    test_crash = pyqtSignal(str, int, str)
    test_timeout = pyqtSignal()
    end_testing = pyqtSignal()
    testing_terminate = pyqtSignal(str)

    def __init__(self, sm, compiler, path, data_path, pos_comparator, neg_comparator,
                 memory_testing=False, coverage=False, time_limit=10):
        super(TestingLooper, self).__init__()
        self.time_limit = time_limit
        self.compiler = compiler
        self.memory_testing = memory_testing
        self.path = path
        self.data_path = data_path
        self.pos_comparator = pos_comparator
        self.neg_comparator = neg_comparator
        self.coverage = coverage
        self.sm = sm

    def run(self):
        code, errors = self.compiler(coverage=self.coverage)
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
                        res = CommandManager.cmd_command(
                            f"{self.path}/app.exe {CommandManager.read_file(f'{self.path}/func_tests/data/{pos}_{i + 1:0>2}_args.txt')}",
                            input=dct.get('in', ''), timeout=self.time_limit, shell=True)
                    except TimeoutExpired:
                        self.test_timeout.emit()
                        continue
                    if res.stderr:
                        self.test_crash.emit(res.stdout, res.returncode, res.stderr)
                        continue
                    comparator = self.pos_comparator if pos == 'pos' else self.neg_comparator
                    comparator_res = comparator(dct.get('out', ''), res.stdout)
                    prog_out = {"STDOUT": res.stdout}

                    for j, file in enumerate(dct.get('out_files', [])):
                        if file.get('type', 'txt') == 'txt':
                            text = CommandManager.read_file(f"{self.path}/func_tests/data_files/temp_{j + 1}.txt", '')
                            comparator_res = comparator_res and file.text == text
                            prog_out[f"out_file_{i}.txt"] = text
                        else:
                            text = CommandManager.read_binary(f"{self.path}/func_tests/data_files/temp_{j + 1}.bin",
                                                              b'')
                            comparator_res = comparator_res and CommandManager.read_binary(
                                f"{self.path}/func_tests/data_files/{pos}_{i + 1:0>2}_out{j + 1}.bin", b'') == text
                            prog_out[f"out_file_{i}.txt"] = ' '.join(f"{b:0>3}" for b in text)

                    for j, file in dct.get('check_files', dict()).items():
                        if file.get('type', 'txt') == 'txt':
                            text = CommandManager.read_file(
                                f"{self.path}/func_tests/data_files/{pos}_{i + 1:0>2}_in{j}.txt", '')
                            comparator_res = comparator_res and file.text == text
                            prog_out[f"in_file_{i}.txt"] = text
                        else:
                            text = CommandManager.read_binary(
                                f"{self.path}/func_tests/data_files/{pos}_{i + 1:0>2}_in{j}.bin", b'')
                            comparator_res = comparator_res and CommandManager.read_binary(
                                f"{self.path}/func_tests/data_files/{pos}_{i + 1:0>2}_check{j}.bin", b'') == text
                            prog_out[f"in_file_{i}.txt"] = ' '.join(f"{b:0>3}" for b in text)

                    for j, file in enumerate(dct.get('in_files', [])):
                        if file.get('type', 'txt') == 'txt':
                            MacrosConverter.convert_txt(
                                file['text'], f"{self.path}/func_tests/data_files/{pos}_{i + 1:0>2}_in{j + 1}.txt",
                                self.sm.get('line_sep'))
                        else:
                            MacrosConverter.convert_bin(
                                file['text'], f"{self.path}/func_tests/data_files/{pos}_{i + 1:0>2}_in{j + 1}.bin")

                    if self.memory_testing:
                        valgrind_out = CommandManager.cmd_command(
                            ["valgrind", "-q", "./app.exe", dct.get('args', '')], input=dct.get('in', '')).stderr
                    else:
                        valgrind_out = ""

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

        # if os.path.isdir(f"{self.data_path}/neg"):
        #     lst = list(filter(lambda s: s.rstrip('.json').isdigit(), os.listdir(f"{self.data_path}/neg")))
        #     lst.sort(key=lambda s: int(s.rstrip('.json')))
        #     for i, el in enumerate(lst):
        #         try:
        #             dct = loads(CommandManager.read_file(f"{self.data_path}/neg/{el}"))
        #             try:
        #                 res = CommandManager.cmd_command(
        #                     f"{self.path}/app.exe {CommandManager.read_file(f'{self.path}/func_tests/data/neg_{i + 1:0>2}_args.txt')}",
        #                     input=dct.get('in', ''), timeout=self.time_limit, shell=True)
        #             except TimeoutExpired:
        #                 self.test_timeout.emit()
        #                 continue
        #             if res.stderr:
        #                 self.test_crash.emit(res.stdout, res.returncode, res.stderr)
        #                 continue
        #             comparator_res = self.neg_comparator(dct.get('out', ''), res.stdout)
        #
        #             for j, file in enumerate(dct.get('out_files', [])):
        #                 if file.get('type', 'txt') == 'txt':
        #                     comparator_res = comparator_res and file.text == CommandManager.read_file(
        #                         f"{self.path}/func_tests/data_files/temp_{j + 1}.txt", '')
        #                 else:
        #                     comparator_res = comparator_res and CommandManager.read_binary(
        #                         f"{self.path}/func_tests/data_files/_{i + 1:0>2}_out{j + 1}.bin", b'') == \
        #                                      CommandManager.read_binary(
        #                                          f"{self.path}/func_tests/data_files/temp_{j + 1}.bin", b'')
        #
        #             for j, file in dct.get('check_files', dict()).items():
        #                 if file.get('type', 'txt') == 'txt':
        #                     comparator_res = comparator_res and file.text == CommandManager.read_file(
        #                         f"{self.path}/func_tests/data_files/_{i + 1:0>2}_in{j}.txt", '')
        #                 else:
        #                     comparator_res = comparator_res and CommandManager.read_binary(
        #                         f"{self.path}/func_tests/data_files/_{i + 1:0>2}_check{j}.bin", b'') == \
        #                                      CommandManager.read_binary(
        #                                          f"{self.path}/func_tests/data_files/_{i + 1:0>2}_in{j}.bin", b'')
        #
        #             for j, file in enumerate(dct.get('in_files', [])):
        #                 if file.get('type', 'txt') == 'txt':
        #                     MacrosConverter.convert_txt(
        #                         file['text'], f"{self.path}/func_tests/data_files/neg_{i + 1:0>2}_in{j + 1}.txt",
        #                         self.sm.get('line_sep'))
        #                 else:
        #                     MacrosConverter.convert_bin(
        #                         file['text'], f"{self.path}/func_tests/data_files/neg_{i + 1:0>2}_in{j + 1}.bin")
        #
        #             if self.memory_testing:
        #                 valgrind_out = CommandManager.cmd_command(
        #                     ["valgrind", "-q", "./app.exe", dct.get('args', '')], input=dct.get('in', '')).stderr
        #             else:
        #                 valgrind_out = ""
        #
        #             expected_code = dct.get('exit', None)
        #             expected_code = int(expected_code) if expected_code else None
        #             self.test_complete.emit(
        #                 (res.returncode if expected_code is None else res.returncode == expected_code) and
        #                 comparator_res, res.stdout, res.returncode, not valgrind_out, valgrind_out)
        #             sleep(0.1)
        #             i += 1
        #         except JSONDecodeError:
        #             pass

        self.end_testing.emit()

    def terminate(self) -> None:
        sleep(0.1)
        for file in os.listdir(self.path):
            if '.gcda' in file or '.gcno' in file or 'temp.txt' in file or '.gcov' in file:
                os.remove(f"{self.path}/{file}")
        super(TestingLooper, self).terminate()
