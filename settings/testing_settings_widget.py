from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel

from ui.options_window import OptionsWidget


class TestingSettingsWidget(QWidget):
    def __init__(self, sm, tm):
        super().__init__()
        self.sm = sm
        self.tm = tm

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(20, 20, 20, 20)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        self.compiler_checkbox = QCheckBox()
        self.compiler_checkbox.stateChanged.connect(self.compiler_checkbox_triggered)
        layout.addWidget(self.compiler_checkbox)
        self.compiler_label = QLabel("Глобальные настройки компилятора/интерпретатора")
        layout.addWidget(self.compiler_label)
        main_layout.addLayout(layout)

        self.language_widgets = dict()
        self.language_keys = dict()

        self.language_widgets['Python'] = OptionsWidget({
            "Python": {'type': 'program', 'width': 500, 'sm': self.sm, 'file': 'python.exe', 'key': 'python',
                       'initial': self.sm.get_smart('python', 'python'), 'global': False},
            "Python coverage": {'type': 'program', 'width': 500, 'sm': self.sm, 'file': 'coverage.exe', 'global': False,
                                'key': 'python_coverage', 'initial': self.sm.get_smart('python_coverage', 'coverage')},
        }, margins=(5, 5, 5, 5))
        self.language_keys['Python'] = {'Python': 'python', 'Python coverage': 'python_coverage'}

        self.language_widgets['C'] = OptionsWidget({
            "Ключи компилятора": {'type': str, 'width': 400, 'initial': self.sm.get_smart('c_compiler_keys', '')},
            "Ключ -lm": {'type': bool, 'name': OptionsWidget.NAME_RIGHT,
                         'initial': bool(self.sm.get_smart('c_lm', True))},
        }, margins=(5, 5, 5, 5))
        self.language_keys['C'] = {'Ключи компилятора': 'c_compiler_keys', 'Ключ -lm': '-lm'}

        for el in self.language_widgets.values():
            main_layout.addWidget(el)
            el.clicked.connect(self.save_settings)
            el.hide()

        layout2 = QHBoxLayout()
        layout2.setAlignment(Qt.AlignLeft)
        self.testing_checkbox = QCheckBox()
        self.testing_checkbox.stateChanged.connect(self.testing_checkbox_triggered)
        layout2.addWidget(self.testing_checkbox)
        self.testing_label = QLabel("Глобальные настройки тестирования")
        layout2.addWidget(self.testing_label)
        main_layout.addLayout(layout2)

        self.testing_widget = OptionsWidget({
            "Компаратор для позитивных тестов:": {'type': 'combo', 'name': OptionsWidget.NAME_LEFT, 'values': [
                'Числа', 'Числа как текст', 'Текст после подстроки', 'Слова после подстроки', 'Текст', 'Слова']},
            "Компаратор для негативных тестов:": {'type': 'combo', 'name': OptionsWidget.NAME_LEFT, 'values': [
                'Нет', 'Числа', 'Числа как текст', 'Текст после подстроки', 'Слова после подстроки', 'Текст', 'Слова']},
            'Погрешность сравнения чисел:': {'type': float, 'name': OptionsWidget.NAME_LEFT},
            'Подстрока для позитивных тестов': {'type': str, 'name': OptionsWidget.NAME_RIGHT},
            'Подстрока для негативных тестов': {'type': str, 'name': OptionsWidget.NAME_RIGHT},
            "Coverage": {'type': bool, 'name': OptionsWidget.NAME_RIGHT},
            "Тестирование по памяти": {'type': bool, 'name': OptionsWidget.NAME_RIGHT},
            "Ограничение по времени:": {'type': float, 'min': 0.01, 'max': 600, 'name': OptionsWidget.NAME_LEFT},
        }, margins=(5, 0, 0, 0))
        self.testing_widget.clicked.connect(self.save_settings)
        self.testing_keys = {'Компаратор для позитивных тестов:': 'pos_comparator',
                             'Компаратор для негативных тестов:': 'neg_comparator',
                             'Погрешность сравнения чисел:': 'epsilon',
                             'Подстрока для позитивных тестов': 'pos_substring',
                             'Подстрока для негативных тестов': 'neg_substring',
                             'Coverage': 'coverage',
                             'Тестирование по памяти': 'memory_testing',
                             'Ограничение по времени:': 'time_limit'}
        main_layout.addWidget(self.testing_widget)
        self.setLayout(main_layout)

        self.compiler_checkbox.setChecked(self.sm.get('default_compiler_settings', True))
        self.testing_checkbox.setChecked(self.sm.get('default_testing_settings', True))

    def compiler_checkbox_triggered(self):
        self.sm.set('default_compiler_settings', self.compiler_checkbox.isChecked())
        language = self.sm.get('language', 'C')
        if self.compiler_checkbox.isChecked():
            self.language_widgets[language].hide()
            for item in self.language_keys[language].values():
                self.sm.remove(item)
        else:
            self.language_widgets[language].show()
            for item in self.language_keys[language].values():
                self.sm.set(item, self.sm.get_smart(item))

    def testing_checkbox_triggered(self):
        self.sm.set('default_testing_settings', self.testing_checkbox.isChecked())
        if self.testing_checkbox.isChecked():
            self.testing_widget.hide()
            for item in self.testing_keys.values():
                self.sm.remove(item)
        else:
            self.testing_widget.show()
            for item in self.testing_keys.values():
                if value := self.sm.get_smart(item):
                    self.sm.set(item, value)

    def open(self):
        for el in self.language_widgets.values():
            el.hide()
        self.apply_values()
        self.compiler_checkbox.setChecked(self.sm.get('default_compiler_settings', True))
        self.testing_checkbox.setChecked(self.sm.get('default_testing_settings', True))
        # self.language_widgets[self.sm.get('language', 'C')].show()

    def save_settings(self):
        for key, item in self.language_keys[self.sm.get('language', 'C')].items():
            if value := self.language_widgets[self.sm.get('language', 'C')][key]:
                self.sm.set(item, value)
        for key, item in self.testing_keys.items():
            if value := self.testing_widget[key]:
                self.sm.set(item, value)

    def apply_values(self):
        for key, item in self.language_keys[self.sm.get('language', 'C')].items():
            if value := self.sm.get(item):
                self.language_widgets[self.sm.get('language', 'C')].set_value(key, value)
        for key, item in self.testing_keys.items():
            if value := self.sm.get(item):
                self.testing_widget.set_value(key, value)

    def set_theme(self):
        for el in [self.testing_label, self.compiler_label]:
            self.tm.auto_css(el)
        for el in self.language_widgets.values():
            self.tm.css_to_options_widget(el)
        self.tm.css_to_options_widget(self.testing_widget)
