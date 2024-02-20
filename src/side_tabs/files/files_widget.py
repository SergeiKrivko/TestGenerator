import os
import platform
import shutil
import subprocess
import typing

from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal, Qt, QUrl, QMimeData
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLineEdit, \
    QPushButton, QLabel, QListWidgetItem, QTreeWidget, QTreeWidgetItem, QMenu, QWidget, QApplication
import send2trash

from src.language.languages import languages
from src.other.report.markdown_patterns import MarkdownPatternsDialog
from src.side_tabs.files.open_file_options import get_open_file_options
from src.side_tabs.files.zip_manager import ZipManager
from src.ui.custom_dialog import CustomDialog
from src.ui.message_box import MessageBox
from src.ui.side_panel_widget import SidePanelWidget
from src.backend.managers import BackendManager


class TreeFile(QTreeWidgetItem):
    def __init__(self, path: str, tm):
        self.tm = tm
        self.path = path
        self.name = os.path.basename(self.path)
        if '.' not in self.name:
            self.file_type = 'icons/unknown_file'
        else:
            self.file_type = self.name[self.name.rindex('.') + 1:]

        super().__init__([self.name])

        self.setIcon(0, QIcon(self.tm.get_image('files/' + self.file_type, 'icons/unknown_file')))
        self.setFont(0, self.tm.font_medium)


class TreeDirectory(QTreeWidgetItem):
    def __init__(self, path, tm):
        super().__init__()
        self.tm = tm
        self.path = path
        self.name = os.path.basename(self.path)
        self.file_type = 'directory'

        super().__init__([self.name])

        self.setIcon(0, QIcon(self.tm.get_image('icons/' + self.file_type, 'icons/unknown_file')))
        self.setFont(0, self.tm.font_medium)

        self.update_files_list()

    def update_files_list(self):
        i = 0
        j = 0
        lst = list(filter(lambda p: os.path.isdir(os.path.join(self.path, p)), os.listdir(self.path))) + \
              list(filter(lambda p: os.path.isfile(os.path.join(self.path, p)), os.listdir(self.path)))
        lst = list(map(lambda p: os.path.join(self.path, p), lst))
        while i < self.childCount() and j < len(lst):
            if (path := self.child(i).path) != lst[j]:
                if path.startswith(self.path) and (os.path.isfile(path) or os.path.isdir(path)):
                    if os.path.isdir(lst[j]):
                        self.insertChild(i, TreeDirectory(lst[j], self.tm))
                    else:
                        self.insertChild(i, TreeFile(lst[j], self.tm))
                    i += 1
                    j += 1
                else:
                    self.takeChild(i)
            elif isinstance(item := self.child(i), TreeDirectory):
                item.update_files_list()
                i += 1
                j += 1
            else:
                i += 1
                j += 1
        while i < self.childCount():
            self.takeChild(i)
        while j < len(lst):
            if os.path.isdir(lst[j]):
                self.addChild(TreeDirectory(lst[j], self.tm))
            else:
                self.addChild(TreeFile(lst[j], self.tm))
            j += 1


class TreeWidget(QTreeWidget):
    moveFile = pyqtSignal(str, str)

    def __init__(self, tm):
        super().__init__()
        self.tm = tm
        self.moving_item = None
        self.moving_file = None
        self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)

    def mouseMoveEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        super().mouseMoveEvent(event)
        if isinstance(self.moving_file, MovedFile):
            self.moving_file.show()
            self.moving_file.move(self.mapToGlobal(event.pos()))

    def mousePressEvent(self, e: typing.Optional[QtGui.QMouseEvent]) -> None:
        super().mousePressEvent(e)
        if e.button() == Qt.MouseButton.LeftButton:
            item = self.currentItem()
            if isinstance(item, TreeDirectory):
                self.moving_file = MovedFile(self.tm, item.name)
            elif isinstance(item, TreeFile):
                self.moving_file = MovedFile(self.tm, item.name)
            else:
                return
            self.setSelectionMode(QTreeWidget.SelectionMode.NoSelection)
            self.moving_item = item
            self.moving_file.move(self.mapToGlobal(e.pos()))

    def mouseReleaseEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        super().mouseReleaseEvent(event)
        if isinstance(self.moving_file, MovedFile):
            self.moving_file.close()
            self.moving_file = None
            item = self.currentItem()
            if self.moving_item != item:
                if isinstance(item, TreeDirectory):
                    path = item.path
                elif isinstance(item, TreeFile):
                    path, _ = os.path.split(item.path)
                else:
                    self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
                    return
                self.moveFile.emit(self.moving_item.path, path)
                self.moving_item = None
        if self.moving_file is None:
            self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)


