import json
import os
import shutil
from subprocess import TimeoutExpired
from time import sleep

from PyQt5.QtCore import pyqtSignal, Qt, QThread
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QLabel, QHBoxLayout, QVBoxLayout, QTextEdit, \
    QPushButton, QProgressBar, QComboBox, QLineEdit, QScrollArea, QSizePolicy

from code_tab.compiler_errors_window import CompilerErrorWindow
from tests.binary_decoder import decode, comparator as bytes_comparator
from tests.commands import CommandManager
from tests.macros_converter import MacrosConverter
from ui.message_box import MessageBox


class TestingWidget(QWidget):
    showTab = pyqtSignal()
    startTesting = pyqtSignal()
    save_tests = pyqtSignal()
    jump_to_code = pyqtSignal(str, int, int)

    def __init__(self, sm, cm, tm, side_panel):
        super(TestingWidget, self).__init__()
        self.sm = sm
        self.cm = cm
        self.tm = tm
        self.side_panel = side_panel
        self.labels = []

        self.tests = []
        self.test_count = {'pos': 0, 'neg': 0, 'completed': 0}

        self.side_list = side_panel.tabs['tests']

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.sm.finishChangeTask.connect(self.open_task)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setAlignment(Qt.AlignLeft)

        self.button = QPushButton('Тестировать')
        top_layout.addWidget(self.button)
        self.button.clicked.connect(self.button_pressed)
        self.button.setFixedSize(180, 26)

        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        self.progress_bar.setFixedSize(200, 26)
        top_layout.addWidget(self.progress_bar)

        self.coverage_bar = QLabel()
        self.labels.append(self.coverage_bar)
        self.coverage_bar.setAlignment(Qt.AlignCenter)
        self.coverage_bar.hide()
        self.coverage_bar.setFixedSize(200, 26)
        top_layout.addWidget(self.coverage_bar)

        self.pos_result_bar = TestCountIndicator(self.tm, "POS:")
        self.labels.append(self.pos_result_bar)
        self.pos_result_bar.hide()
        top_layout.addWidget(self.pos_result_bar)

        self.neg_result_bar = TestCountIndicator(self.tm, "NEG:")
        self.labels.append(self.neg_result_bar)
        self.neg_result_bar.hide()
        top_layout.addWidget(self.neg_result_bar)

        layout.addLayout(top_layout)

        layout2 = QHBoxLayout()
        layout.addLayout(layout2)

        l = QVBoxLayout()
        layout2.addLayout(l)
        h_l = QHBoxLayout()
        l.addLayout(h_l)
        # h_l.addWidget(label := QLabel("Общая информация:"))
        # self.labels.append(label)
        # self.test_name_bar = QLineEdit()
        # self.test_name_bar.setReadOnly(True)
        # h_l.addWidget(self.test_name_bar)

        self.info_widget = TestInfoWidget(self.tm)
        l.addWidget(self.info_widget)

        l = QVBoxLayout()
        layout2.addLayout(l)
        h_l = QHBoxLayout()
        l.addLayout(h_l)
        h_l.addWidget(label := QLabel("Вывод программы"))
        self.labels.append(label)
        self.prog_out_combo_box = QComboBox()
        self.prog_out_combo_box.currentIndexChanged.connect(self.prog_out_combo_box_triggered)
        h_l.addWidget(self.prog_out_combo_box)
        self.prog_out = QTextEdit()
        self.prog_out.setReadOnly(True)
        self.prog_out.setFont(QFont("Courier", 10))
        l.addWidget(self.prog_out)

        layout3 = QHBoxLayout()
        layout.addLayout(layout3)

        l = QVBoxLayout()
        layout3.addLayout(l)
        h_l = QHBoxLayout()
        l.addLayout(h_l)
        h_l.addWidget(label := QLabel("Входные данные"))
        self.labels.append(label)
        self.in_data_combo_box = QComboBox()
        self.in_data_combo_box.currentIndexChanged.connect(self.in_data_combo_box_triggered)
        h_l.addWidget(self.in_data_combo_box)
        self.in_data = QTextEdit()
        self.in_data.setReadOnly(True)
        self.in_data.setFont(QFont("Courier", 10))
        l.addWidget(self.in_data)

        l = QVBoxLayout()
        layout3.addLayout(l)
        h_l = QHBoxLayout()
        l.addLayout(h_l)
        h_l.addWidget(label := QLabel("Выходные данные"))
        self.labels.append(label)
        self.out_data_combo_box = QComboBox()
        self.out_data_combo_box.currentIndexChanged.connect(self.out_data_combo_box_triggered)
        h_l.addWidget(self.out_data_combo_box)
        self.out_data = QTextEdit()
        self.out_data.setReadOnly(True)
        self.out_data.setFont(QFont("Courier", 10))
        l.addWidget(self.out_data)

        self.old_dir = os.getcwd()
        self.ui_disable_func = None
        self.side_list.jump_to_testing.connect(self.open_test_info)
        self.testing_looper = None

        self.current_item = None

    def set_theme(self):
        for el in [self.button, self.progress_bar, self.prog_out_combo_box, self.in_data_combo_box,
                   self.out_data_combo_box]:
            self.tm.auto_css(el)
        for el in [self.prog_out, self.in_data, self.out_data]:
            self.tm.auto_css(el, code_font=True)
        for label in self.labels:
            label.setFont(self.tm.font_small)
        self.info_widget.set_theme()
        self.pos_result_bar.set_theme()
        self.neg_result_bar.set_theme()

    def open_task(self):
        self.test_mode(False)
        self.in_data.setText("")
        self.out_data.setText("")
        self.prog_out.setText("")
        self.side_list.clear()

    def open_test_info(self, index=None, *args):
        if index is not None:
            if isinstance(self.current_item, Test):
                pass
                # self.current_item.unload()
            self.current_item = self.tests[index]
            # self.current_item.load()
        if isinstance(self.current_item, Test):
            current_in, current_out = self.current_item.get('current_in', 0), self.current_item.get('current_out', 0)

            self.in_data_combo_box.clear()
            self.in_data_combo_box.addItems(self.current_item.in_data.keys())
            self.in_data.setText(self.current_item.get('in', ''))
            self.out_data_combo_box.clear()
            self.out_data_combo_box.addItems(self.current_item.out_data.keys())
            self.out_data.setText(self.current_item.get('out', ''))
            self.prog_out_combo_box.clear()
            self.prog_out_combo_box.addItems(self.current_item.prog_out.keys())
            self.prog_out.setText(self.current_item.prog_out.get('STDOUT', ''))
            self.info_widget.set_test(self.current_item)
            self.info_widget.open_test_info()

            self.in_data_combo_box.setCurrentIndex(current_in)
            self.out_data_combo_box.setCurrentIndex(current_out)

    def in_data_combo_box_triggered(self):
        self.in_data.setText(self.current_item.in_data.get(self.in_data_combo_box.currentText(), ''))

    def out_data_combo_box_triggered(self):
        self.out_data.setText(self.current_item.out_data.get(self.out_data_combo_box.currentText(), ''))

    def prog_out_combo_box_triggered(self):
        self.prog_out.setText(self.current_item.prog_out.get(self.prog_out_combo_box.currentText(), ''))

    def button_pressed(self, *args):
        if self.button.text() == "Тестировать":
            self.testing()
        else:
            self.stop_testing()

    def stop_testing(self):
        self.testing_looper.terminate()
        self.button.setText("Тестировать")
        self.testing_is_terminated(None)

    def test_mode(self, flag=True):
        if flag:
            self.showTab.emit()
            self.old_dir = os.getcwd()
            os.chdir(self.sm.lab_path())

            self.side_list.buttons['run'].hide()
            self.side_list.buttons['cancel'].show()
            self.button.setText("Прервать")

            self.coverage_bar.hide()
            self.progress_bar.show()
            self.pos_result_bar.show()
            self.neg_result_bar.show()
        else:
            self.side_list.buttons['run'].show()
            self.side_list.buttons['cancel'].hide()
            self.button.setText("Тестировать")
            self.button.setDisabled(False)
            os.chdir(self.old_dir)

    def clear_tests(self):
        self.tests.clear()
        self.side_list.clear()

    def add_test(self, path, name, test_type):
        self.tests.append(test := Test(path, name, test_type))
        self.side_list.add_item(test)

    def set_tests_status(self, index, status):
        if status in [Test.PASSED, Test.FAILED, Test.TIMEOUT]:
            self.test_count['completed'] += 1
        if self.tests[index].type() == 'pos':
            self.pos_result_bar.add_test(status)
        else:
            self.neg_result_bar.add_test(status)

        self.progress_bar.setValue(self.test_count['completed'])

        self.tests[index].set_status(status)
        self.side_list.set_status(index, status)

    def load_tests(self):
        for key in self.test_count:
            self.test_count[key] = 0
        for pos in ['pos', 'neg']:
            data_dir = f"{self.sm.data_lab_path()}/func_tests"
            if os.path.isdir(f"{data_dir}/{pos}"):
                lst = list(filter(lambda s: s.rstrip('.json').isdigit(), os.listdir(f"{data_dir}/{pos}")))
                lst.sort(key=lambda s: int(s.rstrip('.json')))
                for i, el in enumerate(lst):
                    self.add_test(f"{data_dir}/{pos}/{el}", f"{pos}{i + 1}", pos)
                    self.test_count[pos] += 1

    def count(self):
        return self.test_count['pos'] + self.test_count['neg']

    def testing(self):
        self.startTesting.emit()
        try:
            self.cm.clear_coverage_files()
        except FileNotFoundError:
            MessageBox(MessageBox.Warning, "Ошибка",
                       "Папки с данным заданием не существует. Тестирование невозможно", self.tm)
            return

        self.test_mode(True)
        self.clear_tests()
        self.load_tests()

        self.pos_result_bar.set_count(self.test_count['pos'])
        self.neg_result_bar.set_count(self.test_count['neg'])

        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.count())
        self.progress_bar.setValue(0)

        command = self.sm.get_task('preprocessor', '')
        if command:
            self.looper = self.cm.cmd_command_looper(command, shell=True)
            self.looper.finished.connect(self.start_testing)
            self.looper.start()
        else:
            self.start_testing()

    def start_testing(self):
        self.testing_looper = TestingLooper(self.sm, self.cm, self.tests)
        self.testing_looper.testStatusChanged.connect(self.set_tests_status)
        self.testing_looper.compileFailed.connect(self.testing_is_terminated)
        self.testing_looper.finished.connect(self.end_testing)
        self.testing_looper.start()

    def end_testing(self):
        self.progress_bar.hide()
        self.coverage_bar.show()

        if self.sm.get_smart('coverage', False):
            self.coverage_bar.setText(f"Coverage: {self.cm.collect_coverage():.1f}%")
        else:
            self.coverage_bar.setText("")

        command = self.sm.get_task('postprocessor', '')
        if command:
            self.looper = self.cm.cmd_command_looper(command, shell=True)
            self.looper.finished.connect(lambda: self.test_mode(False))
            self.looper.start()
        else:
            self.test_mode(False)

    def testing_is_terminated(self, errors=''):
        self.progress_bar.hide()
        self.coverage_bar.show()

        if self.sm.get_smart('coverage', False):
            self.coverage_bar.setText(f"Coverage: {self.cm.collect_coverage():.1f}%")

        if errors:
            dialog = CompilerErrorWindow(errors, os.listdir(self.sm.lab_path()), self.tm)
            if dialog.exec():
                if dialog.goto:
                    self.jump_to_code.emit(*dialog.goto)

        for i in range(self.test_count['completed'], self.count()):
            self.side_list.set_status(i, Test.TERMINATED)

        self.cm.clear_coverage_files()

        try:
            with open(f"{self.sm.data_lab_path()}/settings.json") as f:
                settings = json.loads(f.read())
                command = settings.get('postprocessor')
        except FileNotFoundError:
            command = ''
        except json.JSONDecodeError:
            command = ''
        if command:
            self.looper = self.cm.cmd_command_looper(command, shell=True)
            self.looper.finished.connect(lambda: self.test_mode(False))
            self.looper.start()
        else:
            self.test_mode(False)


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


