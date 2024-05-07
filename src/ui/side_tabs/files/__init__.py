import os
import platform
import shutil
import subprocess
import typing

import send2trash
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QUrl, QMimeData
from PyQtUIkit.widgets import *

from src.backend.language.icons import FILE_ICONS
from src.backend.language.languages import LANGUAGES
from src.backend.managers import BackendManager
from src.ui.side_tabs.files.open_file_options import get_open_file_options
from src.ui.side_tabs.files.zip_manager import ZipManager
from src.ui.widgets.side_panel_widget import SidePanelWidget, SidePanelButton


class TreeFile(KitTreeWidgetItem):
    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(self.path)
        if '.' not in self.name:
            self.file_type = None
        else:
            self.file_type = self.name[self.name.rindex('.') + 1:]

        super().__init__(self.name, FILE_ICONS.get(self.file_type, 'line-help'))


class TreeDirectory(KitTreeWidgetItem):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.name = os.path.basename(self.path)
        self.file_type = 'directory'
        self.always_expandable = True

        super().__init__(self.name, 'line-folder')

        self.update_files_list()

    def update_files_list(self):
        if not self.expanded():
            self.clear()
            return

        i = 0
        j = 0
        lst = list(filter(lambda p: os.path.isdir(os.path.join(self.path, p)), os.listdir(self.path))) + \
              list(filter(lambda p: os.path.isfile(os.path.join(self.path, p)), os.listdir(self.path)))
        lst = list(map(lambda p: os.path.join(self.path, p), lst))
        while i < self.childrenCount() and j < len(lst):
            if (path := self.child(i).path) != lst[j]:
                if path.startswith(self.path) and (os.path.isfile(path) or os.path.isdir(path)):
                    if os.path.isdir(lst[j]):
                        self.insertItem(i, TreeDirectory(lst[j]))
                    else:
                        self.insertItem(i, TreeFile(lst[j]))
                    i += 1
                    j += 1
                else:
                    self.deleteItem(i)
            elif isinstance(item := self.child(i), TreeDirectory):
                item.update_files_list()
                i += 1
                j += 1
            else:
                i += 1
                j += 1
        while i < self.childrenCount():
            self.deleteItem(i)
        while j < len(lst):
            if os.path.isdir(lst[j]):
                self.addItem(TreeDirectory(lst[j]))
            else:
                self.addItem(TreeFile(lst[j]))
            j += 1

    def expand(self):
        super().expand()
        self.update_files_list()

    def collapse(self):
        super().collapse()
        self.clear()


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
            if platform.system() == 'Windows':
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
            if platform.system() == 'Windows':
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

                    for name, icon, func in language.fast_run:
                        action = self.addAction(name, icon)
                        self.connect_run_action(action, func)
                    return

    def connect_run_action(self, action, func):
        action.triggered.connect(lambda: self.set_action(ContextMenu.RUN_FILE, func))

    def add_open_action(self, name, icon, command):
        self.open_menu.addAction(name).triggered.connect(
            lambda: self.set_action(ContextMenu.OPEN_BY_COMMAND, command))

    def set_action(self, action, data=None):
        self.action = action
        self.action_data = data


