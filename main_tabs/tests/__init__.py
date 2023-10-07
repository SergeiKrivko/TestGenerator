import json
import os
import random
from copy import deepcopy

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog, QDialogButtonBox, QScrollArea, \
    QHBoxLayout, QCheckBox, QLabel, QListWidgetItem

from backend.types.func_test import FuncTest
from backend.backend_manager import BackendManager
from ui.main_tab import MainTab
from ui.options_window import OptionsWidget
from main_tabs.tests.test_table_widget import TestTableWidget
from main_tabs.tests.test_edit_widget import TestEditWidget


class TestsWidget(MainTab):
    def __init__(self, sm, bm: BackendManager, tm):
        super(TestsWidget, self).__init__()
        self.sm = sm
        self.bm = bm
        self.tm = tm

        layout = QVBoxLayout()

        self.test_list_widget = TestTableWidget(self.tm, self.sm, self.bm, self.bm)
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

        self.bm.addFuncTest.connect(self._on_test_added)
        self.bm.deleteFuncTest.connect(self._on_test_deleted)
        self.bm.clearFuncTests.connect(self._on_tests_cleared)

    def _on_test_added(self, test: FuncTest, index: int):
        item = Test(test, self.tm)
        item.update_name()
        if test.type() == 'pos':
            self.test_list_widget.pos_test_list.insertItem(index, item)
        else:
            self.test_list_widget.neg_test_list.insertItem(index, item)

    def _on_test_deleted(self, test: FuncTest, index: int):
        if test.type() == 'pos':
            self.test_list_widget.pos_test_list.takeItem(index)
        else:
            self.test_list_widget.neg_test_list.takeItem(index)

    def _on_tests_cleared(self):
        self.test_list_widget.pos_test_list.clear()
        self.test_list_widget.neg_test_list.clear()

    def add_pos_test(self):
        self.tests_changed = True
        if self.test_list_widget.pos_test_list.currentItem():
            index = self.test_list_widget.pos_test_list.currentRow() + 1
        else:
            index = self.test_list_widget.pos_test_list.count()
        self.bm.add_func_test(FuncTest(test_type='pos'), index)
        self.test_list_widget.pos_test_list.setCurrentRow(index)

    def add_neg_test(self):
        if self.test_list_widget.neg_test_list.currentItem():
            index = self.test_list_widget.neg_test_list.currentRow() + 1
        else:
            index = self.test_list_widget.neg_test_list.count()
        self.bm.add_func_test(FuncTest(test_type='neg'), index)
        self.test_list_widget.neg_test_list.setCurrentRow(index)

    def delete_pos_test(self):
        self.tests_changed = True
        ind = self.test_list_widget.pos_test_list.currentRow()
        if ind == -1:
            return
        self.bm.delete_func_test('pos', ind)

    def delete_neg_test(self):
        self.tests_changed = True
        ind = self.test_list_widget.neg_test_list.currentRow()
        if ind == -1:
            return
        self.bm.delete_func_test('neg', ind)

    def copy_tests(self, test_type='pos'):
        self.save_tests(deep=False)
        dlg = TestCopyWindow(self.sm, self.tm)
        if dlg.exec():
            self.tests_changed = True
            for dct in dlg.copy_tests():
                item = Test(self.create_temp_file(), tm=self.tm)

                item.set_dict(dct)
                item['desc'] = dct.get('desc', '-')
                item.store()

                if test_type == 'pos':
                    ind = self.test_list_widget.pos_test_list.currentRow() + 1
                    self.test_list_widget.pos_test_list.insertItem(ind, item)
                    self.test_list_widget.pos_test_list.setCurrentRow(ind)
                else:
                    ind = self.test_list_widget.neg_test_list.currentRow() + 1
                    self.test_list_widget.neg_test_list.insertItem(ind, item)
                    self.test_list_widget.neg_test_list.setCurrentRow(ind)

    def set_tests_changed(self):
        self.tests_changed = True

    def select_pos_test(self):
        item = self.test_list_widget.pos_test_list.currentItem()
        if isinstance(item, Test):
            self.test_list_widget.neg_test_list.setCurrentItem(None)
            self.current_test = item.test
            self.test_edit_widget.open_test(item.test)

    def select_neg_test(self):
        item = self.test_list_widget.neg_test_list.currentItem()
        if isinstance(item, Test):
            self.test_list_widget.pos_test_list.setCurrentItem(None)
            self.current_test = item.test
            self.test_edit_widget.open_test(item.test)

    def move_pos_test_up(self):
        self.tests_changed = True
        self.bm.move_func_test('pos', 'up', self.test_list_widget.pos_test_list.currentRow())
        self.test_list_widget.move_selection('pos', 'up')

    def move_pos_test_down(self):
        self.tests_changed = True
        self.bm.move_func_test('pos', 'down', self.test_list_widget.pos_test_list.currentRow())
        self.test_list_widget.move_selection('pos', 'down')

    def move_neg_test_up(self):
        self.tests_changed = True
        self.bm.move_func_test('neg', 'up', self.test_list_widget.neg_test_list.currentRow())
        self.test_list_widget.move_selection('neg', 'up')

    def move_neg_test_down(self):
        self.tests_changed = True
        self.bm.move_func_test('neg', 'down', self.test_list_widget.neg_test_list.currentRow())
        self.test_list_widget.move_selection('neg', 'down')

    def get_path(self, from_settings=False):
        self.path = self.sm.lab_path()

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

    def remove_temp_files(self):
        for file in os.listdir(f"{self.path}/func_tests/data"):
            if file.startswith('temp'):
                os.remove(f"{self.path}/func_tests/data/{file}")

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

    def show(self) -> None:
        if self.isHidden() and self.current_test:
            self.current_test.load()
        super().show()