def read_file(path, default=None):
    if default is not None:
        try:
            file = open(path, encoding='utf-8')
            res = file.read()
            file.close()
            return res
        except:
            return default
    file = open(path, encoding='utf-8')
    res = file.read()
    file.close()
    return res


class Test:
    IN_PROGRESS = 0
    PASSED = 1
    FAILED = 2
    TERMINATED = 3
    TIMEOUT = 4

    def __init__(self, path, name, test_type='pos'):
        self._path = path
        self._name = name
        self._test_type = test_type
        self._data = None

        self.in_data = dict()
        self.out_data = dict()
        self.prog_out = dict()
        self.utils_output = dict()

        self.load()
        self._status = Test.IN_PROGRESS

        self.exit = 0
        self.args = ''
        self.results = dict()

    def status(self):
        return self._status

    def res(self):
        return all(self.results.values())

    def name(self):
        return self._name

    def set_status(self, status):
        self._status = status

    def type(self):
        return self._test_type

    def load(self):
        try:
            with open(self._path, encoding='utf-8') as f:
                self._data = json.loads(f.read())
                self.in_data = {'STDIN': self.get('in', '')}
                self.out_data = {'STDOUT': self.get('out', '')}
                for i, el in enumerate(self.get('in_files', [])):
                    self.in_data[f"in_file_{i + 1}.{el['type']}"] = el['text']
                    if 'check' in el:
                        self.out_data[f"check_file_{i + 1}.{el['type']}"] = el['check']
                for i, el in enumerate(self.get('out_files', [])):
                    self.out_data[f"out_file_{i + 1}.{el['type']}"] = el['text']
        except json.JSONDecodeError:
            self._data = dict()

    def unload(self):
        self._data = None
        self.in_data.clear()
        self.out_data.clear()

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value