class FilesWidget(SidePanelWidget):
    ignore_files = []

    def __init__(self, bm: BackendManager):
        super(FilesWidget, self).__init__(bm, 'Файлы')

        main_layout = KitVBoxLayout()
        main_layout.setSpacing(3)
        self.setWidget(main_layout)

        self.button_add = SidePanelButton('line-add')
        self.button_add.on_click = self.create_file
        self.buttons_layout.addWidget(self.button_add)

        self.button_remove = SidePanelButton('line-trash')
        self.button_remove.on_click = self.delete_file
        self.buttons_layout.addWidget(self.button_remove)

        self.button_rename = SidePanelButton('custom-rename')
        self.button_rename.on_click = lambda: self.rename_file(False)
        self.buttons_layout.addWidget(self.button_rename)

        self.button_update = SidePanelButton('line-refresh')
        self.button_update.on_click = self.update_files_list
        self.buttons_layout.addWidget(self.button_update)

        self.tree = KitTreeWidget()
        self.tree.contextMenuRequested.connect(self.run_context_menu)
        self.tree.movable = True
        self.tree.moveRequested.connect(self.move_file)
        self.root_item = None
        main_layout.addWidget(self.tree)

        self.tree.doubleClicked.connect(self.open_file)

        self.dialog = None
        self.ctrl_pressed = False
        self.shift_pressed = False
        self.bm.projects.finishOpening.connect(self.open_task)

    def update_files_list(self, hard=False):
        path = self.bm.projects.current.path()
        if isinstance(self.root_item, TreeDirectory):
            if hard:
                self.root_item.deleteSelf()
                hard = True
            else:
                self.root_item.update_files_list()
        else:
            hard = True
        if hard:
            self.root_item = TreeDirectory(path)
            self.tree.addItem(self.root_item)

    def move_file(self, item1, item2):
        file = item1.path
        dist = item2.path

        if not os.path.isdir(dist):
            dist = os.path.dirname(dist)
        try:
            os.rename(file, os.path.join(dist, os.path.basename(file)))
        except Exception:
            pass
        self.update_files_list()

    def open_task(self):
        self.update_files_list(hard=True)

    def keyPressEvent(self, a0: typing.Optional[QtGui.QKeyEvent]) -> None:
        match a0.key():
            case Qt.Key.Key_C:
                if self.ctrl_pressed:
                    self.copy_file()
            case Qt.Key.Key_X:
                if self.ctrl_pressed:
                    self.copy_file()
            case Qt.Key.Key_V:
                if self.ctrl_pressed:
                    self.paste_files()
            case Qt.Key.Key_F2:
                self.rename_file()
            case Qt.Key.Key_Control:
                self.ctrl_pressed = True
            case Qt.Key.Key_Shift:
                self.shift_pressed = True
            case Qt.Key.Key_Delete:
                self.delete_file(to_trash=not self.shift_pressed)

    def keyReleaseEvent(self, a0: typing.Optional[QtGui.QKeyEvent]) -> None:
        if a0.key() == Qt.Key.Key_Control:
            self.ctrl_pressed = False
        if a0.key() == Qt.Key.Key_Shift:
            self.shift_pressed = False

    def run_context_menu(self, point, item):
        if item is None:
            file = None
            path = self.bm.projects.current.path()
        elif isinstance(item, TreeDirectory):
            path = item.path
            file = item.path
        elif isinstance(item, TreeFile):
            file = item.path
            path = item.path
        else:
            raise TypeError("invalid item type")

        menu = ContextMenu(self, path, directory=isinstance(item, TreeDirectory))
        menu.move(self.tree.mapToGlobal(point))
        menu.exec()
        match menu.action:
            case ContextMenu.CREATE_DIR:
                self.create_file(directory=True, base_path=path)
            case ContextMenu.CREATE_FILE:
                self.create_file(base_path=path)
            case ContextMenu.CREATE_PY:
                self.create_file(base_path=path, extension='py')
            case ContextMenu.CREATE_C:
                self.create_file(base_path=path, extension='c')
            case ContextMenu.CREATE_H:
                self.create_file(base_path=path, extension='h')
            case ContextMenu.CREATE_MD:
                file = self.create_markdown(base_path=path)
            case ContextMenu.CREATE_T2B:
                self.create_file(base_path=path, extension='t2b')
            case ContextMenu.DELETE_FILE:
                self.delete_file(to_trash=False)
            case ContextMenu.MOVE_TO_TRASH:
                self.delete_file(to_trash=True)
            case ContextMenu.RENAME_FILE:
                self.rename_file()
            case ContextMenu.COMPRESS_TO_ZIP:
                self.compress_files()
            case ContextMenu.OPEN_IN_CODE:
                self.open_file(item)
            case ContextMenu.OPEN_BY_SYSTEM:
                self.open_by_system(file)
            case ContextMenu.OPEN_IN_EXPLORER:
                self.open_by_system(file)
            case ContextMenu.OPEN_BY_SYSTEM_TERMINAL:
                self.open_in_system_terminal(file)
            case ContextMenu.OPEN_BY_POWER_SHELL:
                self.open_in_system_terminal(file, 'PowerShell')
            case ContextMenu.OPEN_BY_WSL_TERMINAL:
                self.open_in_system_terminal(file, 'WSL')
            case ContextMenu.OPEN_BY_COMMAND:
                subprocess.call(menu.action_data)
            case ContextMenu.COPY_FILES:
                self.copy_file()
            case ContextMenu.CUT_FILES:
                self.copy_file()
            case ContextMenu.COPY_PATH:
                self.copy_path()
            case ContextMenu.PASTE_FILES:
                self.paste_files()
            case ContextMenu.RUN_FILE:
                self.fast_run_file(menu.action_data)

    def rename_file(self, flag=True):
        if not isinstance(item := self.tree.currentItem(), (TreeFile, TreeDirectory)):
            return
        dialog = KitFormDialog(self,
                               KitForm.Label(f"Введите новое имя "
                                             f"{'папки' if isinstance(item, TreeDirectory) else 'файла'}:"),
                               KitForm.StrField(default=os.path.basename(item.path)))
        if dialog.exec():
            new_path = os.path.join(os.path.dirname(item.path), dialog.res()[0])
            if os.path.exists(new_path):
                KitDialog.danger(self, "Ошибка", "Такой файл уже существует")
            else:
                os.rename(item.path, new_path)
                self.update_files_list()

    def fast_run_file(self, func):
        item = self.tree.currentItem()
        if isinstance(item, TreeFile) or isinstance(item, TreeDirectory):
            self.bm.side_tab_show('run')
            self.bm.side_tab_command('run', item.path, func)

    def copy_file(self):
        item = self.tree.currentItem()
        if isinstance(item, TreeFile) or isinstance(item, TreeDirectory):
            mime_data = QMimeData()
            mime_data.setUrls([QUrl.fromLocalFile(item.path)])
            KitApplication.clipboard().setMimeData(mime_data)

    def copy_path(self):
        item = self.tree.currentItem()
        if isinstance(item, TreeFile) or isinstance(item, TreeDirectory):
            KitApplication.clipboard().setText(item.path)

    def paste_files(self):
        item = self.tree.currentItem()
        if isinstance(item, TreeFile):
            path = os.path.split(item.path)[0]
        elif isinstance(item, TreeDirectory):
            path = item.path
        else:
            return

        if KitApplication.clipboard().mimeData().hasUrls():
            urls = KitApplication.clipboard().mimeData().urls()
            for url in urls:
                try:
                    shutil.copy(url.toLocalFile(), os.path.join(path, os.path.basename(url.toLocalFile())))
                except FileExistsError:
                    pass
            self.update_files_list()

    def compress_files(self):
        files = []
        for el in self.tree.selectedItems():
            if isinstance(el, (TreeDirectory, TreeFile)):
                files.append(el.path)
        if not files:
            return
        path = files[0][:files[0].rindex('.')] + '.zip'
        path = self.create_file(base_path=os.path.split(path)[0], base_name=os.path.basename(path), extension='zip')
        if path is None:
            return
        ZipManager.compress(path, files)
        self.update_files_list()

    @staticmethod
    def open_by_system(path):
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(path)
        else:  # linux variants
            subprocess.call(('xdg-open', path))

    @staticmethod
    def open_in_explorer(path):
        match platform.system():
            case 'Windows':
                subprocess.call(['explorer', path])
            case 'Linux':
                subprocess.call(['nautilus', '--browser', path])
            case 'Darwin':
                subprocess.call(['open', path])

    @staticmethod
    def open_in_system_terminal(path, terminal=''):
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        match platform.system():
            case 'Windows':
                match terminal:
                    case 'PowerShell':
                        os.system(f"start powershell.exe -noexit -command Set-Location -literalPath \"{path}\"")
                    case 'WSL':
                        os.system(f"start wsl.exe --cd \"{path}\"")
                    case _:
                        os.system(f"start cmd.exe /s /k pushd \"{path}\"")
            case 'Linux':
                os.system(f"gnome-terminal --working-directory \"{path}\"")
            case 'Darwin':
                os.system(f"open -a Terminal \"{path}\"")

    def create_directory(self):
        self.create_file(directory=True)

    def create_file(self, directory=False, base_path=None, base_name='', extension=''):
        if base_path is None:
            base_path = self.bm.projects.current.path()
        elif os.path.isfile(base_path):
            base_path = os.path.dirname(base_path)
        dialog = KitFormDialog(self,
                               KitForm.Label(f"Введите имя {'папки' if directory else 'файла'}:"),
                               KitForm.StrField())
        if dialog.exec():
            if not dialog.res()[0]:
                KitDialog.danger(self, "Ошибка",
                                 f"Невозможно создать {'директорию' if directory else 'файл'}: имя не задано")
                return
            try:
                path = os.path.join(base_path, dialog.res()[0])
                if extension and not path.endswith('.' + extension):
                    path += '.' + extension
                if directory:
                    os.makedirs(path)
                else:
                    os.makedirs(self.bm.projects.current.path(), exist_ok=True)
                    open(path, 'x').close()
            except FileExistsError:
                KitDialog.danger(self, "Ошибка",
                                 f"Невозможно создать {'директорию' if directory else 'файл'}: "
                                 f"{'директория' if directory else 'файл'} с таким именем уже существует")
            except PermissionError:
                KitDialog.danger(self, "Ошибка",
                                 f"Невозможно создать {'директорию' if directory else 'файл'}: недостаточно прав")
            except Exception as ex:
                KitDialog.danger(self, "Ошибка",
                                 f"Невозможно создать {'директорию' if directory else 'файл'}: {ex.__class__.__name__}: {ex}")
            else:
                self.update_files_list()
                return path

    def create_markdown(self, base_path=None):
        extension = 'md'
        if base_path is None:
            base_path = self.bm.projects.current.path()
        elif os.path.isfile(base_path):
            base_path = os.path.dirname(base_path)

        dialog = KitFormDialog(self,
                               KitForm.Label(f"Введите имя 'файла:"),
                               KitForm.StrField(),
                               KitForm.ComboField('', ['Пустой файл', 'Описание проекта', 'Отчет']))
        if dialog.exec():
            if not dialog.res()[0]:
                KitDialog.danger(self, "Ошибка",
                                 f"Невозможно создать файл: имя файла не задано")
                return
            try:
                path = os.path.join(base_path, dialog.res()[0])
                if extension and not path.endswith('.' + extension):
                    path += '.' + extension
                os.makedirs(self.bm.projects.current.path(), exist_ok=True)
                open(path, 'x').close()
            except FileExistsError:
                KitDialog.danger(self, "Ошибка", f"Невозможно создать файл: файл с таким именем уже существует")
            except PermissionError:
                KitDialog.danger(self, "Ошибка", f"Невозможно создать файл: недостаточно прав")
            except Exception as ex:
                KitDialog.danger(self, "Ошибка", f"Невозможно создать файл: {ex.__class__.__name__}: {ex}")
            else:
                self.update_files_list()
                return path

    def delete_file(self, to_trash=True):
        item = self.tree.currentItem()
        if not isinstance(item, (TreeFile, TreeDirectory)):
            return

        if to_trash:
            try:
                send2trash.send2trash([item.path for item in self.tree.selectedItems()])
            except FileExistsError:
                pass
            except Exception as ex:
                KitDialog.danger(self, "Ошибка", f"{ex.__class__.__name__}: {ex}")
        else:
            if KitDialog.question(self, f"Вы уверены, что хотите удалить файл {self.tree.currentItem().name}?",
                                  ('Нет', 'Да')) == 'Да':
                if os.path.isdir(item.path):
                    shutil.rmtree(item.path)
                else:
                    os.remove(item.path)
        self.update_files_list()

    def open_file(self, item):
        if isinstance(item, (TreeFile, TreeDirectory)):
            if item.file_type != 'directory':
                self.bm.main_tab_show('code')
                self.bm.main_tab_command('code', item.path)