class ContextMenu(QMenu):
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

    def __init__(self, tm, path, directory=False):
        super().__init__()
        self.tm = tm

        self.setContentsMargins(3, 3, 3, 3)
        self.setMinimumWidth(150)

        self.create_menu = QMenu()
        self.create_menu.setMinimumWidth(150)
        self.create_menu.setIcon(QIcon(self.tm.get_image('buttons/plus')))
        self.create_menu.setTitle("Создать")
        self.create_menu.addAction(QIcon(self.tm.get_image('buttons/plus')), "Файл").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_FILE))
        self.create_menu.addAction(QIcon(self.tm.get_image('icons/directory')), "Папку").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_DIR))
        self.create_menu.addAction(QIcon(self.tm.get_image('files/py')), "Python file").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_PY))
        self.create_menu.addAction(QIcon(self.tm.get_image('files/c')), "C source file").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_C))
        self.create_menu.addAction(QIcon(self.tm.get_image('files/h')), "Header file").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_H))
        self.create_menu.addAction(QIcon(self.tm.get_image('files/md')), "Markdown file").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_MD))
        self.create_menu.addAction(QIcon(self.tm.get_image('files/t2b')), "Text-to-Binary file").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_T2B))
        self.addMenu(self.create_menu)

        self.addSeparator()

        self.addAction(QIcon(self.tm.get_image('buttons/cut')), "Вырезать").triggered.connect(
            lambda: self.set_action(ContextMenu.CUT_FILES))
        self.addAction(QIcon(self.tm.get_image('buttons/copy')), "Копировать").triggered.connect(
            lambda: self.set_action(ContextMenu.COPY_FILES))
        self.addAction(QIcon(self.tm.get_image('buttons/copy_path')), "Копировать как путь").triggered.connect(
            lambda: self.set_action(ContextMenu.COPY_PATH))
        self.addAction(QIcon(self.tm.get_image('buttons/paste')), "Вставить").triggered.connect(
            lambda: self.set_action(ContextMenu.PASTE_FILES))

        self.addSeparator()

        self.add_fast_run_actions(path)

        self.addSeparator()

        self.addAction(QIcon(self.tm.get_image('buttons/button_delete')), "Удалить").triggered.connect(
            lambda: self.set_action(ContextMenu.DELETE_FILE))
        self.addAction(QIcon(self.tm.get_image('buttons/button_delete')), "Переместить в корзину").triggered.connect(
            lambda: self.set_action(ContextMenu.MOVE_TO_TRASH))
        self.addAction(QIcon(self.tm.get_image('buttons/button_rename')), "Переименовать").triggered.connect(
            lambda: self.set_action(ContextMenu.RENAME_FILE))
        self.addAction(QIcon(self.tm.get_image('buttons/button_to_zip')), "Сжать в ZIP").triggered.connect(
            lambda: self.set_action(ContextMenu.COMPRESS_TO_ZIP))

        self.addSeparator()

        self.open_menu = QMenu()
        self.open_menu.setMinimumWidth(150)
        self.open_menu.setTitle("Открыть")
        if directory:
            self.open_menu.addAction(QIcon(self.tm.get_image('icons/directory')), "Проводник").triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_IN_EXPLORER))
            self.open_menu.addAction(QIcon(self.tm.get_image('icons/terminal')), "Вкладка \"Терминал\"").triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_IN_TERMINAL))
            if platform.system() == 'Windows':
                self.open_menu.addAction(QIcon(self.tm.get_image('icons/terminal')),
                                         "PowerShell").triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_POWER_SHELL))
                self.open_menu.addAction(QIcon(self.tm.get_image('icons/terminal')),
                                         "Командная строка").triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_SYSTEM_TERMINAL))
                self.open_menu.addAction(QIcon(self.tm.get_image('icons/terminal')),
                                         "Терминал WSL").triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_WSL_TERMINAL))
            else:
                self.open_menu.addAction(QIcon(self.tm.get_image('icons/terminal')),
                                         "Терминал").triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_SYSTEM_TERMINAL))
        else:
            self.open_menu.addAction("Вкладка \"Код\"").triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_IN_CODE))
            self.open_menu.addAction("Стандартное приложение").triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_BY_SYSTEM))
            if platform.system() == 'Windows':
                self.open_menu.addAction(QIcon(self.tm.get_image('icons/terminal')),
                                         "PowerShell").triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_POWER_SHELL))
                self.open_menu.addAction(QIcon(self.tm.get_image('icons/terminal')),
                                         "Командная строка").triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_SYSTEM_TERMINAL))
                self.open_menu.addAction(QIcon(self.tm.get_image('icons/terminal')),
                                         "Терминал WSL").triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_WSL_TERMINAL))
            else:
                self.open_menu.addAction(QIcon(self.tm.get_image('icons/terminal')),
                                         "Терминал").triggered.connect(
                    lambda: self.set_action(ContextMenu.OPEN_BY_SYSTEM_TERMINAL))

            self.open_menu.addSeparator()

            if '.' in path:
                for prog_name, prog_icon, prog_command in get_open_file_options(path):
                    self.add_open_action(prog_name, prog_icon, prog_command)

        self.addMenu(self.open_menu)

        for el in [self, self.create_menu, self.open_menu]:
            self.tm.auto_css(el)
        self.action = None
        self.action_data = None

    def add_fast_run_actions(self, path):
        for language in languages.values():
            for el in language.get('files', []):
                if path.endswith(el):

                    for name, icon, func in language.get('fast_run', []):
                        if icon:
                            icon = QIcon(self.tm.get_image(icon))
                        else:
                            icon = None
                        action = self.addAction(icon, name)
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
    renameFile = pyqtSignal(str)
    ignore_files = []

    def __init__(self, sm, bm: BackendManager, tm, app: QApplication):
        super(FilesWidget, self).__init__(sm, tm, 'Файлы', ['add', 'add_dir', 'delete', 'rename', 'update'])
        self.bm = bm
        self.app = app

        # self.setFixedWidth(225)
        files_layout = QVBoxLayout()
        files_layout.setSpacing(3)
        files_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(files_layout)
        self.path = ''

        self.buttons['rename'].clicked.connect(lambda: self.rename_file(False))
        self.buttons['update'].clicked.connect(self.update_files_list)

        self.files_list = TreeWidget(self.tm)
        # self.files_list.setFocusPolicy(False)
        self.files_list.setHeaderHidden(True)
        self.files_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.files_list.customContextMenuRequested.connect(self.run_context_menu)
        self.files_list.moveFile.connect(self.move_file)
        files_layout.addWidget(self.files_list)

        self.files_list.doubleClicked.connect(self.open_file)
        self.buttons['add'].clicked.connect(self.create_file)
        self.buttons['add_dir'].clicked.connect(self.create_directory)
        self.buttons['delete'].clicked.connect(self.delete_file)

        self.dialog = None
        self.ctrl_pressed = False
        self.shift_pressed = False
        self.sm.projectChanged.connect(self.open_task)

    def update_files_list(self):
        self.path = self.sm.project.path()
        if not self.path or not os.path.isdir(self.path):
            self.files_list.clear()
            return
        i = 0
        j = 0
        lst = list(filter(lambda p: os.path.isdir(os.path.join(self.path, p)), os.listdir(self.path))) + \
              list(filter(lambda p: os.path.isfile(os.path.join(self.path, p)), os.listdir(self.path)))
        lst = list(map(lambda p: os.path.join(self.path, p), lst))
        while i < self.files_list.topLevelItemCount() and j < len(lst):
            if (path := self.files_list.topLevelItem(i).path) != lst[j]:
                if path.startswith(self.path) and (os.path.isfile(path) or os.path.isdir(path)):
                    if os.path.isdir(lst[j]):
                        self.files_list.insertTopLevelItem(i, TreeDirectory(lst[j], self.tm))
                    else:
                        self.files_list.insertTopLevelItem(i, TreeFile(lst[j], self.tm))
                    i += 1
                    j += 1
                else:
                    self.files_list.takeTopLevelItem(i)
            elif isinstance(item := self.files_list.topLevelItem(i), TreeDirectory):
                item.update_files_list()
                i += 1
                j += 1
            else:
                i += 1
                j += 1
        while i < self.files_list.topLevelItemCount():
            self.files_list.takeTopLevelItem(i)
        while j < len(lst):
            if os.path.isdir(lst[j]):
                self.files_list.addTopLevelItem(TreeDirectory(lst[j], self.tm))
            else:
                self.files_list.addTopLevelItem(TreeFile(lst[j], self.tm))
            j += 1

    def move_file(self, file, dist):
        try:
            os.rename(file, os.path.join(dist, os.path.basename(file)))
        except Exception:
            pass
        self.update_files_list()

    def rename_file(self, flag=True):
        if (item := self.files_list.currentItem()) is None:
            return
        self.dialog = RenameFileDialog(item.name, directory=isinstance(item, TreeDirectory), tm=self.tm)
        if self.dialog.exec():
            if not os.path.isfile(f"{self.path}/{self.dialog.line_edit.text()}"):
                os.rename(self.files_list.currentItem().path,
                          f"{self.path}/{self.dialog.line_edit.text()}")
                self.update_files_list()
                self.renameFile.emit(self.dialog.line_edit.text())
            else:
                MessageBox(MessageBox.Icon.Warning, "Ошибка", "Невозможно переименовать файл", self.tm)

    def open_task(self):
        self.path = self.sm.project.path()
        self.update_files_list()

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

    def run_context_menu(self, point):
        item = self.files_list.currentItem()
        if item is None:
            file = None
            path = self.sm.project.path()
        elif isinstance(item, TreeDirectory):
            path = item.path
            file = item.path
        elif isinstance(item, TreeFile):
            file = item.path
            path = item.path
        else:
            raise TypeError("invalid item type")

        menu = ContextMenu(self.tm, path, directory=isinstance(item, TreeDirectory))
        menu.move(self.files_list.mapToGlobal(point))
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
                file = self.create_file(base_path=path, extension='md')
                if isinstance(file, str):
                    dialog = MarkdownPatternsDialog(self.sm, self.tm, file)
                    if dialog.exec():
                        pass
                    else:
                        os.remove(file)
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
                self.open_file()
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

    def fast_run_file(self, func):
        item = self.files_list.currentItem()
        if isinstance(item, TreeFile) or isinstance(item, TreeDirectory):
            self.bm.side_tab_show('run')
            self.bm.side_tab_command('run', item.path, func)

    def copy_file(self):
        item = self.files_list.currentItem()
        if isinstance(item, TreeFile) or isinstance(item, TreeDirectory):
            mime_data = QMimeData()
            mime_data.setUrls([QUrl.fromLocalFile(item.path)])
            self.app.clipboard().setMimeData(mime_data)

    def copy_path(self):
        item = self.files_list.currentItem()
        if isinstance(item, TreeFile) or isinstance(item, TreeDirectory):
            self.app.clipboard().setText(item.path)

    def paste_files(self):
        item = self.files_list.currentItem()
        if isinstance(item, TreeFile):
            path = os.path.split(item.path)[0]
        elif isinstance(item, TreeDirectory):
            path = item.path
        else:
            return

        if self.app.clipboard().mimeData().hasUrls():
            urls = self.app.clipboard().mimeData().urls()
            for url in urls:
                try:
                    shutil.copy(url.toLocalFile(), os.path.join(path, os.path.basename(url.toLocalFile())))
                except FileExistsError:
                    pass
            self.update_files_list()

    def compress_files(self):
        files = []
        for el in self.files_list.selectedItems():
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
            base_path = self.sm.project.path()
        self.dialog = RenameFileDialog(base_name, directory, self.tm)
        if self.dialog.exec():
            if not self.dialog.line_edit.text():
                MessageBox(MessageBox.Icon.Warning, "Ошибка",
                           f"Невозможно создать {'директорию' if directory else 'файл'}: имя файла не задано", self.tm)
                return
            try:
                path = os.path.join(base_path, self.dialog.line_edit.text())
                if extension and not path.endswith('.' + extension):
                    path += '.' + extension
                if directory:
                    os.makedirs(path)
                else:
                    os.makedirs(self.sm.project.path(), exist_ok=True)
                    open(path, 'x').close()
            except FileExistsError:
                MessageBox(MessageBox.Icon.Warning, "Ошибка",
                           f"Невозможно создать {'директорию' if directory else 'файл'}: "
                           f"{'директория' if directory else 'файл'} с таким именем уже существует", self.tm)
            except PermissionError:
                MessageBox(MessageBox.Icon.Warning, "Ошибка",
                           f"Невозможно создать {'директорию' if directory else 'файл'}: недостаточно прав", self.tm)
            except Exception as ex:
                MessageBox(MessageBox.Icon.Warning, "Ошибка",
                           f"Невозможно создать {'директорию' if directory else 'файл'}: {ex.__class__.__name__}: {ex}",
                           self.tm)
            else:
                self.update_files_list()
                return path

    def delete_file(self, to_trash=True):
        if self.files_list.currentItem() is None:
            return
        if to_trash:
            try:
                send2trash.send2trash([item.path for item in self.files_list.selectedItems()])
            except FileExistsError:
                pass
            except Exception as ex:
                MessageBox(MessageBox.Icon.Warning, "Ошибка", f"{ex.__class__.__name__}: {ex}", self.tm)
            self.update_files_list()
            return
        dlg = DeleteFileDialog(f"Вы уверены, что хотите удалить файл {self.files_list.currentItem().name}?", self.tm)
        if dlg.exec():
            if os.path.isdir(self.files_list.currentItem().path):
                shutil.rmtree(self.files_list.currentItem().path)
            else:
                os.remove(self.files_list.currentItem().path)
            self.update_files_list()

    def open_file(self):
        item = self.files_list.currentItem()
        if isinstance(item, (TreeFile, TreeDirectory)):
            if item.file_type != 'directory':
                self.bm.main_tab_show('code')
                self.bm.main_tab_command('code', item.path)

    def set_theme(self):
        super().set_theme()
        self.files_list.setStyleSheet(self.tm.tree_widget_css('Main'))
        # self.update_files_list()