class TestingLooper(QThread):
    testStatusChanged = pyqtSignal(int, int)
    compileFailed = pyqtSignal(str)

    def __init__(self, sm, cm: CommandManager, tests: list[Test]):
        super(TestingLooper, self).__init__()
        self.sm = sm
        self.cm = cm
        self._tests = tests
        self._coverage = self.sm.get_smart('coverage')

    def prepare_test(self, test: Test, index: int):
        if self.sm.get('func_tests_in_project'):
            test.args = CommandManager.read_file(self.sm.test_args_path(test.type(), index))
        else:
            test.args = MacrosConverter.convert_args(
                test.get('args', ''), '', test.type(), index,
                {j + 1: self.sm.test_in_file_path(test.type(), index, j, binary=d.get('type', 'txt') == 'bin')
                 for j, d in enumerate(test.get('in_files', []))},
                {j + 1: self.sm.test_out_file_path(test.type(), index, j, binary=d.get('type', 'txt') == 'bin')
                 for j, d in enumerate(test.get('out_files', []))},
                f"{self.sm.app_data_dir}/temp_files")
            self.convert_test_files('in', test, test.type(), index)
            self.convert_test_files('out', test, test.type(), index)
            self.convert_test_files('check', test, test.type(), index)

    def pos_comparator(self, str1, str2):
        comparator = self.sm.get('pos_comparators', dict()).get(
            f"{self.sm.get('lab')}_{self.sm.get('task')}_{self.sm.get('var')}", -1)
        if comparator == -1:
            comparator = self.sm.get_smart('pos_comparator', 0)
        if comparator == 0:
            return comparator1(str1, str2, self.sm.get_smart('epsilon', 0))
        if comparator == 1:
            return comparator2(str1, str2)
        if comparator == 2:
            return comparator3(str1, str2, self.sm.get_smart('pos_substring', ''))
        if comparator == 3:
            return comparator4(str1, str2, self.sm.get_smart('pos_substring', ''))
        if comparator == 4:
            return comparator5(str1, str2)
        if comparator == 5:
            return comparator6(str1, str2)

    def neg_comparator(self, str1, str2):
        comparator = self.sm.get('neg_comparators', dict()).get(
            f"{self.sm.get('lab')}_{self.sm.get('task')}_{self.sm.get('var')}", -1)
        if comparator == -1:
            comparator = self.sm.get_smart('neg_comparator', 0)
        if comparator == 0:
            return True
        if comparator == 1:
            return comparator1(str1, str2, self.sm.get_smart('epsilon', 0))
        if comparator == 2:
            return comparator2(str1, str2)
        if comparator == 3:
            return comparator3(str1, str2, self.sm.get_smart('neg_substring', ''))
        if comparator == 4:
            return comparator4(str1, str2, self.sm.get_smart('neg_substring', ''))
        if comparator == 5:
            return comparator5(str1, str2)
        if comparator == 6:
            return comparator6(str1, str2)

    def comparator(self, test: Test, str1, str2):
        if test.type() == 'pos':
            return self.pos_comparator(str1, str2)
        return self.neg_comparator(str1, str2)

    def run_comparators(self, test: Test, index: int):
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
            path = "" if self.sm.get('func_tests_in_project') else f"{self.sm.app_data_dir}/temp_files/"
            if file.get('type', 'txt') == 'txt':
                text = CommandManager.read_file(f"{path}temp_{j + 1}.txt", '')
                test.results[f"out_file_{j + 1}.txt"] = self.comparator(test, file['text'], text)
                test.prog_out[f"out_file_{j + 1}.txt"] = text
            else:
                text = CommandManager.read_binary(f"{path}temp_{j + 1}.bin", b'')
                test.results[f"out_file_{j + 1}.bin"] = bytes_comparator(
                    text, file['text'],
                    CommandManager.read_binary(self.sm.test_out_file_path(test.type(), index, j, True), b''))
                test.prog_out[f"out_file_{j + 1}.bin"], _ = decode(file['text'], text)

        for j, file in enumerate(test.get('in_files', [])):
            if 'check' in file:
                if file.get('type', 'txt') == 'txt':
                    text = CommandManager.read_file(self.sm.test_in_file_path(test.type(), index, j, False), '')
                    test.results[f"in_file_{j + 1}.txt"] = self.comparator(test, file['check'], text)
                    test.prog_out[f"in_file_{j + 1}.txt"] = text
                else:
                    text = CommandManager.read_binary(self.sm.test_in_file_path(test.type(), index, j, True), b'')
                    test.results[f"in_file_{j + 1}.bin"] = bytes_comparator(
                        text, file['check'], CommandManager.read_binary(
                            self.sm.test_check_file_path(test.type(), index, j, True), b''))
                    test.prog_out[f"in_file_{j + 1}.bin"], _ = decode(file['check'], text)

    def clear_after_run(self, test: Test, index: int):
        if self.sm.get('func_tests_in_project'):
            self.convert_test_files('in', test, test.type(), index)
        elif os.path.isdir(f"{self.sm.app_data_dir}/temp_files"):
            shutil.rmtree(f"{self.sm.app_data_dir}/temp_files")

    def run_util(self, test: Test, index: int, util_data: dict):
        name = util_data.get('program', 'error_unknown_program')
        if name.startswith('wsl -e '):
            name = os.path.basename(name.split()[2])
        else:
            name = os.path.basename(name.split()[0])
        temp_path = f"{self.sm.app_data_dir}/temp_files/dist.txt"
        res = self.cm.cmd_command(util_data.get('program', '').format(app='./app.exe', file='main.c',
                                                                      args=test.get('args', ''), dict=temp_path),
                                  shell=True, input=test['in'])
        if util_data.get('type', 0) == 0:
            if util_data.get('output_format', 0) == 0:
                output = res.stdout
            elif util_data.get('output_format', 0) == 1:
                output = res.stderr
            else:
                output = read_file(temp_path, default='')
            test.utils_output[name] = output
            test.results[name] = True
            if util_data.get('output_res', False):
                test.results[name] = test.results[name] and not bool(output)
            if util_data.get('exit_code_res', False):
                test.results[name] = test.results[name] and res.returncode == 0
        self.clear_after_run(test, index)

    def run_test(self, test: Test, index: int):
        self.prepare_test(test, index)
        try:
            res = self.cm.run_main_code(test.args, test.get('in', ''), coverage=self._coverage)
            test.exit = res.returncode
            test.prog_out = {'STDOUT': res.stdout}
            self.run_comparators(test, index)
            self.clear_after_run(test, index)
            utils = self.sm.get_smart(f"{self.sm.get('language', 'C')}_utils", [])
            if isinstance(utils, str):
                try:
                    utils = json.loads(utils)
                    for util in utils:
                        self.run_util(test, index, util)
                except json.JSONDecodeError:
                    pass
            test.set_status(Test.PASSED if test.res() else Test.FAILED)
        except TimeoutExpired:
            test.set_status(Test.TIMEOUT)
        self.clear_after_run(test, index)

    def run(self):
        code, errors = self.cm.compile(coverage=self._coverage)
        if not code:
            self.compileFailed.emit(errors)
            return

        pos_count = 0
        for i, test in enumerate(self._tests):
            if self._tests[i].type() == 'pos':
                pos_count += 1
                index = i
            else:
                index = i - pos_count

            self.run_test(test, index)

            self.testStatusChanged.emit(i, test.status())
            sleep(0.01)
            i += 1

    def convert_test_files(self, in_out, test, pos, i):
        if in_out == 'in':
            iterator = enumerate(test.get('in_files', []))
        elif in_out == 'out':
            iterator = enumerate(test.get('out_files', []))
        elif in_out == 'check':
            iterator = test.get('check_files', []).items()
        else:
            raise ValueError(f'Unknown files type: "{in_out}". Can be only "in", "out" and "check" files')

        for j, file in iterator:
            if file.get('type', 'txt') == 'txt':
                MacrosConverter.convert_txt(file['text'], self.sm.test_in_file_path(pos, i, j, False),
                                            self.sm.line_sep)
            else:
                MacrosConverter.convert_bin(file['text'], self.sm.test_in_file_path(pos, i, j, True))

    def terminate(self) -> None:
        sleep(0.1)
        self.cm.clear_coverage_files()
        super(TestingLooper, self).terminate()


