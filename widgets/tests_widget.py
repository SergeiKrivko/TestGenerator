import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog, QDialogButtonBox, QScrollArea, \
    QHBoxLayout, QCheckBox, QLabel, QListWidgetItem

from widgets.generator_window import GeneratorWindow
from widgets.message_box import MessageBox
from widgets.options_window import OptionsWidget
from widgets.test_table_widget import TestTableWidget
from widgets.test_edit_widget import TestEditWidget
from other.macros_converter import MacrosConverter, background_process_manager


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
        # self.generator_window.complete.connect(self.write_readme_after_generation)

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
        self.test_edit_widget.test_edited.connect(self.set_tests_changed)
        # self.test_edit_widget.button_generate.clicked.connect(self.generate_test)
        layout.addWidget(self.test_edit_widget)

        self.setLayout(layout)

        self.selected_test = 'pos'

        self.path = ''
        self.data_dir = ''
        self.current_test = None
        self.loopers = dict()
        self.file_compiled = False
        self.temp_file_index = 0
        self.tests_changed = False

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
        self.tests_changed = True
        if not os.path.isdir(f"{self.data_dir}/pos"):
            os.makedirs(f"{self.data_dir}/pos")
        self.test_list_widget.pos_test_list.addItem(Test(self.create_temp_file(), self.tm))

    def add_neg_test(self):
        self.tests_changed = True
        if not os.path.isdir(f"{self.data_dir}/neg"):
            os.makedirs(f"{self.data_dir}/neg")
        self.test_list_widget.neg_test_list.addItem(Test(self.create_temp_file(), self.tm))

    def delete_pos_test(self):
        self.tests_changed = True
        if self.test_list_widget.pos_test_list.count() == 0:
            return
        ind = self.test_list_widget.pos_test_list.currentRow()
        if ind == -1:
            return
        item = self.test_list_widget.pos_test_list.takeItem(ind)
        item.remove_file()
        if self.test_list_widget.pos_test_list.count() == 0:
            self.test_edit_widget.set_disabled()
        else:
            self.test_list_widget.pos_test_list.setCurrentRow(
                ind if ind < self.test_list_widget.pos_test_list.count() else ind - 1)

    def delete_neg_test(self):
        self.tests_changed = True
        if self.test_list_widget.neg_test_list.count() == 0:
            return
        ind = self.test_list_widget.neg_test_list.currentRow()
        if ind == -1:
            return
        item = self.test_list_widget.neg_test_list.takeItem(ind)
        item.remove_file()
        if self.test_list_widget.neg_test_list.count() == 0:
            self.test_edit_widget.set_disabled()
        else:
            self.test_list_widget.neg_test_list.setCurrentRow(
                ind if ind < self.test_list_widget.neg_test_list.count() else ind - 1)

    def copy_tests(self, test_type='pos'):
        dlg = TestCopyWindow(self.sm, self.tm)
        if dlg.exec():
            for dct in dlg.copy_tests():
                item = Test(self.create_temp_file(), tm=self.tm)

                item.dict = dct
                item['desc'] = dct.get('desc', '-')
                item.store()

                if test_type == 'pos':
                    self.test_list_widget.pos_test_list.addItem(item)
                else:
                    self.test_list_widget.neg_test_list.addItem(item)

    def set_tests_changed(self):
        self.tests_changed = True

    def select_pos_test(self):
        item = self.test_list_widget.pos_test_list.currentItem()
        if self.current_test:
            self.current_test.store()
        if isinstance(item, Test):
            self.test_list_widget.neg_test_list.setCurrentItem(None)
            item.load()
            self.current_test = item
            self.test_edit_widget.open_test(item.dict)

    def select_neg_test(self):
        item = self.test_list_widget.neg_test_list.currentItem()
        if self.current_test:
            self.current_test.store()
        if isinstance(item, Test):
            self.test_list_widget.pos_test_list.setCurrentItem(None)
            item.load()
            self.current_test = item
            self.test_edit_widget.open_test(item.dict)

    def move_pos_test_up(self):
        self.tests_changed = True
        index = self.test_list_widget.pos_test_list.currentRow()
        if index <= 0:
            return
        item = self.test_list_widget.pos_test_list.takeItem(index)
        self.test_list_widget.pos_test_list.insertItem(index - 1, item)
        self.test_list_widget.pos_test_list.setCurrentRow(index - 1)

    def move_pos_test_down(self):
        self.tests_changed = True
        index = self.test_list_widget.pos_test_list.currentRow()
        if index >= self.test_list_widget.pos_test_list.count() - 1:
            return
        item = self.test_list_widget.pos_test_list.takeItem(index)
        self.test_list_widget.pos_test_list.insertItem(index + 1, item)
        self.test_list_widget.pos_test_list.setCurrentRow(index + 1)

    def move_neg_test_up(self):
        self.tests_changed = True
        index = self.test_list_widget.neg_test_list.currentRow()
        if index <= 0:
            return
        item = self.test_list_widget.neg_test_list.takeItem(index)
        self.test_list_widget.neg_test_list.insertItem(index - 1, item)
        self.test_list_widget.neg_test_list.setCurrentRow(index - 1)

    def move_neg_test_down(self):
        self.tests_changed = True
        index = self.test_list_widget.neg_test_list.currentRow()
        if index >= self.test_list_widget.neg_test_list.count() - 1:
            return
        item = self.test_list_widget.neg_test_list.takeItem(index)
        self.test_list_widget.neg_test_list.insertItem(index + 1, item)
        self.test_list_widget.neg_test_list.setCurrentRow(index + 1)

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
        try:
            self.test_list_widget.pos_comparator_widget.setCurrentIndex(self.sm.get('pos_comparators', dict()).get(
                f"{self.sm.get('lab')}_{self.sm.get('task')}_{self.sm.get('var')}", -1) + 1)
            self.test_list_widget.neg_comparator_widget.setCurrentIndex(self.sm.get('neg_comparators', dict()).get(
                f"{self.sm.get('lab')}_{self.sm.get('task')}_{self.sm.get('var')}", -1) + 1)
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")

        path = f"{self.sm.data_lab_path()}/func_tests/preprocessor.txt"
        self.test_edit_widget.preprocessor_line.setText(read_file(path, ''))
        path = f"{self.sm.data_lab_path()}/func_tests/postprocessor.txt"
        self.test_edit_widget.postprocessor_line.setText(read_file(path, ''))

        self.data_dir = f"{self.sm.data_lab_path()}/func_tests"
        if not os.path.isdir(self.data_dir):
            self.open_tests_from_readme()
        else:
            if os.path.isdir(f"{self.data_dir}/pos"):
                lst = list(filter(lambda s: s.rstrip('.json').isdigit(), os.listdir(f"{self.data_dir}/pos")))
                lst.sort(key=lambda s: int(s.rstrip('.json')))
                for el in lst:
                    self.test_list_widget.pos_test_list.addItem(Test(f"{self.data_dir}/pos/{el}", self.tm))

            if os.path.isdir(f"{self.data_dir}/neg"):
                lst = list(filter(lambda s: s.rstrip('.json').isdigit(), os.listdir(f"{self.data_dir}/neg")))
                lst.sort(key=lambda s: int(s.rstrip('.json')))
                for el in lst:
                    self.test_list_widget.neg_test_list.addItem(Test(f"{self.data_dir}/neg/{el}", self.tm))

    def open_tests_from_readme(self):
        if not os.path.isdir(f"{self.path}/func_tests/data"):
            return

        self.remove_temp_files()
        self.temp_file_index = 0

        self.readme_parser()
        self.load_data_files()
        self.tests_changed = True
        self.test_edit_widget.set_disabled()

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

        os.makedirs(f"{self.data_dir}/pos", exist_ok=True)
        os.makedirs(f"{self.data_dir}/neg", exist_ok=True)

        for i in range(len(lines)):
            if "Позитивные тесты" in lines[i]:
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith('- ') and ' - ' in lines[j]:
                        item = Test(self.create_temp_file(), self.tm)
                        item.load()
                        item['desc'] = lines[j][lines[j].index(' - ') + 3:].strip()
                        item.store()
                        self.test_list_widget.pos_test_list.addItem(item)
                    else:
                        break

            elif "Негативные тесты" in lines[i]:
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith('- ') and ' - ' in lines[j]:
                        item = Test(self.create_temp_file(), self.tm)
                        item.load()
                        item['desc'] = lines[j][lines[j].index(' - ') + 3:].strip()
                        item.store()
                        self.test_list_widget.neg_test_list.addItem(item)
                    else:
                        break

            elif "Вход" in lines[i] or "Входные данные" in lines[i]:
                self.options_widget.set_value("Вход:", lines[i + 1].strip())

            elif "Выход" in lines[i] or "Выходные данные" in lines[i]:
                self.options_widget.set_value("Выход:", lines[i + 1].strip())

    def load_data_files(self):
        def get_files(test_type='pos'):
            list_widget = self.test_list_widget.pos_test_list if test_type == 'pos' else \
                self.test_list_widget.neg_test_list
            j = 0
            for j in range(list_widget.count()):
                yield j
            j += 1
            while os.path.isfile(f"{self.path}/func_tests/data/{test_type}_{j + 1:0>2}_in.txt"):
                list_widget.addItem(Test(self.create_temp_file(), self.tm))
                yield j
                j += 1

        if not os.path.isdir(f"{self.path}/func_tests/data"):
            return

        for i in get_files('pos'):
            item = self.test_list_widget.pos_test_list.item(i)
            item.load()
            item['in'] = read_file(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_in.txt", '')
            item['out'] = read_file(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_out.txt", '')
            item['args'] = read_file(f"{self.path}/func_tests/data/pos_{i + 1:0>2}_args.txt", '')
            item.store()

        for i in get_files('neg'):
            item = self.test_list_widget.neg_test_list.item(i)
            item.load()
            item['in'] = read_file(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_in.txt", '')
            item['out'] = read_file(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_out.txt", '')
            item['args'] = read_file(f"{self.path}/func_tests/data/neg_{i + 1:0>2}_args.txt", '')
            item.store()

    def generate_test(self):
        self.data_changed = True
        os.makedirs(f"{self.path}/func_tests/data", exist_ok=True)

        old_dir = os.getcwd()
        os.chdir(self.path)

        item = self.test_list_widget.pos_test_list.currentItem() or self.test_list_widget.neg_test_list.currentItem()
        if not item:
            return

        res, stderr = self.cm.compile(coverage=False)
        if not res:
            MessageBox(MessageBox.Warning, "Ошибка компиляции", stderr, self.tm)
            return

        res = self.cm.cmd_command(
            f"{self.path}/app.exe {read_file(item.args_file, '') if 'args_file' in item.__dict__ else ''}",
            shell=True, input=read_file(item.in_file))
        item['out'] = res.stdout

        # if self.sm.get('clear_words', False):
        #     clear_words(f"{self.path}/func_tests/data/{type}_{index + 1:0>2}_out.txt")

        self.cm.clear_coverage_files()
        os.chdir(old_dir)

    def remove_temp_files(self):
        for file in os.listdir(f"{self.path}/func_tests/data"):
            if file.startswith('temp'):
                os.remove(f"{self.path}/func_tests/data/{file}")

    def save_tests(self):
        if not self.test_list_widget.pos_test_list.count() and not self.test_list_widget.neg_test_list.count() or \
                not self.tests_changed:
            return
        item = self.test_list_widget.pos_test_list.currentItem() or \
               self.test_list_widget.neg_test_list.currentItem()
        if item:
            item.store()

        os.makedirs(f"{self.data_dir}/pos", exist_ok=True)
        os.makedirs(f"{self.data_dir}/neg", exist_ok=True)

        os.makedirs(f"{self.path}/func_tests/data", exist_ok=True)
        readme = open(f"{self.path}/func_tests/readme.md", 'w', encoding='utf-8', newline=self.sm.get('line_sep'))
        readme.write(f"# Тесты для лабораторной работы №{self.sm.get('lab'):0>2}, задания №"
                     f"{self.sm.get('task'):0>2}\n\n"
                     f"## Входные данные\n{self.options_widget['Вход:']}\n\n"
                     f"## Выходные данные\n{self.options_widget['Выход:']}\n")

        for i in range(self.test_list_widget.pos_test_list.count()):
            item = self.test_list_widget.pos_test_list.item(i)
            if not item.path.endswith(f"{i}.json"):
                item.rename_file(f"{self.data_dir}/pos/{i}.json")

        for i in range(self.test_list_widget.neg_test_list.count()):
            item = self.test_list_widget.neg_test_list.item(i)
            if not item.path.endswith(f"{i}.json"):
                item.rename_file(f"{self.data_dir}/neg/{i}.json")

        if self.data_dir in background_process_manager.dict:
            background_process_manager.dict[self.data_dir].close()

        looper = MacrosConverter(self.data_dir, f"{self.sm.lab_path()}", {
            'pos_in': 'func_tests/data/pos_{:0>2}_in.txt',
            'pos_out': 'func_tests/data/pos_{:0>2}_out.txt',
            'pos_args': 'func_tests/data/pos_{:0>2}_args.txt',
            'neg_in': 'func_tests/data/neg_{:0>2}_in.txt',
            'neg_out': 'func_tests/data/neg_{:0>2}_out.txt',
            'neg_args': 'func_tests/data/neg_{:0>2}_args.txt',

            'pos_in_files': 'func_tests/data_files/pos_{:0>2}_in{}',
            'pos_out_files': 'func_tests/data_files/pos_{:0>2}_out{}',
            'pos_check_files': 'func_tests/data_files/pos_{:0>2}_check{}',
            'neg_in_files': 'func_tests/data_files/neg_{:0>2}_in{}',
            'neg_out_files': 'func_tests/data_files/neg_{:0>2}_out{}',
            'neg_check_files': 'func_tests/data_files/neg_{:0>2}_check{}',
        }, self.sm, readme)
        self.loopers[self.sm.lab_path()] = looper
        looper.start()

    def write_file(self, path, data=''):
        file = open(path, 'w', encoding='utf-8', newline=self.sm.get_general('line_sep'))
        file.write(data)
        file.close()

    def create_temp_file(self):
        path = f"{self.data_dir}/temp_{self.temp_file_index}"
        self.temp_file_index += 1
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


class Test(QListWidgetItem):
    files_links = dict()

    def __init__(self, file, tm):
        super(Test, self).__init__()
        self.path = file
        Test.files_links[self.path] = self

        self.load()
        self.setText(self.get('desc', '-'))
        self.dict = None

        self.setFont(tm.font_small)

    def load(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                self.dict = json.loads(f.read())
        except FileNotFoundError:
            self.dict = {'desc': '-', 'in': '', 'out': '', 'args': ''}
        except json.JSONDecodeError:
            self.dict = {'desc': '-', 'in': '', 'out': '', 'args': ''}

    def store(self):
        if self.dict is None:
            return
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.dict))
        self.dict = None

    def get(self, key, default):
        return self.dict.get(key, default)

    def rename_file(self, new_name):
        Test.files_links.pop(self.path)
        if new_name in Test.files_links:
            other_test = Test.files_links[new_name]
            old_name = self.path
            other_test.rename_file(f"{os.path.split(other_test.path)[0]}/temp")
            os.rename(self.path, new_name)
            other_test.rename_file(old_name)
        else:
            os.rename(self.path, new_name)
        self.path = new_name
        Test.files_links[new_name] = self

    def remove_file(self):
        try:
            os.remove(self.path)
            Test.files_links.pop(self.path)
        except FileNotFoundError:
            pass

    def update_name(self):
        self.setText(self.dict.get('desc', ''))

    def __getitem__(self, item):
        return self.dict[item]

    def __setitem__(self, key, value):
        if key == 'desc':
            self.setText(value)
        self.dict[key] = value


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
        self.open_task()
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
        self.open_task()
        self.update_list()

    def get_path(self, from_settings=False):
        if from_settings:
            self.path = self.sm.lab_path()
            self.data_dir = self.sm.data_lab_path() + '/func_tests'
        else:
            self.path = self.sm.lab_path(self.options_widget['Номер лабы:'], self.options_widget['Номер задания:'],
                                         self.options_widget['Номер варианта:'])
            self.data_dir = self.sm.data_lab_path(self.options_widget['Номер лабы:'],
                                                  self.options_widget['Номер задания:'],
                                                  self.options_widget['Номер варианта:']) + '/func_tests'

    def open_task(self):
        self.test_list.clear()
        print(f"{self.data_dir}/pos")
        if os.path.isdir(f"{self.data_dir}/pos"):
            lst = list(filter(lambda s: s.rstrip('.json').isdigit(), os.listdir(f"{self.data_dir}/pos")))
            lst.sort(key=lambda s: int(s.rstrip('.json')))
            for i, el in enumerate(lst):
                with open(f"{self.data_dir}/pos/{el}", encoding='utf-8') as f:
                    try:
                        desc = json.loads(f.read()).get('desc', '-')
                    except json.JSONDecodeError:
                        desc = '-'
                    self.test_list.append(f"POS {i}\t{desc}")

        if os.path.isdir(f"{self.data_dir}/neg"):
            lst = list(filter(lambda s: s.rstrip('.json').isdigit(), os.listdir(f"{self.data_dir}/neg")))
            lst.sort(key=lambda s: int(s.rstrip('.json')))
            for i, el in enumerate(lst):
                with open(f"{self.data_dir}/neg/{el}", encoding='utf-8') as f:
                    try:
                        desc = json.loads(f.read()).get('desc', '-')
                    except json.JSONDecodeError:
                        desc = '-'
                    self.test_list.append(f"neg {i}\t{desc}")

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
                    with open(f"{self.data_dir}/pos/{self.test_list[i].split()[1]}.json",
                              encoding='utf-8') as f:
                        try:
                            yield json.loads(f.read())
                        except json.JSONDecodeError:
                            yield dict()

            else:
                neg_ind += 1
                with open(f"{self.data_dir}/neg/{self.test_list[i].split()[1]}.json", encoding='utf-8') as f:
                    try:
                        yield json.loads(f.read())
                    except json.JSONDecodeError:
                        yield dict()
