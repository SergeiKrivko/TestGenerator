from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFileDialog

from widgets.code_widget import CodeWidget
from widgets.testing_widget import TestingWidget
from widgets.options_window import OptionsWindow
from widgets.tests_widget import TestsWidget
from widgets.git_widget import GitWidget
from widgets.menu_bar import MenuBar
from other.commands import CommandManager
from widgets.todo_widget import TODOWidget
from widgets.lib_dialog import LibDialog
import json
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.q_settings = QSettings()
        try:
            settings = json.loads(self.q_settings.value("settings", defaultValue="{}"))
        except Exception:
            settings = dict()
        self.settings = settings.get(settings.get('path', ''), dict())
        self.settings['path'] = settings.get('path', '')
        del settings
        if 'compiler' not in self.settings:
            self.settings['compiler'] = 'gcc -std=c99 -Wall -Werror'
        if '-lm' not in self.settings:
            self.settings['-lm'] = True
        if 'lab' not in self.settings:
            self.settings['lab'] = 1
        if 'task' not in self.settings:
            self.settings['task'] = 1
        if 'var' not in self.settings:
            self.settings['var'] = 0

        self.setWindowTitle("TestGenerator")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(layout)

        self.cm = CommandManager(self.settings)

        self.tests_widget = TestsWidget(self.settings, self.cm)
        layout.addWidget(self.tests_widget)

        self.testing_widget = TestingWidget(self.settings, self.cm)
        layout.addWidget(self.testing_widget)
        self.testing_widget.hide()

        self.code_widget = CodeWidget(self.settings, self.q_settings, self.cm)
        layout.addWidget(self.code_widget)
        self.testing_widget.testing_start.connect(self.code_widget.testing_start)
        self.testing_widget.add_test.connect(self.code_widget.add_test)
        self.testing_widget.testing_end.connect(self.code_widget.end_testing)
        self.code_widget.testing_signal.connect(self.testing_widget.testing)
        self.code_widget.test_res_widget.doubleClicked.connect(self.open_test_from_code)
        self.code_widget.hide()

        self.git_widget = GitWidget(self.settings)
        layout.addWidget(self.git_widget)
        self.git_widget.hide()

        self.todo_widget = TODOWidget(self.settings, self.cm)
        layout.addWidget(self.todo_widget)
        self.todo_widget.jumpToCode.connect(self.jump_to_code_from_todo)
        self.todo_widget.hide(save_data=False)

        pos_comparator = self.settings.get('pos_comparator', (0, 0))[0]
        neg_comparator = self.settings.get('neg_comparator', (0, 0))[0]

        self.options_window = OptionsWindow({
            "Компилятор": {'type': str, 'initial': self.settings.get('compiler', 'gcc -std=c99 -Wall -Werror'),
                           'width': 400},
            "Ключ -lm": {'type': bool, 'initial': True, 'name': OptionsWindow.NAME_RIGHT},
            "Удалять слова при генерации выходного файла": {'type': bool, 'name': OptionsWindow.NAME_RIGHT,
                                                            'initial': self.settings.get('clear_words', False)},
            "Компаратор для позитивных тестов:": {'type': 'combo', 'values': {
                'Числа': {'value': {'type': float, 'initial': 0 if pos_comparator != 0 else self.settings.get(
                    'pos_comparator', (0, {'value': 0}))[1].get('value', 0),
                                    'min': 0, 'name': OptionsWindow.NAME_SKIP}},
                'Числа как текст': None,
                'Текст после подстроки': {
                    'value': {'type': str, 'initial': '' if pos_comparator != 2 else self.settings.get(
                        'pos_comparator', (0, {'value': 0}))[1].get('value', 0), 'name': OptionsWindow.NAME_SKIP}}
            },
                                                  'initial': self.settings.get('pos_comparator', (0, 0))[0]},
            "Компаратор для негативных тестов:": {'type': 'combo', 'values': {
                'Нет': None,
                'Числа': {'value': {'type': float, 'initial': 0 if neg_comparator != 1 else self.settings.get(
                    'neg_comparator', (0, {'value': 0}))[1].get('value', 0),
                                    'min': 0, 'name': OptionsWindow.NAME_SKIP}},
                'Числа как текст': None,
                'Текст после подстроки': {
                    'value': {'type': str, 'initial': '' if neg_comparator != 3 else self.settings.get(
                        'neg_comparator', (0, {'value': 0}))[1].get('value', 0), 'name': OptionsWindow.NAME_SKIP}}
            },
                                                  'initial': self.settings.get('neg_comparator', (0, 0))[0]},
            "Coverage": {'type': bool, 'name': OptionsWindow.NAME_RIGHT,
                         'initial': self.settings.get('coverage', 0)},
            "Тестирование по памяти": {'type': bool, 'name': OptionsWindow.NAME_RIGHT,
                                       'initial': self.settings.get('memory_testing', 0)},
            "lib": {'type': 'button', 'name': OptionsWindow.NAME_SKIP, 'text': 'Библиотеки'}
        }, self, name="Настройки")
        self.options_window.clicked.connect(self.options_window_triggered)
        self.lib_dialog = LibDialog(self, "Библиотеки", self.q_settings)

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

        if 'path' in self.settings and os.path.isdir(self.settings.get('path', '')):
            self.tests_widget.open_tests()
        else:
            self.open_project()

    def open_project(self):
        path = QFileDialog.getExistingDirectory(directory=self.settings.get('path', os.getcwd()))
        if path:
            self.settings['path'] = path
            self.tests_widget.open_tests()

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
                pass

    def open_settings(self):
        if self.options_window.exec():
            self.save_settings(self.options_window.values)

    def save_settings(self, dct):
        self.settings['compiler'] = dct['Компилятор']
        self.settings['-lm'] = dct['Ключ -lm']
        self.settings['clear_words'] = dct["Удалять слова при генерации выходного файла"]
        self.settings['pos_comparator'] = dct["Компаратор для позитивных тестов:"]
        self.settings['neg_comparator'] = dct["Компаратор для негативных тестов:"]
        self.settings['memory_testing'] = dct["Тестирование по памяти"]
        self.settings['coverage'] = dct["Coverage"]

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
        try:
            settings = json.loads(self.q_settings.value("settings", defaultValue="{}"))
        except Exception:
            settings = dict()
        settings[self.settings['path']] = self.settings
        settings['path'] = self.settings['path']
        self.q_settings.setValue("settings", json.dumps(settings))
        # self.settings.pop('path')
        # file = open("settings.txt", 'w', encoding="utf-8")
        # file.write(json.dumps(settings))
        # file.close()
        super(MainWindow, self).close()
