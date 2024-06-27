import os
import shutil
from subprocess import TimeoutExpired
from time import sleep, time
from uuid import UUID

from PyQt6.QtCore import pyqtSignal

from src.backend.backend_types import Build
from src.backend.commands import read_file, read_binary, cmd_command, get_files
from src.backend.backend_types.func_test import FuncTest
from src.backend.backend_types.project import Project
from src.backend.backend_types.util import Util
from src.backend.managers._processes import CustomThread
from src.other.binary_redactor.binary_decoder import decode, comparator as bytes_comparator
from src.backend.macros_converter import MacrosConverter


class TestingLooper(CustomThread):
    testStatusChanged = pyqtSignal(FuncTest, object)
    compileFailed = pyqtSignal(str)
    utilFailed = pyqtSignal(str, str, str)

    def __init__(self, bm, project: Project, tests: list[FuncTest], verbose=False):
        super(TestingLooper, self).__init__()
        self._bm = bm
        self._project = project

        self._tests = tests
        self._path = self._project.path()
        self.util_res = dict()
        self.util_output = dict()
        self.utils = []
        self.coverage = None
        self.coverage_html = None
        self._temp_dir = f"{self._bm.sm.temp_dir()}/out"

        self._build = None
        build_id = self._project.get_data('func_tests_build')
        if build_id:
            self._build: Build = self._bm.builds.get(UUID(build_id))

        self._verbose = verbose

    def prepare_test(self, test: FuncTest, index: int):
        if False and self._project.get('func_tests_in_project'):        # TODO: remove False
            test.res.args = read_file(self._project.test_args_path(test.type, index), '')
        else:
            test.res.args = MacrosConverter.convert_args(test, index, self._project)
            self.convert_test_files(test, index)

    def comparator(self, test: FuncTest, str1, str2):
        comparator = FuncTest.Comparator(self._project.get_data(f'{test.type.value}_comparator', 0))
        if comparator == FuncTest.Comparator.DEFAULT:
            comparator = FuncTest.Comparator(self._project.get(f'{test.type.value}_comparator', 0))

        match comparator:
            case FuncTest.Comparator.NONE:
                return True
            case FuncTest.Comparator.NUMBERS:
                return comparator_numbers(str1, str2, self._project.get('epsilon', 0))
            case FuncTest.Comparator.NUMBERS_AS_STRING:
                return comparator_numbers_as_string(str1, str2)
            case FuncTest.Comparator.TEXT_AFTER:
                return comparator_text_after(str1, str2, self._project.get(f'{test.type.value}_substring', ''))
            case FuncTest.Comparator.WORDS_AFTER:
                return comparator_words_after(str1, str2, self._project.get(f'{test.type.value}_substring', ''))
            case FuncTest.Comparator.TEXT:
                return comparator_text(str1, str2)
            case FuncTest.Comparator.WORDS:
                return comparetor_words(str1, str2)

    def run_comparators(self, test: FuncTest, index: int):
        test.res.results['STDOUT'] = self.comparator(test, test.stdout, test.res.files.get('STDOUT'))

        if test.exit:
            code_res = test.res.code == int(test.exit)
        elif test.type == FuncTest.Type.POS:
            code_res = test.res.code == 0
        else:
            code_res = test.res.code != 0
        test.res.results['Exit code'] = code_res

        for j, file in enumerate(test.out_files):
            path = self._project.test_temp_file_path(j, binary=file.type == 'bin')
            if file.type == 'txt':
                text = read_file(path, '')
                test.res.results[f"out_file_{j + 1}.txt"] = self.comparator(test, file.data, text)
                test.res.files[f"out_file_{j + 1}.txt"] = text
            else:
                text = read_binary(path, b'')
                test.res.results[f"out_file_{j + 1}.bin"] = bytes_comparator(
                    text, file.data,
                    read_binary(self._project.test_out_file_path(test.type, index, j, True), b''))
                test.res.files[f"out_file_{j + 1}.bin"], _ = decode(file.data, text)

        for j, file in enumerate(test.in_files):
            if file.check:
                if file.type == 'txt':
                    text = read_file(self._project.test_in_file_path(test.type, index, j, False), '')
                    test.res.results[f"in_file_{j + 1}.txt"] = self.comparator(test, file.check, text)
                    test.res.files[f"in_file_{j + 1}.txt"] = text
                else:
                    text = read_binary(self._project.test_in_file_path(test.type, index, j, True), b'')
                    test.res.results[f"in_file_{j + 1}.bin"] = bytes_comparator(
                        text, file.check, read_binary(
                            self._project.test_check_file_path(test.type, index, j, True), b''))
                    test.res.files[f"in_file_{j + 1}.bin"], _ = decode(file.check, text)

    def clear_after_run(self, test: FuncTest, index: int):
        if self._project.get('func_tests_in_project'):
            self.convert_test_files(test, index, in_only=True)
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
                                                         files=' '.join(get_files(self._path, '.c'))),
                          shell=True, cwd=self._path)
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
                                                         files=' '.join(get_files(self._path, '.c'))),
                          shell=True, cwd=self._path)
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
        for el in self._tests:
            el.utils_output[name] = output
            el.results[name] = result

    def run_test_util(self, test: FuncTest, index: int, util: Util):
        if util is None:
            return
        if util.get('type', 1) != 1:
            return
        name = util.get('name', '-')
        temp_path = f"{self._temp_dir}/dist.txt"
        res, output = util.run(self._project, self._build, test.args, input=test.stdin)
        test.res.results[name] = res
        test.res.utils_output[name] = output
        self.clear_after_run(test, index)

    def run_test(self, test: FuncTest, index: int):
        self.prepare_test(test, index)
        try:
            t = time()
            res = cmd_command(self._build.command(test.res.args), shell=True, input=test.stdin, cwd=self._path)
            t = time() - t

            test.res.code = res.returncode
            test.res.files['STDOUT'] = res.stdout
            test.res.files['STDERR'] = res.stderr
            test.res.time = t

            self.run_comparators(test, index)

            for util in self.utils:
                self.run_test_util(test, index, util)
            test.status = FuncTest.Status.PASSED if all(test.res.results.values()) else FuncTest.Status.FAILED
        except TimeoutExpired:
            test.status = FuncTest.Status.TIMEOUT
        self.clear_after_run(test, index)

    def run(self):
        if self._build is None:
            print('fail 1')
            self.compileFailed.emit("Invalid build data!")
            return
        res, errors = self._build.run_preproc()
        if res:
            res, errors = self._build.compile()
        if not res:
            print('fail 2')
            self.compileFailed.emit(errors)
            return

        self.utils = [self._bm.get(item['data']) for item in self._build.get('utils', [])]
        for util in self.utils:
            self.run_preproc_util(util)

        pos_count = 0
        for i, test in enumerate(self._tests):
            if self._tests[i].type == 'pos':
                pos_count += 1
                index = i
            else:
                index = i - pos_count

            self.run_test(test, index)

            self.testStatusChanged.emit(test, test.status)
            self.progressChanged.emit((i + 1) * 100 // len(self._tests))

            if self._verbose:
                print(f"\033[33m{test.type.value}{index + 1:<4}\033[33m",
                      {FuncTest.Status.PASSED: '\033[32mPASSED\033[0m',
                       FuncTest.Status.FAILED: '\033[31mFAILED\033[0m'}[test.status],
                      '  ', test.description,
                      *[f"\033[{32 if item else 31}m'{key}'\033[33m" for key, item in test.res.results.items()])

            sleep(0.01)

        for util in self.utils:
            self.run_postproc_util(util)
        res, errors = self._build.run_postproc()
        if not res:
            print('fail 3')
            self.compileFailed.emit(errors)
            return

        self.coverage = self._build.coverage()
        self.coverage_html = self._build.coverage_html()

    def convert_test_files(self, test: FuncTest, index, in_only=False):

        for j, file in enumerate(test.in_files):
            if file.type == 'txt':
                MacrosConverter.convert_txt(file.data, self._project.test_in_file_path(
                    test.type, index, j, False), self._bm.sm.line_sep)
            else:
                MacrosConverter.convert_bin(file.data, self._project.test_in_file_path(test.type, index, j, True))

            if file.check and not in_only:
                if file.type == 'txt':
                    MacrosConverter.convert_txt(file.data, self._project.test_check_file_path(
                        test.type, index, j, False), self._bm.sm.line_sep)
                else:
                    MacrosConverter.convert_bin(file.data, self._project.test_check_file_path(
                        test.type, index, j, True))

        if not in_only:
            for j, file in enumerate(test.out_files):
                if file.type == 'txt':
                    MacrosConverter.convert_txt(file.data, self._project.test_out_file_path(
                        test.type, index, j, False), self._bm.sm.line_sep)
                else:
                    MacrosConverter.convert_bin(file.data, self._project.test_out_file_path(test.type, index, j, True))

    def terminate(self) -> None:
        sleep(0.1)
        # self.cm.clear_coverage_files()
        super().terminate()


def comparator_numbers(str1, str2, eps=0):
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


def comparator_numbers_as_string(str1, str2):
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


def comparator_text_after(str1, str2, substring):
    if substring not in str1 or substring not in str2:
        return False

    return str1[str1.index(substring):] == str2[str2.index(substring):]


def comparator_words_after(str1, str2, substring):
    if substring not in str1 or substring not in str2:
        return False

    return str1[str1.index(substring):].split() == str2[str2.index(substring):].split()


def comparator_text(str1, str2):
    return str1.replace('\r', '') == str2.replace('\r', '')


def comparetor_words(str1, str2):
    return str1.split() == str2.split()
