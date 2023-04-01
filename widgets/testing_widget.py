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

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout1 = QVBoxLayout()
        layout.addLayout(layout1)

        self.options_widget = OptionsWidget({
            'Номер лабы:': {'type': int, 'min': 1, 'initial': self.settings.get('lab', 1),
                            'name': OptionsWidget.NAME_LEFT},
            'Номер задания:': {'type': int, 'min': 1, 'initial': self.settings.get('task', 1),
                               'name': OptionsWidget.NAME_LEFT},
            'Номер варианта:': {'type': int, 'min': -1, 'initial': self.settings.get('var', 0),
                                'name': OptionsWidget.NAME_LEFT}
        })
        self.options_widget.clicked.connect(self.option_changed)
        layout1.addWidget(self.options_widget)

        self.button = QPushButton('Тестировать')
        layout1.addWidget(self.button)
        self.button.clicked.connect(self.button_pressed)
        self.button.setFixedWidth(180)

        self.code_widget = QTextEdit()
        self.code_widget.setFont(QFont("Courier", 10))
        self.code_widget.setReadOnly(True)
        layout1.addWidget(self.code_widget)

        layout2 = QVBoxLayout()
        layout.addLayout(layout2)

        self.coverage_label = QLabel()
        layout2.addWidget(self.coverage_label)
        self.tests_list = QListWidget()
        self.tests_list.itemSelectionChanged.connect(self.open_test_info)
        layout2.addWidget(self.tests_list)

        layout2.addWidget(QLabel("Входные данные"))
        self.in_data = QTextEdit()
        self.in_data.setReadOnly(True)
        self.in_data.setFont(QFont("Courier", 10))
        layout2.addWidget(self.in_data)

        layout3 = QVBoxLayout()
        layout.addLayout(layout3)

        layout3.addWidget(QLabel("Вывод программы"))
        self.prog_out = QTextEdit()
        self.prog_out.setReadOnly(True)
        self.prog_out.setFont(QFont("Courier", 10))
        layout3.addWidget(self.prog_out)

        layout3.addWidget(QLabel("Эталонный вывод"))
        self.out_data = QTextEdit()
        self.out_data.setReadOnly(True)
        self.out_data.setFont(QFont("Courier", 10))
        layout3.addWidget(self.out_data)

        self.tests = []

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
            self.tests.clear()
            self.in_data.setText("")
            self.out_data.setText("")
            self.prog_out.setText("")
            self.tests_list.clear()
            self.current_task = task
        try:
            self.code_widget.setText("")
            file = open(f"{self.path}/main.c")
            self.code_widget.setText(file.read())
            file.close()
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")

    def open_test_info(self):
        index = self.tests_list.currentRow()
        if index < 0 or index >= len(self.tests):
            return
        test_data = self.tests[self.tests_list.currentRow()]
        self.in_data.setText((test_data[1]))
        self.out_data.setText((test_data[2]))
        self.prog_out.setText((test_data[3]))

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

    def add_list_item(self, res, in_file, out_file, prog_out, name, exit_code):
        self.tests.append((res, in_file, out_file, prog_out, name, exit_code))
        item = self.tests_list.item(self.test_count)
        if res and ('pos' in name and not exit_code or 'neg' in name and exit_code):
            item.setText(f"{name} \tPASSED\texit: {exit_code}")
            item.setForeground(Qt.darkGreen)
            self.add_test.emit(f"{name} \tPASSED", Qt.darkGreen)
        else:
            item.setText(f"{name} \tFAILED\texit: {exit_code}")
            self.add_test.emit(f"{name} \tPASSED", Qt.red)
            item.setForeground(Qt.red)
        self.test_count += 1

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
        self.tests.clear()
        self.tests_list.clear()
        self.current_task = self.settings['lab'], self.settings['task'], self.settings['var']
        self.cm.testing(self.pos_comparator, self.neg_comparator)

        self.cm.looper.test_complete.connect(self.add_list_item)
        self.cm.looper.end_testing.connect(self.end_testing)
        self.cm.looper.testing_terminate.connect(self.testing_is_terminated)

        lst = []

        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt"):
            item = QListWidgetItem(f"pos{i}\tin progress...")
            item.setForeground(Qt.gray)
            self.tests_list.addItem(item)
            lst.append(f"pos{i}\tin progress...")
            i += 1

        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt"):
            item = QListWidgetItem(f"neg{i}\tin progress...")
            item.setForeground(Qt.gray)
            self.tests_list.addItem(item)
            lst.append(f"neg{i}\tin progress...")
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
