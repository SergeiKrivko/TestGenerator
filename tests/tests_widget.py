import json
import os
import random
from copy import deepcopy

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog, QDialogButtonBox, QScrollArea, \
    QHBoxLayout, QCheckBox, QLabel, QListWidgetItem

from ui.message_box import MessageBox
from ui.options_window import OptionsWidget
from tests.test_table_widget import TestTableWidget
from tests.test_edit_widget import TestEditWidget
from tests.macros_converter import MacrosConverter, background_process_manager


class TestsWidget(QWidget):
    def __init__(self, sm, cm, tm):
        super(TestsWidget, self).__init__()
        self.sm = sm
        self.cm = cm
        self.tm = tm

        layout = QVBoxLayout()

        self.sm.startChangeTask.connect(self.save_tests)
        self.sm.finishChangeTask.connect(self.open_tests)

        self.test_list_widget = TestTableWidget(self.tm, self.sm)
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
        self.test_list_widget.neg_button_generate.clicked.connect(self.generate_neg_tests)
        # self.test_list_widget.pos_button_generate.clicked.connect(self.open_pos_generator_window)
        # self.test_list_widget.neg_button_generate.clicked.connect(self.open_neg_generator_window)
        self.test_list_widget.pos_test_list.itemSelectionChanged.connect(self.select_pos_test)
        self.test_list_widget.neg_test_list.itemSelectionChanged.connect(self.select_neg_test)
        layout.addWidget(self.test_list_widget)

        self.test_edit_widget = TestEditWidget(self.tm)
        self.test_edit_widget.test_edited.connect(self.set_tests_changed)
        self.test_edit_widget.preprocessor_line.textEdited.connect(self.set_preprocessor)
        self.test_edit_widget.postprocessor_line.textEdited.connect(self.set_postprocessor)
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

    def open_tests_after_generation(self):
        self.tests_changed = False
        self.open_tests()

    def set_preprocessor(self):
        self.sm.set_task('preprocessor', self.test_edit_widget.preprocessor_line.text())
        self.tests_changed = True

    def set_postprocessor(self):
        self.sm.set_task('postprocessor', self.test_edit_widget.postprocessor_line.text())
        self.tests_changed = True

    def add_pos_test(self):
        self.tests_changed = True
        if not os.path.isdir(f"{self.data_dir}/pos"):
            os.makedirs(f"{self.data_dir}/pos")
        test = Test(self.create_temp_file(), self.tm)
        if self.test_list_widget.pos_test_list.currentItem():
            index = self.test_list_widget.pos_test_list.currentRow() + 1
        else:
            index = self.test_list_widget.pos_test_list.count()
        self.test_list_widget.pos_test_list.insertItem(index, test)
        self.test_list_widget.pos_test_list.setCurrentRow(index)

    def add_neg_test(self):
        self.tests_changed = True
        if not os.path.isdir(f"{self.data_dir}/neg"):
            os.makedirs(f"{self.data_dir}/neg")
        test = Test(self.create_temp_file(), self.tm)
        if self.test_list_widget.neg_test_list.currentItem():
            index = self.test_list_widget.neg_test_list.currentRow() + 1
        else:
            index = self.test_list_widget.neg_test_list.count()
        self.test_list_widget.neg_test_list.insertItem(index, test)
        self.test_list_widget.neg_test_list.setCurrentRow(index)

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
            self.tests_changed = True
            for dct in dlg.copy_tests():
                item = Test(self.create_temp_file(), tm=self.tm)

                item.set_dict(dct)
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
            self.test_edit_widget.open_test(item)

    def select_neg_test(self):
        item = self.test_list_widget.neg_test_list.currentItem()
        if self.current_test:
            self.current_test.store()
        if isinstance(item, Test):
            self.test_list_widget.pos_test_list.setCurrentItem(None)
            item.load()
            self.current_test = item
            self.test_edit_widget.open_test(item)

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
        self.path = self.sm.lab_path()

    def open_tests(self):
        self.get_path()
        self.test_list_widget.pos_test_list.clear()
        self.test_list_widget.neg_test_list.clear()
        self.test_edit_widget.set_disabled()
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

        self.test_list_widget.in_data_edit.setText('-')
        self.test_list_widget.out_data_edit.setText('-')

        self.data_dir = f"{self.sm.data_lab_path()}/func_tests"
        if not os.path.isdir(self.data_dir):
            try:
                self.open_tests_from_readme()
            except Exception:
                pass
        else:
            self.test_edit_widget.preprocessor_line.setText(self.sm.get_task('preprocessor', ''))
            self.test_edit_widget.postprocessor_line.setText(self.sm.get_task('postprocessor', ''))
            self.test_list_widget.in_data_edit.setText(self.sm.get_task('in_data', '-'))
            self.test_list_widget.out_data_edit.setText(self.sm.get_task('out_data', '-'))

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
                self.test_list_widget.in_data_edit.setText(lines[i + 1].strip())

            elif "Выход" in lines[i] or "Выходные данные" in lines[i]:
                self.test_list_widget.out_data_edit.setText(lines[i + 1].strip())

    def load_data_files(self):
        def get_files(test_type='pos'):
            list_widget = self.test_list_widget.pos_test_list if test_type == 'pos' else \
                self.test_list_widget.neg_test_list
            j = 0
            for j in range(list_widget.count()):
                yield j
            j += 1
            while os.path.isfile(self.sm.test_in_path(test_type, j)):
                list_widget.addItem(Test(self.create_temp_file(), self.tm))
                yield j
                j += 1

        if not os.path.isdir(f"{self.path}/func_tests/data"):
            return

        for i in get_files('pos'):
            item = self.test_list_widget.pos_test_list.item(i)
            item.load()
            item['in'] = read_file(self.sm.test_in_path('pos', i), '')
            item['out'] = read_file(self.sm.test_out_path('pos', i), '')
            item['args'] = read_file(self.sm.test_args_path('pos', i), '')
            item.store()

        for i in get_files('neg'):
            item = self.test_list_widget.neg_test_list.item(i)
            item.load()
            item['in'] = read_file(self.sm.test_in_path('neg', i), '')
            item['out'] = read_file(self.sm.test_out_path('neg', i), '')
            item['args'] = read_file(self.sm.test_args_path('neg', i), '')
            item.store()

    def generate_test(self):
        self.data_changed = True

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
        if self.current_test:
            self.current_test.store()
        if self.path == '':
            return
        if not (self.test_list_widget.pos_test_list.count() or self.test_list_widget.neg_test_list.count()):
            return

        self.sm.set_task('in_data', self.test_list_widget.in_data_edit.text())
        self.sm.set_task('out_data', self.test_list_widget.out_data_edit.text())
        os.makedirs(self.sm.data_lab_path(), exist_ok=True)

        if not self.test_list_widget.pos_test_list.count() and not self.test_list_widget.neg_test_list.count() or \
                not self.tests_changed:
            return
        item = self.test_list_widget.pos_test_list.currentItem() or \
               self.test_list_widget.neg_test_list.currentItem()
        if item:
            item.store()

        for i in range(self.test_list_widget.pos_test_list.count()):
            item = self.test_list_widget.pos_test_list.item(i)
            if not item.path.endswith(f"{i}.json"):
                item.rename_file(f"{self.data_dir}/pos/{i}.json")

        for i in range(self.test_list_widget.neg_test_list.count()):
            item = self.test_list_widget.neg_test_list.item(i)
            if not item.path.endswith(f"{i}.json"):
                item.rename_file(f"{self.data_dir}/neg/{i}.json")

        if self.sm.get('func_tests_in_project', False):
            os.makedirs(f"{self.data_dir}/pos", exist_ok=True)
            os.makedirs(f"{self.data_dir}/neg", exist_ok=True)

            os.makedirs(os.path.split(self.sm.readme_path())[0], exist_ok=True)
            readme = open(self.sm.readme_path(), 'w', encoding='utf-8', newline=self.sm.line_sep)
            readme.write(f"# Тесты для лабораторной работы №{self.sm.get('lab'):0>2}, задания №"
                         f"{self.sm.get('task'):0>2}\n\n"
                         f"## Входные данные\n{self.test_list_widget.in_data_edit.text()}\n\n"
                         f"## Выходные данные\n{self.test_list_widget.out_data_edit.text()}\n")

            if self.data_dir in background_process_manager.dict:
                background_process_manager.dict[self.data_dir].close()

            looper = MacrosConverter(self.data_dir, self.sm.lab_path(), self.sm.project, self.sm, readme)
            self.loopers[self.sm.lab_path()] = looper
            looper.start()

    def write_file(self, path, data=''):
        file = open(path, 'w', encoding='utf-8', newline=self.sm.line_sep)
        file.write(data)
        file.close()

    def create_temp_file(self):
        path = f"{self.data_dir}/temp_{self.temp_file_index}"
        self.temp_file_index += 1
        return path

    def set_theme(self):
        self.test_list_widget.set_theme()
        self.test_edit_widget.set_theme()

    def resizeEvent(self, a0) -> None:
        # if self.height() < 530:
        #     self.options_widget.hide()
        # else:
        #     self.options_widget.show()
        if self.height() < 560:
            self.test_edit_widget.preprocessor_line.hide()
            self.test_edit_widget.preprocessor_label.hide()
            self.test_edit_widget.postprocessor_line.hide()
            self.test_edit_widget.postprocessor_label.hide()
        else:
            self.test_edit_widget.preprocessor_line.show()
            self.test_edit_widget.preprocessor_label.show()
            self.test_edit_widget.postprocessor_line.show()
            self.test_edit_widget.postprocessor_label.show()
        if self.height() < 500:
            self.test_list_widget.pos_comparator_widget.hide()
            self.test_list_widget.pos_comparator_label.hide()
            self.test_list_widget.neg_comparator_widget.hide()
            self.test_list_widget.neg_comparator_label.hide()
        else:
            self.test_list_widget.pos_comparator_widget.show()
            self.test_list_widget.pos_comparator_label.show()
            self.test_list_widget.neg_comparator_widget.show()
            self.test_list_widget.neg_comparator_label.show()

    def generate_neg_tests(self):
        in_data = self.sm.get_task('in_data_list', [])
        for el in in_data:
            for desc, neg_data in get_negatives(el):
                test = Test(self.create_temp_file(), self.tm)
                test.load()
                in_text = []
                for el2 in in_data:
                    if el2 == el:
                        in_text.append(neg_data)
                    else:
                        in_text.append(random_value(el2))
                in_text.append('')
                test['in'] = '\n'.join(map(convert, in_text))
                test['desc'] = desc
                test.store()
                self.test_list_widget.neg_test_list.addItem(test)

    def hide(self) -> None:
        if not self.isHidden():
            self.save_tests()
        super(TestsWidget, self).hide()

    def show(self) -> None:
        if self.isHidden() and self.current_test:
            self.current_test.load()
        super().show()


