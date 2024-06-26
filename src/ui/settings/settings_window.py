from PyQt6.QtCore import Qt
from PyQtUIkit.widgets import *

from src.backend.backend_types.program import PROGRAMS
from src.backend.language.languages import PROJECT_LANGUAGES
from src.backend.managers import BackendManager
from src.config import APP_NAME
from src.ui.settings.plugins_widget import PluginsWidget
from src.ui.settings.settings_widget import SettingsWidget, ComboBox, CheckBox, KEY_GLOBAL, LineEdit, SwitchBox, \
    KEY_DATA, TextEdit, KEY_LOCAL, ProgramEdit, SpinBox

line_sep = {'\n': 'LF (\\n)', '\r\n': 'CRLF (\\r\\n)', '\r': 'CR (\\r)'}
line_sep_reverse = {'LF (\\n)': '\n', 'CRLF (\\r\\n)': '\r\n', 'CR (\\r)': '\r'}


class SettingsWindow(KitDialog):
    def __init__(self, parent, bm: BackendManager, side_tabs):
        super(SettingsWindow, self).__init__(parent)
        self.name = f"{APP_NAME} - настройки"
        self.bm = bm
        self.sm = bm.sm

        self.__layout = KitHBoxLayout()
        self.__layout.setSpacing(20)
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__layout.setContentsMargins(10, 10, 0, 10)
        self.setWidget(self.__layout)

        self.__tabs = dict()

        self.setFixedSize(920, 600)

        self.tree_widget = KitTreeWidget()
        self.tree_widget.border = 0
        self.tree_widget.main_palette = 'Bg'
        self.tree_widget.setFixedWidth(175)
        self.tree_widget.currentItemChanged.connect(self.select_tab)
        self.__layout.addWidget(self.tree_widget)

        self.__layout.addWidget(KitVSeparator())

        self.add_tab('Основные', SettingsWidget(
            self.sm,
            ComboBox(self.bm, "Символ переноса строки: ", list(line_sep.values()), key='line_sep'),
            CheckBox(self.bm, "Уведомления", key='notifications'),
            CheckBox(self.bm, "Поиск программ при каждом запуске", key='search_after_start'),
            CheckBox(self.bm, "Открывать файлы в режиме LightEdit", key='open_file_in_light_edit'),
            CheckBox(self.bm, "Использовать WSL", key='use_wsl'),
            key_type=KEY_GLOBAL))

        self.add_tab('Интерфейс', SettingsWidget(
            self.sm,
            ComboBox(self.bm, "Тема:", ['light', 'dark'], key='theme', text_mode=True,
                     on_state_changed=self._on_theme_changed),
            ComboBox(self.bm, "Тема редактора кода:", ['classic', 'neon', 'twilight'],
                     key='code_theme', text_mode=True,
                     on_state_changed=self._on_theme_changed),
            # *[CheckBox(item, True, f'side_button_{key}') for key, item in side_bar.desc.items()],
            key_type=KEY_GLOBAL))

        self.add_tab('Проект', SettingsWidget(
            self.sm,
            LineEdit(self.bm, "Название:", '', width=500, key='name', key_type=KEY_DATA),
            ComboBox(self.bm, "Язык:", PROJECT_LANGUAGES, key='language', text_mode=True),
            SwitchBox(self.bm, lambda: self.sm.get('temp'), children={True: [
                CheckBox(self.bm, "Временный проект", True, key='temp')
            ]}),
            TextEdit(self.bm, "Описание:", '', key='description', key_type=KEY_DATA),
            key_type=KEY_LOCAL))

        self.add_tab('Проект/Структура', SettingsWidget(
            self.sm,
            CheckBox(self.bm, "Стандартная структура", state=True, key='default_struct', children={False: [
                CheckBox(self.bm, "Сохранять тесты в папке проекта", state=False, key='func_tests_in_project',
                         children={True: [
                             LineEdit(self.bm, "Файл с входными данными:",
                                      "func_tests/data/{test_type}_{number:0>2}_in.txt",
                                      key='stdin_pattern', width=500, check_func=SettingsWindow.check_std_pattern),
                             LineEdit(self.bm, "Файл с выходными данными:",
                                      "func_tests/data/{test_type}_{number:0>2}_out.txt",
                                      key='stdout_pattern', width=500, check_func=SettingsWindow.check_std_pattern),
                             LineEdit(self.bm, "Файл с аргументами:",
                                      "func_tests/data/{test_type}_{number:0>2}_args.txt",
                                      key='args_pattern', width=500, check_func=SettingsWindow.check_std_pattern),
                             LineEdit(self.bm, "Входные файлы:",
                                      "func_tests/data_files/{test_type}_{number:0>2}_in{index}.{extension}",
                                      key='fin_pattern', width=500, check_func=SettingsWindow.check_file_name_pattern),
                             LineEdit(self.bm, "Выходные файлы:",
                                      "func_tests/data_files/{test_type}_{number:0>2}_out{index}.{extension}",
                                      key='fout_pattern', width=500, check_func=SettingsWindow.check_file_name_pattern),
                             LineEdit(self.bm, "Файлы проверки состояния входных:",
                                      "func_tests/data_files/{test_type}_{number:0>2}_check{index}.{extension}",
                                      key='fcheck_pattern', width=500,
                                      check_func=SettingsWindow.check_file_name_pattern),
                             LineEdit(self.bm, "Информация о тестах", "func_tests/readme.md",
                                      key='readme_pattern', width=500, check_func=SettingsWindow.check_path)
                         ]}),
                LineEdit(self.bm, "Папка с модульными тестами", "unit_tests",
                         key='unit_tests_dir', width=500, check_func=SettingsWindow.check_path),
                LineEdit(self.bm, "Приложение для модульных тестов", "unit_tests.exe",
                         key='unit_tests_app', width=500, check_func=SettingsWindow.check_path),
                LineEdit(self.bm, "Папка с временными файлами", "out",
                         key='temp_files_dir', width=500, check_func=SettingsWindow.check_path)
            ]}),
            key_type=KEY_LOCAL
        ))

        self.add_tab('Проект/Тестирование', SettingsWidget(
            self.sm,
            CheckBox(self.bm, "Глобальные настройки компилятора/интерпретатора", key='default_compiler_settings',
                     children={
                         False: SwitchBox(self.bm, lambda: self.sm.get('language'), {
                             'C': [
                                 *self.c_settings(),
                             ],
                             'C++': [
                                 ProgramEdit(self.bm, "Компилятор:", PROGRAMS['g++']),
                             ],
                             'Python': [
                                 ProgramEdit(self.bm, "Python:", PROGRAMS['python']),
                             ],
                         })
                     }),
            CheckBox(self.bm, "Глобальные настройки тестирования", key='default_testing_settings', children={False: [
                ComboBox(self.bm, "Компаратор для позитивных тестов:",
                         ['Числа', 'Числа как текст', 'Текст после подстроки',
                          'Слова после подстроки', 'Текст', 'Слова'],
                         key='pos_comparator'),
                ComboBox(self.bm, "Компаратор для негативных тестов:",
                         ['Нет', 'Числа', 'Числа как текст', 'Текст после подстроки',
                          'Слова после подстроки', 'Текст', 'Слова'],
                         key='neg_comparator'),
                SpinBox(self.bm, "Погрешность сравнения чисел:", min_value=0, max_value=1000, key='epsilon',
                        double=True),
                LineEdit(self.bm, "Подстрока для позитивных тестов", text='Result:', key='pos_substring',
                         one_line=True),
                LineEdit(self.bm, "Подстрока для негативных тестов", text='Error:', key='neg_substring', one_line=True),
                CheckBox(self.bm, "Coverage", key='coverage'),
                SpinBox(self.bm, "Ограничение по времени:", min_value=0, max_value=600, key='time_limit', double=True),
            ]}),
            key_type=KEY_LOCAL
        ))

        self.add_tab('Языки/C', SettingsWidget(
            self.sm,
            *self.c_settings(),
            key_type=KEY_GLOBAL
        ))

        self.add_tab('Языки/C++', SettingsWidget(
            self.sm,
            ProgramEdit(self.bm, "Компилятор:", PROGRAMS['g++']),
            key_type=KEY_GLOBAL
        ))

        self.add_tab('Языки/Python', SettingsWidget(
            self.sm,
            ProgramEdit(self.bm, "Python:", PROGRAMS['python']),
            key_type=KEY_GLOBAL
        ))

        self.add_tab('Языки/Bash', SettingsWidget(
            self.sm,
            ProgramEdit(self.bm, "Интерпретатор Bash:", PROGRAMS['bash']),
            key_type=KEY_GLOBAL,
        ))

        self.add_tab('Тестирование', SettingsWidget(
            self.sm,
            ComboBox(self.bm, "Компаратор для позитивных тестов:", ['Числа', 'Числа как текст', 'Текст после подстроки',
                                                                    'Слова после подстроки', 'Текст', 'Слова'],
                     key='pos_comparator'),
            ComboBox(self.bm, "Компаратор для негативных тестов:",
                     ['Нет', 'Числа', 'Числа как текст', 'Текст после подстроки',
                      'Слова после подстроки', 'Текст', 'Слова'],
                     key='neg_comparator'),
            SpinBox(self.bm, "Погрешность сравнения чисел:", min_value=0, max_value=1000, key='epsilon', double=True),
            LineEdit(self.bm, "Подстрока для позитивных тестов", text='Result:', key='pos_substring', one_line=True),
            LineEdit(self.bm, "Подстрока для негативных тестов", text='Error:', key='neg_substring', one_line=True),
            CheckBox(self.bm, "Coverage", key='coverage'),
            SpinBox(self.bm, "Ограничение по времени:", min_value=0, max_value=600, key='time_limit', double=True),
            key_type=KEY_GLOBAL
        ))

        self.add_tab('Расширения', PluginsWidget(self.bm))

    def c_settings(self):
        return [ProgramEdit(self.bm, "Компилятор:", PROGRAMS['gcc']),
                ProgramEdit(self.bm, "Lcov:", PROGRAMS['lcov']),
                ProgramEdit(self.bm, "Genhtml:", PROGRAMS['genhtml'])]

    def _on_theme_changed(self):
        theme = f"{self.sm.get_general('theme', 'dark')}-{self.sm.get_general('code_theme', 'classic')}"
        if self.theme_manager and self.theme_manager.active and self.theme_manager.current_theme != theme:
            self.theme_manager.set_theme(theme)
            self._apply_theme()

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

    def add_tab(self, key, widget):
        if '/' not in key:
            name = key
            parent = self.tree_widget
        else:
            name = key.split('/')[-1]
            path = key.split('/')[0]
            items = {item.key: item for item in self.tree_widget.items()}
            if path in items:
                parent = items[path]
            else:
                parent = _TreeWidgetItem(path, path)
                self.tree_widget.addItem(parent)

        item = _TreeWidgetItem(name, key)
        parent.addItem(item)
        self.__tabs[key] = widget
        widget.hide()
        self.__layout.addWidget(widget)

    def select_tab(self, item: '_TreeWidgetItem'):
        if item.key not in self.__tabs:
            return
        for key, el in self.__tabs.items():
            if key != item.key:
                el.hide()
        self.__tabs[item.key].show()
        
    def showEvent(self, a0) -> None:
        if not self._tm:
            super().showEvent(a0)

    def exec(self) -> int:
        for el in self.__dict__.values():
            if isinstance(el, SettingsWidget):
                el.load_values()
        return super().exec()


class _TreeWidgetItem(KitTreeWidgetItem):
    def __init__(self, name, key):
        super().__init__(name)
        self.key = key
