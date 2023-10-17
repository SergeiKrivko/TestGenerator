import os

from PyQt6.QtCore import pyqtSignal, Qt, QUrl
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QLabel, QHBoxLayout, QVBoxLayout, QTextEdit, \
    QPushButton, QProgressBar, QComboBox, QLineEdit, QScrollArea

from backend.backend_manager import BackendManager
from backend.types.func_test import FuncTest
from main_tabs.code_tab.compiler_errors_window import CompilerErrorWindow
from language.languages import languages
from ui.main_tab import MainTab


class TestingWidget(MainTab):
    showTab = pyqtSignal()
    startTesting = pyqtSignal()
    save_tests = pyqtSignal()
    jump_to_code = pyqtSignal(str, int, int)

    def __init__(self, sm, bm: BackendManager, tm):
        super(TestingWidget, self).__init__()
        self.sm = sm
        self.bm = bm
        self.tm = tm
        self.labels = []
        self._coverage_html = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.button = QPushButton('Тестировать')
        top_layout.addWidget(self.button)
        self.button.clicked.connect(self.button_pressed)
        self.button.setFixedSize(180, 26)

        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        self.progress_bar.setFixedSize(200, 26)
        top_layout.addWidget(self.progress_bar)

        self._coverage_window = QWebEngineView()
        self._coverage_window.resize(720, 480)

        self.coverage_bar = QPushButton()
        self.coverage_bar.clicked.connect(self.show_coverage_html)
        # self.coverage_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.coverage_bar.hide()
        self.coverage_bar.setFixedSize(200, 26)
        top_layout.addWidget(self.coverage_bar)

        self.pos_result_bar = TestCountIndicator(self.tm, "POS:")
        self.labels.append(self.pos_result_bar)
        self.pos_result_bar.hide()
        top_layout.addWidget(self.pos_result_bar)

        self.neg_result_bar = TestCountIndicator(self.tm, "NEG:")
        self.labels.append(self.neg_result_bar)
        self.neg_result_bar.hide()
        top_layout.addWidget(self.neg_result_bar)

        layout.addLayout(top_layout)

        layout2 = QHBoxLayout()
        layout.addLayout(layout2)

        l = QVBoxLayout()
        layout2.addLayout(l)
        h_l = QHBoxLayout()
        l.addLayout(h_l)
        # h_l.addWidget(label := QLabel("Общая информация:"))
        # self.labels.append(label)
        # self.test_name_bar = QLineEdit()
        # self.test_name_bar.setReadOnly(True)
        # h_l.addWidget(self.test_name_bar)

        self.info_widget = TestInfoWidget(self.tm)
        l.addWidget(self.info_widget)

        l = QVBoxLayout()
        layout2.addLayout(l)
        h_l = QHBoxLayout()
        l.addLayout(h_l)
        h_l.addWidget(label := QLabel("Вывод программы"))
        self.labels.append(label)
        self.prog_out_combo_box = QComboBox()
        self.prog_out_combo_box.currentIndexChanged.connect(self.prog_out_combo_box_triggered)
        h_l.addWidget(self.prog_out_combo_box)
        self.prog_out = QTextEdit()
        self.prog_out.setReadOnly(True)
        self.prog_out.setFont(QFont("Courier", 10))
        l.addWidget(self.prog_out)

        layout3 = QHBoxLayout()
        layout.addLayout(layout3)

        l = QVBoxLayout()
        layout3.addLayout(l)
        h_l = QHBoxLayout()
        l.addLayout(h_l)
        h_l.addWidget(label := QLabel("Входные данные"))
        self.labels.append(label)
        self.in_data_combo_box = QComboBox()
        self.in_data_combo_box.currentIndexChanged.connect(self.in_data_combo_box_triggered)
        h_l.addWidget(self.in_data_combo_box)
        self.in_data = QTextEdit()
        self.in_data.setReadOnly(True)
        self.in_data.setFont(QFont("Courier", 10))
        l.addWidget(self.in_data)

        l = QVBoxLayout()
        layout3.addLayout(l)
        h_l = QHBoxLayout()
        l.addLayout(h_l)
        h_l.addWidget(label := QLabel("Выходные данные"))
        self.labels.append(label)
        self.out_data_combo_box = QComboBox()
        self.out_data_combo_box.currentIndexChanged.connect(self.out_data_combo_box_triggered)
        h_l.addWidget(self.out_data_combo_box)
        self.out_data = QTextEdit()
        self.out_data.setReadOnly(True)
        self.out_data.setFont(QFont("Courier", 10))
        l.addWidget(self.out_data)

        self.old_dir = os.getcwd()
        self.ui_disable_func = None

        self.current_item = None

        self.bm.startTesting.connect(self.testing)
        self.bm.testingError.connect(self.testing_is_terminated)
        self.bm.testingUtilError.connect(self.util_failed)
        self.bm.endTesting.connect(self.end_testing)
        self.bm.changeTestStatus.connect(self.set_tests_status)

    def set_theme(self):
        for el in [self.button, self.progress_bar, self.prog_out_combo_box, self.in_data_combo_box,
                   self.out_data_combo_box]:
            self.tm.auto_css(el)
        self.tm.auto_css(self.coverage_bar, palette='Bg', border=False)
        for el in [self.prog_out, self.in_data, self.out_data]:
            self.tm.auto_css(el, code_font=True)
        for label in self.labels:
            label.setFont(self.tm.font_medium)
        self.info_widget.set_theme()
        self.pos_result_bar.set_theme()
        self.neg_result_bar.set_theme()

    def open_task(self):
        self.test_mode(False)
        self.in_data.setText("")
        self.out_data.setText("")
        self.prog_out.setText("")

    def open_test_info(self, index=None, *args):
        if index is not None:
            if isinstance(self.current_item, FuncTest):
                pass
                # self.current_item.unload()
            try:
                self.current_item = self.bm.get_func_test('all', index)
            except IndexError:
                return
            # self.current_item.load()
        if isinstance(self.current_item, FuncTest):
            current_in, current_out = self.current_item.get('current_in', 0), self.current_item.get('current_out', 0)

            self.in_data_combo_box.clear()
            self.in_data_combo_box.addItems(self.current_item.in_data.keys())
            self.in_data.setText(self.current_item.get('in', ''))
            self.out_data_combo_box.clear()
            self.out_data_combo_box.addItems(self.current_item.out_data.keys())
            self.out_data.setText(self.current_item.get('out', ''))
            self.prog_out_combo_box.clear()
            self.prog_out_combo_box.addItems(self.current_item.prog_out.keys())
            self.prog_out.setText(self.current_item.prog_out.get('STDOUT', ''))
            self.info_widget.set_test(self.current_item)
            self.info_widget.open_test_info()

            self.in_data_combo_box.setCurrentIndex(current_in)
            self.out_data_combo_box.setCurrentIndex(current_out)

    def in_data_combo_box_triggered(self):
        self.in_data.setText(self.current_item.in_data.get(self.in_data_combo_box.currentText(), ''))

    def out_data_combo_box_triggered(self):
        self.out_data.setText(self.current_item.out_data.get(self.out_data_combo_box.currentText(), ''))

    def prog_out_combo_box_triggered(self):
        self.prog_out.setText(self.current_item.prog_out.get(self.prog_out_combo_box.currentText(), ''))

    def command(self, test: int = None, *args, run=False, stop=False, **kwargs):
        if run:
            self.bm.start_testing()
        if stop:
            self.stop_testing()
        self.open_test_info(test)

    def button_pressed(self, *args):
        if self.button.text() == "Тестировать":
            self.bm.start_testing()
        else:
            self.stop_testing()

    def stop_testing(self):
        self.button.setText("Тестировать")
        self.testing_is_terminated(None)

    def test_mode(self, flag=True):
        if flag:
            self.showTab.emit()

            self.button.setText("Прервать")

            self.coverage_bar.hide()
            self.progress_bar.show()
            self.pos_result_bar.show()
            self.neg_result_bar.show()
        else:
            self.button.setText("Тестировать")
            self.button.setDisabled(False)

    def set_tests_status(self, test: FuncTest):
        if test.status() in [FuncTest.PASSED, FuncTest.FAILED, FuncTest.TIMEOUT]:
            if test.type() == 'pos':
                self.pos_result_bar.add_test(test.status())
            else:
                self.neg_result_bar.add_test(test.status())
        self.progress_bar.setValue(self.bm.func_test_completed)
        self.open_test_info()

    def testing(self):
        self.test_mode(True)
        self.bm.side_tab_show('tests')

        self.pos_result_bar.set_count(self.bm.func_tests_count('pos'))
        self.neg_result_bar.set_count(self.bm.func_tests_count('neg'))

        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.bm.func_tests_count('all'))
        self.progress_bar.setValue(0)

    def end_testing(self, coverage, html_page):
        self.progress_bar.hide()
        self.coverage_bar.show()

        if coverage is not None:
            self.coverage_bar.setText(f"Coverage: {coverage:.1f}%")
        else:
            self.coverage_bar.setText("")

        self._coverage_html = html_page

        self.test_mode(False)

    def util_failed(self, name, errors, mask):
        dialog = CompilerErrorWindow(errors, self.tm, mask, name)
        if dialog.exec():
            if dialog.goto:
                self.jump_to_code.emit(os.path.join(self.sm.lab_path(), dialog.goto[0]),
                                       dialog.goto[1], dialog.goto[2])

    def testing_is_terminated(self, errors=''):
        if errors:
            dialog = CompilerErrorWindow(errors, self.tm, languages[self.sm.get('language', 'C')].get('compiler_mask'))
            if dialog.exec():
                if dialog.goto:
                    self.jump_to_code.emit(os.path.join(self.sm.lab_path(), dialog.goto[0]),
                                           dialog.goto[1], dialog.goto[2])

        self.end_testing(None, None)

    def show_coverage_html(self):
        if self._coverage_html is None:
            return
        self._coverage_window.setUrl(QUrl(f"file:///{self._coverage_html}"))
        self._coverage_window.show()