class SimpleField(QWidget):
    def __init__(self, tm, name, text):
        super().__init__()
        self._tm = tm

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._label = QLabel(f"{name} {text}")
        layout.addWidget(self._label)

    def set_theme(self):
        for el in [self._label]:
            self._tm.auto_css(el)


class LineField(QWidget):
    def __init__(self, tm, name, text):
        super().__init__()
        self._tm = tm

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._label = QLabel(name)
        layout.addWidget(self._label)

        self._line_edit = QLineEdit()
        self._line_edit.setText(text)
        self._line_edit.setReadOnly(True)
        layout.addWidget(self._line_edit)

    def set_theme(self):
        for el in [self._label, self._line_edit]:
            self._tm.auto_css(el)


class TextField(QWidget):
    def __init__(self, tm, name, text):
        super().__init__()
        self._tm = tm

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._label = QLabel(name)
        layout.addWidget(self._label)

        self._text_edit = QLabel()
        self._text_edit.setText(text)
        self._text_edit.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        layout.addWidget(self._text_edit)

    def set_theme(self):
        for el in [self._label]:
            self._tm.auto_css(el)
        self._text_edit.setStyleSheet(self._tm.base_css())
        self._text_edit.setFont(self._tm.code_font)


class _ListFieldItem(QListWidgetItem):
    def __init__(self, tm, name, status):
        super().__init__()
        self._tm = tm
        self._status = status
        self.setText(name)

    def set_theme(self):
        self.setFont(self._tm.font_small)
        if self._status:
            self.setIcon(QIcon(self._tm.get_image('passed', color=self._tm['TestPassed'])))
            self.setForeground(self._tm['TestPassed'])
        else:
            self.setIcon(QIcon(self._tm.get_image('failed', color=self._tm['TestFailed'])))
            self.setForeground(self._tm['TestFailed'])


