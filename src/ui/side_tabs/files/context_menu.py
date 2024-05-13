from sys import platform

from PyQtUIkit.widgets import KitMenu

from src.backend.language.languages import LANGUAGES
from src.ui.side_tabs.files.open_file_options import get_open_file_options


class ContextMenu(KitMenu):
    CREATE_FILE = 0
    CREATE_DIR = 1
    CREATE_PY = 2
    CREATE_C = 3
    CREATE_H = 4
    CREATE_MD = 5
    CREATE_T2B = 6

    DELETE_FILE = 100
    RENAME_FILE = 101
    OPEN_IN_CODE = 102
    OPEN_BY_SYSTEM = 103
    OPEN_IN_TERMINAL = 104
    OPEN_BY_SYSTEM_TERMINAL = 105
    OPEN_IN_EXPLORER = 106
    OPEN_BY_COMMAND = 107
    MOVE_TO_TRASH = 108
    RUN_FILE = 109
    COMPRESS_TO_ZIP = 110
    OPEN_BY_POWER_SHELL = 111
    OPEN_BY_WSL_TERMINAL = 112

    COPY_FILES = 200
    PASTE_FILES = 201
    CUT_FILES = 202
    COPY_PATH = 203

    def __init__(self, parent, path, directory=False):
        super().__init__(parent)

        self.setContentsMargins(3, 3, 3, 3)
        self.setMinimumWidth(150)

        self.create_menu = self.addMenu("Создать", 'line-add')

        self.create_menu.addAction("Файл", 'custom-text').triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_FILE))
        self.create_menu.addAction("Папку", 'line-folder').triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_DIR))
        self.create_menu.addAction("Python file", 'solid-logo-python').triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_PY))
        self.create_menu.addAction("C source file", 'custom-c').triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_C))
        self.create_menu.addAction("Header file", 'custom-header').triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_H))
        self.create_menu.addAction("Markdown file", 'custom-markdown').triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_MD))
        self.create_menu.addAction("Text-to-Binary file", 'custom-t2b').triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_T2B))

        self.addSeparator()

        self.addAction("Вырезать", 'line-cut').triggered.connect(
            lambda: self.set_action(ContextMenu.CUT_FILES))
        self.addAction("Копировать", 'line-copy').triggered.connect(
            lambda: self.set_action(ContextMenu.COPY_FILES))
        self.addAction("Копировать как путь", 'custom-path').triggered.connect(
            lambda: self.set_action(ContextMenu.COPY_PATH))
        self.addAction("Вставить", 'line-clipboard').triggered.connect(
            lambda: self.set_action(ContextMenu.PASTE_FILES))

        self.addSeparator()

        self.add_fast_run_actions(path)

        self.addSeparator()

        self.addAction("Удалить", 'line-trash').triggered.connect(
            lambda: self.set_action(ContextMenu.DELETE_FILE))
        self.addAction("Переместить в корзину", 'solid-trash').triggered.connect(
            lambda: self.set_action(ContextMenu.MOVE_TO_TRASH))
        self.addAction("Переименовать", 'custom-rename').triggered.connect(
            lambda: self.set_action(ContextMenu.RENAME_FILE))
        self.addAction("Сжать в ZIP", 'custom-zip').triggered.connect(
            lambda: self.set_action(ContextMenu.COMPRESS_TO_ZIP))

        self.addSeparator()

        self.open_menu = self.addMenu("Открыть")
        if directory:
            self.open_menu.addAction("Проводник", 'line-folder').triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_IN_EXPLORER))
            self.open_menu.addAction("Вкладка \"Терминал\"", 'custom-terminal').triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_IN_TERMINAL))
            if platform == 'win32':
                self.open_menu.addAction("PowerShell", 'custom-terminal').triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_POWER_SHELL))
                self.open_menu.addAction("Командная строка", 'custom-terminal').triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_SYSTEM_TERMINAL))
                self.open_menu.addAction("Терминал WSL", 'custom-terminal').triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_WSL_TERMINAL))
            else:
                self.open_menu.addAction("Терминал", 'custom-terminal').triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_SYSTEM_TERMINAL))
        else:
            self.open_menu.addAction("Вкладка \"Код\"").triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_IN_CODE))
            self.open_menu.addAction("Стандартное приложение").triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_BY_SYSTEM))
            if platform == 'win32':
                self.open_menu.addAction("PowerShell", 'custom-terminal').triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_POWER_SHELL))
                self.open_menu.addAction("Командная строка", 'custom-terminal').triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_SYSTEM_TERMINAL))
                self.open_menu.addAction("Терминал WSL", 'custom-terminal').triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_WSL_TERMINAL))
            else:
                self.open_menu.addAction("Терминал", 'custom-terminal').triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_SYSTEM_TERMINAL))

            # self.open_menu.addSeparator()

            if '.' in path:
                for prog_name, prog_icon, prog_command in get_open_file_options(path):
                    self.add_open_action(prog_name, prog_icon, prog_command)

        self.action = None
        self.action_data = None

    def add_fast_run_actions(self, path):
        for language in LANGUAGES.values():
            for el in language.extensions:
                if path.endswith(el):

                    for option in language.fast_run:
                        action = self.addAction(option.name, option.icon)
                        action.triggered.connect(lambda x, op=option: self.set_action(ContextMenu.RUN_FILE, op))
                    return

    def add_open_action(self, name, icon, command):
        self.open_menu.addAction(name).triggered.connect(
            lambda: self.set_action(ContextMenu.OPEN_BY_COMMAND, command))

    def set_action(self, action, data=None):
        self.action = action
        self.action_data = data