class Test(QListWidgetItem):
    def __init__(self, test: FuncTest, tm):
        super(Test, self).__init__()
        self.test = test

        self.setFont(tm.font_medium)

    def get(self, key, default=None):
        return self.test.get(key, default)

    def update_name(self):
        self.setText(self.test.get('desc', '-'))

    def __getitem__(self, item):
        return self.test[item]

    def __setitem__(self, key, value):
        self.test[key] = value

    def pop(self, key):
        self.test.pop(key)


def random_value(data: dict):
    if data.get('type') == 'int':
        return random_int(data)
    if data.get('type') == 'float':
        return random_float(data)
    if data.get('type') == 'str':
        return random_str(data)
    if data.get('type') == 'array':
        return random_array(data)
    if data.get('type') == 'struct':
        return random_struct(data)


def get_negatives(data: dict):
    if data.get('type') == 'int':
        return int_negatives(data)
    if data.get('type') == 'float':
        return float_negatives(data)
    if data.get('type') == 'str':
        return str_negatives(data)
    if data.get('type') == 'array':
        return array_negatives(data)
    if data.get('type') == 'struct':
        return struct_negatives(data)


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


def random_struct(data: dict):
    lst = []
    for item in data.get('items', []):
        lst.append(random_value(item))
    sep = ' ' if data.get('one_lie', True) else '\n'
    return sep.join(map(str, lst))


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
            random.randint(min(-10000, data.get('min') * 100), data.get('min'))
    if data.get('max') is not None:
        yield f"{data.get('name')} больше {data.get('max')}", \
            random.randint(data.get('max') + 1, max(10000, data.get('max') * 100) + 1)
    yield f"{data.get('name')} - вещественное число", random.random()
    yield f"{data.get('name')} - набор символов", random_str()


def float_negatives(data: dict):
    if data.get('open_brace', '(') == '(' and data.get('min') is not None:
        yield f"{data.get('name')} равно {data.get('min')}", data.get('min')
    if data.get('close_brace', ')') == ')' and data.get('max') is not None:
        yield f"{data.get('name')} равно {data.get('max')}", data.get('max')
    if data.get('min') is not None:
        yield f"{data.get('name')} меньше {data.get('min')}", \
            random.randint(min(-10000, data.get('min') * 100) - 1, data.get('min') - 1) + random.random()
    if data.get('max') is not None:
        yield f"{data.get('name')} больше {data.get('max')}", \
            random.randint(data.get('max'), max(10000, data.get('max') * 100)) + random.random()
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


def struct_negatives(data: dict):
    sep = ' ' if data.get('one_lie', True) else '\n'
    for item in data.get('items', []):
        for desc, el in get_negatives(item):
            lst = []
            for elem in data.get('items', []):
                if elem == item:
                    lst.append(el)
                else:
                    lst.append(random_value(elem))
            yield f"{data.get('name', '')}.{desc}", sep.join(map(str, lst))


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
        self.setFixedSize(600, 480)
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
            self.tm.auto_css(check_box)
            layout.addWidget(label := QLabel(el))
            label.setFont(self.tm.font_medium)
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
