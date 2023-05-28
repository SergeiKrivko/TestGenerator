import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog, QDialogButtonBox, QScrollArea, \
    QHBoxLayout, QCheckBox, QLabel, QListWidgetItem

from widgets.generator_window import GeneratorWindow
from widgets.message_box import MessageBox
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

        self.generator_window = GeneratorWindow(self.sm, self.cm, self.tm)
        self.generator_window.hide()
        self.generator_window.complete.connect(self.write_readme_after_generation)

        self.test_list_widget = TestTableWidget(self.tm, self.sm)
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
        self.test_list_widget.pos_button_generate.clicked.connect(self.open_pos_generator_window)
        self.test_list_widget.neg_button_generate.clicked.connect(self.open_neg_generator_window)
        self.test_list_widget.pos_test_list.itemSelectionChanged.connect(self.select_pos_test)
        self.test_list_widget.neg_test_list.itemSelectionChanged.connect(self.select_neg_test)
        layout.addWidget(self.test_list_widget)

        self.test_edit_widget = TestEditWidget(self.tm)
        self.test_edit_widget.setMinimumHeight(300)
        self.test_edit_widget.test_name_edit.textEdited.connect(self.set_test_name)
        self.test_edit_widget.test_in_edit.textChanged.connect(self.set_test_in)
        self.test_edit_widget.test_out_edit.textChanged.connect(self.set_test_out)
        self.test_edit_widget.cmd_args_edit.textEdited.connect(self.set_test_args)
        self.test_edit_widget.exit_code_edit.textEdited.connect(self.set_test_exit_code)
        self.test_edit_widget.button_generate.clicked.connect(self.button_generate_test)
        layout.addWidget(self.test_edit_widget)

        self.setLayout(layout)

        self.selected_test = 'pos'

        self.path = ''
        self.file_compiled = False
        self.file_edit_time = dict()
        self.files_links = dict()
        self.temp_file_index = 0
        self.data_changed = False
        self.readme_changed = False

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

    def open_pos_generator_window(self):
        self.save_tests()
        self.generator_window.test_type = 'pos'
        self.generator_window.tests_list = [self.test_list_widget.pos_test_list.item(i).desc for i in
                                            range(self.test_list_widget.pos_test_list.count())]
        self.generator_window.show()

    def open_neg_generator_window(self):
        self.save_tests()
        self.generator_window.test_type = 'neg'
        self.generator_window.tests_list = [self.test_list_widget.neg_test_list.item(i).desc for i in
                                            range(self.test_list_widget.neg_test_list.count())]
        self.generator_window.show()

    def add_pos_test(self):
        self.readme_changed = True
        self.data_changed = True
        if not os.path.isdir(f"{self.path}/func_tests/data"):
            os.makedirs(f"{self.path}/func_tests/data")
        item = CustomListWidgetItem('-', tm=self.tm)
        item.in_file = self.create_temp_file(item)
        item.out_file = self.create_temp_file(item)
        self.test_list_widget.pos_test_list.addItem(item)

    def add_neg_test(self):
        self.readme_changed = True
        self.data_changed = True
        if not os.path.isdir(f"{self.path}/func_tests/data"):
            os.makedirs(f"{self.path}/func_tests/data")
        item = CustomListWidgetItem('-', tm=self.tm)
        item.in_file = self.create_temp_file(item)
        item.out_file = self.create_temp_file(item)
        self.test_list_widget.neg_test_list.addItem(item)

    def delete_pos_test(self):
        self.readme_changed = True
        self.data_changed = True
        if self.test_list_widget.pos_test_list.count() == 0:
            return
        ind = self.test_list_widget.pos_test_list.currentRow()
        if ind == -1:
            return
        item = self.test_list_widget.pos_test_list.takeItem(ind)
        if os.path.isfile(item.in_file):
            os.remove(item.in_file)
        if os.path.isfile(item.out_file):
            os.remove(item.out_file)
        if os.path.isfile(item.args_file):
            os.remove(item.args_file)
        if self.test_list_widget.pos_test_list.count() == 0:
            self.test_edit_widget.set_disabled()
        else:
            self.test_list_widget.pos_test_list.setCurrentRow(
                ind if ind < self.test_list_widget.pos_test_list.count() else ind - 1)

    def delete_neg_test(self):
        self.readme_changed = True
        self.data_changed = True
        if self.test_list_widget.neg_test_list.count() == 0:
            return
        ind = self.test_list_widget.neg_test_list.currentRow()
        if ind == -1:
            return
        item = self.test_list_widget.neg_test_list.takeItem(ind)
        if os.path.isfile(item.in_file):
            os.remove(item.in_file)
        if os.path.isfile(item.out_file):
            os.remove(item.out_file)
        if os.path.isfile(item.args_file):
            os.remove(item.args_file)
        if self.test_list_widget.neg_test_list.count() == 0:
            self.test_edit_widget.set_disabled()
        else:
            self.test_list_widget.neg_test_list.setCurrentRow(
                ind if ind < self.test_list_widget.neg_test_list.count() else ind - 1)

    def copy_tests(self, test_type='pos'):
        dlg = TestCopyWindow(self.sm, self.tm)
        if dlg.exec():
            for desc, in_data, out_data, args_data in dlg.copy_tests():
                item = CustomListWidgetItem(desc, tm=self.tm)

                item.in_file = self.create_temp_file(item)
                self.write_file(item.in_file, in_data)

                item.out_file = self.create_temp_file(item)
                self.write_file(item.out_file, out_data)

                if args_data:
                    item.args_file = self.create_temp_file(item)
                    self.write_file(item.args_file, args_data)

                if test_type == 'pos':
                    self.test_list_widget.pos_test_list.addItem(item)
                else:
                    self.test_list_widget.neg_test_list.addItem(item)

    def select_pos_test(self):
        try:
            item = self.test_list_widget.pos_test_list.currentItem()
            if item:
                self.test_list_widget.neg_test_list.setCurrentItem(None)
            self.test_edit_widget.open_test(
                item.desc, read_file(item.in_file, default=''), read_file(item.out_file, default=''),
                read_file(item.args_file, default=''), str(item.exit_code) if item.exit_code is not None else '')
        except AttributeError:
            pass

    def select_neg_test(self):
        try:
            item = self.test_list_widget.neg_test_list.currentItem()
            if item:
                self.test_list_widget.pos_test_list.setCurrentItem(None)
            self.test_edit_widget.open_test(
                item.desc, read_file(item.in_file, default=''), read_file(item.out_file, default=''),
                read_file(item.args_file, default=''), item.exit_code)
        except AttributeError:
            pass

    def set_test_name(self, name):
        self.readme_changed = True
        if self.test_list_widget.pos_test_list.currentItem() is not None:
            self.test_list_widget.pos_test_list.currentItem().set_desc(name)
        elif self.test_list_widget.neg_test_list.currentItem() is not None:
            self.test_list_widget.neg_test_list.currentItem().set_desc(name)

    def set_test_in(self):
        data = self.test_edit_widget.test_in_edit.toPlainText()
        item = self.test_list_widget.pos_test_list.currentItem() or self.test_list_widget.neg_test_list.currentItem()
        if item:
            self.write_file(item.in_file, data)

    def set_test_args(self):
        data = self.test_edit_widget.cmd_args_edit.text()
        item = self.test_list_widget.pos_test_list.currentItem() or self.test_list_widget.neg_test_list.currentItem()
        if item:
            if not data and item.args_file:
                os.remove(item.args_file)
                item.args_file = ''
            elif data:
                if not item.args_file:
                    item.args_file = self.create_temp_file(item)
                self.write_file(item.args_file, data)

    def set_test_out(self):
        data = self.test_edit_widget.test_out_edit.toPlainText()
        item = self.test_list_widget.pos_test_list.currentItem() or self.test_list_widget.neg_test_list.currentItem()
        if item:
            if not item.out_file:
                item.out_file = self.create_temp_file(item)
            self.write_file(item.out_file, data)

    def set_test_exit_code(self):
        code = self.test_edit_widget.exit_code_edit.text()
        item = self.test_list_widget.pos_test_list.currentItem() or self.test_list_widget.neg_test_list.currentItem()
        if item:
            item.exit_code = int(code) if code else None
        self.data_changed = True

    def move_pos_test_up(self):
        self.readme_changed = True
        self.data_changed = True
        index = self.test_list_widget.pos_test_list.currentRow()
        if index <= 0:
            return
        item = self.test_list_widget.pos_test_list.takeItem(index)
        self.test_list_widget.pos_test_list.insertItem(index - 1, item)
        self.test_list_widget.pos_test_list.setCurrentRow(index - 1)

    def move_pos_test_down(self):
        self.readme_changed = True
        self.data_changed = True
        index = self.test_list_widget.pos_test_list.currentRow()
        if index >= self.test_list_widget.pos_test_list.count() - 1:
            return
        item = self.test_list_widget.pos_test_list.takeItem(index)
        self.test_list_widget.pos_test_list.insertItem(index + 1, item)
        self.test_list_widget.pos_test_list.setCurrentRow(index + 1)

    def move_neg_test_up(self):
        self.readme_changed = True
        self.data_changed = True
        index = self.test_list_widget.neg_test_list.currentRow()
        if index <= 0:
            return
        item = self.test_list_widget.neg_test_list.takeItem(index)
        self.test_list_widget.neg_test_list.insertItem(index - 1, item)
        self.test_list_widget.neg_test_list.setCurrentRow(index - 1)

    def move_neg_test_down(self):
        self.readme_changed = True
        self.data_changed = True
        index = self.test_list_widget.neg_test_list.currentRow()
        if index >= self.test_list_widget.neg_test_list.count() - 1:
            return
        item = self.test_list_widget.neg_test_list.takeItem(index)
        self.test_list_widget.neg_test_list.insertItem(index + 1, item)
        self.test_list_widget.neg_test_list.setCurrentRow(index + 1)

    def button_generate_test(self):
        self.data_changed = True
        if self.test_list_widget.pos_test_list.currentItem() is not None:
            self.generate_test('pos')
        elif self.test_list_widget.neg_test_list.currentItem() is not None:
            self.generate_test('neg')

    def get_path(self, from_settings=False):
        if from_settings:
            self.path = self.sm.lab_path()
        else:
            self.path = self.sm.lab_path(self.options_widget['Номер лабы:'], self.options_widget['Номер задания:'],
                                         self.options_widget['Номер варианта:'])

    def open_tests(self):
        self.get_path()
        self.test_list_widget.pos_test_list.clear()
        self.test_list_widget.neg_test_list.clear()
        if not os.path.isdir(f"{self.path}/func_tests/data"):
            return
        try:
            self.test_list_widget.pos_comparator_widget.setCurrentIndex(self.sm.get('pos_comparators', dict()).get(
                f"{self.sm.get('lab')}_{self.sm.get('task')}_{self.sm.get('var')}", -1) + 1)
            self.test_list_widget.neg_comparator_widget.setCurrentIndex(self.sm.get('neg_comparators', dict()).get(
                f"{self.sm.get('lab')}_{self.sm.get('task')}_{self.sm.get('var')}", -1) + 1)
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")

        self.remove_temp_files()
        self.files_links.clear()
        self.temp_file_index = 0

        self.readme_parser()
        self.readme_changed = False
        self.load_data_files()
        self.data_changed = False
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
                        self.test_list_widget.pos_test_list.addItem(
                            CustomListWidgetItem(lines[j][lines[j].index(' - ') + 3:].strip(), '', '', tm=self.tm))
                    else:
                        break

            elif "Негативные тесты" in lines[i]:
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith('- ') and ' - ' in lines[j]:
                        self.test_list_widget.neg_test_list.addItem(
                            CustomListWidgetItem(lines[j][lines[j].index(' - ') + 3:].strip(), '', '', tm=self.tm))
                    else:
                        break

            elif "Вход" in lines[i] or "Входные данные" in lines[i]:
                self.options_widget.set_value("Вход:", lines[i + 1].strip())

            elif "Выход" in lines[i] or "Выходные данные" in lines[i]:
                self.options_widget.set_value("Выход:", lines[i + 1].strip())

    def load_data_files(self):
        path = f"{self.sm.lab_path(appdata=True)}/func_tests/preprocessor.txt"
        self.test_edit_widget.preprocessor_line.setText(read_file(path, ''))
        path = f"{self.sm.lab_path(appdata=True)}/func_tests/postprocessor.txt"
        self.test_edit_widget.postprocessor_line.setText(read_file(path, ''))

        exit_codes = json.loads(read_file(f"{self.sm.lab_path(appdata=True)}/exit_codes.txt", '{}'))

        if not os.path.isdir(f"{self.path}/func_tests/data"):
            return

        lst, count = [], 0

        for file in os.listdir(f"{self.path}/func_tests/data"):
            if file.startswith('pos_') and file.endswith('_in.txt') and file.lstrip('pos_').rstrip('_in.txt').isdigit():
                index = int(file.lstrip('pos_').rstrip('_in.txt'))
                count += 1
                item = self.test_list_widget.pos_test_list.item(index - 1)
                if index <= self.test_list_widget.pos_test_list.count():
                    item.in_file = f"{self.path}/func_tests/data/{file}"
                    self.files_links[item.in_file] = item
                    if os.path.isfile(f := f"{self.path}/func_tests/data/{file.replace('in', 'out')}"):
                        item.out_file = f
                        self.files_links[f] = item
                    if os.path.isfile(f := f"{self.path}/func_tests/data/{file.replace('in', 'args')}"):
                        item.args_file = f
                        self.files_links[f] = item
                else:
                    lst.append(index)

        lst.sort()
        for _ in range(count - self.test_list_widget.pos_test_list.count()):
            self.test_list_widget.pos_test_list.addItem(CustomListWidgetItem('-', tm=self.tm))
        for i in range(self.test_list_widget.pos_test_list.count()):
            item = self.test_list_widget.pos_test_list.item(i)
            item.exit_code = exit_codes.get(f"pos{i + 1}")
            if not item.in_file:
                if len(lst):
                    item.in_file = f"{self.path}/func_tests/data/pos_{lst[0]:0>2}_in.txt"
                    self.files_links[item.in_file] = item
                    if os.path.isfile(f := f"{self.path}/func_tests/data/pos_{lst[0]:0>2}_out.txt"):
                        item.out_file = f
                        self.files_links[f] = item
                    if os.path.isfile(f := f"{self.path}/func_tests/data/pos_{lst[0]:0>2}_args.txt"):
                        item.args_file = f
                        self.files_links[f] = item
                    lst.pop(0)
                else:
                    item.in_file = self.create_temp_file(item)
                    item.out_file = self.create_temp_file(item)

        lst, count = [], 0

        for file in os.listdir(f"{self.path}/func_tests/data"):
            if file.startswith('neg_') and file.endswith('_in.txt') and file.lstrip('neg_').rstrip('_in.txt').isdigit():
                index = int(file.lstrip('neg_').rstrip('_in.txt'))
                count += 1
                item = self.test_list_widget.neg_test_list.item(index - 1)
                if index <= self.test_list_widget.neg_test_list.count():
                    item.in_file = f"{self.path}/func_tests/data/{file}"
                    self.files_links[item.in_file] = item
                    if os.path.isfile(f := f"{self.path}/func_tests/data/{file.replace('in', 'out')}"):
                        item.out_file = f
                        self.files_links[f] = item
                    if os.path.isfile(f := f"{self.path}/func_tests/data/{file.replace('in', 'args')}"):
                        item.args_file = f
                        self.files_links[f] = item
                else:
                    lst.append(index)

        lst.sort()
        for _ in range(count - self.test_list_widget.neg_test_list.count()):
            self.test_list_widget.neg_test_list.addItem(CustomListWidgetItem('-', tm=self.tm))
        for i in range(self.test_list_widget.neg_test_list.count()):
            item = self.test_list_widget.neg_test_list.item(i)
            item.exit_code = exit_codes.get(f"neg{i + 1}")
            if not item.in_file:
                if len(lst):
                    item.in_file = f"{self.path}/func_tests/data/neg_{lst[0]:0>2}_in.txt"
                    self.files_links[item.in_file] = item
                    if os.path.isfile(f := f"{self.path}/func_tests/data/neg_{lst[0]:0>2}_out.txt"):
                        item.out_file = f
                        self.files_links[f] = item
                    if os.path.isfile(f := f"{self.path}/func_tests/data/neg_{lst[0]:0>2}_args.txt"):
                        item.args_file = f
                        self.files_links[f] = item
                    lst.pop(0)
                else:
                    item.in_file = self.create_temp_file(item)
                    item.out_file = self.create_temp_file(item)

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

        item = self.test_list_widget.pos_test_list.item(index) if type == 'pos' else \
            self.test_list_widget.neg_test_list.item(index)

        in_name = f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_in.txt"
        out_name = f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_out.txt"
        args_name = f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_args.txt"

        if item.in_file != in_name:
            if in_name in self.files_links:
                other_item = self.files_links[in_name]
                if os.path.isfile(other_item.in_file):
                    self.rename_in_file(other_item, self.create_temp_file(other_item, create_file=False))
            self.rename_in_file(item, in_name)

        if item.out_file != out_name:
            if out_name in self.files_links:
                other_item = self.files_links[out_name]
                if os.path.isfile(other_item.out_file):
                    self.rename_out_file(other_item, self.create_temp_file(other_item, create_file=False))
            self.rename_out_file(item, out_name)

        if item.args_file and item.args_file != args_name:
            if args_name in self.files_links:
                other_item = self.files_links[args_name]
                if os.path.isfile(other_item.args_file):
                    self.rename_args_file(other_item, self.create_temp_file(other_item, create_file=False))
            self.rename_args_file(item, args_name)

    def generate_test(self, type='pos'):
        self.data_changed = True
        os.makedirs(f"{self.path}/func_tests/data", exist_ok=True)

        old_dir = os.getcwd()
        os.chdir(self.path)

        item = self.test_list_widget.pos_test_list.currentItem() if type == 'pos' else \
            self.test_list_widget.neg_test_list.currentItem()
        if not item:
            return

        if not self.compare_edit_time():
            self.update_edit_time()
            if not self.cm.compile(coverage=False):
                return

        res = self.cm.cmd_command(
            f"{self.path}/app.exe {read_file(item.args_file, '') if 'args_file' in item.__dict__ else ''}",
            shell=True, input=read_file(item.in_file))
        self.write_file(item.out_file, res.stdout)
        # if self.sm.get('clear_words', False):
        #     clear_words(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_out.txt")

        self.cm.clear_coverage_files()
        os.chdir(old_dir)

    def remove_temp_files(self):
        for file in os.listdir(f"{self.path}/func_tests/data"):
            if file.startswith('temp'):
                os.remove(f"{self.path}/func_tests/data/{file}")

    def write_readme_after_generation(self, lst, type='pos'):
        self.readme_changed = True
        self.data_changed = True
        readme = open(f"{self.path}/func_tests/readme.md", 'w', encoding='utf-8', newline=self.sm.get('line_sep'))
        readme.write(f"# Тесты для лабораторной работы №{self.sm.get('lab'):0>2}, задания №"
                     f"{self.sm.get('task'):0>2}\n\n"
                     f"## Входные данные\n{self.options_widget['Вход:']}\n\n"
                     f"## Выходные данные\n{self.options_widget['Выход:']}\n\n"
                     f"## Позитивные тесты:\n")
        if type == 'pos':
            for i in range(1, len(lst) + 1):
                readme.write(f"- {i + 1:0>2} - {lst[i - 1]}\n")
        else:
            for i in range(self.test_list_widget.pos_test_list.count()):
                readme.write(f"- {i + 1:0>2} - {self.test_list_widget.pos_test_list.item(i).desc}\n")

        readme.write("\n## Негативные тесты:\n")

        if type == 'neg':
            for i in range(1, len(lst) + 1):
                readme.write(f"- {i + 1:0>2} - {lst[i - 1]}\n")
        else:
            for i in range(self.test_list_widget.neg_test_list.count()):
                readme.write(f"- {i + 1:0>2} - {self.test_list_widget.neg_test_list.item(i).desc}\n")

        readme.close()

        self.open_tests()

    def save_tests(self):
        if not os.path.isfile(f"{self.path}/main.c") and not self.test_list_widget.pos_test_list.count() and \
                not self.test_list_widget.neg_test_list.count() and \
                not os.path.isfile(f"{self.path}/func_tests/readme.md"):
            return
        try:
            if self.readme_changed:
                os.makedirs(f"{self.path}/func_tests/data", exist_ok=True)
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

            if self.data_changed:
                exit_codes = dict()
                for i in range(self.test_list_widget.pos_test_list.count()):
                    self.save_a_test(i, 'pos')
                    if code := self.test_list_widget.pos_test_list.item(i).exit_code:
                        exit_codes[f"pos{i + 1}"] = code
                for i in range(self.test_list_widget.neg_test_list.count()):
                    self.save_a_test(i, 'neg')
                    if code := self.test_list_widget.neg_test_list.item(i).exit_code:
                        exit_codes[f"neg{i + 1}"] = code
                os.makedirs(self.sm.lab_path(appdata=True), exist_ok=True)
                self.write_file(f"{self.sm.lab_path(appdata=True)}/exit_codes.txt", json.dumps(exit_codes))
                self.remove_temp_files()

            os.makedirs(f"{self.sm.lab_path(appdata=True)}/func_tests", exist_ok=True)
            text = self.test_edit_widget.preprocessor_line.text()
            path = f"{self.sm.lab_path(appdata=True)}/func_tests/preprocessor.txt"
            if text:
                self.write_file(path, text)
            elif os.path.isfile(path):
                os.remove(path)

            text = self.test_edit_widget.postprocessor_line.text()
            path = f"{self.sm.lab_path(appdata=True)}/func_tests/postprocessor.txt"
            if text:
                self.write_file(path, text)
            elif os.path.isfile(path):
                os.remove(path)

        except Exception as ex:
            MessageBox(MessageBox.Warning, 'Error', f"{ex.__class__.__name__}: {ex}", self.tm)

    def write_file(self, path, data=''):
        file = open(path, 'w', encoding='utf-8', newline=self.sm.get_general('line_sep'))
        file.write(data)
        file.close()

    def rename_in_file(self, item, path):
        self.files_links.pop(item.in_file)
        self.files_links[path] = item
        item.rename_in_file(path)

    def rename_out_file(self, item, path):
        self.files_links.pop(item.out_file)
        self.files_links[path] = item
        item.rename_out_file(path)

    def rename_args_file(self, item, path):
        self.files_links.pop(item.args_file)
        self.files_links[path] = item
        item.rename_args_file(path)

    def create_temp_file(self, item, create_file=True):
        path = f"{self.path}/func_tests/data/temp_{self.temp_file_index}"
        if create_file:
            open(path, 'x').close()
        self.temp_file_index += 1
        self.files_links[path] = item
        return path

    def set_theme(self):
        self.test_list_widget.set_theme()
        self.test_edit_widget.set_theme()
        self.options_widget.set_widget_style_sheet('Номер лабы:', self.tm.spin_box_style_sheet)
        self.options_widget.set_widget_style_sheet('Номер задания:', self.tm.spin_box_style_sheet)
        self.options_widget.set_widget_style_sheet('Номер варианта:', self.tm.spin_box_style_sheet)
        self.options_widget.set_widget_style_sheet('Вход:', self.tm.style_sheet)
        self.options_widget.set_widget_style_sheet('Выход:', self.tm.style_sheet)
        self.options_widget.setFont(self.tm.font_small)
        self.generator_window.set_theme()

    def show(self):
        if self.isHidden():
            self.update_options()
            self.open_tests()
        super(TestsWidget, self).show()

    def hide(self) -> None:
        if not self.isHidden():
            self.save_tests()
            self.test_list_widget.pos_test_list.clear()
            self.test_list_widget.neg_test_list.clear()
        super(TestsWidget, self).hide()


