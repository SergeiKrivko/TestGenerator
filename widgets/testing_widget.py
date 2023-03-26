import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QListWidget, QLabel, QHBoxLayout, QVBoxLayout, QTextEdit, QMessageBox, \
    QListWidgetItem
from widgets.options_window import OptionsWidget


class TestingWidget(QWidget):
    testing_signal = pyqtSignal(list)

    def __init__(self, settings):
        super(TestingWidget, self).__init__()
        self.settings = settings

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
                                'name': OptionsWidget.NAME_LEFT},
            'Тестировать': {'type': 'button', 'text': 'Тестировать', 'name': OptionsWidget.NAME_SKIP}
        })
        self.options_widget.clicked.connect(self.option_changed)
        layout1.addWidget(self.options_widget)

        self.code_widget = QTextEdit()
        self.code_widget.setFont(QFont("Courier", 10))
        self.code_widget.setReadOnly(True)
        layout1.addWidget(self.code_widget)

        layout2 = QVBoxLayout()
        layout.addLayout(layout2)

        layout2.addWidget(QLabel("Список тестов"))
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
        elif key == 'Тестировать':
            self.testing()

    def update_options(self):
        self.options_widget.set_value('Номер лабы:', self.settings.get('lab', self.options_widget['Номер лабы:']))
        self.options_widget.set_value('Номер задания:', self.settings.get('task', self.options_widget['Номер задания:']))
        self.options_widget.set_value('Номер варианта:', self.settings.get('var', self.options_widget['Номер варианта:']))

    def open_task(self):
        self.get_path()
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

    def testing(self):
        if self.isHidden():
            self.get_path(True)
        self.tests.clear()
        self.tests_list.clear()
        os.system(f"{self.settings['compiler']} {self.path}/main.c -o {self.path}/app.exe"
                  f"{' -lm' if self.settings['-lm'] else ''} 2> {self.path}/temp.txt")
        errors = read_file(f"{self.path}/temp.txt")
        if errors:
            QMessageBox.warning(self, "Ошибка компиляции", errors)
            if os.path.isfile(f"{self.path}/temp.txt"):
                os.remove(f"{self.path}/temp.txt")
            return

        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt"):
            os.system(f"{self.path}/app.exe < {self.path}/func_tests/data/pos_{i:0>2}_in.txt > {self.path}/temp.txt")
            self.tests.append((comparator(f"{self.path}/func_tests/data/pos_{i:0>2}_out.txt", f"{self.path}/temp.txt"),
                               read_file(f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt"),
                               read_file(f"{self.path}/func_tests/data/pos_{i:0>2}_out.txt"),
                               read_file(f"{self.path}/temp.txt"), f"pos{i}"))
            if self.tests[-1][0]:
                item = QListWidgetItem(f"pos{i} \tPASSED")
            else:
                item = QListWidgetItem(f"pos{i} \tFAILED")
            self.tests_list.addItem(item)
            i += 1

        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt"):
            os.system(f"{self.path}/app.exe < {self.path}/func_tests/data/neg_{i:0>2}_in.txt > {self.path}/temp.txt")
            self.tests.append((comparator(f"{self.path}/func_tests/data/neg_{i:0>2}_out.txt", f"{self.path}/temp.txt"),
                               read_file(f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt"),
                               read_file(f"{self.path}/func_tests/data/neg_{i:0>2}_out.txt"),
                               read_file(f"{self.path}/temp.txt"), f"neg{i}"))
            if self.tests[-1][0]:
                item = QListWidgetItem(f"neg{i} \tPASSED")
            else:
                item = QListWidgetItem(f"neg{i} \tFAILED")
            self.tests_list.addItem(item)
            i += 1

        if os.path.isfile(f"{self.path}/temp.txt"):
            os.remove(f"{self.path}/temp.txt")
        self.testing_signal.emit(self.tests)

    def show(self) -> None:
        self.update_options()
        self.open_task()
        super(TestingWidget, self).show()


def comparator(path1, path2):
    file1 = open(path1, encoding='utf-8')
    lst1 = []
    for word in file1.read().split():
        try:
            lst1.append(float(word))
        except Exception:
            pass
    file1.close()

    file2 = open(path2, encoding='utf-8')
    lst2 = []
    for word in file2.read().split():
        try:
            lst2.append(float(word))
        except Exception:
            pass
    file2.close()

    return lst1 == lst2


def read_file(path):
    file = open(path, encoding='utf-8')
    res = file.read()
    file.close()
    return res
