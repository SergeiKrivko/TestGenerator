import os

from PyQtUIkit.widgets import *

from src.backend.backend_types.func_test import FuncTest
from src.backend.managers import BackendManager
from src.ui.main_tabs.tests.test_edit_widget import TestEditWidget
from src.ui.main_tabs.tests.test_list_widget import TestListWidget
from src.ui.side_tabs.builds.build_box import BuildBox
from src.ui.widgets.main_tab import MainTab


class TestsWidget(MainTab):
    def __init__(self, bm: BackendManager):
        super(TestsWidget, self).__init__()
        self.bm = bm
        self.sm = bm.sm
        self.need_project = True
        self.padding = 10
        self.spacing = 6

        self._build_box = BuildBox(self.bm)
        self._build_box.currentChanged.connect(self._on_build_changed)
        self.addWidget(self._build_box)

        main_layout = KitHBoxLayout()
        main_layout.spacing = 12
        self.addWidget(main_layout)

        self._pos_list = TestListWidget(self.bm, FuncTest.Type.POS)
        self._pos_list.testSelected.connect(self._select_test)
        main_layout.addWidget(self._pos_list)

        self._neg_list = TestListWidget(self.bm, FuncTest.Type.NEG)
        self._neg_list.testSelected.connect(self._select_test)
        main_layout.addWidget(self._neg_list)

        self.test_edit_widget = TestEditWidget()
        self.test_edit_widget.testEdited.connect(self._set_tests_changed)
        self.test_edit_widget.testNameChanged.connect(self.update_test_name)
        # self.test_edit_widget.button_generate.clicked.connect(self.generate_test)
        self.addWidget(self.test_edit_widget)

        self._tests_changed = False

    def _set_tests_changed(self):
        self._tests_changed = True

    def _on_build_changed(self, value):
        self.sm.set_data('func_tests_build', str(value))

    def update_test_name(self):
        self._pos_list.update_test_name()
        self._neg_list.update_test_name()

    def _select_test(self, test: FuncTest):
        if test.type == FuncTest.Type.POS:
            self._neg_list.clear_selection()
        else:
            self._pos_list.clear_selection()

        self.test_edit_widget.open_test(test)

    def get_path(self, from_settings=False):
        self.path = self.sm.lab_path()

    def remove_temp_files(self):
        for file in os.listdir(f"{self.path}/func_tests/data"):
            if file.startswith('temp'):
                os.remove(f"{self.path}/func_tests/data/{file}")

    def write_file(self, path, data=''):
        file = open(path, 'w', encoding='utf-8', newline=self.sm.line_sep)
        file.write(data)
        file.close()

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
