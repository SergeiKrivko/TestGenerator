from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFileDialog

from other.themes import ThemeManager
from widgets.code_widget import CodeWidget
from widgets.testing_widget import TestingWidget
from widgets.options_window import OptionsWindow
from widgets.tests_widget import TestsWidget
from widgets.git_widget import GitWidget
from widgets.menu_bar import MenuBar
from other.commands import CommandManager
from widgets.todo_widget import TODOWidget
from widgets.lib_dialog import LibDialog
from other.settings_manager import SettingsManager
import os

line_sep = {'\n': 'LF (\\n)', '\r\n': 'CRLF (\\r\\n)', '\r': 'CR (\\r)'}
line_sep_reverse = {'LF (\\n)': '\n', 'CRLF (\\r\\n)': '\r\n', 'CR (\\r)': '\r'}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("TestGenerator")

        self.sm = SettingsManager()

        if not os.path.isdir(self.sm.get_general('__project__', '')):
            self.open_project(False)
        else:
            self.sm.repair_settings()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(layout)

        self.cm = CommandManager(self.sm)
        self.tm = ThemeManager(self.sm.get_general('theme'))

        self.tests_widget = TestsWidget(self.sm, self.cm, self.tm)
        layout.addWidget(self.tests_widget)

        self.testing_widget = TestingWidget(self.sm, self.cm, self.tm)
        layout.addWidget(self.testing_widget)
        self.testing_widget.hide()

        self.code_widget = CodeWidget(self.sm, self.cm, self.tm)
        layout.addWidget(self.code_widget)
        self.testing_widget.testing_start.connect(self.code_widget.testing_start)
        self.testing_widget.add_test.connect(self.code_widget.add_test)
        self.testing_widget.testing_end.connect(self.code_widget.end_testing)
        self.code_widget.testing_signal.connect(self.testing_widget.testing)
        self.code_widget.test_res_widget.doubleClicked.connect(self.open_test_from_code)
        self.code_widget.hide()

        self.git_widget = GitWidget(self.sm, self.cm)
        layout.addWidget(self.git_widget)
        self.git_widget.hide()

        self.todo_widget = TODOWidget(self.sm, self.cm)
        layout.addWidget(self.todo_widget)
        self.todo_widget.jumpToCode.connect(self.jump_to_code_from_todo)
        self.todo_widget.hide(save_data=False)

        self.options_window = OptionsWindow({
            "Символ переноса строки: ": {'type': 'combo', 'values': line_sep.values(), 'name': OptionsWindow.NAME_LEFT,
                                         'initial': list(line_sep.keys()).index(self.sm.get('line_sep', '\n'))},
            "Компилятор": {'type': str, 'initial': self.sm.get('compiler', 'gcc -std=c99 -Wall -Werror'),
                           'width': 400},
            "Ключ -lm": {'type': bool, 'initial': self.sm.get('-lm', True), 'name': OptionsWindow.NAME_RIGHT},
            "Удалять слова при генерации выходного файла": {'type': bool, 'name': OptionsWindow.NAME_RIGHT,
                                                            'initial': self.sm.get('clear_words', False)},
            "Компаратор для позитивных тестов:": {'type': 'combo',
                                                  'values': ['Числа', 'Числа как текст', 'Текст после подстроки'],
                                                  'initial': self.sm.get('pos_comparator', 0)},
            "Компаратор для негативных тестов:": {'type': 'combo', 'values': ['Нет', 'Числа', 'Числа как текст',
                                                                              'Текст после подстроки'],
                                                  'initial': self.sm.get('pos_comparator', 0)},
            'Погрешность сравнения чисел:': {'type': float, 'initial': self.sm.get('epsilon', 0),
                                             'name': OptionsWindow.NAME_LEFT},
            'Подстрока для позитивных тестов:': {'type': str, 'initial': self.sm.get('pos_substring', 0),
                                                 'name': OptionsWindow.NAME_LEFT},
            'Подстрока для негативных тестов:': {'type': str, 'initial': self.sm.get('neg_substring', 0),
                                                 'name': OptionsWindow.NAME_LEFT},
            "Coverage": {'type': bool, 'name': OptionsWindow.NAME_RIGHT,
                         'initial': self.sm.get('coverage', 0)},
            "Тестирование по памяти": {'type': bool, 'name': OptionsWindow.NAME_RIGHT,
                                       'initial': self.sm.get('memory_testing', 0)},
            "lib": {'type': 'button', 'name': OptionsWindow.NAME_SKIP, 'text': 'Библиотеки'},
            "Тема:": {'type': 'combo', 'values': list(self.tm.themes.keys()), 'name': OptionsWindow.NAME_LEFT,
                      'initial': list(self.tm.themes.keys()).index(self.tm.theme_name)}
        }, self, name="Настройки")
        self.options_window.clicked.connect(self.options_window_triggered)
        self.lib_dialog = LibDialog(self, "Библиотеки", self.sm)

        self.menu_bar = MenuBar({
            'Открыть': (self.open_project, None),
            'Код': (self.show_code, None),
            'Тесты': (self.show_tests, None),
            'Тестирование': (self.show_testing, None),
            'TODO': (self.show_todo, None),
            'Git': (self.show_git, None),
            'Настройки': (self.open_settings, None)
        })
        self.setMenuBar(self.menu_bar)
        self.testing_widget.ui_disable_func = self.menu_bar.setDisabled

        self.set_theme()

        if not os.path.isdir(self.sm.get_general('__project__', '')):
            self.open_project()
        else:
            self.tests_widget.open_tests()

    def set_theme(self):
        self.central_widget.setStyleSheet(self.tm.bg_style_sheet)
        self.menu_bar.setStyleSheet(self.tm.bg_style_sheet)
        self.tests_widget.set_theme()
        self.code_widget.set_theme()
        self.testing_widget.set_theme()
        self.menu_bar.setStyleSheet(f"""
        QMenuBar {{
        color: {self.tm['TextColor']};
        background-color: {self.tm['BgColor']};
        }}
        QMenuBar::item::selected {{
        background-color: {self.tm['MainColor']};
        }}
        """)

    def open_project(self, show_tests=True):
        path = QFileDialog.getExistingDirectory(directory=self.sm.get_general('__project__', os.getcwd()))
        if path:
            self.sm.set_general('__project__', path)
            self.sm.repair_settings()
            if show_tests:
                self.show_tests()

    def jump_to_code_from_todo(self, file_name, line):
        self.show_code()
        for i in range(self.code_widget.files_widget.files_list.count()):
            if self.code_widget.files_widget.files_list.item(i).text() == file_name:
                self.code_widget.files_widget.files_list.setCurrentRow(i)
                self.code_widget.code_edit.setCursorPosition(line, 0)
                break

    def options_window_triggered(self, key):
        if key == "lib":
            if self.lib_dialog.exec():
                self.code_widget.code_edit.update_libs()

    def open_settings(self):
        if self.options_window.exec():
            self.save_settings(self.options_window.values)

    def save_settings(self, dct):
        self.sm.set('compiler', dct['Компилятор'])
        self.sm.set('-lm', dct['Ключ -lm'])
        self.sm.set('clear_words', dct['Удалять слова при генерации выходного файла'])
        self.sm.set('pos_comparator', dct['Компаратор для позитивных тестов:'])
        self.sm.set('neg_comparator', dct['Компаратор для негативных тестов:'])
        self.sm.set('memory_testing', dct['Тестирование по памяти'])
        self.sm.set('coverage', dct['Coverage'])
        self.sm.set('pos_comparator', dct['Компаратор для позитивных тестов:'])
        self.sm.set('neg_comparator', dct['Компаратор для негативных тестов:'])
        self.sm.set('epsilon', dct['Погрешность сравнения чисел:'])
        self.sm.set('pos_substring', dct['Подстрока для позитивных тестов:'])
        self.sm.set('neg_substring', dct['Подстрока для негативных тестов:'])
        self.sm.set('line_sep', list(line_sep.keys())[dct['Символ переноса строки: ']])
        self.sm.set_general('theme', th := list(self.tm.themes.keys())[dct['Тема:']])
        self.tm.set_theme(th)
        self.set_theme()

    def show_tests(self):
        self.testing_widget.hide()
        self.code_widget.hide()
        self.git_widget.hide()
        self.todo_widget.hide()
        self.tests_widget.show()

    def show_testing(self):
        self.tests_widget.hide()
        self.code_widget.hide()
        self.git_widget.hide()
        self.todo_widget.hide()
        self.testing_widget.show()

    def show_code(self):
        self.testing_widget.hide()
        self.tests_widget.hide()
        self.git_widget.hide()
        self.todo_widget.hide()
        self.code_widget.show()

    def show_todo(self):
        self.testing_widget.hide()
        self.tests_widget.hide()
        self.git_widget.hide()
        self.code_widget.hide()
        self.todo_widget.show()

    def show_git(self):
        self.testing_widget.hide()
        self.tests_widget.hide()
        self.code_widget.hide()
        self.todo_widget.hide()
        self.git_widget.show()

    def open_test_from_code(self):
        index = self.code_widget.test_res_widget.currentRow()
        self.testing_widget.get_path(True)
        self.testing_widget.tests_list.setCurrentRow(index)
        self.testing_widget.open_test_info()
        self.show_testing()

    def closeEvent(self, a0):
        self.todo_widget.hide()
        self.code_widget.hide()
        self.tests_widget.hide()
        self.testing_widget.hide()
        self.git_widget.hide()
        super(MainWindow, self).close()
