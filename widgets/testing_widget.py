import os

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QLabel, QHBoxLayout, QVBoxLayout, QTextEdit, \
    QPushButton, QMessageBox
from widgets.options_window import OptionsWidget


class TestingWidget(QWidget):
    testing_start = pyqtSignal(list)
    add_test = pyqtSignal(str, QColor)
    clear_tests = pyqtSignal()
    testing_end = pyqtSignal()

    def __init__(self, settings, cm):
        super(TestingWidget, self).__init__()
        self.settings = settings
        self.cm = cm

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.options_widget = OptionsWidget({
            'h_line': {
                'Номер лабы:': {'type': int, 'min': 1, 'initial': self.settings.get('lab', 1),
                                'name': OptionsWidget.NAME_LEFT, 'width': 60},
                'Номер задания:': {'type': int, 'min': 1, 'initial': self.settings.get('task', 1),
                                   'name': OptionsWidget.NAME_LEFT, 'width': 60},
                'Номер варианта:': {'type': int, 'min': -1, 'initial': self.settings.get('var', 0),
                                    'name': OptionsWidget.NAME_LEFT, 'width': 60}
            }
        })
        self.options_widget.clicked.connect(self.option_changed)
        layout.addWidget(self.options_widget)

        self.button = QPushButton('Тестировать')
        layout.addWidget(self.button)
        self.button.clicked.connect(self.button_pressed)
        self.button.setFixedWidth(180)

        layout2 = QHBoxLayout()
        layout.addLayout(layout2)

        l = QVBoxLayout()
        layout2.addLayout(l)
        self.coverage_label = QLabel()
        l.addWidget(self.coverage_label)
        self.tests_list = QListWidget()
        self.tests_list.itemSelectionChanged.connect(self.open_test_info)
        l.addWidget(self.tests_list)

        l = QVBoxLayout()
        layout2.addLayout(l)
        l.addWidget(QLabel("Вывод программы"))
        self.prog_out = QTextEdit()
        self.prog_out.setReadOnly(True)
        self.prog_out.setFont(QFont("Courier", 10))
        l.addWidget(self.prog_out)

        layout3 = QHBoxLayout()
        layout.addLayout(layout3)

        l = QVBoxLayout()
        layout3.addLayout(l)
        l.addWidget(QLabel("Входные данные"))
        self.in_data = QTextEdit()
        self.in_data.setReadOnly(True)
        self.in_data.setFont(QFont("Courier", 10))
        l.addWidget(self.in_data)

        l = QVBoxLayout()
        layout3.addLayout(l)
        l.addWidget(QLabel("Эталонный вывод"))
        self.out_data = QTextEdit()
        self.out_data.setReadOnly(True)
        self.out_data.setFont(QFont("Courier", 10))
        l.addWidget(self.out_data)

        self.current_task = (0, 0, 0)
        self.old_dir = os.getcwd()
        self.ui_disable_func = None
        self.test_count = 0

    def option_changed(self, key):
        if key in ('Номер лабы:', 'Номер задания:'):
            self.settings['lab'] = self.options_widget["Номер лабы:"]
            self.settings['task'] = self.options_widget["Номер задания:"]
            if os.path.isdir(self.settings['path'] + f"/lab_{self.options_widget['Номер лабы:']:0>2}_"
                                                     f"{self.options_widget['Номер задания:']:0>2}"):
                self.options_widget.set_value('Номер варианта:', -1)
            else:
                for i in range(100):
                    if os.path.isdir(self.settings['path'] + f"/lab_{self.options_widget['Номер лабы:']:0>2}_"
                                                             f"{self.options_widget['Номер задания:']:0>2}_{i:0>2}"):
                        self.options_widget.set_value('Номер варианта:', i)
                        break
            self.settings['var'] = self.options_widget["Номер варианта:"]
            self.open_task()
        elif key == 'Номер варианта:':
            self.settings['var'] = self.options_widget["Номер варианта:"]
            self.open_task()

    def update_options(self):
        self.options_widget.set_value('Номер лабы:', self.settings.get('lab', self.options_widget['Номер лабы:']))
        self.options_widget.set_value('Номер задания:',
                                      self.settings.get('task', self.options_widget['Номер задания:']))
        self.options_widget.set_value('Номер варианта:',
                                      self.settings.get('var', self.options_widget['Номер варианта:']))

    def open_task(self):
        self.get_path()
        task = self.settings['lab'], self.settings['task'], self.settings['var']
        if task != self.current_task:
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
            if self.settings['var'] == -1:
                self.path = self.settings['path'] + f"/lab_{self.settings['lab']:0>2}_" \
                                                    f"{self.settings['task']:0>2}"
            else:
                self.path = self.settings['path'] + f"/lab_{self.settings['lab']:0>2}_" \
                                                    f"{self.settings['task']:0>2}_" \
                                                    f"{self.settings['var']:0>2}"
        elif self.options_widget['Номер варианта:'] == -1:
            self.path = self.settings['path'] + f"/lab_{self.options_widget['Номер лабы:']:0>2}_" \
                                                f"{self.options_widget['Номер задания:']:0>2}"
        else:
            self.path = self.settings['path'] + f"/lab_{self.options_widget['Номер лабы:']:0>2}_" \
                                                f"{self.options_widget['Номер задания:']:0>2}_" \
                                                f"{self.options_widget['Номер варианта:']:0>2}"

    def add_list_item(self, res, prog_out, exit_code, memory_res, valgrind_out):
        self.tests_list.item(self.test_count).set_completed(res, prog_out, exit_code, memory_res, valgrind_out)
        self.add_test.emit(f"{self.tests_list.item(self.test_count).name:6}  {'PASSED' if res else 'FAILED'}",
                           Qt.darkGreen if res and memory_res else Qt.red)
        self.test_count += 1
        self.open_test_info()

    def button_pressed(self, *args):
        if self.button.text() == "Тестировать":
            self.testing()
        else:
            self.stop_testing()

    def stop_testing(self):
        self.cm.looper.terminate()
        self.cm.looper.wait()
        self.button.setText("Тестировать")

    def testing(self):
        self.options_widget.setDisabled(True)
        self.ui_disable_func(True)
        self.button.setText("Прервать тестирование")
        self.button.setDisabled(True)

        self.get_path(True)
        self.old_dir = os.getcwd()
        os.chdir(self.path)

        if self.isHidden():
            self.get_path(True)
        self.tests_list.clear()
        self.current_task = self.settings['lab'], self.settings['task'], self.settings['var']
        self.cm.testing(self.pos_comparator, self.neg_comparator)

        self.cm.looper.test_complete.connect(self.add_list_item)
        self.cm.looper.end_testing.connect(self.end_testing)
        self.cm.looper.testing_terminate.connect(self.testing_is_terminated)

        lst = []

        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt"):
            self.tests_list.addItem(TestingListWidgetItem(
                f"pos{i}", read_file(f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt"),
                read_file(f"{self.path}/func_tests/data/pos_{i:0>2}_out.txt")))
            lst.append(f"pos{i}")
            i += 1

        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt"):
            self.tests_list.addItem(TestingListWidgetItem(
                f"neg{i}", read_file(f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt"),
                read_file(f"{self.path}/func_tests/data/neg_{i:0>2}_out.txt")))
            lst.append(f"neg{i}")
            i += 1

        self.test_count = 0
        self.testing_start.emit(lst)

    def end_testing(self):
        self.options_widget.setDisabled(False)
        self.ui_disable_func(False)
        self.button.setText("Тестировать")
        self.button.setDisabled(False)

        if os.path.isfile(f"{self.path}/temp.txt"):
            os.remove(f"{self.path}/temp.txt")
        self.testing_end.emit()

        self.coverage_label.setText(f"Coverage: {self.cm.collect_coverage():.1f}%")

        os.chdir(self.old_dir)

    def testing_is_terminated(self, errors):
        self.options_widget.setDisabled(False)
        self.ui_disable_func(False)
        self.button.setText("Тестировать")
        self.button.setDisabled(False)

        if os.path.isfile(f"{self.path}/temp.txt"):
            os.remove(f"{self.path}/temp.txt")
        self.testing_end.emit()

        QMessageBox.warning(self, "Error", errors)

        for i in range(self.test_count, self.tests_list.count()):
            self.tests_list.item(i).set_terminated()

        self.cm.clear_coverage_files()

        os.chdir(self.old_dir)

    def pos_comparator(self, path1, path2):
        comparator = self.settings.get('pos_comparator', (0, {'value': 0}))
        if comparator[0] == 0:
            return comparator1(path1, path2, comparator[1]['value'])
        if comparator[0] == 1:
            return comparator2(path1, path2)
        if comparator[0] == 2:
            return comparator3(path1, path2, comparator[1]['value'])

    def neg_comparator(self, path1, path2):
        comparator = self.settings.get('neg_comparator', (0, {'value': 0}))
        if comparator[0] == 0:
            return True
        if comparator[0] == 1:
            return comparator1(path1, path2, comparator[1]['value'])
        if comparator[0] == 2:
            return comparator2(path1, path2)
        if comparator[0] == 3:
            return comparator3(path1, path2, comparator[1]['value'])

    def show(self) -> None:
        self.update_options()
        self.open_task()
        super(TestingWidget, self).show()


def comparator1(path1, path2, eps=0):
    lst1 = []
    for word in read_file(path1).split():
        try:
            lst1.append(float(word))
        except Exception:
            pass

    lst2 = []
    for word in read_file(path2).split():
        try:
            lst2.append(float(word))
        except Exception:
            pass

    for a, b in zip(lst1, lst2):
        if abs(a - b) > eps:
            return False
    return True


def comparator2(path1, path2):
    lst1 = []
    for word in read_file(path1).split():
        try:
            float(word)
            lst1.append(word)
        except Exception:
            pass

    lst2 = []
    for word in read_file(path2).split():
        try:
            float(word)
            lst2.append(word)
        except Exception:
            pass

    return lst1 == lst2


def comparator3(path1, path2, substring):
    text1 = read_file(path1)
    text2 = read_file(path2)
    if substring not in text1 or substring not in text2:
        return False

    return text1[text1.index(substring):] == text2[text2.index(substring):]


def read_file(path):
    file = open(path, encoding='utf-8')
    res = file.read()
    file.close()
    return res


class TestingListWidgetItem(QListWidgetItem):
    in_progress = 0
    passed = 1
    failed = 2
    terminated = 3

    def __init__(self, name, in_data, out_data):
        super(TestingListWidgetItem, self).__init__()
        self.setText(f"{name:6}  in progress…")
        self.setForeground(Qt.gray)
        self.name = name
        self.in_data = in_data
        self.out_data = out_data
        self.status = TestingListWidgetItem.in_progress
        self.prog_out = ''
        self.exit_code = 0
        self.setFont(QFont("Courier", 10))

    def set_completed(self, res, prog_out, exit_code, memory_res, valgrind_out):
        self.status = TestingListWidgetItem.passed if res else TestingListWidgetItem.failed
        self.prog_out = prog_out
        self.exit_code = exit_code
        self.setText(f"{self.name:6}  {'PASSED' if res else 'FAILED'}    exit: {exit_code:<5} "
                     f"{'MEMORY_OK' if memory_res else 'MEMORY_FAIL'}")
        self.setToolTip(valgrind_out)
        self.setForeground(Qt.darkGreen if res and memory_res else Qt.red)

    def set_terminated(self, message="terminated"):
        self.status = TestingListWidgetItem.terminated
        self.setText(f"{self.name:6}  {message}")
        self.setForeground(Qt.gray)
