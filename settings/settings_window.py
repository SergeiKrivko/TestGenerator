from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget, QDialog, QVBoxLayout, QPushButton

from settings.lib_dialog import LibWidget
from settings.program_combo_box import ProgramBox
from settings.project_settings_widget import ProjectSettingsWidget
from ui.options_window import OptionsWidget
from ui.settings_widget import SettingsWidget, LineEdit, CheckBox, ComboBox, KEY_GLOBAL, SpinBox, FileEdit, KEY_LOCAL, \
    KEY_SMART, SwitchBox

line_sep = {'\n': 'LF (\\n)', '\r\n': 'CRLF (\\r\\n)', '\r': 'CR (\\r)'}
line_sep_reverse = {'LF (\\n)': '\n', 'CRLF (\\r\\n)': '\r\n', 'CR (\\r)': '\r'}


class SettingsWindow(QDialog):
    change_theme = pyqtSignal()

    def __init__(self, sm, tm):
        super(SettingsWindow, self).__init__()
        self.sm = sm
        self.tm = tm

        main_layout = QVBoxLayout()
        layout = QHBoxLayout()
        main_layout.addLayout(layout)

        self.setFixedSize(800, 500)

        self.list_widget = QListWidget()
        self.list_widget.addItems(['Основные', 'Проект', 'Проект - структура', 'Проект - тестирование', 'C',
                                   'Python', 'Тестирование', 'Библиотеки'])
        self.list_widget.setFixedWidth(175)
        self.list_widget.currentItemChanged.connect(self.select_tab)
        layout.addWidget(self.list_widget)

        self.main_settings_widget = SettingsWidget(
            self.sm, self.tm,
            ComboBox("Символ переноса строки: ", list(line_sep.values()), key='line_sep'),
            ComboBox("Тема: ", list(self.tm.themes.keys()), key='theme', text_mode=True,
                     on_state_changed=self.change_theme.emit),
            CheckBox("Поиск программ при каждом запуске", key='search_after_start'),
            CheckBox("Не предлагать создание проекта при открытии файла", key='not_create_project'),
            key_type=KEY_GLOBAL)
        layout.addWidget(self.main_settings_widget)

        self.project_settings_widget = SettingsWidget(
            self.sm, self.tm,
            FileEdit("Папка проекта:", mode=FileEdit.MODE_DIR),
            ComboBox("Язык:", ['C', 'Python'], key='language', text_mode=True),
            key_type=KEY_LOCAL)
        self.project_settings_widget.hide()
        layout.addWidget(self.project_settings_widget)

        self.project_struct_widget = SettingsWidget(
            self.sm, self.tm,
            ComboBox("Структура проекта", ['Лаба - задание - вариант', 'Без структуры'], key='struct', width=250),
            CheckBox("Сохранять тесты в папке проекта", state=False, key='func_tests_in_project'),
            key_type=KEY_LOCAL
        )
        self.project_struct_widget.hide()
        layout.addWidget(self.project_struct_widget)

        self.project_testing_widget = SettingsWidget(
            self.sm, self.tm,
            CheckBox("Глобальные настройки компилятора/интерпретатора", key='default_compiler_settings', children={
                False: SwitchBox(lambda: self.sm.get('language'), {
                    'C': [
                        ProgramBox(self.sm, self.tm, 'gcc.exe', 'gcc', True, "Компилятор:"),
                        LineEdit("Ключи компилятора: ", key='c_compiler_keys', width=450),
                        CheckBox("Ключ -lm", True, key='-lm'),
                        ProgramBox(self.sm, self.tm, 'gcov.exe', 'gcov', True, "Coverage:"),
                    ],
                    'Python': [
                        ProgramBox(self.sm, self.tm, 'python.exe', 'python', True, "Python:"),
                        ProgramBox(self.sm, self.tm, 'coverage.exe', 'python_coverage', True, "Python coverage:"),
                    ],
                })
                }),
            CheckBox("Глобальные настройки тестирования", key='default_testing_settings', children={False: [
                ComboBox("Компаратор для позитивных тестов:", ['Числа', 'Числа как текст', 'Текст после подстроки',
                                                               'Слова после подстроки', 'Текст', 'Слова'],
                         key='pos_comparator'),
                ComboBox("Компаратор для негативных тестов:",
                         ['Нет', 'Числа', 'Числа как текст', 'Текст после подстроки',
                          'Слова после подстроки', 'Текст', 'Слова'],
                         key='neg_comparator'),
                SpinBox("Погрешность сравнения чисел:", min_value=0, max_value=1000, key='epsilon', double=True),
                LineEdit("Подстрока для позитивных тестов", text='Result:', key='pos_substring'),
                LineEdit("Подстрока для негативных тестов", text='Error:', key='neg_substring'),
                CheckBox("Coverage", key='coverage'),
                CheckBox("Тестирование по памяти", key='memory_testing'),
                SpinBox("Ограничение по времени:", min_value=0, max_value=600, key='time_limit', double=True),
            ]}),
            key_type=KEY_SMART
        )
        self.project_testing_widget.hide()
        layout.addWidget(self.project_testing_widget)

        self.c_settings_widget = SettingsWidget(
            self.sm, self.tm,
            ProgramBox(self.sm, self.tm, 'gcc.exe', 'gcc', True, "Компилятор:"),
            LineEdit("Ключи компилятора: ", key='c_compiler_keys', width=450),
            CheckBox("Ключ -lm", True, key='-lm'),
            ProgramBox(self.sm, self.tm, 'gcov.exe', 'gcov', True, "Coverage:"),
            key_type=KEY_GLOBAL
        )
        self.c_settings_widget.hide()
        layout.addWidget(self.c_settings_widget)

        self.python_settings_widget = SettingsWidget(
            self.sm, self.tm,
            ProgramBox(self.sm, self.tm, 'python.exe', 'python', True, "Python:"),
            ProgramBox(self.sm, self.tm, 'coverage.exe', 'python_coverage', True, "Python coverage:"),
            key_type=KEY_GLOBAL
        )
        self.python_settings_widget.hide()
        layout.addWidget(self.python_settings_widget)

        self.testing_settings_widget = SettingsWidget(
            self.sm, self.tm,
            ComboBox("Компаратор для позитивных тестов:", ['Числа', 'Числа как текст', 'Текст после подстроки',
                                                           'Слова после подстроки', 'Текст', 'Слова'],
                     key='pos_comparator'),
            ComboBox("Компаратор для негативных тестов:", ['Нет', 'Числа', 'Числа как текст', 'Текст после подстроки',
                                                           'Слова после подстроки', 'Текст', 'Слова'],
                     key='neg_comparator'),
            SpinBox("Погрешность сравнения чисел:", min_value=0, max_value=1000, key='epsilon', double=True),
            LineEdit("Подстрока для позитивных тестов", text='Result:', key='pos_substring'),
            LineEdit("Подстрока для негативных тестов", text='Error:', key='neg_substring'),
            CheckBox("Coverage", key='coverage'),
            CheckBox("Тестирование по памяти", key='memory_testing'),
            SpinBox("Ограничение по времени:", min_value=0, max_value=600, key='time_limit', double=True),
            key_type=KEY_GLOBAL
        )
        self.testing_settings_widget.hide()
        layout.addWidget(self.testing_settings_widget)

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
        self.setStyleSheet(self.tm.bg_style_sheet)
        # self.button_ok.setStyleSheet(self.tm.button_css('Main'))
        # self.button_ok.setFont(self.tm.font_small)
        self.list_widget.setStyleSheet(self.tm.list_widget_css('Main'))
        self.tm.set_theme_to_list_widget(self.list_widget, self.tm.font_medium)
        self.libs_widget.set_theme()
        self.project_settings_widget.set_theme()
        self.main_settings_widget.set_theme()
        self.c_settings_widget.set_theme()
        self.python_settings_widget.set_theme()
        self.testing_settings_widget.set_theme()
        self.project_struct_widget.set_theme()
        self.project_testing_widget.set_theme()

    def exec(self) -> int:
        self.set_theme()
        for el in self.__dict__.values():
            if isinstance(el, SettingsWidget):
                el.load_values()
        return super().exec()

    def select_tab(self, item):
        if item is not None:
            self.main_settings_widget.hide()
            self.project_settings_widget.hide()
            self.project_struct_widget.hide()
            self.project_testing_widget.hide()
            self.c_settings_widget.hide()
            self.python_settings_widget.hide()
            self.testing_settings_widget.hide()
            self.libs_widget.hide()
            tab = item.text()
            if tab == 'Основные':
                self.main_settings_widget.show()
            if tab == 'Проект':
                self.project_settings_widget.show()
            if tab == 'Проект - структура':
                self.project_struct_widget.show()
            if tab == 'Проект - тестирование':
                self.project_testing_widget.show()
            if tab == 'C':
                self.c_settings_widget.show()
            if tab == 'Python':
                self.python_settings_widget.show()
            if tab == 'Тестирование':
                self.testing_settings_widget.show()
            if tab == 'Библиотеки':
                self.libs_widget.show()
