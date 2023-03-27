from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFileDialog

from widgets.code_widget import CodeWidget
from widgets.testing_widget import TestingWidget
from widgets.options_window import OptionsWindow
from widgets.tests_widget import TestsWidget
from widgets.git_widget import GitWidget
from widgets.menu_bar import MenuBar
import json
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.settings = dict() if not os.path.isfile("settings.txt") else \
            json.loads(open('settings.txt', encoding='utf-8').read())
        if 'compiler' not in self.settings:
            self.settings['compiler'] = 'gcc -std=c99 -Wall -Werror'
        if '-lm' not in self.settings:
            self.settings['-lm'] = True

        self.setWindowTitle("TestGenerator")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(layout)

        self.tests_widget = TestsWidget(self.settings)
        layout.addWidget(self.tests_widget)

        self.testing_widget = TestingWidget(self.settings)
        layout.addWidget(self.testing_widget)
        self.testing_widget.hide()

        self.code_widget = CodeWidget(self.settings)
        layout.addWidget(self.code_widget)
        self.testing_widget.testing_signal.connect(self.code_widget.update_test_info)
        self.code_widget.testing_signal.connect(self.testing_widget.testing)
        self.code_widget.test_res_widget.doubleClicked.connect(self.open_test_from_code)
        self.code_widget.hide()

        self.git_widget = GitWidget(self.settings)
        layout.addWidget(self.git_widget)
        self.git_widget.hide()

        self.options_window = OptionsWindow({
            "Компилятор": {'type': str, 'initial': self.settings.get('compiler', 'gcc -std=c99 -Wall -Werror -lm'),
                           'width': 400},
            "Ключ -lm": {'type': bool, 'initial': True, 'name': OptionsWindow.NAME_RIGHT}
        })
        self.options_window.returnPressed.connect(self.save_settings)

        self.menu_bar = MenuBar({
            'Открыть': (self.open_project, None),
            'Код': (self.show_code, None),
            'Тесты': (self.show_tests, None),
            'Тестирование': (self.show_testing, None),
            'Git': (self.show_git, None),
            'Настройки': (self.options_window.show, None)
        })
        self.setMenuBar(self.menu_bar)

    def open_project(self):
        path = QFileDialog.getExistingDirectory(directory=self.settings.get('path', os.getcwd()))
        if path:
            self.settings['path'] = path
            self.tests_widget.open_tests()

    def save_settings(self, dct):
        self.settings['compiler'] = dct['Компилятор']
        self.settings['-lm'] = dct['Ключ -lm']

    def show_tests(self):
        self.testing_widget.hide()
        self.code_widget.hide()
        self.git_widget.hide()
        self.tests_widget.show()

    def show_testing(self):
        self.tests_widget.hide()
        self.code_widget.hide()
        self.git_widget.hide()
        self.testing_widget.show()

    def show_code(self):
        self.testing_widget.hide()
        self.tests_widget.hide()
        self.git_widget.hide()
        self.code_widget.show()

    def show_git(self):
        self.testing_widget.hide()
        self.tests_widget.hide()
        self.code_widget.hide()
        self.git_widget.show()

    def open_test_from_code(self):
        index = self.code_widget.test_res_widget.currentRow()
        self.testing_widget.get_path(True)
        self.testing_widget.testing()
        self.testing_widget.tests_list.setCurrentRow(index)
        self.testing_widget.open_test_info()
        self.show_testing()

    def closeEvent(self, a0):
        file = open("settings.txt", 'w', encoding="utf-8")
        file.write(json.dumps(self.settings))
        file.close()
        super(MainWindow, self).close()