class Test(QListWidgetItem):
    files_links = dict()

    def __init__(self, file, tm):
        super(Test, self).__init__()
        self.path = file
        Test.files_links[self.path] = self

        self.load()
        self.update_name()
        self._dict = None

        self.setFont(tm.font_small)

    def is_loaded(self):
        return self._dict is not None

    def set_dict(self, dct):
        self._dict = dct

    def load(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                self._dict = json.loads(f.read())
        except FileNotFoundError:
            self._dict = {'desc': '-', 'in': '', 'out': '', 'args': ''}
        except json.JSONDecodeError:
            self._dict = {'desc': '-', 'in': '', 'out': '', 'args': ''}

    def store(self):
        if self._dict is None:
            return
        os.makedirs(os.path.split(self.path)[0], exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._dict))
        self._dict = None

    def get(self, key, default=None):
        return self._dict.get(key, default)

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
        self.setText(self.get('desc', '-'))

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        if self._dict is None:
            return
        self._dict[key] = value
        if key == 'desc':
            self.update_name()

    def pop(self, key):
        self._dict.pop(key)


def random_value(data: dict):
    if data.get('type') == 'int':
        return random_int(data)
    if data.get('type') == 'float':
        return random_float(data)
    if data.get('type') == 'str':
        return random_str(data)
    if data.get('type') == 'array':
        return random_array(data)


