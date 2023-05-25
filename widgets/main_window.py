from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from other.themes import ThemeManager
from widgets.code_widget import CodeWidget
from widgets.project_widget import ProjectWidget
from widgets.settings_widget import SettingsWidget
from widgets.testing_widget import TestingWidget
from widgets.tests_widget import TestsWidget
from widgets.git_widget import GitWidget
from widgets.menu_bar import MenuBar
from other.commands import CommandManager
from widgets.todo_widget import TODOWidget
from other.settings_manager import SettingsManager
import os

line_sep = {'\n': 'LF (\\n)', '\r\n': 'CRLF (\\r\\n)', '\r': 'CR (\\r)'}
line_sep_reverse = {'LF (\\n)': '\n', 'CRLF (\\r\\n)': '\r\n', 'CR (\\r)': '\r'}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("TestGenerator")

        self.sm = SettingsManager()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(layout)

        self.cm = CommandManager(self.sm)
        self.tm = ThemeManager(self.sm.get_general('theme'))

        self.menu_bar = MenuBar({
            'Проект': (lambda: self.show_tab('project_widget'), None),
            'Код': (lambda: self.show_tab('code_widget'), None),
            'Тесты': (lambda: self.show_tab('tests_widget'), None),
            'Тестирование': (lambda: self.show_tab('testing_widget'), None),
            'TODO': (lambda: self.show_tab('todo_widget'), None),
            'Git': (lambda: self.show_tab('git_widget'), None),
            'Настройки': (lambda: self.show_tab('settings_widget'), None)
        })
        self.setMenuBar(self.menu_bar)

        self.project_widget = ProjectWidget(self.sm, self.tm, self.menu_bar.setDisabled)
        self.project_widget.hide()
        layout.addWidget(self.project_widget)

        self.tests_widget = TestsWidget(self.sm, self.cm, self.tm)
        self.tests_widget.hide()
        layout.addWidget(self.tests_widget)

        self.testing_widget = TestingWidget(self.sm, self.cm, self.tm)
        layout.addWidget(self.testing_widget)
        self.testing_widget.hide()

        self.code_widget = CodeWidget(self.sm, self.cm, self.tm)
        layout.addWidget(self.code_widget)
        self.testing_widget.testing_start.connect(self.code_widget.testing_start)
        self.testing_widget.add_test.connect(self.code_widget.add_test)
        self.testing_widget.testing_end.connect(self.code_widget.end_testing)
        self.code_widget.testing_signal.connect(self.testing_widget.testing)
        self.code_widget.test_res_widget.doubleClicked.connect(self.open_test_from_code)
        self.code_widget.hide()

        self.git_widget = GitWidget(self.sm, self.cm, self.tm)
        layout.addWidget(self.git_widget)
        self.git_widget.hide()

        self.todo_widget = TODOWidget(self.sm, self.cm, self.tm)
        layout.addWidget(self.todo_widget)
        self.todo_widget.jumpToCode.connect(self.jump_to_code_from_todo)
        self.todo_widget.hide(save_data=False)

        self.settings_widget = SettingsWidget(self.sm, self.tm)
        layout.addWidget(self.settings_widget)
        self.settings_widget.change_theme.connect(self.set_theme)
        self.settings_widget.hide(save_settings=False)

        self.testing_widget.ui_disable_func = self.menu_bar.setDisabled

        self.resize(800, 600)

        if not os.path.isdir(self.sm.get_general('__project__', '')) or not self.project_widget.list_widget.count():
            self.show_tab('project_widget')
            self.menu_bar.setDisabled(True)
        else:
            self.show_tab('project_widget')

    def set_theme(self):
        self.central_widget.setStyleSheet(self.tm.bg_style_sheet)
        self.menu_bar.setStyleSheet(self.tm.bg_style_sheet)
        self.project_widget.set_theme()
        self.tests_widget.set_theme()
        self.code_widget.set_theme()
        self.testing_widget.set_theme()
        self.todo_widget.set_theme()
        self.git_widget.set_theme()
        self.settings_widget.set_theme()
        self.menu_bar.setFont(self.tm.font_small)
        self.menu_bar.setStyleSheet(f"""
        QMenuBar {{
        color: {self.tm['TextColor']};
        background-color: {self.tm['BgColor']};
        }}
        QMenuBar::item::selected {{
        background-color: {self.tm['MainColor']};
        }}
        """)

    def jump_to_code_from_todo(self, file_name, line):
        self.show_tab('code_widget')
        for i in range(self.code_widget.files_widget.files_list.count()):
            if self.code_widget.files_widget.files_list.item(i).text() == file_name:
                self.code_widget.files_widget.files_list.setCurrentRow(i)
                self.code_widget.code_edit.setCursorPosition(line, 0)
                break

    def show_tab(self, tab):
        self.project_widget.hide()
        self.code_widget.hide()
        self.tests_widget.hide()
        self.testing_widget.hide()
        self.todo_widget.hide()
        self.git_widget.hide()
        self.settings_widget.hide()
        try:
            self.__dict__[tab].show()
        except KeyError:
            self.project_widget.show()

    def open_test_from_code(self):
        index = self.code_widget.test_res_widget.currentRow()
        self.testing_widget.get_path(True)
        self.testing_widget.tests_list.setCurrentRow(index)
        self.testing_widget.open_test_info()
        self.show_tab('testing_widget')

    def closeEvent(self, a0):
        self.project_widget.hide()
        self.todo_widget.hide()
        self.code_widget.hide()
        self.tests_widget.hide()
        self.testing_widget.hide()
        self.git_widget.hide()
        self.settings_widget.hide()
        self.sm.store()
        super(MainWindow, self).close()