class SimpleField(QWidget):
    def __init__(self, tm, name, text):
        super().__init__()
        self._tm = tm

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._label = QLabel(f"{name} {text}")
        layout.addWidget(self._label)

    def set_theme(self):
        for el in [self._label]:
            self._tm.auto_css(el)


class LineField(QWidget):
    def __init__(self, tm, name, text):
        super().__init__()
        self._tm = tm

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._label = QLabel(name)
        layout.addWidget(self._label)

        self._line_edit = QLineEdit()
        self._line_edit.setText(text)
        self._line_edit.setReadOnly(True)
        layout.addWidget(self._line_edit)

    def set_theme(self):
        for el in [self._label, self._line_edit]:
            self._tm.auto_css(el)


class TextField(QWidget):
    def __init__(self, tm, name, text):
        super().__init__()
        self._tm = tm

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._label = QLabel(name)
        layout.addWidget(self._label)

        self._text_edit = QLabel()
        self._text_edit.setText(text)
        self._text_edit.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        layout.addWidget(self._text_edit)

    def set_theme(self):
        for el in [self._label]:
            self._tm.auto_css(el)
        self._text_edit.setStyleSheet(self._tm.base_css())
        self._text_edit.setFont(self._tm.code_font)


class _ListFieldItem(QListWidgetItem):
    def __init__(self, tm, name, status):
        super().__init__()
        self._tm = tm
        self._status = status
        self.setText(name)

    def set_theme(self):
        self.setFont(self._tm.font_medium)
        if self._status:
            self.setIcon(QIcon(self._tm.get_image('passed', color=self._tm['TestPassed'])))
            self.setForeground(self._tm['TestPassed'])
        else:
            self.setIcon(QIcon(self._tm.get_image('failed', color=self._tm['TestFailed'])))
            self.setForeground(self._tm['TestFailed'])


