from sys import argv

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QDialog, QDialogButtonBox, QLabel, QHBoxLayout

from tests.macros_converter import background_process_manager
from ui.main_menu import MainMenu
from ui.side_bar import SideBar, SidePanel
from ui.themes import ThemeManager
from code_tab.code_widget import CodeWidget
from settings.project_widget import ProjectWidget
from settings.settings_widget import SettingsWidget
from tests.testing_widget import TestingWidget
from tests.tests_widget import TestsWidget
from other.git_widget import GitWidget
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
        self.setMinimumSize(800, 360)

        self.sm = SettingsManager()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.cm = CommandManager(self.sm)
        self.tm = ThemeManager(self.sm, self.sm.get_general('theme'))

        self.menu_bar = MainMenu(self.sm, self.tm)
        self.menu_bar.tab_changed.connect(self.show_tab)
        main_layout.addWidget(self.menu_bar)

        layout = QHBoxLayout()
        main_layout.addLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(main_layout)

        self.side_panel = SidePanel(self.sm, self.tm, self.cm)
        self.side_bar = SideBar(self.sm, self.tm, self.side_panel)
        layout.addWidget(self.side_bar)
        layout.addWidget(self.side_panel)

        self.project_widget = ProjectWidget(self.sm, self.tm, self.menu_bar.setDisabled)
        self.project_widget.hide()
        self.project_widget.jump_to_code.connect(self.jump_to_code_from_project)

        self.tests_widget = TestsWidget(self.sm, self.cm, self.tm)
        self.tests_widget.hide()
        layout.addWidget(self.tests_widget, 100)

        self.testing_widget = TestingWidget(self.sm, self.cm, self.tm, self.side_panel)
        layout.addWidget(self.testing_widget, 100)
        self.testing_widget.jump_to_code.connect(self.jump_to_code_from_testing)
        self.testing_widget.hide()
        self.side_panel.tabs['tests'].buttons['run'].clicked.connect(self.testing_widget.button_pressed)
        self.side_panel.tabs['tests'].jump_to_testing.connect(lambda *args: self.show_tab(MainMenu.TAB_TESTING))

        self.code_widget = CodeWidget(self.sm, self.cm, self.tm, self.side_panel)
        layout.addWidget(self.code_widget, 100)
        self.code_widget.testing_signal.connect(self.testing_widget.testing)
        self.code_widget.hide()

        self.git_widget = GitWidget(self.sm, self.cm, self.tm)
        self.git_widget.hide()

        self.todo_widget = TODOWidget(self.sm, self.cm, self.tm)
        self.todo_widget.jumpToCode.connect(self.jump_to_code_from_todo)
        self.todo_widget.hide(save_data=False)

        self.settings_widget = SettingsWidget(self.sm, self.tm)
        self.settings_widget.change_theme.connect(self.set_theme)
        self.settings_widget.hide(save_settings=False)

        self.testing_widget.ui_disable_func = self.menu_bar.setDisabled

        self.resize(1000, 600)

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

        self.show_tab(MainMenu.TAB_CODE)

    def set_theme(self):
        self.central_widget.setStyleSheet(self.tm.bg_style_sheet)
        self.project_widget.set_theme()
        self.tests_widget.set_theme()
        self.code_widget.set_theme()
        self.testing_widget.set_theme()
        self.todo_widget.set_theme()
        self.git_widget.set_theme()
        self.settings_widget.set_theme()
        self.menu_bar.set_theme()
        self.side_bar.set_theme()
        self.side_panel.set_theme()

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

    def show_tab(self, index):
        self.code_widget.hide()
        self.tests_widget.hide()
        self.testing_widget.hide()
        if index == MainMenu.TAB_CODE:
            self.code_widget.show()
            self.menu_bar.button_code.setChecked(True)
        else:
            self.menu_bar.button_code.setChecked(False)
        if index == MainMenu.TAB_TESTS:
            self.tests_widget.show()
            self.menu_bar.button_tests.setChecked(True)
        else:
            self.menu_bar.button_tests.setChecked(False)
        if index == MainMenu.TAB_TESTING:
            self.testing_widget.show()
            self.menu_bar.button_testing.setChecked(True)
        else:
            self.menu_bar.button_testing.setChecked(False)

    def open_test_from_code(self):
        index = 0
        self.testing_widget.get_path()
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
        self.buttonBox.button(QDialogButtonBox.Close).setStyleSheet(self.tm.button_css())
        self.buttonBox.button(QDialogButtonBox.Close).setFixedSize(80, 24)
        self.buttonBox.button(QDialogButtonBox.Cancel).setStyleSheet(self.tm.button_css())
        self.buttonBox.button(QDialogButtonBox.Cancel).setFixedSize(80, 24)

        layout.addWidget(label)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
