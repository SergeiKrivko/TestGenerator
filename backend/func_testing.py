import json
import os
import shutil
from subprocess import TimeoutExpired
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from backend.commands import read_file, read_binary, cmd_command
from backend.types.func_test import FuncTest
from backend.types.project import Project
from backend.types.util import Util
from language.utils import get_files
from other.binary_redactor.binary_decoder import decode, comparator as bytes_comparator
from backend.macros_converter import MacrosConverter


class TestingLooper(QThread):
    testStatusChanged = pyqtSignal(FuncTest, int)
    compileFailed = pyqtSignal(str)
    utilFailed = pyqtSignal(str, str, str)

    def __init__(self, sm, project: Project, manager, tests: list[FuncTest]):
        super(TestingLooper, self).__init__()
        self.sm = sm
        self._project = project
        self._manager = manager
        self.tests = tests
        self.path = self._project.path()
        self.util_res = dict()
        self.util_output = dict()
        self.utils = []
        self.coverage = None
        self.coverage_html = None
        self._temp_dir = f"{self.sm.temp_dir()}/out"
        self._build_id = self._project.get('build')
        self._build = None
        if self._build_id is not None:
            self._build = self._manager.get_build(self._build_id)

    def prepare_test(self, test: FuncTest, index: int):
        if self._project.get('func_tests_in_project'):
            test.args = read_file(self._project.test_args_path(test.type(), index), '')
        else:
            test.args = MacrosConverter.convert_args(
                test.get('args', ''), '', test.type(), index,
                {j + 1: self._project.test_in_file_path(test.type(), index, j, binary=d.get('type', 'txt') == 'bin')
                 for j, d in enumerate(test.get('in_files', []))},
                {j + 1: self._project.test_out_file_path(test.type(), index, j, binary=d.get('type', 'txt') == 'bin')
                 for j, d in enumerate(test.get('out_files', []))}, self._temp_dir)
            self.convert_test_files('in', test, test.type(), index)
            self.convert_test_files('out', test, test.type(), index)
            self.convert_test_files('check', test, test.type(), index)

    def pos_comparator(self, str1, str2):
        comparator = self._project.get('pos_comparator', -1)
        if comparator == -1:
            comparator = self._project.get('pos_comparator', 0)
        if comparator == 0:
            return comparator1(str1, str2, self._project.get('epsilon', 0))
        if comparator == 1:
            return comparator2(str1, str2)
        if comparator == 2:
            return comparator3(str1, str2, self._project.get('pos_substring', ''))
        if comparator == 3:
            return comparator4(str1, str2, self._project.get('pos_substring', ''))
        if comparator == 4:
            return comparator5(str1, str2)
        if comparator == 5:
            return comparator6(str1, str2)

    def neg_comparator(self, str1, str2):
        comparator = self._project.get('neg_comparator', -1)
        if comparator == -1:
            comparator = self._project.get('neg_comparator', 0)
        if comparator == 0:
            return True
        if comparator == 1:
            return comparator1(str1, str2, self._project.get('epsilon', 0))
        if comparator == 2:
            return comparator2(str1, str2)
        if comparator == 3:
            return comparator3(str1, str2, self._project.get('neg_substring', ''))
        if comparator == 4:
            return comparator4(str1, str2, self._project.get('neg_substring', ''))
        if comparator == 5:
            return comparator5(str1, str2)
        if comparator == 6:
            return comparator6(str1, str2)

    def comparator(self, test: FuncTest, str1, str2):
        if test.type() == 'pos':
            return self.pos_comparator(str1, str2)
        return self.neg_comparator(str1, str2)

    def run_comparators(self, test: FuncTest, index: int):
        test.results['STDOUT'] = self.comparator(test, test.get('out', ''), test.prog_out.get('STDOUT'))

        expected_code = test.get('exit', '')
        if expected_code:
            code_res = test.exit == int(expected_code)
        elif test.type() == 'pos':
            code_res = test.exit == 0
        else:
            code_res = test.exit != 0
        test.results['Exit code'] = code_res

        for j, file in enumerate(test.get('out_files', [])):
            path = self._project.temp_dir() + '/' if self._project.get('func_tests_in_project') else \
                f"{self._temp_dir}/"
            if file.get('type', 'txt') == 'txt':
                text = read_file(f"{path}temp_{j + 1}.txt", '')
                test.results[f"out_file_{j + 1}.txt"] = self.comparator(test, file['text'], text)
                test.prog_out[f"out_file_{j + 1}.txt"] = text
            else:
                text = read_binary(f"{path}temp_{j + 1}.bin", b'')
                test.results[f"out_file_{j + 1}.bin"] = bytes_comparator(
                    text, file['text'],
                    read_binary(self._project.test_out_file_path(test.type(), index, j, True), b''))
                test.prog_out[f"out_file_{j + 1}.bin"], _ = decode(file['text'], text)

        for j, file in enumerate(test.get('in_files', [])):
            if 'check' in file:
                if file.get('type', 'txt') == 'txt':
                    text = read_file(self._project.test_in_file_path(test.type(), index, j, False), '')
                    test.results[f"in_file_{j + 1}.txt"] = self.comparator(test, file['check'], text)
                    test.prog_out[f"in_file_{j + 1}.txt"] = text
                else:
                    text = read_binary(self._project.test_in_file_path(test.type(), index, j, True), b'')
                    test.results[f"in_file_{j + 1}.bin"] = bytes_comparator(
                        text, file['check'], read_binary(
                            self._project.test_check_file_path(test.type(), index, j, True), b''))
                    test.prog_out[f"in_file_{j + 1}.bin"], _ = decode(file['check'], text)

    def clear_after_run(self, test: FuncTest, index: int):
        if self._project.get('func_tests_in_project'):
            self.convert_test_files('in', test, test.type(), index)
        elif os.path.isdir(self._temp_dir):
            shutil.rmtree(self._temp_dir)

    @staticmethod
    def parse_util_name(data: dict):
        name = data.get('program', 'error_unknown_program')
        if name.startswith('wsl -e '):
            name = os.path.basename(name.split()[2])
        elif not name.strip():
            name = 'unknown_program'
        else:
            name = os.path.basename(name.split()[0])
        return name

    def run_preproc_util(self, util: Util):
        if util is None:
            return
        if util.get('type', 0) != 1:
            return
        name = self.parse_util_name(util)
        temp_path = f"{self._temp_dir}/dist.txt"
        res = cmd_command(util.get('program', '').format(app='./app.exe', file='main.c', dict=temp_path,
                                                         files=' '.join(get_files(self.path, '.c'))),
                          shell=True, cwd=self.path)
        if util.get('1_output_format', 0) == 0:
            output = res.stdout
        elif util.get('1_output_format', 0) == 1:
            output = res.stderr
        else:
            output = read_file(temp_path, default='')
        result = True
        if util.get('1_output_res', False):
            result = result and not bool(output)
        if util.get('1_exit_code_res', False):
            result = result and res.returncode == 0
        # self.util_res[name] = result
        # self.util_output[name] = output
        if not result:
            self.utilFailed.emit(name, output, util.get('1_mask', ''))
            # if not util.get('1_continue_testing', True):
            #     self.terminate()

    def run_postproc_util(self, util: Util):
        if util is None:
            return
        if util.get('type', 0) != 2:
            return
        name = self.parse_util_name(util)
        temp_path = f"{self._temp_dir}/dist.txt"
        res = cmd_command(util.get('program', '').format(app='./app.exe', file='main.c', dict=temp_path,
                                                         files=' '.join(get_files(self.path, '.c'))),
                          shell=True, cwd=self.path)
        if util.get('2_output_format', 0) == 0:
            output = res.stdout
        elif util.get('2_output_format', 0) == 1:
            output = res.stderr
        else:
            output = read_file(temp_path, default='')
        result = True
        if util.get('2_output_res', False):
            result = result and not bool(output)
        if util.get('2_exit_code_res', False):
            result = result and res.returncode == 0
        for el in self.tests:
            el.utils_output[name] = output
            el.results[name] = result

    def run_test_util(self, test: FuncTest, index: int, util: Util):
        if util is None:
            return
        if util.get('type', 1) != 1:
            return
        name = util.get('name', '-')
        temp_path = f"{self._temp_dir}/dist.txt"
        res, output = util.run(self._project, self._build, test.args, input=test.get('in', ''))
        test.results[name] = res
        test.utils_output[name] = output
        self.clear_after_run(test, index)

    def run_test(self, test: FuncTest, index: int):
        self.prepare_test(test, index)
        try:
            res = self._manager.run_build(self._project.get('build'), test.args, test.get('in', ''))
            test.exit = res.returncode
            test.prog_out = {'STDOUT': res.stdout, 'STDERR': res.stderr}
            self.run_comparators(test, index)
            self.clear_after_run(test, index)

            for util in self.utils:
                self.run_test_util(test, index, util)
            test.set_status(FuncTest.PASSED if test.res() else FuncTest.FAILED)
        except TimeoutExpired:
            test.set_status(FuncTest.TIMEOUT)
        self.clear_after_run(test, index)

    def run(self):
        if self._build is None:
            self.compileFailed.emit("Invalid build data!")
            return
        res, errors = self._manager.compile_build(self._build_id, self._project)
        if not res:
            self.compileFailed.emit(errors)
            return
        command = self._project.get('preprocessor', [])
        self._manager.run_scenarios(command, self.path)

        self.utils = [self._manager.get_util(item['data']) for item in self._build.get('utils', [])]
        for util in self.utils:
            self.run_preproc_util(util)

        pos_count = 0
        for i, test in enumerate(self.tests):
            if self.tests[i].type() == 'pos':
                pos_count += 1
                index = i
            else:
                index = i - pos_count

            self.run_test(test, index)

            self.testStatusChanged.emit(test, test.status())
            sleep(0.01)
            i += 1

        for util in self.utils:
            self.run_postproc_util(util)
        command = self._project.get('postprocessor', '')
        self._manager.run_scenarios(command, self.path)

        self.coverage, self.coverage_html = self._manager.collect_coverage(self._project.get('build'), self._project)

    def convert_test_files(self, in_out, test, pos, i):
        if in_out == 'in':
            iterator = enumerate(test.get('in_files', []))
            key = 'text'
        elif in_out == 'out':
            iterator = enumerate(test.get('out_files', []))
            key = 'text'
        elif in_out == 'check':
            iterator = enumerate(test.get('in_files', []))
            key = 'check'
        else:
            raise ValueError(f'Unknown files type: "{in_out}". Can be only "in", "out" and "check" files')

        for j, file in iterator:
            if key in file:
                if file.get('type', 'txt') == 'txt':
                    MacrosConverter.convert_txt(file[key], self._project.test_in_file_path(pos, i, j, False),
                                                self.sm.line_sep)
                else:
                    MacrosConverter.convert_bin(file[key], self._project.test_in_file_path(pos, i, j, True))

    def terminate(self) -> None:
        sleep(0.1)
        # self.cm.clear_coverage_files()
        super(TestingLooper, self).terminate()


def comparator1(str1, str2, eps=0):
    lst1 = []
    for word in str1.split():
        try:
            lst1.append(float(word))
        except Exception:
            pass

    lst2 = []
    for word in str2.split():
        try:
            lst2.append(float(word))
        except Exception:
            pass

    if len(lst1) != len(lst2):
        return False

    for a, b in zip(lst1, lst2):
        if abs(a - b) > float(eps):
            return False
    return True


def comparator2(str1, str2):
    lst1 = []
    for word in str1.split():
        try:
            float(word)
            lst1.append(word)
        except Exception:
            pass

    lst2 = []
    for word in str2.split():
        try:
            float(word)
            lst2.append(word)
        except Exception:
            pass

    return lst1 == lst2


def comparator3(str1, str2, substring):
    if substring not in str1 or substring not in str2:
        return False

    return str1[str1.index(substring):] == str2[str2.index(substring):]


def comparator4(str1, str2, substring):
    if substring not in str1 or substring not in str2:
        return False

    return str1[str1.index(substring):].split() == str2[str2.index(substring):].split()


def comparator5(str1, str2):
    return str1.replace('\r', '') == str2.replace('\r', '')


def comparator6(str1, str2):
    return str1.split() == str2.split()