class FileListWidgetItem(QListWidgetItem):
    def __init__(self, path, tm, sm):
        super(FileListWidgetItem, self).__init__()
        self.path = path

        self.tm = tm
        self.sm = sm
        language = languages[self.sm.get('language', 'C')]

        if path == '..':
            self.name = '..'
            self.setText(self.name)
            self.setIcon(QIcon(self.tm.get_image('icons/directory')))
            # self.setText('▲ ..')
            self.file_type = 'dir'
            self.priority = 0
        else:
            self.name = os.path.basename(path)
            self.setText(self.name)
            if os.path.isdir(self.path):
                # self.setText(f"▼ {self.name}")
                self.file_type = 'dir'
                self.setIcon(QIcon(self.tm.get_image('icons/directory')))
                self.priority = 1
            elif self.path.endswith(f"main{language.get('files')[0]}"):
                # self.setText(f"◆ {self.name}")
                self.file_type = 'main'
                self.priority = 2
            elif self.path.endswith(language.get('files')[0]):
                # self.setText(f"◆ {self.name}")
                self.file_type = 'code'
                self.priority = 3
            else:
                for elem in language.get('files'):
                    if self.path.endswith(elem):
                        # self.setText(f"◆ {self.name}")
                        self.file_type = 'header'
                        self.priority = 3
                        break
                else:
                    for key, item in languages.items():
                        flag = False
                        for el in item.get('files', []):
                            if self.path.endswith(el):
                                # self.setText(f" ●  {self.name}")
                                self.file_type = 'text'
                                self.priority = 4
                                flag = True
                        if flag:
                            break
                    else:
                        # self.setText(f" ?  {self.name}")

                        self.file_type = 'unknown'
                        self.priority = 5

        self.set_theme()

    def set_theme(self):
        if self.file_type == 'dir':
            color = self.tm['Directory']
        elif self.file_type == 'main':
            color = self.tm['MainC']
        elif self.file_type == 'code':
            color = self.tm['CFile']
        elif self.file_type == 'header':
            color = self.tm['HFile']
        elif self.file_type == 'text':
            color = self.tm['TxtFile']
        else:
            color = QColor(self.tm['TextColor'])
        self.setForeground(color)

        if self.file_type == 'dir':
            self.setIcon(QIcon(self.tm.get_image('icons/directory', color=color)))
        elif '.' in self.name:
            self.setIcon(QIcon(self.tm.get_image(self.name.split('.')[1], 'unknown_file', color=color)))
        else:
            self.setIcon(QIcon(self.tm.get_image('icons/unknown_file', color=color)))
        self.setFont(self.tm.font_medium)


