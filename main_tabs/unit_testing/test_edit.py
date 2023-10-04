from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QScrollArea

from main_tabs.code_tab.syntax_highlighter import CodeEditor
from main_tabs.tests.commands import CommandManager
from backend.types.unit_test import UnitTest
from backend.types.unit_tests_suite import UnitTestsSuite


class UnitTestEdit(QScrollArea):
    def __init__(self, sm, tm):
        super().__init__()
        self._sm = sm
        self._tm = tm
        self._labels = []
        self._test = None

        main_widget = QWidget()
        self.setWidgetResizable(True)
        self.setWidget(main_widget)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        main_widget.setLayout(main_layout)

        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(name_layout)

        label = QLabel("Название")
        self._labels.append(label)
        name_layout.addWidget(label)

        self._name_edit = QLineEdit()
        name_layout.addWidget(self._name_edit)

        desc_layout = QHBoxLayout()
        desc_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(desc_layout)

        label = QLabel("Описание")
        self._labels.append(label)
        desc_layout.addWidget(label)

        self._desc_edit = QLineEdit()
        desc_layout.addWidget(self._desc_edit)

        label = QLabel("Данные")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._in_edit = CodeEditor(self._sm, self._tm, language='C')
        self._in_edit.textChanged.connect(self._resize_code_edits)
        main_layout.addWidget(self._in_edit)

        label = QLabel("Запуск")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._run_edit = CodeEditor(self._sm, self._tm, language='C')
        self._run_edit.textChanged.connect(self._resize_code_edits)
        main_layout.addWidget(self._run_edit)

        label = QLabel("Проверка")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._out_edit = CodeEditor(self._sm, self._tm, language='C')
        self._out_edit.textChanged.connect(self._resize_code_edits)
        main_layout.addWidget(self._out_edit)

        label = QLabel("Результат")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._result_field = QLineEdit()
        self._result_field.setReadOnly(True)
        main_layout.addWidget(self._result_field)

        self._looper = None
        main_layout.addWidget(QWidget(), 100)

    def open_test(self, test: UnitTest | None):
        self.store_test()
        self._test = test
        if isinstance(self._test, UnitTest):
            self._name_edit.setText(self._test.get('name', ''))
            self._desc_edit.setText(self._test.get('desc', ''))
            self._in_edit.setText(self._test.get('in_code', ''))
            self._run_edit.setText(self._test.get('run_code', ''))
            self._out_edit.setText(self._test.get('out_code', ''))
            self._result_field.setText(self._test.get('test_res', ''))
        else:
            self._name_edit.setText("")
            self._desc_edit.setText("")
            self._in_edit.setText("")
            self._run_edit.setText("")
            self._out_edit.setText("")
        self._looper = CommandManager.after_second(self._resize_code_edits, 0.1)

    def _resize_code_edits(self):
        for el in [self._in_edit, self._run_edit, self._out_edit]:
            el.setFixedHeight(el.lines() * el.textHeight(0))

    def store_test(self):
        if not isinstance(self._test, UnitTest):
            return
        self._test['name'] = self._name_edit.text()
        self._test['desc'] = self._desc_edit.text()
        self._test['in_code'] = self._in_edit.text()
        self._test['run_code'] = self._run_edit.text()
        self._test['out_code'] = self._out_edit.text()
        # self._test.store()

    def set_theme(self):
        self._tm.auto_css(self, palette='Bg', border=False)
        for el in [self._name_edit, self._desc_edit, self._result_field]:
            self._tm.auto_css(el)
        for el in [self._in_edit, self._run_edit, self._out_edit]:
            el.set_theme()
        self._in_edit.setFont(self._tm.code_font)
        self._run_edit.setFont(self._tm.code_font)
        self._out_edit.setFont(self._tm.code_font)
        for el in self._labels:
            self._tm.auto_css(el)


class TestSuiteEdit(QScrollArea):
    def __init__(self, sm, tm):
        super().__init__()
        self._sm = sm
        self._tm = tm
        self._labels = []
        self._suite = None

        main_widget = QWidget()
        self.setWidget(main_widget)
        self.setWidgetResizable(True)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        self.setLayout(main_layout)

        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(name_layout)

        label = QLabel("Название")
        self._labels.append(label)
        name_layout.addWidget(label)

        self._name_edit = QLineEdit()
        name_layout.addWidget(self._name_edit)

        label = QLabel("Код")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._code_edit = CodeEditor(self._sm, self._tm, language='C')
        self._code_edit.textChanged.connect(self._resize_code_edits)
        main_layout.addWidget(self._code_edit)

        main_layout.addWidget(QWidget(), 100)

    def open_suite(self, suite: UnitTestsSuite | None):
        self.store_suite()
        self._suite = suite
        if isinstance(self._suite, UnitTestsSuite):
            self._name_edit.setText(self._suite.name())
            self._code_edit.setText(self._suite.code())
        else:
            self._name_edit.setText("")
            self._code_edit.setText("")
        self._looper = CommandManager.after_second(self._resize_code_edits, 0.1)

    def store_suite(self):
        if not isinstance(self._suite, UnitTestsSuite):
            return
        self._suite.set_name(self._name_edit.text())
        self._suite.set_code(self._code_edit.text())

    def _resize_code_edits(self):
        for el in [self._code_edit]:
            el.setFixedHeight(el.lines() * el.textHeight(0))

    def set_theme(self):
        self._tm.auto_css(self, palette='Bg', border=False)
        for el in self._labels:
            self._tm.auto_css(el)
        for el in [self._name_edit]:
            self._tm.auto_css(el)
        self._code_edit.set_theme()
