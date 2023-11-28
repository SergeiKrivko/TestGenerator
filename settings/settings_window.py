import os

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem

from backend.backend_types.program import PROGRAMS
from config import APP_NAME
from language.languages import PROJECT_LANGUAGES
from settings.in_data_window import InDataWidget
from settings.lib_dialog import LibWidget
from settings.settings_widget import SettingsWidget, LineEdit, CheckBox, ComboBox, KEY_GLOBAL, SpinBox, KEY_LOCAL, \
    KEY_DATA, SwitchBox, ProgramEdit, TextEdit
from settings.utils_edit import UtilsEdit
from ui.custom_dialog import CustomDialog

line_sep = {'\n': 'LF (\\n)', '\r\n': 'CRLF (\\r\\n)', '\r': 'CR (\\r)'}
line_sep_reverse = {'LF (\\n)': '\n', 'CRLF (\\r\\n)': '\r\n', 'CR (\\r)': '\r'}


class SettingsWindow(CustomDialog):
    change_theme = pyqtSignal()

    def __init__(self, sm, bm, tm, side_bar):
        super(SettingsWindow, self).__init__(tm, f"{APP_NAME} - настройки", True, True)
        self.sm = sm
        self.bm = bm

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 0, 10)
        main_layout.addLayout(layout)

        self.setFixedSize(920, 600)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        # self.tree_widget.setFocusPolicy(False)
        self.tree_widget.setFixedWidth(200)

        self.tree_widget.addTopLevelItem(QTreeWidgetItem(['Основные']))
        self.tree_widget.addTopLevelItem(QTreeWidgetItem(['Интерфейс']))

        self.tree_widget.addTopLevelItem(item := QTreeWidgetItem(['Проект']))
        item.addChild(QTreeWidgetItem(['Структура']))
        item.addChild(QTreeWidgetItem(['Тестирование']))
        item.addChild(QTreeWidgetItem(['Входные данные']))

        self.tree_widget.addTopLevelItem(item := QTreeWidgetItem(['Языки']))
        item.addChild(QTreeWidgetItem(['C']))
        item.addChild(QTreeWidgetItem(['C++']))
        item.addChild(QTreeWidgetItem(['Python']))
        item.addChild(QTreeWidgetItem(['Bash']))

        self.tree_widget.addTopLevelItem(QTreeWidgetItem(['Тестирование ']))
        self.tree_widget.addTopLevelItem(QTreeWidgetItem(['Сторонние утилиты']))
        self.tree_widget.addTopLevelItem(QTreeWidgetItem(['Библиотеки']))

        self.tree_widget.currentItemChanged.connect(self.select_tab)
        layout.addWidget(self.tree_widget)

        self.main_settings_widget = SettingsWidget(
            self.sm, self.tm,
            ComboBox("Символ переноса строки: ", list(line_sep.values()), key='line_sep'),
            CheckBox("Уведомления", key='notifications'),
            CheckBox("Поиск программ при каждом запуске", key='search_after_start'),
            CheckBox("Создавать временный проект при открытии файла", key='open_file_temp_project'),
            CheckBox("Создавать временный проект при открытии директории", key='open_dir_temp_project'),
            CheckBox("Использовать WSL", key='use_wsl'),
            LineEdit("Папка с диалогами GPT", key='gpt_dialogs_path', one_line=True, width=400),
            key_type=KEY_GLOBAL)
        layout.addWidget(self.main_settings_widget)

        self.ui_settings_widget = SettingsWidget(
            self.sm, self.tm,
            ComboBox("Тема: ", list(self.tm.themes.keys()), key='theme', text_mode=True,
                     on_state_changed=self.change_theme.emit),
            *[CheckBox(item, True, f'side_button_{key}') for key, item in side_bar.desc.items()],
            key_type=KEY_GLOBAL)
        self.ui_settings_widget.hide()
        layout.addWidget(self.ui_settings_widget)

        self.project_settings_widget = SettingsWidget(
            self.sm, self.tm,
            LineEdit("Название:", '', width=500, key='name', key_type=KEY_DATA),
            ComboBox("Язык:", PROJECT_LANGUAGES, key='language', text_mode=True),
            TextEdit("Описание:", '', key='description', key_type=KEY_DATA),
            key_type=KEY_LOCAL)
        self.project_settings_widget.hide()
        layout.addWidget(self.project_settings_widget)

        self.project_struct_widget = SettingsWidget(
            self.sm, self.tm,
            CheckBox("Стандартная структура", state=True, key='default_struct', children={False: [
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
                LineEdit("Папка с модульными тестами", "unit_tests",
                         key='unit_tests_dir', width=500, check_func=SettingsWindow.check_path),
                LineEdit("Приложение для модульных тестов", "unit_tests.exe",
                         key='unit_tests_app', width=500, check_func=SettingsWindow.check_path),
                LineEdit("Папка с временными файлами", "out",
                         key='temp_files_dir', width=500, check_func=SettingsWindow.check_path)
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
                        *self.c_settings(),
                    ],
                    'C++': [
                        ProgramEdit("Компилятор:", PROGRAMS['g++']),
                    ],
                    'Python': [
                        ProgramEdit("Python:", PROGRAMS['python']),
                        ProgramEdit("Python coverage:", PROGRAMS['python_coverage']),
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
                LineEdit("Подстрока для позитивных тестов", text='Result:', key='pos_substring', one_line=True),
                LineEdit("Подстрока для негативных тестов", text='Error:', key='neg_substring', one_line=True),
                CheckBox("Coverage", key='coverage'),
                SpinBox("Ограничение по времени:", min_value=0, max_value=600, key='time_limit', double=True),
            ]}),
            key_type=KEY_LOCAL
        )
        self.project_testing_widget.hide()
        layout.addWidget(self.project_testing_widget)

        self.project_in_widget = InDataWidget(self.sm, self.bm, self.tm)
        self.project_in_widget.hide()
        layout.addWidget(self.project_in_widget)

        self.c_settings_widget = SettingsWidget(
            self.sm, self.tm,
            *self.c_settings(),
            key_type=KEY_GLOBAL
        )
        self.c_settings_widget.hide()
        layout.addWidget(self.c_settings_widget)

        self.cpp_settings_widget = SettingsWidget(
            self.sm, self.tm,
            ProgramEdit("Компилятор:", PROGRAMS['g++']),
            key_type=KEY_GLOBAL
        )
        self.cpp_settings_widget.hide()
        layout.addWidget(self.cpp_settings_widget)

        self.python_settings_widget = SettingsWidget(
            self.sm, self.tm,
            ProgramEdit("Python:", PROGRAMS['python']),
            ProgramEdit("Python coverage:", PROGRAMS['python_coverage']),
            key_type=KEY_GLOBAL
        )
        self.python_settings_widget.hide()
        layout.addWidget(self.python_settings_widget)

        self.bash_settings_widget = SettingsWidget(
            self.sm, self.tm,
            ProgramEdit("Интерпретатор Bash:", PROGRAMS['bash']),
            key_type=KEY_GLOBAL,
        )
        self.bash_settings_widget.hide()
        layout.addWidget(self.bash_settings_widget)

        self.testing_settings_widget = SettingsWidget(
            self.sm, self.tm,
            ComboBox("Компаратор для позитивных тестов:", ['Числа', 'Числа как текст', 'Текст после подстроки',
                                                           'Слова после подстроки', 'Текст', 'Слова'],
                     key='pos_comparator'),
            ComboBox("Компаратор для негативных тестов:", ['Нет', 'Числа', 'Числа как текст', 'Текст после подстроки',
                                                           'Слова после подстроки', 'Текст', 'Слова'],
                     key='neg_comparator'),
            SpinBox("Погрешность сравнения чисел:", min_value=0, max_value=1000, key='epsilon', double=True),
            LineEdit("Подстрока для позитивных тестов", text='Result:', key='pos_substring', one_line=True),
            LineEdit("Подстрока для негативных тестов", text='Error:', key='neg_substring', one_line=True),
            CheckBox("Coverage", key='coverage'),
            SpinBox("Ограничение по времени:", min_value=0, max_value=600, key='time_limit', double=True),
            key_type=KEY_GLOBAL
        )
        self.testing_settings_widget.hide()
        layout.addWidget(self.testing_settings_widget)

        self.utils_widget = UtilsEdit(self.bm, self.tm)
        self.utils_widget.hide()
        layout.addWidget(self.utils_widget)

        self.libs_widget = LibWidget(self.sm, self.tm)
        self.libs_widget.hide()
        layout.addWidget(self.libs_widget)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
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
    def c_settings():
        return [ProgramEdit("Компилятор:", PROGRAMS['gcc']),
                ProgramEdit("Lcov:", PROGRAMS['lcov']),
                ProgramEdit("Genhtml:", PROGRAMS['genhtml'])]

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
            command.format(app='app.exe', file='main.c', args='1 2 3', dist='dist.txt', files='main.c logic.c')
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
        super().set_theme()
        # self.button_ok.setStyleSheet(self.tm.button_css('Main'))
        # self.button_ok.setFont(self.tm.font_small)
        self.tree_widget.setStyleSheet(self.tm.tree_widget_css('Bg', border=False))
        self.tree_widget.setFont(self.tm.font_big)
        self.libs_widget.set_theme()
        self.project_settings_widget.set_theme()
        self.main_settings_widget.set_theme()
        self.ui_settings_widget.set_theme()
        self.c_settings_widget.set_theme()
        self.cpp_settings_widget.set_theme()
        self.python_settings_widget.set_theme()
        self.bash_settings_widget.set_theme()
        self.testing_settings_widget.set_theme()
        self.project_struct_widget.set_theme()
        self.project_testing_widget.set_theme()
        self.project_in_widget.set_theme()
        self.utils_widget.set_theme()

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
            self.ui_settings_widget.hide()
            self.project_settings_widget.hide()
            self.project_struct_widget.hide()
            self.project_testing_widget.hide()
            self.project_in_widget.hide()
            self.c_settings_widget.hide()
            self.cpp_settings_widget.hide()
            self.python_settings_widget.hide()
            self.bash_settings_widget.hide()
            self.testing_settings_widget.hide()
            self.libs_widget.hide()
            self.utils_widget.hide()

            if tab == 'Основные':
                self.main_settings_widget.show()
            if tab == 'Интерфейс':
                self.ui_settings_widget.show()
            if tab == 'Проект':
                self.project_settings_widget.show()
            if tab == 'Структура':
                self.project_struct_widget.show()
            if tab == 'Тестирование':
                self.project_testing_widget.show()
            if tab == 'Входные данные':
                self.project_in_widget.show()
            if tab == 'C':
                self.c_settings_widget.show()
            if tab == 'C++':
                self.cpp_settings_widget.show()
            if tab == 'Python':
                self.python_settings_widget.show()
            if tab == 'Bash':
                self.bash_settings_widget.show()
            if tab == 'Тестирование ':
                self.testing_settings_widget.show()
            if tab == 'Библиотеки':
                self.libs_widget.show()
            if tab == 'Сторонние утилиты':
                self.utils_widget.show()