class DeleteFileDialog(CustomDialog):
    def __init__(self, message, tm):
        super().__init__(tm)

        self.setWindowTitle("Удаление файла")

        self.layout = QVBoxLayout()
        label = QLabel(message)
        label.setFont(tm.font_medium)
        self.layout.addWidget(label)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.button_ok = QPushButton("Ок")
        self.button_ok.setFixedSize(70, 24)
        self.button_ok.clicked.connect(self.accept)
        button_layout.addWidget(self.button_ok)

        self.button_cancel = QPushButton("Отмена")
        self.button_cancel.setFixedSize(70, 24)
        self.button_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.button_cancel)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        super().set_theme()
        for el in [self.button_cancel, self.button_ok]:
            tm.auto_css(el)


class RenameFileDialog(CustomDialog):
    def __init__(self, name, directory, tm):
        file = 'папки' if directory else 'файла'
        super().__init__(tm, f"Введите новое имя {file}:" if name else f"Введите имя {file}:", False)

        self.layout = QVBoxLayout()

        self.line_edit = QLineEdit()
        self.line_edit.setText(name)
        self.layout.addWidget(self.line_edit)
        self.line_edit.setSelection(0, len(name) if directory or '.' not in name else name.rindex('.'))

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.button_ok = QPushButton("Ок")
        self.button_ok.setFixedSize(70, 24)
        self.button_ok.clicked.connect(self.accept)
        button_layout.addWidget(self.button_ok)

        self.button_cancel = QPushButton("Отмена")
        self.button_cancel.setFixedSize(70, 24)
        self.button_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.button_cancel)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        super().set_theme()
        for el in [self.button_ok, self.button_cancel, self.line_edit]:
            tm.auto_css(el)

        self.resize(280, 50)


class MovedFile(QWidget):
    def __init__(self, tm, file):
        super().__init__()
        self.tm = tm
        self._name = file

        self.setFixedHeight(25)
        self.setMinimumWidth(150)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        self.label = QLabel(self._name)
        layout.addWidget(self.label)

        self.setStyleSheet(f"color: {self.tm['TextColor']}; background-color: {self.tm['BgColor']};")
        for el in [self.label]:
            self.tm.auto_css(el)
