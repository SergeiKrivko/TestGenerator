from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QMessageBox, QDialog, QDialogButtonBox, QScrollArea, \
    QHBoxLayout, QCheckBox, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont
from widgets.options_window import OptionsWidget
from widgets.test_table_widget import TestTableWidget
from widgets.test_edit_widget import TestEditWidget
import os


class TestsWidget(QWidget):
    def __init__(self, sm, cm, tm):
        super(TestsWidget, self).__init__()
        self.sm = sm
        self.cm = cm
        self.tm = tm

        layout = QVBoxLayout()

        self.options_widget = OptionsWidget({
            'h_line1': {
                'Номер лабы:': {'type': int, 'min': 1, 'name': OptionsWidget.NAME_LEFT, 'width': 60},
                'Номер задания:': {'type': int, 'min': 1, 'name': OptionsWidget.NAME_LEFT, 'width': 60},
                'Номер варианта:': {'type': int, 'min': -1, 'name': OptionsWidget.NAME_LEFT, 'width': 60}
            },
            'h_line2': {
                'Вход:': {'type': str, 'initial': '-', 'width': 300, 'name': OptionsWidget.NAME_LEFT},
                'Выход:': {'type': str, 'initial': '-', 'width': 300, 'name': OptionsWidget.NAME_LEFT}
            }
        }, margins=(0, 0, 0, 0))
        self.options_widget.clicked.connect(self.option_changed)
        layout.addWidget(self.options_widget)

        self.code_widget = QTextEdit()
        self.code_widget.setFont(QFont("Courier", 10))
        self.code_widget.setReadOnly(True)

        self.test_list_widget = TestTableWidget(self.tm)
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
        self.test_list_widget.pos_button_copy.clicked.connect(lambda: self.copy_tests('pos'))
        self.test_list_widget.neg_button_copy.clicked.connect(lambda: self.copy_tests('neg'))
        self.test_list_widget.pos_test_list.itemSelectionChanged.connect(self.select_pos_test)
        self.test_list_widget.neg_test_list.itemSelectionChanged.connect(self.select_neg_test)
        layout.addWidget(self.test_list_widget)

        self.test_edit_widget = TestEditWidget(self.tm)
        self.test_edit_widget.setMinimumHeight(300)
        self.test_edit_widget.test_name_edit.textChanged.connect(self.set_test_name)
        self.test_edit_widget.test_in_edit.textChanged.connect(self.set_test_in)
        self.test_edit_widget.test_out_edit.textChanged.connect(self.set_test_out)
        self.test_edit_widget.cmd_args_edit.textChanged.connect(self.set_test_args)
        self.test_edit_widget.button_generate.clicked.connect(self.button_generate_test)
        layout.addWidget(self.test_edit_widget)

        self.setLayout(layout)

        self.selected_test = 'pos'

        self.path = ''
        self.file_compiled = False
        self.file_edit_time = dict()

    def option_changed(self, key):
        if key in ('Номер лабы:', 'Номер задания:'):
            self.save_tests()
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
            self.open_tests()
        elif key == 'Номер варианта:':
            self.save_tests()
            self.sm.set('var', self.options_widget["Номер варианта:"])
            self.open_tests()

    def update_options(self):
        self.options_widget.set_value('Номер лабы:', self.sm.get('lab', self.options_widget['Номер лабы:']))
        self.options_widget.set_value('Номер задания:',
                                      self.sm.get('task', self.options_widget['Номер задания:']))
        self.options_widget.set_value('Номер варианта:',
                                      self.sm.get('var', self.options_widget['Номер варианта:']))

    def add_pos_test(self):
        self.test_list_widget.pos_test_list.addItem(CustomListWidgetItem('-', '', ''))

    def add_neg_test(self):
        self.test_list_widget.neg_test_list.addItem(CustomListWidgetItem('-', '', ''))

    def delete_pos_test(self):
        if self.test_list_widget.pos_test_list.count() == 0:
            return
        ind = self.test_list_widget.pos_test_list.currentRow()
        if ind == -1:
            return
        self.test_list_widget.pos_test_list.takeItem(ind)
        if self.test_list_widget.pos_test_list.count() == 0:
            self.test_edit_widget.set_disabled()
        else:
            self.test_list_widget.pos_test_list.setCurrentRow(
                ind if ind < self.test_list_widget.pos_test_list.count() else ind - 1)

    def delete_neg_test(self):
        if self.test_list_widget.neg_test_list.count() == 0:
            return
        ind = self.test_list_widget.neg_test_list.currentRow()
        if ind == -1:
            return
        self.test_list_widget.neg_test_list.takeItem(ind)
        if self.test_list_widget.neg_test_list.count() == 0:
            self.test_edit_widget.set_disabled()
        else:
            self.test_list_widget.neg_test_list.setCurrentRow(
                ind if ind < self.test_list_widget.neg_test_list.count() else ind - 1)

    def copy_tests(self, test_type='pos'):
        dlg = TestCopyWindow(self.sm)
        if dlg.exec():
            for desc, in_data, out_data in dlg.copy_tests():
                if test_type == 'pos':
                    self.test_list_widget.pos_test_list.addItem(CustomListWidgetItem(desc, in_data, out_data))
                else:
                    self.test_list_widget.neg_test_list.addItem(CustomListWidgetItem(desc, in_data, out_data))

    def select_pos_test(self):
        try:
            item = self.test_list_widget.pos_test_list.currentItem()
            if item:
                self.test_list_widget.neg_test_list.setCurrentItem(None)
            self.test_edit_widget.open_test(item.desc, item.in_data, item.out_data, item.cmd_args, item.exit_code)
        except AttributeError:
            pass

    def select_neg_test(self):
        try:
            item = self.test_list_widget.neg_test_list.currentItem()
            if item:
                self.test_list_widget.pos_test_list.setCurrentItem(None)
            self.test_edit_widget.open_test(item.desc, item.in_data, item.out_data, item.cmd_args, item.exit_code)
        except AttributeError:
            pass

    def set_test_name(self, name):
        if self.test_list_widget.pos_test_list.currentItem() is not None:
            self.test_list_widget.pos_test_list.currentItem().set_desc(name)
        elif self.test_list_widget.neg_test_list.currentItem() is not None:
            self.test_list_widget.neg_test_list.currentItem().set_desc(name)

    def set_test_in(self):
        if self.test_list_widget.pos_test_list.currentItem() is not None:
            self.test_list_widget.pos_test_list.currentItem().in_data = self.test_edit_widget.test_in_edit.toPlainText()
        elif self.test_list_widget.neg_test_list.currentItem() is not None:
            self.test_list_widget.neg_test_list.currentItem().in_data = self.test_edit_widget.test_in_edit.toPlainText()

    def set_test_args(self):
        if self.test_list_widget.pos_test_list.currentItem() is not None:
            self.test_list_widget.pos_test_list.currentItem().cmd_args = self.test_edit_widget.cmd_args_edit.text()
        elif self.test_list_widget.neg_test_list.currentItem() is not None:
            self.test_list_widget.neg_test_list.currentItem().cmd_args = self.test_edit_widget.cmd_args_edit.text()

    def set_test_out(self):
        if self.test_list_widget.pos_test_list.currentItem() is not None:
            self.test_list_widget.pos_test_list.currentItem().out_data = \
                self.test_edit_widget.test_out_edit.toPlainText()
        elif self.test_list_widget.neg_test_list.currentItem() is not None:
            self.test_list_widget.neg_test_list.currentItem().out_data = \
                self.test_edit_widget.test_out_edit.toPlainText()

    def move_pos_test_up(self):
        index = self.test_list_widget.pos_test_list.currentRow()
        if index <= 0:
            return
        item = self.test_list_widget.pos_test_list.takeItem(index)
        self.test_list_widget.pos_test_list.insertItem(index - 1, item)
        self.test_list_widget.pos_test_list.setCurrentRow(index - 1)

    def move_pos_test_down(self):
        index = self.test_list_widget.pos_test_list.currentRow()
        if index >= self.test_list_widget.pos_test_list.count() - 1:
            return
        item = self.test_list_widget.pos_test_list.takeItem(index)
        self.test_list_widget.pos_test_list.insertItem(index + 1, item)
        self.test_list_widget.pos_test_list.setCurrentRow(index + 1)

    def move_neg_test_up(self):
        index = self.test_list_widget.neg_test_list.currentRow()
        if index <= 0:
            return
        item = self.test_list_widget.neg_test_list.takeItem(index)
        self.test_list_widget.neg_test_list.insertItem(index - 1, item)
        self.test_list_widget.neg_test_list.setCurrentRow(index - 1)

    def move_neg_test_down(self):
        index = self.test_list_widget.neg_test_list.currentRow()
        if index >= self.test_list_widget.neg_test_list.count() - 1:
            return
        item = self.test_list_widget.neg_test_list.takeItem(index)
        self.test_list_widget.neg_test_list.insertItem(index + 1, item)
        self.test_list_widget.neg_test_list.setCurrentRow(index + 1)

    def button_generate_test(self):
        if self.test_list_widget.pos_test_list.currentItem() is not None:
            index = self.test_list_widget.pos_test_list.currentRow()
            self.test_list_widget.pos_test_list.item(index).out_data = ''
            self.generate_test(index, 'pos')
            file = open(f"{self.path}/func_tests/data/pos_{index + 1:0>2}_out.txt")
            self.test_list_widget.pos_test_list.item(index).out_data = file.read()
            file.close()
            self.test_edit_widget.test_out_edit.setText(self.test_list_widget.pos_test_list.item(index).out_data)
        elif self.test_list_widget.neg_test_list.currentItem() is not None:
            index = self.test_list_widget.neg_test_list.currentRow()
            self.test_list_widget.neg_test_list.item(index).out_data = ''
            self.generate_test(index, 'neg')
            file = open(f"{self.path}/func_tests/data/neg_{index + 1:0>2}_out.txt")
            self.test_list_widget.neg_test_list.item(index).out_data = file.read()
            file.close()
            self.test_edit_widget.test_out_edit.setText(self.test_list_widget.neg_test_list.item(index).out_data)

    def get_path(self, from_settings=False):
        if from_settings:
            self.path = self.sm.lab_path()
        else:
            self.path = self.sm.lab_path(self.options_widget['Номер лабы:'], self.options_widget['Номер задания:'],
                                         self.options_widget['Номер варианта:'])

    def open_tests(self):
        self.get_path()
        try:
            self.test_list_widget.pos_comparator_widget.setCurrentIndex(self.sm.get('pos_comparators', dict()).get(
                (self.sm.get('lab'), self.sm.get('task'), self.sm.get('var')), -1) + 1)
            self.test_list_widget.neg_comparator_widget.setCurrentIndex(self.sm.get('neg_comparators', dict()).get(
                (self.sm.get('lab'), self.sm.get('task'), self.sm.get('var')), -1) + 1)
        except Exception as ex:
            print(f"{ex.__class__.__name__}")
        self.readme_parser()
        self.test_edit_widget.set_disabled()
        self.file_edit_time.clear()

    def readme_parser(self):
        self.test_list_widget.pos_test_list.clear()
        self.test_list_widget.neg_test_list.clear()

        if not os.path.isfile(f"{self.path}/func_tests/readme.md"):
            return
        file = open(f"{self.path}/func_tests/readme.md", encoding='utf-8')
        lines = file.readlines()
        file.close()
        self.options_widget.set_value("Вход:", "-")
        self.options_widget.set_value("Выход:", "-")

        for i in range(len(lines)):
            if "Позитивные тесты" in lines[i]:
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith('- ') and ' - ' in lines[j]:
                        self.test_list_widget.pos_test_list.addItem(CustomListWidgetItem(lines[j][7:].strip(), '', ''))
                    else:
                        break

            elif "Негативные тесты" in lines[i]:
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith('- ') and ' - ' in lines[j]:
                        self.test_list_widget.neg_test_list.addItem(CustomListWidgetItem(lines[j][7:].strip(), '', ''))
                    else:
                        break

            elif "Вход" in lines[i] or "Входные данные" in lines[i]:
                self.options_widget.set_value("Вход:", lines[i + 1].strip())

            elif "Выход" in lines[i] or "Выходные данные" in lines[i]:
                self.options_widget.set_value("Выход:", lines[i + 1].strip())

        pos_count = 0
        neg_count = 0
        for file in os.listdir(f"{self.path}/func_tests/data"):
            pos_count += file.startswith('pos_') and file.endswith('_in.txt')
            neg_count += file.startswith('neg_') and file.endswith('_in.txt')
        for i in range(self.test_list_widget.pos_test_list.count(), pos_count):
            self.test_list_widget.pos_test_list.addItem(CustomListWidgetItem('-', '', ''))
        for i in range(self.test_list_widget.neg_test_list.count(), neg_count):
            self.test_list_widget.neg_test_list.addItem(CustomListWidgetItem('-', '', ''))

        for i in range(self.test_list_widget.pos_test_list.count()):
            if os.path.isfile(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_in.txt"):
                file = open(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_in.txt")
                self.test_list_widget.pos_test_list.item(i).in_data = file.read()
                file.close()
                if os.path.isfile(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_out.txt"):
                    file = open(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_out.txt")
                    self.test_list_widget.pos_test_list.item(i).out_data = file.read()
                    file.close()
                if os.path.isfile(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_args.txt"):
                    file = open(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_args.txt")
                    self.test_list_widget.pos_test_list.item(i).cmd_args = file.read()
                    file.close()

        for i in range(self.test_list_widget.neg_test_list.count()):
            if os.path.isfile(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_in.txt"):
                file = open(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_in.txt")
                self.test_list_widget.neg_test_list.item(i).in_data = file.read()
                file.close()
                if os.path.isfile(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_out.txt"):
                    file = open(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_out.txt")
                    self.test_list_widget.neg_test_list.item(i).out_data = file.read()
                    file.close()
                if os.path.isfile(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_args.txt"):
                    file = open(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_args.txt")
                    self.test_list_widget.neg_test_list.item(i).cmd_args = file.read()
                    file.close()

    def compare_edit_time(self):
        for file in os.listdir(self.path):
            if ('.c' in file or '.h' in file) and \
                    self.file_edit_time.get(file, 0) != os.path.getmtime(f"{self.path}/{file}"):
                return False
        return True

    def update_edit_time(self):
        for file in os.listdir(self.path):
            if '.c' in file or '.h' in file:
                self.file_edit_time[file] = os.path.getmtime(f"{self.path}/{file}")

    def save_a_test(self, index, type='pos'):
        os.makedirs(f"{self.path}/func_tests/data", exist_ok=True)

        tests = self.test_list_widget.pos_test_list if type == 'pos' else self.test_list_widget.neg_test_list

        file_in = open(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_in.txt", "w",
                       newline=self.sm.get('line_sep'))
        file_in.write(tests.item(index).in_data)
        file_in.close()

        file_out = open(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_out.txt", "w",
                        newline=self.sm.get('line_sep'))
        file_out.write(tests.item(index).out_data)
        file_out.close()

        if tests.item(index).cmd_args.strip():
            file_out = open(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_args.txt", "w",
                            newline=self.sm.get('line_sep'))
            file_out.write(tests.item(index).cmd_args)
            file_out.close()
        elif os.path.isfile(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_args.txt"):
            os.remove(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_args.txt")

    def generate_test(self, index, type='pos'):
        os.makedirs(f"{self.path}/func_tests/data", exist_ok=True)

        tests = self.test_list_widget.pos_test_list if type == 'pos' else self.test_list_widget.neg_test_list
        file_in = open(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_in.txt", "w",
                       newline=self.sm.get('line_sep'))
        file_in.write(tests.item(index).in_data)
        file_in.close()

        if not self.compare_edit_time():
            self.update_edit_time()
            if not self.cm.compile2(coverage=False):
                return

        res = self.cm.cmd_command(
            f"{self.path}/app.exe {read_file(f'{self.path}/func_tests/data/{type}_{index + 1:0>2}_args.txt', default='')}",
            shell=True, input=read_file(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_in.txt"))
        file = open(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_out.txt", 'w', encoding='utf-8',
                    newline=self.sm.get('line_sep'))
        file.write(res.stdout)
        file.close()
        if self.sm.get('clear_words', False):
            clear_words(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_out.txt")

        self.cm.clear_coverage_files()

    def remove_files(self):
        for file in os.listdir(f"{self.path}/func_tests/data"):
            if file.startswith('pos_') or file.startswith('neg_') and \
                    file.endswith('_in.txt') or file.endswith('_out.txt') or file.endswith('_args.txt'):
                os.remove(f"{self.path}/func_tests/data/{file}")

    def save_tests(self):
        if not os.path.isfile(f"{self.path}/main.c") and not self.test_list_widget.pos_test_list.count() and \
                not self.test_list_widget.neg_test_list.count():
            return
        try:
            os.makedirs(f"{self.path}/func_tests/data", exist_ok=True)
            self.remove_files()
            readme = open(f"{self.path}/func_tests/readme.md", 'w', encoding='utf-8', newline=self.sm.get('line_sep'))
            readme.write(f"# Тесты для лабораторной работы №{self.sm.get('lab'):0>2}, задания №"
                         f"{self.sm.get('task'):0>2}\n\n"
                         f"## Входные данные\n{self.options_widget['Вход:']}\n\n"
                         f"## Выходные данные\n{self.options_widget['Выход:']}\n\n"
                         f"## Позитивные тесты:\n")
            for i in range(self.test_list_widget.pos_test_list.count()):
                readme.write(f"- {i + 1:0>2} - {self.test_list_widget.pos_test_list.item(i).desc}\n")
                self.save_a_test(i, 'pos')

            readme.write("\n## Негативные тесты:\n")

            for i in range(self.test_list_widget.neg_test_list.count()):
                readme.write(f"- {i + 1:0>2} - {self.test_list_widget.neg_test_list.item(i).desc}\n")
                self.save_a_test(i, 'neg')

            dct = self.sm.get('pos_comparators', dict())
            dct[(self.sm.get('lab'), self.sm.get('task'), self.sm.get('var'))] = \
                self.test_list_widget.pos_comparator_widget.currentIndex() - 1
            self.sm.set('pos_comparators', dct)
            dct = self.sm.get('neg_comparators', dict())
            dct[(self.sm.get('lab'), self.sm.get('task'), self.sm.get('var'))] = \
                self.test_list_widget.neg_comparator_widget.currentIndex() - 1
            self.sm.set('neg_comparators', dct)
        except Exception as ex:
            QMessageBox.warning(self, 'Error', f"{ex.__class__.__name__}: {ex}")

    def set_theme(self):
        self.test_list_widget.set_theme()
        self.test_edit_widget.set_theme()
        self.options_widget.set_widget_style_sheet('Номер лабы:', self.tm.spin_box_style_sheet)
        self.options_widget.set_widget_style_sheet('Номер задания:', self.tm.spin_box_style_sheet)
        self.options_widget.set_widget_style_sheet('Номер варианта:', self.tm.spin_box_style_sheet)
        self.options_widget.set_widget_style_sheet('Вход:', self.tm.style_sheet)
        self.options_widget.set_widget_style_sheet('Выход:', self.tm.style_sheet)

    def show(self):
        self.update_options()
        self.open_tests()
        super(TestsWidget, self).show()

    def hide(self) -> None:
        if not self.isHidden():
            self.save_tests()
        super(TestsWidget, self).hide()


class CustomListWidgetItem(QListWidgetItem):
    def __init__(self, desc, in_data, out_data, cmd_args="", exit_code=None):
        super(CustomListWidgetItem, self).__init__()
        self.desc = desc
        self.setText(desc)
        self.in_data = in_data
        self.out_data = out_data
        self.cmd_args = cmd_args
        self.exit_code = exit_code

    def set_desc(self, new_desc):
        self.desc = new_desc
        self.setText(new_desc)


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


def clear_words(path):
    file = open(path, 'r', encoding='utf-8')
    result = []
    for line in file:
        lst = []
        for word in line.split():
            try:
                float(word)
                lst.append(word)
            except Exception:
                pass
        if len(lst):
            result.append(' '.join(lst))
    file.close()

    file = open(path, 'w', encoding='utf-8')
    file.write("\n".join(result))
    file.close()


class TestCopyWindow(QDialog):
    def __init__(self, settings):
        super().__init__()
        self.sm = settings

        self.setWindowTitle("Копировать тесты")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.options_widget = OptionsWidget({
            'h_line': {
                'Номер лабы:': {'type': int, 'min': 1, 'initial': self.sm.get('lab', 1),
                                'name': OptionsWidget.NAME_LEFT, 'width': 60},
                'Номер задания:': {'type': int, 'min': 1, 'initial': self.sm.get('task', 1),
                                   'name': OptionsWidget.NAME_LEFT, 'width': 60},
                'Номер варианта:': {'type': int, 'min': -1, 'initial': self.sm.get('var', 0),
                                    'name': OptionsWidget.NAME_LEFT, 'width': 60}
            }
        })
        self.layout.addWidget(self.options_widget)
        self.options_widget.clicked.connect(self.options_changed)

        self.scroll_area = QScrollArea()
        self.widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(480, 320)
        self.layout.addWidget(self.scroll_area)

        self.layout.addWidget(self.buttonBox)

        self.path = ""
        self.test_list = []
        self.check_boxes = []

        self.get_path()
        self.parse_readme_md()
        self.update_list()

    def options_changed(self, key):
        if key in ('Номер лабы:', 'Номер задания:'):
            if os.path.isdir(self.sm.lab_path(self.options_widget['Номер лабы:'], self.options_widget['Номер задания:'],
                                              -1)):
                self.options_widget.set_value('Номер варианта:', -1)
            else:
                for i in range(100):
                    if os.path.isdir(self.sm.lab_path(self.options_widget['Номер лабы:'],
                                                      self.options_widget['Номер задания:'], i)):
                        self.options_widget.set_value('Номер варианта:', i)
                        break
        self.clear_scroll_area()
        self.check_boxes.clear()
        self.get_path()
        self.parse_readme_md()
        self.update_list()

    def get_path(self, from_settings=False):
        if from_settings:
            self.path = self.sm.lab_path()
        else:
            self.path = self.sm.lab_path(self.options_widget['Номер лабы:'], self.options_widget['Номер задания:'],
                                         self.options_widget['Номер варианта:'])

    def parse_readme_md(self):
        self.test_list.clear()
        if not os.path.isfile(f"{self.path}/func_tests/readme.md"):
            return
        file = open(f"{self.path}/func_tests/readme.md", encoding='utf-8')
        lines = file.readlines()
        file.close()

        for i in range(len(lines)):
            if "Позитивные тесты" in lines[i]:
                for j in range(i + 1, len(lines)):
                    if lines[j][:2] == '- ' and lines[j][4:7] == ' - ':
                        self.test_list.append("POS\t" + lines[j][7:].strip())
                    else:
                        break

            elif "Негативные тесты" in lines[i]:
                for j in range(i + 1, len(lines)):
                    if lines[j][:2] == '- ' and lines[j][4:7] == ' - ':
                        self.test_list.append("NEG\t" + lines[j][7:].strip())
                    else:
                        break

    def update_list(self):
        for el in self.test_list:
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignLeft)
            check_box = QCheckBox()
            self.check_boxes.append(check_box)
            layout.addWidget(check_box)
            layout.addWidget(QLabel(el))
            widget.setLayout(layout)
            self.scroll_layout.addWidget(widget)

    def clear_scroll_area(self):
        for i in range(self.scroll_layout.count() - 1, -1, -1):
            self.scroll_layout.itemAt(i).widget().deleteLater()

    def copy_tests(self):
        pos_ind = 0
        neg_ind = 0
        for i in range(len(self.test_list)):
            if self.test_list[i].startswith("POS"):
                pos_ind += 1
                if self.check_boxes[i].isChecked():
                    yield self.test_list[i][4:], \
                          read_file(f"{self.path}/func_tests/data/pos_{pos_ind:0>2}_in.txt"), \
                          read_file(f"{self.path}/func_tests/data/pos_{pos_ind:0>2}_out.txt")
            else:
                neg_ind += 1
                if self.check_boxes[i].isChecked():
                    yield self.test_list[i][4:], \
                          read_file(f"{self.path}/func_tests/data/neg_{neg_ind:0>2}_in.txt"), \
                          read_file(f"{self.path}/func_tests/data/neg_{neg_ind:0>2}_out.txt")