def get_negatives(data: dict):
    if data.get('type') == 'int':
        return int_negatives(data)
    if data.get('type') == 'float':
        return float_negatives(data)
    if data.get('type') == 'str':
        return str_negatives(data)
    if data.get('type') == 'array':
        return array_negatives(data)


def convert(arg):
    if isinstance(arg, float):
        return "{arg:.{n}g}".format(arg=arg, n=random.randint(2, 8))
    return str(arg)


def array_to_str(lst: list, data: dict):
    text = ''
    if data.get('size_input', 0) == 1:
        text = str(len(lst)) + '\n'
    if data.get("one_line"):
        return text + ' '.join(map(convert, lst))
    return text + '\n'.join(map(convert, lst))


def random_int(data: dict):
    minimum = -10000 if data.get('min') is None else data.get('min')
    maximum = 10000 if data.get('max') is None else data.get('max')
    return random.randint(int(minimum), int(maximum))


def random_float(data: dict):
    minimum = -10000 if data.get('min') is None else data.get('min')
    maximum = 10000 if data.get('max') is None else data.get('max')
    return random.randint(int(minimum), int(maximum) - 1) + random.random()


def random_str(data: dict = None):
    st = "abcdefghijklmnopqrstuvwxyz"
    if data is None:
        return ''.join(random.choices(st, k=random.randint(1, 10)))
    if data.get('spaces', False):
        st += " " * 6
    minimum = data.get('min')
    if minimum is None or int(minimum) < 0:
        minimum = 0
    else:
        minimum = int(minimum)
        if data.get('open_brace') == '(':
            minimum += 1
    maximum = data.get('max')
    if maximum is None:
        maximum = 100 if data.get('spaces', False) else 10
    else:
        maximum = int(maximum)
        if data.get('close_brace') == ')':
            maximum -= 1
    return ''.join(random.choices(st, k=random.randint(minimum, maximum)))


