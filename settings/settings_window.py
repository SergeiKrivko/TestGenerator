import os

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QHBoxLayout, QDialog, QVBoxLayout, QTreeWidget, QTreeWidgetItem

from settings.lib_dialog import LibWidget
from ui.settings_widget import SettingsWidget, LineEdit, CheckBox, ComboBox, KEY_GLOBAL, SpinBox, FileEdit, KEY_LOCAL, \
    KEY_SMART, SwitchBox, ProgramEdit, ListWidget

line_sep = {'\n': 'LF (\\n)', '\r\n': 'CRLF (\\r\\n)', '\r': 'CR (\\r)'}
line_sep_reverse = {'LF (\\n)': '\n', 'CRLF (\\r\\n)': '\r\n', 'CR (\\r)': '\r'}


class SettingsWindow(QDialog):
    change_theme = pyqtSignal()

    def __init__(self, sm, tm):
        super(SettingsWindow, self).__init__()
        self.sm = sm
        self.tm = tm

        self.setWindowTitle("TestGenerator - настройки")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 0, 10)
        main_layout.addLayout(layout)

        self.setFixedSize(800, 500)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setFocusPolicy(False)
        self.tree_widget.setFixedWidth(200)

        self.tree_widget.addTopLevelItem(QTreeWidgetItem(['Основные']))

        self.tree_widget.addTopLevelItem(item := QTreeWidgetItem(['Проект']))
        item.addChild(QTreeWidgetItem(['Структура']))
        item.addChild(QTreeWidgetItem(['Тестирование']))

        self.tree_widget.addTopLevelItem(item := QTreeWidgetItem(['Языки']))
        item.addChild(QTreeWidgetItem(['C']))
        item.addChild(QTreeWidgetItem(['Python']))

        self.tree_widget.addTopLevelItem(QTreeWidgetItem(['Тестирование ']))
        self.tree_widget.addTopLevelItem(QTreeWidgetItem(['Библиотеки']))

        self.tree_widget.currentItemChanged.connect(self.select_tab)
        layout.addWidget(self.tree_widget)

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
            ComboBox("Структура проекта", ['Лаба - задание - вариант', 'Без структуры'], key='struct', width=250,
                     children={0: [
                         LineEdit("Шаблон имени папки с лабой:", "lab_{lab:0>2}_{task:0>2}_{var:0>2}",
                                  key='dir_pattern', width=300, check_func=SettingsWindow.check_dir_pattern),
                         LineEdit("Шаблон имени папки с лабой при отсутствии варианта:", "lab_{lab:0>2}_{task:0>2}",
                                  key='dir_no_var_pattern', width=300, check_func=SettingsWindow.check_dir_pattern)
                     ]}),
            CheckBox("Сохранять тесты в папке проекта", state=False, key='func_tests_in_project', children={True: [
                LineEdit("Файл с входными данными:", "func_tests/data/{test_type}_{number:0>2}_in.txt",
                         key='stdin_pattern', width=500, check_func=SettingsWindow.check_std_pattern),
                LineEdit("Файл с выходными данными:", "func_tests/data/{test_type}_{number:0>2}_out.txt",
                         key='stdout_pattern', width=500, check_func=SettingsWindow.check_std_pattern),
                LineEdit("Файл с аргументами:", "func_tests/data/{test_type}_{number:0>2}_args.txt",
                         key='args_pattern', width=500, check_func=SettingsWindow.check_std_pattern),
                LineEdit("Входные файлы:", "func_tests/data_files/{test_type}_{number:0>2}_in{index}.{extension}",
                         key='fin_pattern', width=500, check_func=SettingsWindow.check_file_name_pattern),
                LineEdit("Выходные файлы:", "func_tests/data_files/{test_type}_{number:0>2}_out{index}.{extension}",
                         key='fout_pattern', width=500, check_func=SettingsWindow.check_file_name_pattern),
                LineEdit("Файлы проверки состояния входных:",
                         "func_tests/data_files/{test_type}_{number:0>2}_check{index}.{extension}",
                         key='fcheck_pattern', width=500, check_func=SettingsWindow.check_file_name_pattern),
                LineEdit("Информация о тестах", "func_tests/readme.md",
                         key='readme_pattern', width=500, check_func=SettingsWindow.check_path)
            ]}),
            key_type=KEY_LOCAL
        )
        self.project_struct_widget.hide()
        layout.addWidget(self.project_struct_widget)

        self.project_testing_widget = SettingsWidget(
            self.sm, self.tm,
            CheckBox("Глобальные настройки компилятора/интерпретатора", key='default_compiler_settings', children={
                False: SwitchBox(lambda: self.sm.get('language'), {
                    'C': [
                        self.c_settings(),
                        self.utils_settings('C'),
                    ],
                    'Python': [
                        ProgramEdit("Python:", 'python.exe', 'python'),
                        ProgramEdit("Python coverage:", 'coverage.exe', 'python_coverage'),
                        self.utils_settings('Python'),
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
            self.c_settings(),
            self.utils_settings('C'),
            key_type=KEY_GLOBAL
        )
        self.c_settings_widget.hide()
        layout.addWidget(self.c_settings_widget)

        self.python_settings_widget = SettingsWidget(
            self.sm, self.tm,
            ProgramEdit("Python:", 'python.exe', 'python'),
            ProgramEdit("Python coverage:", 'coverage.exe', 'python_coverage'),
            self.utils_settings('Python'),
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

    @staticmethod
    def utils_settings(language='C'):
        return ListWidget("Сторонние утилиты:", children=lambda: [
            LineEdit("Строка запуска: ", key='program', width=400),
            ComboBox("Тип:", ["Для теста"], children={
                0: [ComboBox("Тип вывода:", ["STDOUT", "STDERR", "Файл ({dist})"], key='output_format'),
                    CheckBox("Наличие вывода считается отрицательным результатом", key='output_res'),
                    CheckBox("Ненулевой код возврата считается отрицательным результатом", key='exit_code_res')],
                1: LineEdit("Команда:", key='report_command', width=350),
            }, key='type', width=250)], key=f'{language}_utils')

    @staticmethod
    def c_settings():
        return SwitchBox(lambda: os.name == 'posix', {True: [
            LineEdit("Ключи компилятора: ", key='c_compiler_keys', width=450),
            CheckBox("Ключ -lm", True, key='-lm'),
        ], False: CheckBox("Использовать WSL", False, key="C_wsl", children={True: [
            LineEdit("Ключи компилятора: ", key='c_compiler_keys', width=450),
            CheckBox("Ключ -lm", True, key='-lm'),
        ], False: [
            ProgramEdit("Компилятор:", 'gcc.exe', 'gcc'),
            LineEdit("Ключи компилятора: ", key='c_compiler_keys', width=450),
            ProgramEdit("Coverage:", 'gcov.exe', 'gcov'),
        ]}, not_delete_keys=True)
        }, not_delete_keys=True)

    @staticmethod
    def check_path(path: str):
        for el in "\"'!?:;":
            if el in path:
                return False
        return True

    @staticmethod
    def check_std_pattern(pattern: str):
        try:
            path = pattern.format(test_type='pos', number=1)
            return SettingsWindow.check_path(path)
        except Exception:
            return False

    @staticmethod
    def check_util(command: str):
        try:
            command.format(app='app.exe', file='main.c', args='1 2 3', dist='dist.txt')
            return True
        except Exception:
            return False

    @staticmethod
    def check_file_name_pattern(pattern: str):
        try:
            path = pattern.format(test_type='pos', number=1, index=1, extension='txt')
            return SettingsWindow.check_path(path)
        except Exception:
            return False

    @staticmethod
    def check_dir_pattern(pattern: str):
        try:
            path = pattern.format(lab=1, task=1, var=0)
            return SettingsWindow.check_path(path)
        except Exception:
            return False

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        # self.button_ok.setStyleSheet(self.tm.button_css('Main'))
        # self.button_ok.setFont(self.tm.font_small)
        self.tree_widget.setStyleSheet(self.tm.tree_widget_css('Bg', border=False))
        self.tree_widget.setFont(self.tm.font_medium)
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

    def select_tab(self, item: QTreeWidgetItem):
        if item is not None:
            tab = item.text(0)
            if tab == 'Языки':
                return

            self.main_settings_widget.hide()
            self.project_settings_widget.hide()
            self.project_struct_widget.hide()
            self.project_testing_widget.hide()
            self.c_settings_widget.hide()
            self.python_settings_widget.hide()
            self.testing_settings_widget.hide()
            self.libs_widget.hide()

            if tab == 'Основные':
                self.main_settings_widget.show()
            if tab == 'Проект':
                self.project_settings_widget.show()
            if tab == 'Структура':
                self.project_struct_widget.show()
            if tab == 'Тестирование':
                self.project_testing_widget.show()
            if tab == 'C':
                self.c_settings_widget.show()
            if tab == 'Python':
                self.python_settings_widget.show()
            if tab == 'Тестирование ':
                self.testing_settings_widget.show()
            if tab == 'Библиотеки':
                self.libs_widget.show()
