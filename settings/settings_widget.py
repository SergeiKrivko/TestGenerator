from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget, QDialog, QVBoxLayout, QPushButton

from settings.lib_dialog import LibWidget
from settings.project_settings_widget import ProjectSettingsWidget
from ui.options_window import OptionsWidget

line_sep = {'\n': 'LF (\\n)', '\r\n': 'CRLF (\\r\\n)', '\r': 'CR (\\r)'}
line_sep_reverse = {'LF (\\n)': '\n', 'CRLF (\\r\\n)': '\r\n', 'CR (\\r)': '\r'}


class SettingsWidget(QDialog):
    change_theme = pyqtSignal()

    def __init__(self, sm, tm):
        super(SettingsWidget, self).__init__()
        self.sm = sm
        self.tm = tm

        main_layout = QVBoxLayout()
        layout = QHBoxLayout()
        main_layout.addLayout(layout)

        self.setFixedSize(800, 500)

        self.list_widget = QListWidget()
        self.list_widget.addItems(['Основные', 'Проект', 'C', 'Python', 'Тестирование', 'Библиотеки'])
        self.list_widget.setFixedWidth(175)
        self.list_widget.currentItemChanged.connect(self.select_tab)
        layout.addWidget(self.list_widget)

        self.main_options_widget = OptionsWidget({
            "Символ переноса строки: ": {'type': 'combo', 'values': line_sep.values(), 'name': OptionsWidget.NAME_LEFT,
                                         'initial': list(line_sep.keys()).index(self.sm.get_general('line_sep', '\n'))},
            "Тема:": {'type': 'combo', 'values': list(self.tm.themes.keys()), 'name': OptionsWidget.NAME_LEFT,
                      'initial': list(self.tm.themes.keys()).index(self.tm.theme_name)},
            "Поиск программ при каждом запуске": {'type': bool, 'name': OptionsWidget.NAME_RIGHT,
                                                  'initial': self.sm.get_general('search_after_start', True)},
            "Не предлагать создание проекта при открытии файла": {
                'type': bool, 'name': OptionsWidget.NAME_RIGHT,
                'initial': self.sm.get_general('not_create_project', False)}
        }, margins=(20, 20, 20, 20))
        self.main_options_widget.clicked.connect(self.save_main_settings)
        layout.addWidget(self.main_options_widget)

        self.project_settings_widget = ProjectSettingsWidget(self.sm, self.tm)
        self.project_settings_widget.hide()
        layout.addWidget(self.project_settings_widget)

        self.c_options_widget = OptionsWidget({
            "Компилятор": {'type': 'program', 'width': 500, 'sm': self.sm, 'file': 'gcc.exe', 'key': 'gcc',
                           'initial': self.sm.get_general('gcc', '')},
            "Ключи компилятора": {'type': str, 'width': 400, 'initial': self.sm.get_general('c_compiler_keys', '')},
            "Ключ -lm": {'type': bool, 'name': OptionsWidget.NAME_RIGHT,
                         'initial': bool(self.sm.get_general('-lm', True))},
            "Coverage": {'type': 'program', 'width': 500, 'sm': self.sm, 'file': 'gcov.exe', 'key': 'gcov',
                         'initial': self.sm.get_general('gcov', '')},
        }, margins=(20, 20, 20, 20))
        self.c_options_widget.clicked.connect(self.save_c_settings)
        self.c_options_widget.hide()
        layout.addWidget(self.c_options_widget)

        self.python_options_widget = OptionsWidget({
            "Python": {'type': 'program', 'width': 500, 'sm': self.sm, 'file': 'python.exe', 'key': 'python',
                       'initial': self.sm.get_general('python', '')},
            "Python coverage": {'type': 'program', 'width': 500, 'sm': self.sm, 'file': 'coverage.exe',
                                'key': 'python_coverage',
                                'initial': self.sm.get_general('python_coverage', 'coverage')},
        }, margins=(20, 20, 20, 20))
        self.python_options_widget.clicked.connect(self.save_python_settings)
        self.python_options_widget.hide()
        layout.addWidget(self.python_options_widget)

        self.testing_widget = OptionsWidget({
            "Компаратор для позитивных тестов:": {'type': 'combo', 'name': OptionsWidget.NAME_LEFT, 'values': [
                'Числа', 'Числа как текст', 'Текст после подстроки', 'Слова после подстроки', 'Текст', 'Слова'],
                                                  'initial': self.sm.get_general('pos_comparator', 0)},
            "Компаратор для негативных тестов:": {'type': 'combo', 'name': OptionsWidget.NAME_LEFT, 'values': [
                'Нет', 'Числа', 'Числа как текст', 'Текст после подстроки', 'Слова после подстроки', 'Текст', 'Слова'],
                                                  'initial': self.sm.get_general('neg_comparator', 0)},
            'Погрешность сравнения чисел:': {'type': float, 'name': OptionsWidget.NAME_LEFT,
                                             'initial': self.sm.get_general('epsilon', 0)},
            'Подстрока для позитивных тестов': {'type': str, 'name': OptionsWidget.NAME_RIGHT,
                                                'initial': self.sm.get_general('pos_substring', 'Result:')},
            'Подстрока для негативных тестов': {'type': str, 'name': OptionsWidget.NAME_RIGHT,
                                                'initial': self.sm.get_general('neg_substring', 'Error:')},
            "Coverage": {'type': bool, 'name': OptionsWidget.NAME_RIGHT,
                         'initial': bool(self.sm.get_general('coverage', False))},
            "Тестирование по памяти": {'type': bool, 'name': OptionsWidget.NAME_RIGHT,
                                       'initial': bool(self.sm.get_general('memory_testing', False))},
            "Ограничение по времени:": {'type': float, 'min': 0.01, 'max': 600, 'name': OptionsWidget.NAME_LEFT,
                                        'initial': self.sm.get_general('time_limit', 3)},
        }, margins=(20, 20, 20, 20))
        self.testing_widget.hide()
        layout.addWidget(self.testing_widget)

        self.libs_widget = LibWidget(self.sm, self.tm)
        self.libs_widget.hide()
        layout.addWidget(self.libs_widget)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)
        main_layout.addLayout(buttons_layout)

        # self.button_cancel = QPushButton("Отмена")
        # self.button_cancel.setFixedSize(120, 24)
        # buttons_layout.addWidget(self.button_cancel)

        # self.button_ok = QPushButton("Ок")
        # self.button_ok.setFixedSize(120, 24)
        # self.button_ok.clicked.connect(self.accept)
        # buttons_layout.addWidget(self.button_ok)

        self.setLayout(main_layout)

    def set_theme(self):
        print(1)
        self.setStyleSheet(self.tm.bg_style_sheet)
        # self.button_ok.setStyleSheet(self.tm.button_css('Main'))
        # self.button_ok.setFont(self.tm.font_small)
        self.list_widget.setStyleSheet(self.tm.list_widget_css('Main'))
        self.tm.set_theme_to_list_widget(self.list_widget, self.tm.font_medium)
        self.main_options_widget.setFont(self.tm.font_small)
        self.testing_widget.setFont(self.tm.font_small)
        self.tm.css_to_options_widget(self.main_options_widget)
        self.tm.css_to_options_widget(self.c_options_widget)
        self.tm.css_to_options_widget(self.python_options_widget)
        self.tm.css_to_options_widget(self.testing_widget)
        self.libs_widget.set_theme()
        self.project_settings_widget.set_theme()

    def save_main_settings(self):
        dct = self.main_options_widget.values
        self.sm.set_general('line_sep', list(line_sep.keys())[dct['Символ переноса строки: ']])
        self.sm.set_general('search_after_start', int(dct['Поиск программ при каждом запуске']))
        self.sm.set_general('not_create_project', int(dct['Не предлагать создание проекта при открытии файла']))
        self.sm.set_general('theme', th := list(self.tm.themes.keys())[dct['Тема:']])
        self.tm.set_theme(th)
        self.change_theme.emit()

    def save_c_settings(self):
        dct = self.c_options_widget.values
        self.sm.set_general('c_compiler_keys', dct['Ключи компилятора'])
        self.sm.set_general('-lm', int(dct['Ключ -lm']))

    def save_python_settings(self):
        dct = self.python_options_widget.values
        self.sm.set_general('python', dct['Python'])

    def save_testing_settings(self):
        dct = self.testing_widget.values
        self.sm.set_general('pos_comparator', dct['Компаратор для позитивных тестов:'])
        self.sm.set_general('neg_comparator', dct['Компаратор для негативных тестов:'])
        self.sm.set_general('memory_testing', int(dct['Тестирование по памяти']))
        self.sm.set_general('coverage', int(dct['Coverage']))
        self.sm.set_general('epsilon', dct['Погрешность сравнения чисел:'])
        self.sm.set_general('pos_substring', dct['Подстрока для позитивных тестов'])
        self.sm.set_general('neg_substring', dct['Подстрока для негативных тестов'])
        self.sm.set_general('time_limit', float(dct['Ограничение по времени:']))

    def exec(self) -> int:
        self.set_theme()
        return super().exec()

    def hide(self, save_settings=True):
        if not self.isHidden() and save_settings:
            self.save_main_settings()
            self.save_testing_settings()
        super(SettingsWidget, self).hide()

    def select_tab(self, item):
        if item is not None:
            self.main_options_widget.hide()
            self.project_settings_widget.hide()
            self.c_options_widget.hide()
            self.python_options_widget.hide()
            self.testing_widget.hide()
            self.libs_widget.hide()
            tab = item.text()
            if tab == 'Основные':
                self.main_options_widget.show()
            if tab == 'Проект':
                self.project_settings_widget.show()
            if tab == 'C':
                self.c_options_widget.show()
            if tab == 'Python':
                self.python_options_widget.show()
            if tab == 'Тестирование':
                self.testing_widget.show()
            if tab == 'Библиотеки':
                self.libs_widget.show()
