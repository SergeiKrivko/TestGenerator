import os
import sys

from PyQtUIkit.themes import icons
from PyQtUIkit.widgets import *
from qasync import asyncSlot

from src import config
from src.backend.arg_parser import args
from src.backend.managers import BackendManager
from src.backend.notification import notification
from src.ui.main_tabs.code_tab import CodeWidget
from src.ui.main_tabs.testing import TestingWidget
from src.ui.main_tabs.tests import TestsWidget
from src.ui.settings.settings_window import SettingsWindow
from src.ui.side_tabs.builds import BuildWindow
from src.ui.side_tabs.files import FilesWidget
from src.ui.side_tabs.terminal import TerminalTab
from src.ui.side_tabs.tests import TestingPanel
from src.ui.themes import themes
from src.ui.widgets.main_menu import MainMenu
from src.ui.widgets.main_tab import MainTab
from src.ui.widgets.opening_dialog import OpeningDialog
from src.ui.widgets.side_bar import SideBar


class MainWindow(KitMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("TestGenerator")
        self.resize(1100, 700)

        self.bm = BackendManager()
        self.bm.processes.set_win_id(self.winId())

        self.theme_manager.add_icons('assets.icons', 'custom')
        for key, item in themes.items():
            self.theme_manager.add_theme(key, item)
        self.set_theme('dark')

        self._tabs = dict()

        main_layout = KitVBoxLayout()
        self.setCentralWidget(main_layout)

        self.menu_bar = MainMenu(self.bm)
        self.menu_bar.tab_changed.connect(self.show_tab)
        main_layout.addWidget(self.menu_bar)

        main_layout.addWidget(KitHSeparator())

        layout = KitHBoxLayout()
        main_layout.addWidget(layout)

        self.side_bar = SideBar(self.bm)
        layout.addWidget(self.side_bar, 100)

        for key, item in (side_tabs := {
            'files': (FilesWidget(self.bm), 'line-folder', "Файлы"),
            'build': (BuildWindow(self, self.bm), 'line-hammer', "Конфигурации"),
            'tests': (TestingPanel(self.bm), 'line-play', "Тестирование"),
            # 'todo': (TODOPanel(self.sm, self.cm, self.tm), "TODO"),
            # 'git': (GitPanel(self.sm, self.cm, self.tm), "Git"),
            # 'generator': (GeneratorTab(self.sm, self.bm, self.tm), "Генерация тестов"),
            'terminal': (TerminalTab(self.bm), 'custom-terminal', "Терминал"),
            # 'run': (ConsolePanel(self.sm, self.tm, self.bm), "Выполнение"),
        }).items():
            self.side_bar.add_tab(key, *item)

        self._tab_layout = KitHBoxLayout()
        layout.addWidget(self._tab_layout, 1)

        self.code_widget = CodeWidget(self.bm)
        self.add_tab(self.code_widget, 'code', "Код")

        self.tests_widget = TestsWidget(self.bm)
        self.add_tab(self.tests_widget, 'tests', "Тесты")

        self.testing_widget = TestingWidget(self.bm)
        self.add_tab(self.testing_widget, 'testing', "Тестирование")

        # self.unit_testing_widget = UnitTestingWidget(self.sm, self.bm, self.cm, self.tm, self.app)
        # self.add_tab(self.unit_testing_widget, 'unit_tests', 'Модульное тестирование')

        self.settings_widget = SettingsWindow(self, self.bm, side_tabs)
        self.settings_widget.hide()
        self.menu_bar.button_settings.clicked.connect(self.settings_widget.exec)

        # self.testing_widget.ui_disable_func = self.menu_bar.setDisabled
        self.bm.projects.startOpening.connect(self._on_start_opening_project)
        self.bm.projects.startClosing.connect(self._on_start_closing_project)
        self.bm.projects.finishOpening.connect(self._on_finish_opening_project)

        self.bm.showMainTab.connect(self.show_tab)
        self.bm.showSideTab.connect(self.side_bar.select_tab)
        self.bm.mainTabCommand.connect(self.tab_command)
        self.bm.sideTabCommand.connect(self.side_bar.tab_command)
        self.bm.toTopRequired.connect(self.toTop)
        # self.bm.showNotification.connect(self.notification)

        self._current_tab = ''
        self.show_tab('code')
        self._progress_dialog = None

    @asyncSlot()
    async def run(self):
        await self.bm.parse_cmd_args(args)
        await self.bm.poll_shared_files()

    def add_tab(self, widget: MainTab, identifier: str, name: str):
        self._tab_layout.addWidget(widget, 1)
        self._tabs[identifier] = widget
        self.menu_bar.add_tab(identifier, name)
        widget.hide()

    def show_tab(self, tab):
        self._current_tab = tab
        for key, item in self._tabs.items():
            item.hide()
        self._tabs[tab].show()
        self.menu_bar.select_tab(tab, True)

    def tab_command(self, tab, args: tuple, kwargs: dict):
        self._tabs[tab].command(*args, **kwargs)

    def notification(self, title, message):
        flag = False

        def set_flag():
            nonlocal flag
            flag = True

        if not self.isActiveWindow() and self.sm.get_general('notifications', False):
            notification(title, message, on_click=lambda arg: set_flag())
        if flag:
            self.toTop()

    def _on_start_opening_project(self):
        self._progress_dialog = OpeningDialog(self, self.bm)
        self._progress_dialog.show()

    def _on_start_closing_project(self):
        for key, tab in self._tabs.items():
            self.menu_bar.set_tab_hidden(key, tab.need_project)
            if key == self._current_tab and tab.need_project:
                self.show_tab('code')

    def _on_finish_opening_project(self):
        for key, tab in self._tabs.items():
            self.menu_bar.set_tab_hidden(key, tab.need_project and self.bm.projects.light_edit)

    def showEvent(self, a0):
        super().showEvent(a0)
        self.run()

    def closeEvent(self, a0):
        self._close()
        a0.ignore()

    @asyncSlot()
    async def _close(self):
        await self.bm.projects.close()
        sys.exit(0)