def random_array(data: dict, lst=False, not_empty=False):
    if data.get('size_input', 0) == 0:
        size = data.get('size', 0)
    else:
        minimum = 0 if data.get('min') is None else max(0, data.get('min'))
        maximum = 100 if data.get('max') is None else max(1, data.get('max'))
        size = random.randint(max(1 if not_empty else 0, int(minimum)), int(maximum))
    item_data = data.get('item', dict())
    if lst:
        return [random_value(item_data) for _ in range(size)]
    return array_to_str([random_value(item_data) for _ in range(size)], data)


def int_negatives(data: dict):
    if data.get('open_brace', '(') == '(' and data.get('min') is not None:
        yield f"{data.get('name')} равно {data.get('min')}", data.get('min')
    if data.get('close_brace', ')') == ')' and data.get('max') is not None:
        yield f"{data.get('name')} равно {data.get('max')}", data.get('max')
    if data.get('min') is not None:
        yield f"{data.get('name')} меньше {data.get('min')}", \
            random.randint(min(-10000, data.get('min') * 2), data.get('min'))
    if data.get('max') is not None:
        yield f"{data.get('name')} больше {data.get('max')}", \
            random.randint(data.get('max') * 2 + 1, max(10000, data.get('max') * 2) + 1)
    yield f"{data.get('name')} - вещественное число", random.random()
    yield f"{data.get('name')} - набор символов", random_str()