class ListField(QWidget):
    def __init__(self, tm, name, dct: dict):
        super().__init__()
        self._tm = tm

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._label = QLabel(name)
        layout.addWidget(self._label)

        self._list_widget = QListWidget()
        self._list_widget.setMinimumHeight(len(dct) * 22 + 2)
        layout.addWidget(self._list_widget)
        for key, item in dct.items():
            self._list_widget.addItem(_ListFieldItem(tm, key, item))

    def set_theme(self):
        for el in [self._label, self._list_widget]:
            self._tm.auto_css(el, palette='Bg', border=False)


class TestInfoWidget(QScrollArea):
    def __init__(self, tm):
        super().__init__()
        self._tm = tm
        self._test = None

        scroll_widget = QWidget()
        self.setWidget(scroll_widget)
        self.setWidgetResizable(True)

        self._scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(self._scroll_layout)
        self._scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._widgets = []

    def clear(self):
        for el in self._widgets:
            el.setParent(None)
        self._widgets.clear()

    def add_widget(self, widget):
        self._scroll_layout.addWidget(widget)
        self._widgets.append(widget)
        if hasattr(widget, 'set_theme'):
            widget.set_theme()

    def open_test_info(self):
        self.clear()
        self.add_widget(LineField(self._tm, "Описание:", self._test.get('desc', '')))
        self.add_widget(LineField(self._tm, "Аргументы:", self._test.get('args', '')))
        if self._test.status() in (FuncTest.PASSED, FuncTest.FAILED):
            if self._test.get('exit', ''):
                self.add_widget(SimpleField(self._tm, "Код возврата:", f"{self._test.exit} ({self._test['exit']})"))
            else:
                self.add_widget(SimpleField(self._tm, "Код возврата:", self._test.exit))
            self.add_widget(ListField(self._tm, "Результаты:", self._test.results))

            for key, item in self._test.utils_output.items():
                self.add_widget(TextField(self._tm, key, item))

    def set_test(self, test: FuncTest):
        self._test = test

    def set_theme(self):
        self._tm.auto_css(self, palette='Bg', border=False)
        for el in self._widgets:
            if hasattr(el, 'set_theme'):
                el.set_theme()


class TestCountIndicator(QLabel):
    def __init__(self, tm, name='POS:'):
        super().__init__()
        self._tm = tm
        self._name = name

        self.setFixedSize(125, 26)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._count = 0
        self._passed = 0
        self._completed = 0

    def set_text(self):
        self.setText(f"{self._name} {self._passed}/{self._count}")

    def set_count(self, count):
        self._passed = 0
        self._completed = 0
        self._count = count
        self.set_text()
        self.set_theme()

    def add_test(self, status):
        self._completed += 1
        if status == FuncTest.PASSED:
            self._passed += 1
        self.set_text()
        self.set_theme()

    def _get_color(self):
        if self._passed == self._count:
            return self._tm['TestPassed'].name()
        if self._passed == self._completed:
            return self._tm['TextColor']
        return self._tm['TestFailed'].name()

    def set_theme(self):
        self.setFont(self._tm.font_medium)
        self.setStyleSheet(f"color: {self._get_color()};")