class ListField(QWidget):
    def __init__(self, tm, name, dct: dict):
        super().__init__()
        self._tm = tm

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._label = QLabel(name)
        layout.addWidget(self._label)

        self._list_widget = QListWidget()
        self._list_widget.setMinimumHeight(len(dct) * 22 + 2)
        layout.addWidget(self._list_widget)
        for key, item in dct.items():
            self._list_widget.addItem(_ListFieldItem(tm, key, item))

    def set_theme(self):
        for el in [self._label, self._list_widget]:
            self._tm.auto_css(el, palette='Bg', border=False)


class TestInfoWidget(QScrollArea):
    def __init__(self, tm):
        super().__init__()
        self._tm = tm
        self._test = None

        scroll_widget = QWidget()
        self.setWidget(scroll_widget)
        self.setWidgetResizable(True)

        self._scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(self._scroll_layout)
        self._scroll_layout.setAlignment(Qt.AlignTop)

        self._widgets = []

    def clear(self):
        for el in self._widgets:
            el.setParent(None)
        self._widgets.clear()

    def add_widget(self, widget):
        self._scroll_layout.addWidget(widget)
        self._widgets.append(widget)
        if hasattr(widget, 'set_theme'):
            widget.set_theme()

    def open_test_info(self):
        self.clear()
        self.add_widget(LineField(self._tm, "Описание:", self._test['desc']))
        self.add_widget(LineField(self._tm, "Аргументы:", self._test['args']))
        if self._test.status() in (Test.PASSED, Test.FAILED):
            if self._test.get('exit', ''):
                self.add_widget(SimpleField(self._tm, "Код возврата:", f"{self._test.exit} ({self._test['exit']})"))
            else:
                self.add_widget(SimpleField(self._tm, "Код возврата:", self._test.exit))
            self.add_widget(ListField(self._tm, "Результаты:", self._test.results))

            for key, item in self._test.utils_output.items():
                self.add_widget(TextField(self._tm, key, item))

    def set_test(self, test: Test):
        self._test = test

    def set_theme(self):
        self._tm.auto_css(self, palette='Bg', border=False)
        for el in self._widgets:
            if hasattr(el, 'set_theme'):
                el.set_theme()


class TestCountIndicator(QLabel):
    def __init__(self, tm, name='POS:'):
        super().__init__()
        self._tm = tm
        self._name = name

        self.setFixedSize(125, 26)
        self.setAlignment(Qt.AlignCenter)

        self._count = 0
        self._passed = 0
        self._completed = 0

    def set_text(self):
        self.setText(f"{self._name} {self._passed}/{self._count}")

    def set_count(self, count):
        self._passed = 0
        self._completed = 0
        self._count = count
        self.set_text()
        self.set_theme()

    def add_test(self, status):
        self._completed += 1
        if status == Test.PASSED:
            self._passed += 1
        self.set_text()
        self.set_theme()

    def _get_color(self):
        if self._passed == self._count:
            return self._tm['TestPassed'].name()
        if self._passed == self._completed:
            return self._tm['TextColor']
        return self._tm['TestFailed'].name()

    def set_theme(self):
        self.setFont(self._tm.font_small)
        self.setStyleSheet(f"color: {self._get_color()};")