class CustomListWidgetItem(QListWidgetItem):
    def __init__(self, desc, in_file="", out_file="", args_file="", exit_code=None, tm=None):
        super(CustomListWidgetItem, self).__init__()
        self.desc = desc
        self.setText(desc)
        self.in_file = in_file
        self.out_file = out_file
        self.args_file = args_file
        self.exit_code = exit_code

        self.setFont(tm.font_small)

    def rename_in_file(self, path):
        os.rename(self.in_file, path)
        self.in_file = path

    def rename_out_file(self, path):
        os.rename(self.out_file, path)
        self.out_file = path

    def rename_args_file(self, path):
        os.rename(self.args_file, path)
        self.args_file = path

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
    def __init__(self, settings, tm):
        super().__init__()
        self.sm = settings
        self.tm = tm

        self.setWindowTitle("Копировать тесты")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.Ok).setStyleSheet(self.tm.buttons_style_sheet)
        self.buttonBox.button(QDialogButtonBox.Ok).setFixedSize(80, 24)
        self.buttonBox.button(QDialogButtonBox.Cancel).setStyleSheet(self.tm.buttons_style_sheet)
        self.buttonBox.button(QDialogButtonBox.Cancel).setFixedSize(80, 24)

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
        self.options_widget.widgets['Номер лабы:'].setStyleSheet(self.tm.spin_box_style_sheet)
        self.options_widget.widgets['Номер задания:'].setStyleSheet(self.tm.spin_box_style_sheet)
        self.options_widget.widgets['Номер варианта:'].setStyleSheet(self.tm.spin_box_style_sheet)
        self.options_widget.setFont(self.tm.font_small)
        self.layout.addWidget(self.options_widget)
        self.options_widget.clicked.connect(self.options_changed)

        self.scroll_area = QScrollArea()
        self.widget = QWidget()
        self.widget.setStyleSheet(f"background-color: {self.tm['MainColor']};")
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(480, 320)
        self.scroll_area.setStyleSheet(self.tm.scroll_area_style_sheet)
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
            layout.addWidget(label := QLabel(el))
            label.setFont(self.tm.font_small)
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
                          read_file(f"{self.path}/func_tests/data/pos_{pos_ind:0>2}_out.txt"), \
                          read_file(f"{self.path}/func_tests/data/pos_{pos_ind:0>2}_args.txt", default='')
            else:
                neg_ind += 1
                if self.check_boxes[i].isChecked():
                    yield self.test_list[i][4:], \
                          read_file(f"{self.path}/func_tests/data/neg_{neg_ind:0>2}_in.txt"), \
                          read_file(f"{self.path}/func_tests/data/neg_{neg_ind:0>2}_out.txt"), \
                          read_file(f"{self.path}/func_tests/data/neg_{neg_ind:0>2}_args.txt", default='')
