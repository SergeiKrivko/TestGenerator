import json
import os
import random
from copy import deepcopy

from PyQt6.QtCore import QMimeData
from PyQt6.QtWidgets import QVBoxLayout, QListWidgetItem, QApplication

from backend.backend_manager import BackendManager
from backend.backend_types.func_test import FuncTest
from main_tabs.tests.test_edit_widget import TestEditWidget
from main_tabs.tests.test_table_widget import TestTableWidget
from ui.main_tab import MainTab


class TestsWidget(MainTab):
    def __init__(self, sm, bm: BackendManager, app: QApplication, tm):
        super(TestsWidget, self).__init__()
        self.sm = sm
        self.bm = bm
        self.tm = tm
        self.app = app

        layout = QVBoxLayout()

        self.test_list_widget = TestTableWidget(self.tm, self.sm, self.bm, self.bm)
        self.test_list_widget.pos_add_button.clicked.connect(self.add_pos_test)
        self.test_list_widget.neg_add_button.clicked.connect(self.add_neg_test)
        self.test_list_widget.pos_button_up.clicked.connect(self.move_pos_test_up)
        self.test_list_widget.pos_button_down.clicked.connect(self.move_pos_test_down)
        self.test_list_widget.neg_button_up.clicked.connect(self.move_neg_test_up)
        self.test_list_widget.neg_button_down.clicked.connect(self.move_neg_test_down)

        self.test_list_widget.copyTests.connect(self.copy_tests)
        self.test_list_widget.cutTests.connect(self.cut_tests)
        self.test_list_widget.pasteTests.connect(self.paste_tests)
        self.test_list_widget.deleteTests.connect(self.delete_tests)
        self.test_list_widget.undo.connect(self.bm.undo_func_tests)

        self.test_list_widget.neg_button_generate.clicked.connect(self.generate_neg_tests)
        self.test_list_widget.pos_test_list.itemSelectionChanged.connect(self.select_pos_test)
        self.test_list_widget.neg_test_list.itemSelectionChanged.connect(self.select_neg_test)
        layout.addWidget(self.test_list_widget)

        self.test_edit_widget = TestEditWidget(self.tm)
        self.test_edit_widget.test_edited.connect(self.set_tests_changed)
        self.test_edit_widget.testNameChanged.connect(self.update_test_name)
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
            self.test_list_widget.pos_test_list.clearSelection()
            self.test_list_widget.pos_test_list.setCurrentRow(index)
        else:
            self.test_list_widget.neg_test_list.insertItem(index, item)
            self.test_list_widget.neg_test_list.clearSelection()
            self.test_list_widget.neg_test_list.setCurrentRow(index)

    def _on_test_deleted(self, test: FuncTest, index: int):
        if test.type() == 'pos':
            self.test_list_widget.pos_test_list.takeItem(index)
            self.test_list_widget.pos_test_list.setCurrentRow(
                min(index, self.test_list_widget.pos_test_list.count() - 1))
        else:
            self.test_list_widget.neg_test_list.takeItem(index)
            self.test_list_widget.neg_test_list.setCurrentRow(
                min(index, self.test_list_widget.neg_test_list.count() - 1))

    def _on_tests_cleared(self):
        self.test_list_widget.pos_test_list.clear()
        self.test_list_widget.neg_test_list.clear()

    def add_pos_test(self):
        self.tests_changed = True
        if self.test_list_widget.pos_test_list.currentItem():
            index = self.test_list_widget.pos_test_list.currentRow() + 1
        else:
            index = self.test_list_widget.pos_test_list.count()
        self.bm.new_func_test('pos', index)
        self.test_list_widget.pos_test_list.setCurrentRow(index)

    def add_neg_test(self):
        if self.test_list_widget.neg_test_list.currentItem():
            index = self.test_list_widget.neg_test_list.currentRow() + 1
        else:
            index = self.test_list_widget.neg_test_list.count()
        self.bm.new_func_test('neg', index)
        self.test_list_widget.neg_test_list.setCurrentRow(index)

    def delete_tests(self, test_type=''):
        lst = self.test_list_widget.pos_test_list.selectedIndexes()
        if test_type == 'neg' or (not test_type and not lst):
            lst = self.test_list_widget.neg_test_list.selectedIndexes()
            test_type = 'neg'
        else:
            test_type = 'pos'
        self.tests_changed = True
        self.bm.delete_some_func_tests(test_type, [index.row() for index in lst])

    def copy_tests(self, *args):
        if not (items := self.test_list_widget.pos_test_list.selectedItems()):
            items = self.test_list_widget.neg_test_list.selectedItems()

        mime_data = QMimeData()
        mime_data.setData(f'TestGeneratorFuncTests',
                          json.dumps([item.test.to_dict() for item in items]).encode('utf-8'))
        self.app.clipboard().setMimeData(mime_data)

    def cut_tests(self, test_type):
        self.copy_tests()
        self.delete_tests()

    def paste_tests(self, tests_type='pos'):
        if tests_type == '':
            if self.test_list_widget.pos_test_list.currentItem():
                tests_type = 'pos'
            elif self.test_list_widget.neg_test_list.currentItem():
                tests_type = 'neg'
            else:
                return
        if tests_type == 'pos':
            index = self.test_list_widget.pos_test_list.currentRow() + 1
            if index == 0:
                index = self.test_list_widget.pos_test_list.count()
        else:
            index = self.test_list_widget.neg_test_list.currentRow() + 1
            if index == 0:
                index = self.test_list_widget.neg_test_list.count()

        tests = self.app.clipboard().mimeData().data(f'TestGeneratorFuncTests')
        if tests:
            try:
                tests = json.loads(tests.data().decode('utf-8'))
                self.bm.add_some_func_tests(tests_type, {i + index: el for i, el in enumerate(tests)})
            except UnicodeDecodeError:
                pass
            except json.JSONDecodeError:
                pass

    def set_tests_changed(self):
        self.tests_changed = True

    def update_test_name(self):
        if isinstance(self.current_test, Test):
            self.current_test.setText(self.current_test.test.get('desc'))

    def select_pos_test(self):
        item = self.test_list_widget.pos_test_list.currentItem()
        if isinstance(item, Test):
            self.test_list_widget.neg_test_list.setCurrentItem(None)
            self.current_test = item
            self.test_edit_widget.open_test(item.test)

    def select_neg_test(self):
        item = self.test_list_widget.neg_test_list.currentItem()
        if isinstance(item, Test):
            self.test_list_widget.pos_test_list.setCurrentItem(None)
            self.current_test = item
            self.test_edit_widget.open_test(item.test)

    def move_pos_test_up(self):
        self.tests_changed = True
        self.bm.move_func_test('pos', 'up', ind := self.test_list_widget.pos_test_list.currentRow())
        self.test_list_widget.move_selection('pos', 'up', ind)

    def move_pos_test_down(self):
        self.tests_changed = True
        self.bm.move_func_test('pos', 'down', ind := self.test_list_widget.pos_test_list.currentRow())
        self.test_list_widget.move_selection('pos', 'down', ind)

    def move_neg_test_up(self):
        self.tests_changed = True
        self.bm.move_func_test('neg', 'up', ind := self.test_list_widget.neg_test_list.currentRow())
        self.test_list_widget.move_selection('neg', 'up', ind)

    def move_neg_test_down(self):
        self.tests_changed = True
        self.bm.move_func_test('neg', 'down', ind := self.test_list_widget.neg_test_list.currentRow())
        self.test_list_widget.move_selection('neg', 'down', ind)

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