def float_negatives(data: dict):
    if data.get('open_brace', '(') == '(' and data.get('min') is not None:
        yield f"{data.get('name')} равно {data.get('min')}", data.get('min')
    if data.get('close_brace', ')') == ')' and data.get('max') is not None:
        yield f"{data.get('name')} равно {data.get('max')}", data.get('max')
    if data.get('min') is not None:
        yield f"{data.get('name')} меньше {data.get('min')}", \
            random.randint(min(-10000, data.get('min') * 2) - 1, data.get('min') - 1) + random.random()
    if data.get('max') is not None:
        yield f"{data.get('name')} больше {data.get('max')}", \
            random.randint(data.get('max'), max(10000, data.get('max') * 2)) + random.random()
    yield f"{data.get('name')} - набор символов", random_str()


def str_negatives(data: dict):
    if data.get('min') or data.get('min') == 0 and data.get('open_brace') == '(':
        yield f"{data.get('name')} - строка нулевой длины", ""
    if data.get('max'):
        st = "abcdefghijklmnopqrstuvwxyz"
        if data.get('spaces', False):
            st += " " * 6
        yield f"{data.get('name')} - слишком длинная строка", "".join(random.choices(
            st, k=random.randint(int(data.get('max') + 1), int(data.get('max') * 2))))
        if data.get('close_brace') == ')':
            yield f"{data.get('name')} - строка длиной {data.get('max')}", "".join(random.choices(
                st, k=int(data.get('max'))))


def array_negatives(data: dict):
    if data.get('size_input', 0) == 1:
        data_copy = deepcopy(data)
        data_copy['name'] = f"Размер массива {data.get('name', '')}"
        for el in int_negatives(data_copy):
            yield el
    elif data.get('size_input', 0) == 2:
        if data.get('close_brace', ')') == ']' and data.get('max') is not None:
            yield f"Длина массива {data.get('name')} равна {data.get('max')}", array_to_str(
                [random_value(data.get('item')) for _ in range(data.get('max'))], data)
        if data.get('max') is not None:
            yield f"Длина массива {data.get('name')} больше {data.get('max')}", array_to_str(
                [random_value(data.get('item')) for _ in range(random.randint(
                    data.get('max') * 2 + 1, max(50, data.get('max') * 2) + 1))], data)
    data_copy = deepcopy(data.get('item'))
    data_copy['name'] = f"Элемент массива {data.get('name')}"
    for desc, el in get_negatives(data_copy):
        lst = random_array(data, lst=True, not_empty=True)
        lst[random.randint(0, len(lst) - 1)] = el
        yield desc, array_to_str(lst, data)

