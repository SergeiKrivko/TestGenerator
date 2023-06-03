from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget

from settings.lib_dialog import LibWidget
from widgets.options_window import OptionsWidget

line_sep = {'\n': 'LF (\\n)', '\r\n': 'CRLF (\\r\\n)', '\r': 'CR (\\r)'}
line_sep_reverse = {'LF (\\n)': '\n', 'CRLF (\\r\\n)': '\r\n', 'CR (\\r)': '\r'}


class SettingsWidget(QWidget):
    change_theme = pyqtSignal()

    def __init__(self, sm, tm):
        super(SettingsWidget, self).__init__()
        self.sm = sm
        self.tm = tm

        layout = QHBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.addItems(['Основные', 'Тестирование', 'Библиотеки'])
        self.list_widget.setFixedWidth(175)
        self.list_widget.currentItemChanged.connect(self.select_tab)
        layout.addWidget(self.list_widget)

        self.main_options_widget = OptionsWidget({
            "Символ переноса строки: ": {'type': 'combo', 'values': line_sep.values(), 'name': OptionsWidget.NAME_LEFT,
                                         'initial': list(line_sep.keys()).index(self.sm.get_general('line_sep', '\n'))},
            "Тема:": {'type': 'combo', 'values': list(self.tm.themes.keys()), 'name': OptionsWidget.NAME_LEFT,
                      'initial': list(self.tm.themes.keys()).index(self.tm.theme_name)},
            "Python": {'type': str, 'initial': self.sm.get_general('python', 'python3'), 'width': 250}
        }, margins=(20, 20, 20, 20))
        self.main_options_widget.clicked.connect(self.save_main_settings)
        layout.addWidget(self.main_options_widget)

        self.testing_widget = OptionsWidget({
            "Компилятор": {'type': str, 'width': 400, 'initial': self.sm.get_general('compiler', 'gcc')},
            "Ключ -lm": {'type': bool, 'name': OptionsWidget.NAME_RIGHT,
                         'initial': bool(self.sm.get_general('-lm', True))},
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

        self.setLayout(layout)

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        self.list_widget.setStyleSheet(self.tm.list_widget_style_sheet)
        self.tm.set_theme_to_list_widget(self.list_widget, self.tm.font_medium)
        self.main_options_widget.setFont(self.tm.font_small)
        self.testing_widget.setFont(self.tm.font_small)
        self.main_options_widget.widgets['Символ переноса строки: '].setStyleSheet(self.tm.combo_box_style_sheet)
        self.main_options_widget.widgets['Тема:'].setStyleSheet(self.tm.combo_box_style_sheet)
        self.main_options_widget.widgets['Python'].setStyleSheet(self.tm.style_sheet)
        self.testing_widget.widgets['Компилятор'].setStyleSheet(self.tm.style_sheet)
        self.testing_widget.widgets['Компаратор для позитивных тестов:'].setStyleSheet(self.tm.combo_box_style_sheet)
        self.testing_widget.widgets['Компаратор для негативных тестов:'].setStyleSheet(self.tm.combo_box_style_sheet)
        self.testing_widget.widgets['Погрешность сравнения чисел:'].setStyleSheet(self.tm.double_spin_box_style_sheet)
        self.testing_widget.widgets['Подстрока для позитивных тестов'].setStyleSheet(self.tm.style_sheet)
        self.testing_widget.widgets['Подстрока для негативных тестов'].setStyleSheet(self.tm.style_sheet)
        self.testing_widget.widgets['Ограничение по времени:'].setStyleSheet(self.tm.double_spin_box_style_sheet)
        self.libs_widget.set_theme()

    def save_main_settings(self):
        dct = self.main_options_widget.values
        self.sm.set_general('line_sep', list(line_sep.keys())[dct['Символ переноса строки: ']])
        self.sm.set_general('theme', th := list(self.tm.themes.keys())[dct['Тема:']])
        self.tm.set_theme(th)
        self.change_theme.emit()
        self.sm.set_general('python', dct['Python'])

    def save_testing_settings(self):
        dct = self.testing_widget.values
        self.sm.set_general('compiler', dct['Компилятор'])
        self.sm.set_general('-lm', int(dct['Ключ -lm']))
        self.sm.set_general('pos_comparator', dct['Компаратор для позитивных тестов:'])
        self.sm.set_general('neg_comparator', dct['Компаратор для негативных тестов:'])
        self.sm.set_general('memory_testing', int(dct['Тестирование по памяти']))
        self.sm.set_general('coverage', int(dct['Coverage']))
        self.sm.set_general('epsilon', dct['Погрешность сравнения чисел:'])
        self.sm.set_general('pos_substring', dct['Подстрока для позитивных тестов'])
        self.sm.set_general('neg_substring', dct['Подстрока для негативных тестов'])
        self.sm.set_general('time_limit', dct['Ограничение по времени:'])

    def hide(self, save_settings=True):
        if not self.isHidden() and save_settings:
            self.save_main_settings()
            self.save_testing_settings()
        super(SettingsWidget, self).hide()

    def select_tab(self, item):
        if item is not None:
            self.main_options_widget.hide()
            self.testing_widget.hide()
            self.libs_widget.hide()
            tab = item.text()
            if tab == 'Основные':
                self.main_options_widget.show()
            if tab == 'Тестирование':
                self.testing_widget.show()
            if tab == 'Библиотеки':
                self.libs_widget.show()
