import os
import webbrowser

from PyQt6.QtCore import pyqtSignal, Qt, QUrl
from PyQtUIkit.widgets import *

from src import config
from src.backend.language.languages import LANGUAGES
from src.backend.managers import BackendManager
from src.backend.backend_types.func_test import FuncTest
from src.ui.main_tabs.code_tab.compiler_errors_window import CompilerErrorWindow
from src.ui.main_tabs.testing.indicator import TestCountIndicator
from src.ui.main_tabs.testing.test_info import TestInfoWidget
from src.ui.widgets.main_tab import MainTab


class TestingWidget(MainTab):
    showTab = pyqtSignal()
    startTesting = pyqtSignal()
    save_tests = pyqtSignal()
    jump_to_code = pyqtSignal(str, int, int)

    def __init__(self, bm: BackendManager):
        super(TestingWidget, self).__init__()
        self.sm = bm.sm
        self.bm = bm
        self.need_project = True
        self._coverage_html = None

        self.padding = 10
        self.spacing = 6

        top_layout = KitHBoxLayout()
        top_layout.spacing = 6
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addWidget(top_layout)

        self.button = KitButton('Тестировать')
        top_layout.addWidget(self.button)
        self.button.on_click = self._on_button_pressed
        self.button.setFixedSize(180, 26)

        self.progress_bar = KitProgressBar()
        self.progress_bar.hide()
        self.progress_bar.setFixedSize(200, 26)
        top_layout.addWidget(self.progress_bar)

        if config.USE_WEB_ENGINE:
            from PyQt6.QtWebEngineWidgets import QWebEngineView
            self._coverage_window = QWebEngineView()
            self._coverage_window.resize(720, 480)

        self.coverage_bar = KitButton()
        self.coverage_bar.on_click = self._show_coverage_html
        self.coverage_bar.hide()
        self.coverage_bar.setFixedSize(200, 26)
        top_layout.addWidget(self.coverage_bar)

        self.pos_result_bar = TestCountIndicator(FuncTest.Type.POS)
        self.pos_result_bar.hide()
        top_layout.addWidget(self.pos_result_bar)

        self.neg_result_bar = TestCountIndicator(FuncTest.Type.NEG)
        self.neg_result_bar.hide()
        top_layout.addWidget(self.neg_result_bar)

        layout2 = KitHBoxLayout()
        layout2.spacing = 6
        self.addWidget(layout2)

        self.info_widget = TestInfoWidget()
        layout2.addWidget(self.info_widget)

        vertical_layout = KitVBoxLayout()
        vertical_layout.spacing = 6
        layout2.addWidget(vertical_layout)
        
        horizontal_layout = KitHBoxLayout()
        horizontal_layout.spacing = 6
        vertical_layout.addWidget(horizontal_layout)
        
        horizontal_layout.addWidget(KitLabel("Вывод программы"))

        self.prog_out_combo_box = KitComboBox()
        self.prog_out_combo_box.currentIndexChanged.connect(self.prog_out_combo_box_triggered)
        horizontal_layout.addWidget(self.prog_out_combo_box)

        self.prog_out = KitTextEdit()
        self.prog_out.setReadOnly(True)
        self.prog_out.font = 'mono'
        vertical_layout.addWidget(self.prog_out)

        layout3 = KitHBoxLayout()
        layout3.spacing = 6
        self.addWidget(layout3)

        vertical_layout = KitVBoxLayout()
        vertical_layout.spacing = 6
        layout3.addWidget(vertical_layout)

        horizontal_layout = KitHBoxLayout()
        horizontal_layout.spacing = 6
        vertical_layout.addWidget(horizontal_layout)
        horizontal_layout.addWidget(KitLabel("Входные данные"))

        self.in_data_combo_box = KitComboBox()
        self.in_data_combo_box.currentIndexChanged.connect(self.in_data_combo_box_triggered)
        horizontal_layout.addWidget(self.in_data_combo_box)

        self.in_data = KitTextEdit()
        self.in_data.setReadOnly(True)
        self.in_data.font = 'mono'
        vertical_layout.addWidget(self.in_data)

        vertical_layout = KitVBoxLayout()
        vertical_layout.spacing = 6
        layout3.addWidget(vertical_layout)

        horizontal_layout = KitHBoxLayout()
        horizontal_layout.spacing = 6
        vertical_layout.addWidget(horizontal_layout)
        horizontal_layout.addWidget(KitLabel("Выходные данные"))

        self.out_data_combo_box = KitComboBox()
        self.out_data_combo_box.currentIndexChanged.connect(self.out_data_combo_box_triggered)
        horizontal_layout.addWidget(self.out_data_combo_box)

        self.out_data = KitTextEdit()
        self.out_data.setReadOnly(True)
        self.out_data.font = 'mono'
        vertical_layout.addWidget(self.out_data)

        self.old_dir = os.getcwd()
        self.ui_disable_func = None

        self._test: FuncTest | None = None

        self.bm.func_tests.startTesting.connect(self.testing)
        self.bm.func_tests.testingError.connect(self.testing_is_terminated)
        self.bm.func_tests.testingUtilError.connect(self.util_failed)
        self.bm.func_tests.endTesting.connect(self.end_testing)
        self.bm.func_tests.onStatusChanged.connect(self.set_tests_status)

    def clear(self):
        self.test_mode(False)
        self.in_data.setText("")
        self.out_data.setText("")
        self.prog_out.setText("")

    def open_test_info(self, index=None, *args):
        if index is not None:
            if isinstance(self._test, FuncTest):
                pass
                # self.current_item.unload()
            try:
                self._test = self.bm.func_tests.get(index=index)
            except IndexError:
                return
            # self.current_item.load()
        if isinstance(self._test, FuncTest):
            current_in, current_out = self._test.current_in, self._test.current_out

            self.in_data_combo_box.clear()
            self.in_data_combo_box.addItem(KitComboBoxItem('STDIN', 0))
            self.in_data_combo_box.addItems([
                KitComboBoxItem(f'in_file_{i + 1}.{file.type}', file) for i, file in enumerate(self._test.in_files)
            ])
            self.in_data.setText(self._test.stdin)

            self.out_data_combo_box.clear()
            self.out_data_combo_box.addItem(KitComboBoxItem('STDOUT', 1))
            self.out_data_combo_box.addItems([
                KitComboBoxItem(f'out_file_{i + 1}.{file.type}', file) for i, file in enumerate(self._test.out_files)
            ])
            self.out_data.setText(self._test.stdout)

            self.prog_out_combo_box.clear()
            self.prog_out_combo_box.addItems(self._test.res.files.keys())
            self.prog_out.setText(self._test.res.files.get('STDOUT', ''))

            self.info_widget.set_test(self._test)
            self.info_widget.open_test_info()

            self.in_data_combo_box.setCurrentIndex(current_in)
            self.out_data_combo_box.setCurrentIndex(current_out)

    def in_data_combo_box_triggered(self, value):
        if value == 0:
            self.in_data.setText(self._test.stdin)
        elif isinstance(value, FuncTest.InFile):
            self.in_data.setText(value.data)

    def out_data_combo_box_triggered(self, value):
        if value == 1:
            self.in_data.setText(self._test.stdout)
        elif isinstance(value, FuncTest.OutFile):
            self.in_data.setText(value.data)

    def prog_out_combo_box_triggered(self, value):
        self.prog_out.setText(self._test.res.files.get(self.prog_out_combo_box.currentValue(), ''))

    def command(self, test: int = None, *args, run=False, stop=False, **kwargs):
        if run:
            self.bm.func_tests.testing()
        if stop:
            self.stop_testing()
        self.open_test_info(test)

    def _on_button_pressed(self, *args):
        if self.button.text == "Тестировать":
            self.bm.func_tests.testing()
        else:
            self.stop_testing()

    def stop_testing(self):
        self.button.setText("Тестировать")
        self.testing_is_terminated()

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
        if test.status in [FuncTest.Status.PASSED, FuncTest.Status.FAILED, FuncTest.Status.TIMEOUT]:
            if test.type == FuncTest.Type.POS:
                self.pos_result_bar.add_test(test.status)
            else:
                self.neg_result_bar.add_test(test.status)
        self.progress_bar.setValue(self.bm.func_tests.tests_completed)
        self.open_test_info()

    def testing(self):
        self.test_mode(True)
        self.bm.side_tab_show('tests')

        self.pos_result_bar.set_count(self.bm.func_tests.count(FuncTest.Type.POS))
        self.neg_result_bar.set_count(self.bm.func_tests.count(FuncTest.Type.NEG))

        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.bm.func_tests.count())
        self.progress_bar.setValue(0)

    def end_testing(self, coverage, html_page):
        self.progress_bar.hide()
        self.coverage_bar.show()

        if coverage is not None:
            self.coverage_bar.setText(f"Coverage: {coverage:.1f}%")
        else:
            self.coverage_bar.setText("")

        self._coverage_html = html_page

        self.bm.notification("Тестирование завершено",
                             f"Позитивные тесты: {self.pos_result_bar.passed}/{self.pos_result_bar.count}\n"
                             f"Негативные тесты: {self.neg_result_bar.passed}/{self.neg_result_bar.count}")

        self.test_mode(False)

    def util_failed(self, name, errors, mask):
        dialog = CompilerErrorWindow(errors, mask, name)
        if dialog.exec():
            if dialog.goto:
                self.jump_to_code.emit(os.path.join(self.sm.lab_path(), dialog.goto[0]),
                                       dialog.goto[1], dialog.goto[2])

    def testing_is_terminated(self, errors=''):
        if errors:
            dialog = CompilerErrorWindow(self, errors) # languages[self.sm.get('language', 'C')].compiler_mask
            if dialog.exec():
                if dialog.goto:
                    self.jump_to_code.emit(os.path.join(self.sm.lab_path(), dialog.goto[0]),
                                           dialog.goto[1], dialog.goto[2])

        self.end_testing(None, None)

    def _show_coverage_html(self):
        if self._coverage_html is None:
            return
        if config.USE_WEB_ENGINE:
            self._coverage_window.setUrl(QUrl.fromLocalFile(self._coverage_html))
            self._coverage_window.show()
        else:
            webbrowser.open('file:///' + self._coverage_html)
