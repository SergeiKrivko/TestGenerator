from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QMessageBox, QFileDialog
from PyQt5.QtGui import QFont
from widgets.options_window import OptionsWidget
from widgets.test_table_widget import TestTableWidget
from widgets.test_edit_widget import TestEditWidget
import os


class TestsWidget(QWidget):
    def __init__(self, settings):
        super(TestsWidget, self).__init__()
        self.settings = settings

        layout = QHBoxLayout()
        layout1 = QVBoxLayout()
        layout.addLayout(layout1)

        self.options_widget = OptionsWidget({
            'Номер лабы:': {'type': int, 'min': 1, 'initial': self.settings.get('lab', 1),
                            'name': OptionsWidget.NAME_LEFT},
            'Номер задания:': {'type': int, 'min': 1, 'initial': self.settings.get('task', 1),
                               'name': OptionsWidget.NAME_LEFT},
            'Номер варианта:': {'type': int, 'min': -1, 'initial': self.settings.get('var', 0),
                                'name': OptionsWidget.NAME_LEFT},
            'Входные данные:': {'type': str, 'initial': '-', 'width': 300},
            'Выходные данные:': {'type': str, 'initial': '-', 'width': 300}
        })
        self.options_widget.clicked.connect(self.option_changed)
        layout1.addWidget(self.options_widget)

        self.code_widget = QTextEdit()
        self.code_widget.setFont(QFont("Courier", 10))
        self.code_widget.setReadOnly(True)
        layout1.addWidget(self.code_widget)

        layout2 = QVBoxLayout()
        layout.addLayout(layout2)

        self.test_list_widget = TestTableWidget()
        self.test_list_widget.setMinimumWidth(400)
        self.test_list_widget.setMinimumHeight(150)
        self.test_list_widget.pos_add_button.clicked.connect(self.add_pos_test)
        self.test_list_widget.pos_delete_button.clicked.connect(self.delete_pos_test)
        self.test_list_widget.neg_add_button.clicked.connect(self.add_neg_test)
        self.test_list_widget.neg_delete_button.clicked.connect(self.delete_neg_test)
        self.test_list_widget.pos_button_up.clicked.connect(self.move_pos_test_up)
        self.test_list_widget.pos_button_down.clicked.connect(self.move_pos_test_down)
        self.test_list_widget.neg_button_up.clicked.connect(self.move_neg_test_up)
        self.test_list_widget.neg_button_down.clicked.connect(self.move_neg_test_down)
        self.test_list_widget.pos_test_list.itemSelectionChanged.connect(self.select_pos_test)
        self.test_list_widget.neg_test_list.itemSelectionChanged.connect(self.select_neg_test)
        layout2.addWidget(self.test_list_widget)

        self.test_edit_widget = TestEditWidget()
        self.test_edit_widget.setMinimumHeight(300)
        self.test_edit_widget.test_name_edit.textChanged.connect(self.set_test_name)
        self.test_edit_widget.test_in_edit.textChanged.connect(self.set_test_in)
        self.test_edit_widget.test_out_edit.textChanged.connect(self.set_test_out)
        self.test_edit_widget.button_generate.clicked.connect(self.button_generate_test)
        layout2.addWidget(self.test_edit_widget)

        self.setLayout(layout)

        self.pos_tests = []
        self.neg_tests = []
        self.selected_test = 'pos'

        self.path = ''
        if 'path' in self.settings and os.path.isdir(self.settings['path']):
            self.open_tests()
        else:
            self.open_project()

    def option_changed(self, key):
        if key in ('Номер лабы:', 'Номер задания:'):
            self.save_tests()
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
            self.open_tests()
        elif key == 'Номер варианта:':
            self.save_tests()
            self.settings['var'] = self.options_widget["Номер варианта:"]
            self.open_tests()

    def update_options(self):
        self.options_widget.set_value('Номер лабы:', self.settings.get('lab', self.options_widget['Номер лабы:']))
        self.options_widget.set_value('Номер задания:',
                                      self.settings.get('task', self.options_widget['Номер задания:']))
        self.options_widget.set_value('Номер варианта:',
                                      self.settings.get('var', self.options_widget['Номер варианта:']))

    def add_pos_test(self):
        self.pos_tests.append(['-', '', ''])
        self.test_list_widget.update_pos_items([item[0] for item in self.pos_tests])

    def add_neg_test(self):
        self.neg_tests.append(['-', '', ''])
        self.test_list_widget.update_neg_items([item[0] for item in self.neg_tests])

    def delete_pos_test(self):
        if len(self.pos_tests) == 0:
            return
        ind = self.test_list_widget.pos_test_list.currentRow()
        if ind == -1:
            return
        self.pos_tests.pop(ind)
        self.test_list_widget.update_pos_items([item[0] for item in self.pos_tests])
        self.test_list_widget.pos_test_list.setCurrentRow(ind if ind < len(self.pos_tests) else ind - 1)

    def delete_neg_test(self):
        if len(self.neg_tests) == 0:
            return
        ind = self.test_list_widget.neg_test_list.currentRow()
        if ind == -1:
            return
        self.neg_tests.pop(ind)
        self.test_list_widget.update_neg_items([item[0] for item in self.neg_tests])
        self.test_list_widget.neg_test_list.setCurrentRow(ind if ind < len(self.neg_tests) else ind - 1)

    def select_pos_test(self):
        self.test_list_widget.neg_test_list.setCurrentItem(None)
        try:
            self.test_edit_widget.open_test(*self.pos_tests[self.test_list_widget.pos_test_list.currentRow()])
        except IndexError:
            pass

    def select_neg_test(self):
        self.test_list_widget.pos_test_list.setCurrentItem(None)
        try:
            self.test_edit_widget.open_test(*self.neg_tests[self.test_list_widget.neg_test_list.currentRow()])
        except IndexError:
            pass

    def set_test_name(self, name):
        if self.test_list_widget.pos_test_list.currentItem() is not None:
            self.pos_tests[self.test_list_widget.pos_test_list.currentRow()][0] = name
            self.test_list_widget.pos_test_list.currentItem().setText(name)
        elif self.test_list_widget.neg_test_list.currentItem() is not None:
            self.neg_tests[self.test_list_widget.neg_test_list.currentRow()][0] = name
            self.test_list_widget.neg_test_list.currentItem().setText(name)

    def set_test_in(self):
        if self.test_list_widget.pos_test_list.currentItem() is not None:
            self.pos_tests[self.test_list_widget.pos_test_list.currentRow()][1] = \
                self.test_edit_widget.test_in_edit.toPlainText()
        elif self.test_list_widget.neg_test_list.currentItem() is not None:
            self.neg_tests[self.test_list_widget.neg_test_list.currentRow()][1] = \
                self.test_edit_widget.test_in_edit.toPlainText()

    def set_test_out(self):
        if self.test_list_widget.pos_test_list.currentItem() is not None:
            self.pos_tests[self.test_list_widget.pos_test_list.currentRow()][2] = \
                self.test_edit_widget.test_out_edit.toPlainText()
        elif self.test_list_widget.neg_test_list.currentItem() is not None:
            self.neg_tests[self.test_list_widget.neg_test_list.currentRow()][2] = \
                self.test_edit_widget.test_out_edit.toPlainText()

    def move_pos_test_up(self):
        index = self.test_list_widget.pos_test_list.currentRow()
        if index <= 0:
            return
        self.pos_tests[index], self.pos_tests[index - 1] = self.pos_tests[index - 1], self.pos_tests[index]
        self.test_list_widget.update_pos_items([item[0] for item in self.pos_tests])
        self.test_list_widget.pos_test_list.setCurrentRow(index - 1)

    def move_pos_test_down(self):
        index = self.test_list_widget.pos_test_list.currentRow()
        if index >= len(self.pos_tests) - 1:
            return
        self.pos_tests[index], self.pos_tests[index + 1] = self.pos_tests[index + 1], self.pos_tests[index]
        self.test_list_widget.update_pos_items([item[0] for item in self.pos_tests])
        self.test_list_widget.pos_test_list.setCurrentRow(index + 1)

    def move_neg_test_up(self):
        index = self.test_list_widget.neg_test_list.currentRow()
        if index <= 0:
            return
        self.neg_tests[index], self.neg_tests[index - 1] = self.neg_tests[index - 1], self.neg_tests[index]
        self.test_list_widget.update_neg_items([item[0] for item in self.neg_tests])
        self.test_list_widget.neg_test_list.setCurrentRow(index - 1)

    def move_neg_test_down(self):
        index = self.test_list_widget.neg_test_list.currentRow()
        if index >= len(self.neg_tests) - 1:
            return
        self.neg_tests[index], self.neg_tests[index + 1] = self.neg_tests[index + 1], self.neg_tests[index]
        self.test_list_widget.update_neg_items([item[0] for item in self.neg_tests])
        self.test_list_widget.neg_test_list.setCurrentRow(index + 1)

    def button_generate_test(self):
        if self.test_list_widget.pos_test_list.currentItem() is not None:
            index = self.test_list_widget.pos_test_list.currentRow()
            self.pos_tests[index][2] = ''
            self.generate_test(index, 'pos')
            file = open(f"{self.path}/func_tests/data/pos_{index + 1:0>2}_out.txt")
            self.pos_tests[index][2] = file.read()
            file.close()
            self.test_edit_widget.test_out_edit.setText(self.pos_tests[index][2])
        elif self.test_list_widget.neg_test_list.currentItem() is not None:
            index = self.test_list_widget.neg_test_list.currentRow()
            self.neg_tests[index][2] = ''
            self.generate_test(index, 'neg')
            file = open(f"{self.path}/func_tests/data/neg_{index + 1:0>2}_out.txt")
            self.neg_tests[index][2] = file.read()
            file.close()
            self.test_edit_widget.test_out_edit.setText(self.neg_tests[index][2])

    def open_project(self):
        path = QFileDialog.getExistingDirectory(directory=self.settings.get('path', os.getcwd()))
        if path:
            self.settings['path'] = path
            self.open_tests()

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

    def open_tests(self):
        self.get_path()
        try:
            self.code_widget.setText("")
            file = open(f"{self.path}/main.c")
            self.code_widget.setText(file.read())
            file.close()
        except Exception:
            pass
        self.readme_parser()
        self.test_list_widget.update_pos_items([item[0] for item in self.pos_tests])
        self.test_list_widget.update_neg_items([item[0] for item in self.neg_tests])

    def readme_parser(self):
        self.pos_tests.clear()
        self.neg_tests.clear()

        if not os.path.isfile(f"{self.path}/func_tests/readme.md"):
            return
        file = open(f"{self.path}/func_tests/readme.md", encoding='utf-8')
        lines = file.readlines()
        file.close()
        self.options_widget.set_value("Входные данные:", "-")
        self.options_widget.set_value("Выходные данные:", "-")

        for i in range(len(lines)):
            if "Позитивные тесты" in lines[i]:
                for j in range(i + 1, len(lines)):
                    if lines[j][:2] == '- ' and lines[j][4:7] == ' - ':
                        self.pos_tests.append([lines[j][7:].strip(), '', ''])
                    else:
                        break

            elif "Негативные тесты" in lines[i]:
                for j in range(i + 1, len(lines)):
                    if lines[j][:2] == '- ' and lines[j][4:7] == ' - ':
                        self.neg_tests.append([lines[j][7:].strip(), '', ''])
                    else:
                        break

            elif "Входные данные" in lines[i]:
                self.options_widget.set_value("Входные данные:", lines[i + 1].strip())

            elif "Выходные данные" in lines[i]:
                self.options_widget.set_value("Выходные данные:", lines[i + 1].strip())

        pos_count = 0
        neg_count = 0
        for file in os.listdir(f"{self.path}/func_tests/data"):
            if file[:4] == 'pos_' and file[6:9] == '_in':
                pos_count += 1
            elif file[:4] == 'neg_' and file[6:9] == '_in':
                neg_count += 1
        for i in range(len(self.pos_tests), pos_count):
            self.pos_tests.append(['-', '', ''])
        for i in range(len(self.neg_tests), neg_count):
            self.neg_tests.append(['-', '', ''])

        for i in range(len(self.pos_tests)):
            if os.path.isfile(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_in.txt"):
                file = open(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_in.txt")
                self.pos_tests[i][1] = file.read()
                file.close()
                if os.path.isfile(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_out.txt"):
                    file = open(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_out.txt")
                    self.pos_tests[i][2] = file.read()
                    file.close()

        for i in range(len(self.neg_tests)):
            if os.path.isfile(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_in.txt"):
                file = open(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_in.txt")
                self.neg_tests[i][1] = file.read()
                file.close()
                if os.path.isfile(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_out.txt"):
                    file = open(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_out.txt")
                    self.neg_tests[i][2] = file.read()
                    file.close()

    def generate_test(self, index, type='pos'):
        os.makedirs(f"{self.path}/func_tests/data", exist_ok=True)

        tests = self.pos_tests if type == 'pos' else self.neg_tests
        file_in = open(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_in.txt", "w")
        file_in.write(tests[index][1])
        file_in.close()

        if tests[index][2].strip() or not os.path.isfile(f"{self.path}/main.c"):
            file = open(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_out.txt", 'w', encoding='utf-8')
            file.write(tests[index][2])
            file.close()
        else:
            if not os.path.isfile(f"{self.path}/app.exe"):
                os.system(f"{self.settings['compiler']} {self.path}/main.c -o {self.path}/app.exe"
                          f"{' -lm' if self.settings['-lm'] else ''} 2> {self.path}/temp.txt")
                errors = read_file(f"{self.path}/temp.txt")
                if errors:
                    QMessageBox.warning(self, "Ошибка компиляции", errors)
                if os.path.isfile(f"{self.path}/temp.txt"):
                    os.remove(f"{self.path}/temp.txt")
            os.system(f"{self.path}/app.exe < {self.path}/func_tests/data/{type}_{index + 1:0>2}_in.txt > "
                      f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_out.txt")

    def save_tests(self):
        if not os.path.isfile(f"{self.path}/main.c") and not self.pos_tests and not self.neg_tests:
            return
        try:
            os.makedirs(f"{self.path}/func_tests/data", exist_ok=True)
            readme = open(f"{self.path}/func_tests/readme.md", 'w', encoding='utf-8')
            readme.write(f"# Тесты для лабораторной работы №{self.settings['lab']:0>2}, задания №"
                         f"{self.settings['task']:0>2}\n\n"
                         f"## Входные данные\n{self.options_widget['Входные данные:']}\n\n"
                         f"## Выходные данные\n{self.options_widget['Выходные данные:']}\n\n"
                         f"## Позитивные тесты:\n")
            for i in range(len(self.pos_tests)):
                readme.write(f"- {i + 1:0>2} - {self.pos_tests[i][0]}\n")
                self.generate_test(i, 'pos')

            readme.write("\n## Негативные тесты:\n")

            for i in range(len(self.neg_tests)):
                readme.write(f"- {i + 1:0>2} - {self.neg_tests[i][0]}\n")
                self.generate_test(i, 'neg')
        except Exception as ex:
            QMessageBox.warning(self, 'Error', f"{ex.__class__.__name__}: {ex}")

    def show(self):
        self.update_options()
        self.open_tests()
        super(TestsWidget, self).show()

    def hide(self) -> None:
        if not self.isHidden():
            self.save_tests()
        super(TestsWidget, self).hide()


def read_file(path):
    file = open(path, encoding='utf-8')
    res = file.read()
    file.close()
    return res
