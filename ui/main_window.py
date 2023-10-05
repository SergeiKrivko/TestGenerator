from sys import argv
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QDialog, QDialogButtonBox, QLabel, QHBoxLayout

from backend.backend_manager import BackendManager
from other.report.report_window import ReportWindow
from side_tabs.builds import BuildWindow
from side_tabs.console import ConsolePanel
from side_tabs.files.files_widget import FilesWidget
from side_tabs.terminal_tab import TerminalTab
from side_tabs.builds.build_panel import BuildPanel
from other.chat_widget import ChatPanel
from side_tabs.git.git_panel import GitPanel
from side_tabs.telegram.telegram_widget import TelegramWidget
from side_tabs.todo_panel import TODOPanel
from side_tabs.projects.project_widget import ProjectWidget
from main_tabs.tests.generator_window import GeneratorTab
from side_tabs.tests.testing_panel import TestingPanel
from ui.main_menu import MainMenu
from ui.main_tab import MainTab
from ui.progress_dialog import ProgressDialog
from ui.side_bar import SideBar, SidePanel
from ui.themes import ThemeManager
from main_tabs.code_tab.code_widget import CodeWidget
from settings.settings_window import SettingsWindow
from main_tabs.testing import TestingWidget
from main_tabs.tests import TestsWidget
from main_tabs.tests.commands import CommandManager

from main_tabs.unit_testing.unit_testing_widget import UnitTestingWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("TestGenerator")
        self.setMinimumSize(800, 360)

        self.setWindowFlags(Qt.CustomizeWindowHint)

        self.bm = BackendManager()
        self.sm = self.bm.sm
        self.cm = CommandManager(self.sm)
        self.tm = ThemeManager(self.sm, self.sm.get_general('theme'))

        self._tabs = dict()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.menu_bar = MainMenu(self.sm, self.bm, self.tm)
        self.menu_bar.tab_changed.connect(self.show_tab)
        self.menu_bar.closeButtonClicked.connect(self.close)
        self.menu_bar.moveWindow.connect(lambda point: self.move(self.pos() + point))
        self.menu_bar.minimize.connect(lambda: self.setWindowState(Qt.WindowState.WindowNoState))
        self.menu_bar.maximize.connect(lambda: self.setWindowState(Qt.WindowState.WindowMaximized))
        self.menu_bar.hideWindow.connect(lambda: self.setWindowState(Qt.WindowState.WindowMinimized))
        main_layout.addWidget(self.menu_bar)

        self._layout = QHBoxLayout()
        main_layout.addLayout(self._layout)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(main_layout)

        self.side_panel = SidePanel(self.sm, self.bm, self.tm, self.cm)
        self.side_bar = SideBar(self.sm, self.tm, self.side_panel)
        self._layout.addWidget(self.side_bar)
        self._layout.addWidget(self.side_panel, 100)

        for key, item in {
            'projects': ProjectWidget(self.sm, self.bm, self.tm),
            'files': FilesWidget(self.sm, self.bm, self.tm),
            'build': BuildWindow(self.bm, self.sm, self.tm),
            'tests': TestingPanel(self.sm, self.bm, self.tm),
            'todo': TODOPanel(self.sm, self.cm, self.tm),
            'git': GitPanel(self.sm, self.cm, self.tm),
            'generator': GeneratorTab(self.sm, self.cm, self.tm),
            'terminal': TerminalTab(self.sm, self.tm),
            'run': ConsolePanel(self.sm, self.tm, self.cm),
            'chat': ChatPanel(self.sm, self.tm),
            'telegram': TelegramWidget(self.sm, self.tm),
            'document': ReportWindow(self.bm, self.sm, self.tm)
        }.items():
            self.side_bar.add_tab(item, key)

        self.code_widget = CodeWidget(self.sm, self.bm, self.tm)
        self.add_tab(self.code_widget, 'code', "Код")

        self.tests_widget = TestsWidget(self.sm, self.bm, self.tm)
        self.add_tab(self.tests_widget, 'tests', "Тесты")

        self.testing_widget = TestingWidget(self.sm, self.bm, self.tm)
        self.add_tab(self.testing_widget, 'testing', "Тестирование")
        # self.testing_widget.showTab.connect(lambda: self.side_bar.select_tab('tests'))
        # self.testing_widget.startTesting.connect(self.tests_widget.save_tests)
        # self.side_panel.tabs['tests'].buttons['run'].clicked.connect(self.testing_widget.button_pressed)
        # self.side_panel.tabs['tests'].buttons['cancel'].clicked.connect(self.testing_widget.button_pressed)
        # self.side_panel.tabs['tests'].jump_to_testing.connect(
        #     lambda index, show_tab: None if not show_tab else self.show_tab(MainMenu.TAB_TESTING))

        self.unit_testing_widget = UnitTestingWidget(self.sm, self.bm, self.cm, self.tm)
        self.add_tab(self.unit_testing_widget, 'unit_tests', 'Модульное тестирование')

        self.settings_widget = SettingsWindow(self.sm, self.tm)
        self.settings_widget.change_theme.connect(self.set_theme)
        self.settings_widget.hide()
        self.menu_bar.button_settings.clicked.connect(self.settings_widget.exec)

        self.testing_widget.ui_disable_func = self.menu_bar.setDisabled
        self.bm.loadingStart.connect(lambda pr: ProgressDialog(self.bm, self.tm, pr).exec())
        self.bm.showMainTab.connect(self.show_tab)
        self.bm.showSideTab.connect(self.side_bar.select_tab)
        self.bm.mainTabCommand.connect(self.tab_command)
        self.bm.sideTabCommand.connect(self.side_panel.tab_command)

        self.resize(1100, 700)

        if len(argv) == 2 and os.path.isfile(argv[1]):
            if argv[1].endswith('.7z'):
                self.side_panel.tabs['projects'].project_from_zip(argv[1])
            else:
                self.side_panel.tabs['projects'].open_as_project(argv[1])
        else:
            self.side_panel.tabs['projects'].open_project(forced=True)

        # self.sm.finish_change_task()
        self.show_tab('code')

        self.bm.open_main_project(self.sm.get_general('project'))

    def add_tab(self, widget: MainTab, identifier: str, name: str):
        self._layout.addWidget(widget, 1)
        self._tabs[identifier] = widget
        self.menu_bar.add_tab(identifier, name)
        widget.hide()

    def set_theme(self):
        self.tm.set_theme(self.sm.get_general('theme', 'basic'))
        self.central_widget.setStyleSheet(self.tm.bg_style_sheet)
        self.tests_widget.set_theme()
        self.code_widget.set_theme()
        self.testing_widget.set_theme()
        self.settings_widget.set_theme()
        self.menu_bar.set_theme()
        self.side_bar.set_theme()
        self.side_panel.set_theme()
        self.unit_testing_widget.set_theme()

    def show_tab(self, tab):
        for key, item in self._tabs.items():
            if key == tab:
                item.show()
            else:
                item.hide()
        self.menu_bar.select_tab(tab, True)

    def tab_command(self, tab, args: tuple, kwargs: dict):
        self._tabs[tab].command(*args, **kwargs)

    def closeEvent(self, a0):
        self.bm.close_project()
        self.sm.store()
        if not self.bm.all_finished():
            dialog = ExitDialog(self.tm)
            self.bm.allProcessFinished.connect(dialog.accept)
            if dialog.exec():
                self.bm.terminate_all()
                self.side_panel.finish_work()
                super(MainWindow, self).close()
            else:
                a0.ignore()
        else:
            self.side_panel.finish_work()
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
        label.setFont(self.tm.font_medium)

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
