from PyQt5.QtWidgets import QTabWidget

from settings.project_struct_widget import ProjectStructWidget
from settings.testing_settings_widget import TestingSettingsWidget
from ui.options_window import OptionsWidget


LANGUAGES = ['C', 'Python']


class ProjectSettingsWidget(QTabWidget):
    def __init__(self, sm, tm):
        super().__init__()
        self.sm = sm
        self.tm = tm

        self.main_settings_widget = OptionsWidget({
            "Папка проекта:": {'type': 'file', 'mode': 'dir', 'width': 400, 'initial': ''},
            'Язык': {'type': 'combo', 'name': OptionsWidget.NAME_LEFT, 'values': LANGUAGES}
        }, margins=(25, 25, 25, 25))
        self.main_settings_widget.clicked.connect(self.save_settings)
        self.addTab(self.main_settings_widget, 'Основные')

        self.struct_settings_widget = ProjectStructWidget(self.sm, self.tm)
        self.addTab(self.struct_settings_widget, 'Структура проекта')

        self.testing_settings_widget = TestingSettingsWidget(self.sm, self.tm)
        self.addTab(self.testing_settings_widget, 'Тестирование')

        self.sm.project_changed.connect(self.open_project)
        self.opening_project = False

    def open_project(self):
        self.opening_project = True

        self.testing_settings_widget.open()

        self.main_settings_widget.widgets['Папка проекта:'].set_path(self.sm.path)
        self.main_settings_widget.widgets['Язык'].setCurrentText(str(self.sm.get('language', 'C')))

        self.struct_settings_widget.apply_values()

        self.opening_project = False

    def save_settings(self):
        if self.opening_project:
            return

        dct = self.main_settings_widget.values
        self.sm.set('language', LANGUAGES[dct['Язык']])

    def set_theme(self):
        self.tm.auto_css(self)
        self.tm.css_to_options_widget(self.main_settings_widget)
        self.testing_settings_widget.set_theme()
        self.struct_settings_widget.set_theme()

