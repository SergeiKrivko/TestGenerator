import os

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QLabel, QHBoxLayout, QVBoxLayout, QTextEdit, \
    QPushButton, QProgressBar

from widgets.message_box import MessageBox
from widgets.options_window import OptionsWidget


class TestingWidget(QWidget):
    testing_start = pyqtSignal(list)
    add_test = pyqtSignal(str, QColor)
    clear_tests = pyqtSignal()
    testing_end = pyqtSignal()

    def __init__(self, sm, cm, tm):
        super(TestingWidget, self).__init__()
        self.sm = sm
        self.cm = cm
        self.tm = tm
        self.labels = []

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.options_widget = OptionsWidget({
            'h_line': {
                'Номер лабы:': {'type': int, 'min': 1, 'name': OptionsWidget.NAME_LEFT, 'width': 60},
                'Номер задания:': {'type': int, 'min': 1, 'name': OptionsWidget.NAME_LEFT, 'width': 60},
                'Номер варианта:': {'type': int, 'min': -1, 'name': OptionsWidget.NAME_LEFT, 'width': 60}
            }
        })
        self.options_widget.clicked.connect(self.option_changed)
        layout.addWidget(self.options_widget)

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

        self.pos_result_bar = QLabel()
        self.labels.append(self.pos_result_bar)
        self.pos_result_bar.hide()
        self.pos_result_bar.setFixedSize(125, 26)
        self.pos_result_bar.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.pos_result_bar)

        self.neg_result_bar = QLabel()
        self.labels.append(self.neg_result_bar)
        self.neg_result_bar.hide()
        self.neg_result_bar.setFixedSize(125, 26)
        self.neg_result_bar.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.neg_result_bar)

        layout.addLayout(top_layout)

        layout2 = QHBoxLayout()
        layout.addLayout(layout2)

        l = QVBoxLayout()
        layout2.addLayout(l)
        l.addWidget(label := QLabel("Список тестов"))
        self.labels.append(label)
        self.tests_list = QListWidget()
        self.tests_list.itemSelectionChanged.connect(self.open_test_info)
        l.addWidget(self.tests_list)

        l = QVBoxLayout()
        layout2.addLayout(l)
        l.addWidget(label := QLabel("Вывод программы"))
        self.labels.append(label)
        self.prog_out = QTextEdit()
        self.prog_out.setReadOnly(True)
        self.prog_out.setFont(QFont("Courier", 10))
        l.addWidget(self.prog_out)

        layout3 = QHBoxLayout()
        layout.addLayout(layout3)

        l = QVBoxLayout()
        layout3.addLayout(l)
        l.addWidget(label := QLabel("Входные данные"))
        self.labels.append(label)
        self.in_data = QTextEdit()
        self.in_data.setReadOnly(True)
        self.in_data.setFont(QFont("Courier", 10))
        l.addWidget(self.in_data)

        l = QVBoxLayout()
        layout3.addLayout(l)
        l.addWidget(label := QLabel("Эталонный вывод"))
        self.labels.append(label)
        self.out_data = QTextEdit()
        self.out_data.setReadOnly(True)
        self.out_data.setFont(QFont("Courier", 10))
        l.addWidget(self.out_data)

        self.current_task = (0, 0, 0)
        self.old_dir = os.getcwd()
        self.ui_disable_func = None
        self.test_count = 0

    def set_theme(self):
        self.button.setStyleSheet(self.tm.buttons_style_sheet)
        self.button.setFont(self.tm.font_small)
        self.tm.set_theme_to_list_widget(self.tests_list)
        self.prog_out.setStyleSheet(self.tm.text_edit_style_sheet)
        self.prog_out.setFont(self.tm.font_small)
        self.in_data.setStyleSheet(self.tm.text_edit_style_sheet)
        self.in_data.setFont(self.tm.font_small)
        self.out_data.setStyleSheet(self.tm.text_edit_style_sheet)
        self.out_data.setFont(self.tm.font_small)
        self.progress_bar.setStyleSheet(self.tm.progress_bar_style_sheet)
        self.progress_bar.setFont(self.tm.font_small)
        self.options_widget.set_widget_style_sheet('Номер лабы:', self.tm.spin_box_style_sheet)
        self.options_widget.set_widget_style_sheet('Номер задания:', self.tm.spin_box_style_sheet)
        self.options_widget.set_widget_style_sheet('Номер варианта:', self.tm.spin_box_style_sheet)
        self.options_widget.setFont(self.tm.font_small)
        for label in self.labels:
            label.setFont(self.tm.font_small)

    def option_changed(self, key):
        if key in ('Номер лабы:', 'Номер задания:'):
            self.sm.set('lab', self.options_widget["Номер лабы:"])
            self.sm.set('task', self.options_widget["Номер задания:"])
            if os.path.isdir(self.sm.lab_path(self.options_widget['Номер лабы:'],
                                              self.options_widget['Номер задания:'], -1)):
                self.options_widget.set_value('Номер варианта:', -1)
            else:
                for i in range(100):
                    if os.path.isdir(self.sm.lab_path(self.options_widget['Номер лабы:'],
                                                      self.options_widget['Номер задания:'], i)):
                        self.options_widget.set_value('Номер варианта:', i)
                        break
            self.sm.set('var', self.options_widget["Номер варианта:"])
            self.open_task()
        elif key == 'Номер варианта:':
            self.sm.set('var', self.options_widget["Номер варианта:"])
            self.open_task()

    def update_options(self):
        self.options_widget.set_value('Номер лабы:', self.sm.get('lab', self.options_widget['Номер лабы:']))
        self.options_widget.set_value('Номер задания:',
                                      self.sm.get('task', self.options_widget['Номер задания:']))
        self.options_widget.set_value('Номер варианта:',
                                      self.sm.get('var', self.options_widget['Номер варианта:']))

    def open_task(self):
        self.get_path()
        task = self.sm['lab'], self.sm['task'], self.sm['var']
        if task != self.current_task:
            self.coverage_bar.hide()
            self.progress_bar.hide()
            self.pos_result_bar.hide()
            self.neg_result_bar.hide()

            self.in_data.setText("")
            self.out_data.setText("")
            self.prog_out.setText("")
            self.tests_list.clear()
            self.current_task = task

    def open_test_info(self):
        item = self.tests_list.currentItem()
        if isinstance(item, TestingListWidgetItem):
            self.in_data.setText(item.in_data)
            self.out_data.setText(item.out_data)
            self.prog_out.setText(item.prog_out)

    def get_path(self, from_settings=False):
        if from_settings:
            self.path = self.sm.lab_path()
        else:
            self.path = self.sm.lab_path(self.options_widget['Номер лабы:'], self.options_widget['Номер задания:'],
                                         self.options_widget['Номер варианта:'])

    def add_list_item(self, res, prog_out, exit_code, memory_res, valgrind_out):
        self.progress_bar.setValue(self.progress_bar.value() + 1)
        self.tests_list.item(self.test_count).set_completed(res, prog_out, exit_code, memory_res, valgrind_out)
        self.modify_testing_res(self.tests_list.item(self.test_count).text()[:3], res and memory_res)
        self.add_test.emit(f"{self.tests_list.item(self.test_count).name:6}  {'PASSED' if res else 'FAILED'}",
                           self.tm['TestPassed'] if res and memory_res else self.tm['TestFailed'])
        self.test_count += 1
        self.open_test_info()

    def add_crash_list_item(self, prog_out, exit_code, prog_errors):
        self.progress_bar.setValue(self.progress_bar.value() + 1)
        self.tests_list.item(self.test_count).set_crashed(prog_out, exit_code, prog_errors)
        self.modify_testing_res(self.tests_list.item(self.test_count).text()[:3], False)
        self.add_test.emit(f"{self.tests_list.item(self.test_count).name:6}  CRASHED", self.tm['TestCrashed'])
        self.test_count += 1
        self.open_test_info()

    def add_timeout_list_item(self):
        self.tests_list.item(self.test_count).set_timeout()
        self.progress_bar.setValue(self.progress_bar.value() + 1)
        self.modify_testing_res(self.tests_list.item(self.test_count).text()[:3], False)
        self.add_test.emit(f"{self.tests_list.item(self.test_count).name:6}  TIMEOUT", self.tm['TestFailed'])
        self.test_count += 1
        self.open_test_info()
        
    def modify_testing_res(self, test_type='pos', res=True):
        widget = self.pos_result_bar if test_type == 'pos' else self.neg_result_bar
        if not res:
            widget.setStyleSheet(f"color: {self.tm['TestFailed'].name()};")
        else:
            lst = widget.text().split()
            lst2 = lst[1].split('/')
            widget.setText(f"{lst[0]} {int(lst2[0]) + 1}/{lst2[1]}")
            if int(lst2[0]) + 1 == int(lst2[1]):
                widget.setStyleSheet(f"color: {self.tm['TestPassed'].name()};")

    def button_pressed(self, *args):
        if self.button.text() == "Тестировать":
            self.testing()
        else:
            self.stop_testing()

    def stop_testing(self):
        self.cm.looper.terminate()
        self.cm.looper.wait()
        self.button.setText("Тестировать")
        self.testing_is_terminated(None)

    def testing(self):
        self.options_widget.setDisabled(True)
        self.ui_disable_func(True)
        self.button.setText("Прервать")

        self.coverage_bar.hide()
        self.progress_bar.show()
        self.pos_result_bar.show()
        self.neg_result_bar.show()

        self.get_path(True)
        self.old_dir = os.getcwd()
        os.chdir(self.path)

        if self.isHidden():
            self.get_path(True)
        self.tests_list.clear()
        self.current_task = self.sm['lab'], self.sm['task'], self.sm['var']

        lst = []

        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt"):
            self.tests_list.addItem(TestingListWidgetItem(
                self.tm, f"pos{i}", read_file(f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt"),
                read_file(f"{self.path}/func_tests/data/pos_{i:0>2}_out.txt"),
                self.sm.get('memory_testing', False)))
            lst.append(f"pos{i}")
            i += 1

        self.pos_result_bar.setStyleSheet(f"color: {self.tm['TextColor']};")
        self.pos_result_bar.setText(f"POS: 0/{i - 1}")

        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt"):
            self.tests_list.addItem(TestingListWidgetItem(
                self.tm, f"neg{i}", read_file(f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt"),
                read_file(f"{self.path}/func_tests/data/neg_{i:0>2}_out.txt"),
                self.sm.get('memory_testing', False)))
            lst.append(f"neg{i}")
            i += 1

        self.neg_result_bar.setStyleSheet(f"color: {self.tm['TextColor']};")
        self.neg_result_bar.setText(f"NEG: 0/{i - 1}")

        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(len(lst))
        self.progress_bar.setValue(0)

        if command := read_file(f"{self.sm.lab_path(appdata=True)}/func_tests/preprocessor.txt", ''):
            self.looper = self.cm.cmd_command_looper(command, shell=True)
            self.looper.finished.connect(lambda: self.start_testing(lst))
            self.looper.start()
        else:
            self.start_testing(lst)

    def start_testing(self, lst):
        self.cm.testing(self.pos_comparator, self.neg_comparator, self.sm.get('memory_testing', False),
                        self.sm.get('coverage', False))

        self.cm.looper.test_complete.connect(self.add_list_item)
        self.cm.looper.test_crash.connect(self.add_crash_list_item)
        self.cm.looper.test_timeout.connect(self.add_timeout_list_item)
        self.cm.looper.end_testing.connect(self.end_testing)
        self.cm.looper.testing_terminate.connect(self.testing_is_terminated)

        self.test_count = 0
        self.testing_start.emit(lst)

    def end_testing(self):
        self.progress_bar.hide()
        self.coverage_bar.show()

        if os.path.isfile(f"{self.path}/temp.txt"):
            os.remove(f"{self.path}/temp.txt")
        self.testing_end.emit()

        if self.sm.get('coverage', False):
            self.coverage_bar.setText(f"Coverage: {self.cm.collect_coverage():.1f}%")

        if command := read_file(f"{self.sm.lab_path(appdata=True)}/func_tests/postprocessor.txt", ''):
            self.looper = self.cm.cmd_command_looper(command, shell=True)
            self.looper.finished.connect(self.enable_ui)
            self.looper.start()
        else:
            self.enable_ui()

    def testing_is_terminated(self, errors):
        self.progress_bar.hide()
        self.coverage_bar.show()

        if self.sm.get('coverage', False):
            self.coverage_bar.setText(f"Coverage: {self.cm.collect_coverage():.1f}%")

        if os.path.isfile(f"{self.path}/temp.txt"):
            os.remove(f"{self.path}/temp.txt")
        self.testing_end.emit()

        if errors:
            MessageBox(MessageBox.Warning, "Error", errors, self.tm)

        for i in range(self.test_count, self.tests_list.count()):
            self.tests_list.item(i).set_terminated()

        self.cm.clear_coverage_files()

        if command := read_file(f"{self.sm.lab_path(appdata=True)}/func_tests/postprocessor.txt", ''):
            self.looper = self.cm.cmd_command_looper(command, shell=True)
            self.looper.finished.connect(self.enable_ui)
            self.looper.start()
        else:
            self.enable_ui()

    def enable_ui(self):
        self.options_widget.setDisabled(False)
        self.ui_disable_func(False)
        self.button.setText("Тестировать")
        self.button.setDisabled(False)
        os.chdir(self.old_dir)

    def pos_comparator(self, str1, str2):
        comparator = self.sm.get('pos_comparators', dict()).get(
            f"{self.sm.get('lab')}_{self.sm.get('task')}_{self.sm.get('var')}", -1)
        if comparator == -1:
            comparator = self.sm.get('pos_comparator', 0)
        if comparator == 0:
            return comparator1(str1, str2, self.sm.get('epsilon', 0))
        if comparator == 1:
            return comparator2(str1, str2)
        if comparator == 2:
            return comparator3(str1, str2, self.sm.get('pos_substring', ''))
        if comparator == 3:
            return comparator4(str1, str2, self.sm.get('pos_substring', ''))
        if comparator == 4:
            return comparator5(str1, str2)
        if comparator == 5:
            return comparator6(str1, str2)

    def neg_comparator(self, str1, str2):
        comparator = self.sm.get('neg_comparators', dict()).get(
            f"{self.sm.get('lab')}_{self.sm.get('task')}_{self.sm.get('var')}", -1)
        if comparator == -1:
            comparator = self.sm.get('neg_comparator', 0)
        if comparator == 0:
            return True
        if comparator == 1:
            return comparator1(str1, str2, self.sm.get('epsilon', 0))
        if comparator == 2:
            return comparator2(str1, str2)
        if comparator == 3:
            return comparator3(str1, str2, self.sm.get('neg_substring', ''))
        if comparator == 4:
            return comparator4(str1, str2, self.sm.get('neg_substring', ''))
        if comparator == 5:
            return comparator5(str1, str2)
        if comparator == 6:
            return comparator6(str1, str2)

    def show(self) -> None:
        self.update_options()
        self.open_task()
        super(TestingWidget, self).show()


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
    return str1 == str2


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


class TestingListWidgetItem(QListWidgetItem):
    in_progress = 0
    passed = 1
    failed = 2
    terminated = 3
    crashed = 2

    def __init__(self, tm, name, in_data, out_data, memory_testing=False):
        super(TestingListWidgetItem, self).__init__()
        self.tm = tm
        self.setText(f"{name:6}  in progress…")
        self.setForeground(self.tm['TestInProgress'])
        self.name = name
        self.in_data = in_data
        self.out_data = out_data
        self.status = TestingListWidgetItem.in_progress
        self.prog_out = ''
        self.exit_code = 0
        self.setFont(self.tm.code_font)
        self.memory_testing = memory_testing

    def set_completed(self, res, prog_out, exit_code, memory_res, valgrind_out):
        self.status = TestingListWidgetItem.passed if res else TestingListWidgetItem.failed
        self.prog_out = prog_out
        self.exit_code = exit_code
        if self.memory_testing:
            self.setText(f"{self.name:6}  {'PASSED' if res else 'FAILED'}    exit: {exit_code:<5} "
                         f"{'MEMORY_OK' if memory_res else 'MEMORY_FAIL'}")
            self.setToolTip(valgrind_out)
        else:
            self.setText(f"{self.name:6}  {'PASSED' if res else 'FAILED'}    exit: {exit_code:<5}")
        self.setForeground(self.tm['TestPassed'] if res and memory_res else self.tm['TestFailed'])

    def set_crashed(self, prog_out, exit_code, prog_errors):
        self.status = TestingListWidgetItem.crashed
        self.prog_out = prog_out
        self.exit_code = exit_code
        self.setText(f"{self.name:6}  CRASHED   exit: {exit_code:<5} ")
        self.setToolTip(prog_errors)
        self.setForeground(self.tm['TestCrashed'])

    def set_timeout(self):
        self.status = TestingListWidgetItem.failed
        self.setText(f"{self.name:6}  TIMEOUT")
        self.setForeground(self.tm['TestFailed'])

    def set_terminated(self, message="terminated"):
        self.status = TestingListWidgetItem.terminated
        self.setText(f"{self.name:6}  {message}")
        self.setForeground(self.tm['TestInProgress'])
