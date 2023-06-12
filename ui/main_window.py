from sys import argv

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QDialog, QDialogButtonBox, QLabel

from tests.macros_converter import background_process_manager
from ui.themes import ThemeManager
from code_tab.code_widget import CodeWidget
from settings.project_widget import ProjectWidget
from settings.settings_widget import SettingsWidget
from tests.testing_widget import TestingWidget
from tests.tests_widget import TestsWidget
from other.git_widget import GitWidget
from ui.menu_bar import MenuBar
from tests.commands import CommandManager
from other.todo_widget import TODOWidget
from settings.settings_manager import SettingsManager
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
        self.project_widget.jump_to_code.connect(self.jump_to_code_from_project)
        layout.addWidget(self.project_widget)

        self.tests_widget = TestsWidget(self.sm, self.cm, self.tm)
        self.tests_widget.hide()
        layout.addWidget(self.tests_widget)

        self.testing_widget = TestingWidget(self.sm, self.cm, self.tm)
        layout.addWidget(self.testing_widget)
        self.testing_widget.jump_to_code.connect(self.jump_to_code_from_testing)
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

        if not os.path.isdir(self.sm.project) or not self.project_widget.list_widget.count():
            self.show_tab('project_widget')
        else:
            self.show_tab('project_widget')
        if len(argv) == 2 and os.path.isfile(argv[1]):
            if argv[1].endswith('.7z'):
                self.project_widget.project_from_zip(argv[1])
            else:
                self.project_widget.open_as_project(argv[1])
        else:
            self.project_widget.open_project(forced=True)

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

    def jump_to_code_from_project(self, path):
        path = os.path.abspath(path)
        self.show_tab('code_widget')
        if self.sm.get('struct', 0) == 1:
            self.code_widget.files_widget.current_path, name = os.path.split(path)
            self.code_widget.files_widget.update_files_list()
            for i in range(self.code_widget.files_widget.files_list.count()):
                if os.path.basename(self.code_widget.files_widget.files_list.item(i).path) == name:
                    self.code_widget.files_widget.files_list.setCurrentRow(i)
                    break
            return
        if not os.path.isdir(f"{self.sm.app_data_dir}/projects/{self.sm.project}"):
            return
        for dir1 in os.listdir(f"{self.sm.app_data_dir}/projects/{self.sm.project}"):
            if not dir1.isdigit():
                continue
            for dir2 in os.listdir(f"{self.sm.app_data_dir}/projects/{self.sm.project}/{dir1}"):
                for dir3 in os.listdir(f"{self.sm.app_data_dir}/projects/{self.sm.project}/{dir1}/{dir2}"):
                    lab_path = os.path.abspath(self.sm.lab_path(int(dir1), int(dir2), int(dir3)))
                    if path.startswith(lab_path):
                        self.sm.set('lab', int(dir1))
                        self.sm.set('task', int(dir2))
                        self.sm.set('var', int(dir3))
                        self.show_tab('code_widget')
                        self.code_widget.files_widget.current_path, name = os.path.split(path)
                        self.code_widget.files_widget.update_files_list()
                        for i in range(self.code_widget.files_widget.files_list.count()):
                            if os.path.basename(self.code_widget.files_widget.files_list.item(i).path) == name:
                                self.code_widget.files_widget.files_list.setCurrentRow(i)
                                return

    def jump_to_code_from_testing(self, file_name, line, pos):
        self.show_tab('code_widget')
        for i in range(self.code_widget.files_widget.files_list.count()):
            if os.path.basename(self.code_widget.files_widget.files_list.item(i).path) == file_name:
                self.code_widget.files_widget.files_list.setCurrentRow(i)
                self.code_widget.code_edit.setCursorPosition(line, pos)
                break

    def jump_to_code_from_todo(self, file_name, line):
        self.show_tab('code_widget')
        for i in range(self.code_widget.files_widget.files_list.count()):
            if os.path.basename(self.code_widget.files_widget.files_list.item(i).path) == file_name:
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
        if len(background_process_manager.dict):
            dialog = ExitDialog(self.tm)
            background_process_manager.all_finished.connect(dialog.accept)
            if dialog.exec():
                for process in background_process_manager.dict.values():
                    process.close()
                self.project_widget.remove_temp_projects()
                super(MainWindow, self).close()
            else:
                a0.ignore()
                self.project_widget.show()
        else:
            self.project_widget.remove_temp_projects()
            super(MainWindow, self).close()


class ExitDialog(QDialog):
    def __init__(self, tm):
        super(ExitDialog, self).__init__()
        self.tm = tm

        self.setWindowTitle("Выход")

        layout = QVBoxLayout()
        label = QLabel("В данный момент идет сохранение одного или нескольких наборов тестов."
                       "Если вы выйдите из программы, данные будут записаны в рабочую директорию не полностью.")
        label.setWordWrap(True)
        label.setFont(self.tm.font_small)

        QBtn = QDialogButtonBox.Close | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.Close).setStyleSheet(self.tm.buttons_style_sheet)
        self.buttonBox.button(QDialogButtonBox.Close).setFixedSize(80, 24)
        self.buttonBox.button(QDialogButtonBox.Cancel).setStyleSheet(self.tm.buttons_style_sheet)
        self.buttonBox.button(QDialogButtonBox.Cancel).setFixedSize(80, 24)

        layout.addWidget(label)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