def read_file(path, default=None):
    if default is not None:
        try:
            file = open(path, encoding='utf-8')
            res = file.read()
            file.close()
            return res
        except Exception:
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
        self.setStyleSheet(self.tm.bg_style_sheet)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.Ok).setStyleSheet(self.tm.button_css())
        self.buttonBox.button(QDialogButtonBox.Ok).setFixedSize(80, 24)
        self.buttonBox.button(QDialogButtonBox.Cancel).setStyleSheet(self.tm.button_css())
        self.buttonBox.button(QDialogButtonBox.Cancel).setFixedSize(80, 24)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.options_widget = OptionsWidget({
            'Проект': {'type': 'combo', 'values': list(self.sm.projects.keys()), 'name': OptionsWidget.NAME_LEFT,
                       'initial': list(self.sm.projects.keys()).index(self.sm.project)},
            'h_line1': {
                'Номер лабы:': {'type': int, 'min': 1, 'initial': self.sm.get('lab', 1),
                                'name': OptionsWidget.NAME_LEFT, 'width': 60},
                'Номер задания:': {'type': int, 'min': 1, 'initial': self.sm.get('task', 1),
                                   'name': OptionsWidget.NAME_LEFT, 'width': 60},
                'Номер варианта:': {'type': int, 'min': -1, 'initial': self.sm.get('var', 0),
                                    'name': OptionsWidget.NAME_LEFT, 'width': 60}
            },
            'h_line2': {
                'Позитивные': {'type': bool, 'name': OptionsWidget.NAME_RIGHT, 'initial': False},
                'Негативные': {'type': bool, 'name': OptionsWidget.NAME_RIGHT, 'initial': False}
            },
        })
        self.tm.css_to_options_widget(self.options_widget)
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
        self.tm.auto_css(self.scroll_area)
        self.layout.addWidget(self.scroll_area)

        self.layout.addWidget(self.buttonBox)

        self.path = self.sm.data_lab_path() + '/func_tests'
        self.test_list = []
        self.check_boxes = []

        self.open_task()
        self.update_list()

    def options_changed(self, key):
        if key == 'Позитивные':
            for i in range(len(self.test_list)):
                if self.test_list[i].startswith("POS"):
                    self.check_boxes[i].setChecked(self.options_widget['Позитивные'])
            return
        if key == 'Негативные':
            for i in range(len(self.test_list)):
                if self.test_list[i].startswith("NEG"):
                    self.check_boxes[i].setChecked(self.options_widget['Негативные'])
            return
        if key == 'Проект':
            project = self.options_widget.widgets['Проект'].currentText()
            print(self.sm.get('lab', 1, project=project), project)
            self.options_widget.set_value('Номер лабы:', self.sm.get('lab', 1, project=project))
            self.options_widget.set_value('Номер задания:', self.sm.get('task', 1, project=project))
            self.options_widget.set_value('Номер варианта:', self.sm.get('var', 1, project=project))
        if key in ('Номер лабы:', 'Номер задания:'):
            for i in range(-1, 100):
                if os.path.isdir(self.sm.data_lab_path(
                        self.options_widget['Номер лабы:'], self.options_widget['Номер задания:'], i,
                        self.options_widget.widgets['Проект'].currentText())):
                    self.options_widget.set_value('Номер варианта:', i)
                    break
        self.clear_scroll_area()
        self.check_boxes.clear()
        self.path = self.sm.data_lab_path(
            self.options_widget['Номер лабы:'], self.options_widget['Номер задания:'],
            self.options_widget['Номер варианта:'], self.options_widget.widgets['Проект'].currentText()) + '/func_tests'
        self.open_task()
        self.update_list()

    def open_task(self):
        self.test_list.clear()
        for test_type in ['pos', 'neg']:
            if os.path.isdir(f"{self.path}/{test_type}"):
                lst = list(filter(lambda s: s.rstrip('.json').isdigit(), os.listdir(f"{self.path}/{test_type}")))
                lst.sort(key=lambda s: int(s.rstrip('.json')))
                for i, el in enumerate(lst):
                    with open(f"{self.path}/{test_type}/{el}", encoding='utf-8') as f:
                        try:
                            desc = json.loads(f.read()).get('desc', '-')
                        except json.JSONDecodeError:
                            desc = '-'
                        self.test_list.append(f"{test_type.upper()} {i + 1}\t{desc}")

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
            if self.check_boxes[i].isChecked():
                if self.test_list[i].startswith("POS"):
                    pos_ind += 1
                    with open(f"{self.path}/pos/{int(self.test_list[i].split()[1]) - 1}.json",
                              encoding='utf-8') as f:
                        try:
                            yield json.loads(f.read())
                        except json.JSONDecodeError:
                            yield dict()

                else:
                    neg_ind += 1
                    with open(f"{self.path}/neg/{int(self.test_list[i].split()[1]) - 1}.json", encoding='utf-8') as f:
                        try:
                            yield json.loads(f.read())
                        except json.JSONDecodeError:
                            yield dict()
