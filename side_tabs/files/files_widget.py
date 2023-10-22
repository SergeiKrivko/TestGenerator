import os
import platform
import shutil
import subprocess

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLineEdit, \
    QPushButton, QDialog, QLabel, QListWidgetItem, QTreeWidget, QTreeWidgetItem, QMenu
import win32api

from language.languages import languages
from ui.message_box import MessageBox
from ui.side_panel_widget import SidePanelWidget
from backend.backend_manager import BackendManager


class TreeFile(QTreeWidgetItem):
    def __init__(self, path: str, tm):
        self.tm = tm
        self.path = path
        self.name = os.path.basename(self.path)
        if '.' not in self.name or (ind := self.name.rindex('.')) == 0:
            self.file_type = 'unknown_file'
        else:
            self.file_type = self.name[ind + 1:]

        super().__init__([self.name])

        self.setIcon(0, QIcon(self.tm.get_image(self.file_type, 'unknown_file')))
        self.setFont(0, self.tm.font_medium)


class TreeDirectory(QTreeWidgetItem):
    def __init__(self, path, tm):
        super().__init__()
        self.tm = tm
        self.path = path
        self.name = os.path.basename(self.path)
        self.file_type = 'directory'

        super().__init__([self.name])

        self.setIcon(0, QIcon(self.tm.get_image(self.file_type, 'unknown_file')))
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

    def __init__(self, tm, directory=False):
        super().__init__()
        self.tm = tm

        self.setContentsMargins(3, 3, 3, 3)
        self.setMinimumWidth(150)

        self.create_menu = QMenu()
        self.create_menu.setMinimumWidth(150)
        self.create_menu.setIcon(QIcon(self.tm.get_image('plus')))
        self.create_menu.setTitle("Создать")
        self.create_menu.addAction(QIcon(self.tm.get_image('plus')), "Файл").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_FILE))
        self.create_menu.addAction(QIcon(self.tm.get_image('directory')), "Папку").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_DIR))
        self.create_menu.addAction(QIcon(self.tm.get_image('py')), "Python file").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_PY))
        self.create_menu.addAction(QIcon(self.tm.get_image('c')), "C source file").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_C))
        self.create_menu.addAction(QIcon(self.tm.get_image('h')), "Header file").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_H))
        self.create_menu.addAction(QIcon(self.tm.get_image('md')), "Markdown file").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_MD))
        self.create_menu.addAction(QIcon(self.tm.get_image('t2b')), "Text-to-Binary file").triggered.connect(
            lambda: self.set_action(ContextMenu.CREATE_T2B))
        self.addMenu(self.create_menu)

        self.addAction(QIcon(self.tm.get_image('button_delete')), "Удалить").triggered.connect(
            lambda: self.set_action(ContextMenu.DELETE_FILE))
        self.addAction(QIcon(self.tm.get_image('button_rename')), "Переименовать").triggered.connect(
            lambda: self.set_action(ContextMenu.RENAME_FILE))

        self.open_menu = QMenu()
        self.open_menu.setMinimumWidth(150)
        self.open_menu.setTitle("Открыть")
        if directory:
            self.open_menu.addAction(QIcon(self.tm.get_image('directory')), "Проводник").triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_IN_EXPLORER))
            self.open_menu.addAction(QIcon(self.tm.get_image('button_terminal')), "Терминал").triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_IN_TERMINAL))
            self.open_menu.addAction(QIcon(self.tm.get_image('button_terminal')), "Системный терминал").triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_BY_SYSTEM_TERMINAL))
        else:
            self.open_menu.addAction("Вкладка \"Код\"").triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_IN_CODE))
            self.open_menu.addAction("Система").triggered.connect(
                lambda: self.set_action(ContextMenu.OPEN_BY_SYSTEM))
        self.addMenu(self.open_menu)

        for el in [self, self.create_menu, self.open_menu]:
            self.tm.auto_css(el)
        self.action = None

    def set_action(self, action):
        self.action = action


class FilesWidget(SidePanelWidget):
    renameFile = pyqtSignal(str)
    ignore_files = []

    def __init__(self, sm, bm: BackendManager, tm):
        super(FilesWidget, self).__init__(sm, tm, 'Файлы', ['add', 'add_dir', 'delete', 'rename', 'update'])
        self.bm = bm

        # self.setFixedWidth(225)
        files_layout = QVBoxLayout()
        files_layout.setSpacing(3)
        files_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(files_layout)
        self.path = ''

        self.buttons['rename'].clicked.connect(lambda: self.rename_file(False))
        self.buttons['update'].clicked.connect(self.update_files_list)

        self.files_list = QTreeWidget()
        # self.files_list.setFocusPolicy(False)
        self.files_list.setHeaderHidden(True)
        self.files_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.files_list.customContextMenuRequested.connect(self.run_context_menu)
        files_layout.addWidget(self.files_list)

        self.files_list.doubleClicked.connect(self.open_file)
        self.buttons['add'].clicked.connect(self.create_file)
        self.buttons['add_dir'].clicked.connect(self.create_directory)
        self.buttons['delete'].clicked.connect(self.delete_file)

        self.dialog = None
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

    def rename_file(self, flag=True):
        if (item := self.files_list.currentItem()) is None:
            return
        self.dialog = RenameFileDialog(item.name, self.tm)
        if self.dialog.exec():
            if not os.path.isfile(f"{self.path}/{self.dialog.line_edit.text()}"):
                os.rename(self.files_list.currentItem().path,
                          f"{self.path}/{self.dialog.line_edit.text()}")
                self.update_files_list()
                self.renameFile.emit(self.dialog.line_edit.text())
            else:
                MessageBox(MessageBox.Warning, "Ошибка", "Невозможно переименовать файл", self.tm)

    def open_task(self):
        self.path = self.sm.project.path()
        self.update_files_list()

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
            path = os.path.split(file)[0]
        else:
            raise TypeError("invalid item type")

        menu = ContextMenu(self.tm, directory=isinstance(item, TreeDirectory))
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
                self.create_file(base_path=path, extension='md')
            case ContextMenu.CREATE_T2B:
                self.create_file(base_path=path, extension='t2b')
            case ContextMenu.DELETE_FILE:
                self.delete_file()
            case ContextMenu.RENAME_FILE:
                self.rename_file()
            case ContextMenu.OPEN_IN_CODE:
                self.open_file()
            case ContextMenu.OPEN_BY_SYSTEM:
                self.open_by_system(file)
            case ContextMenu.OPEN_IN_EXPLORER:
                self.open_by_system(file)
            case ContextMenu.OPEN_BY_SYSTEM_TERMINAL:
                self.open_in_system_terminal(file)

    @staticmethod
    def open_by_system(filepath):
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))

    @staticmethod
    def open_in_explorer(path):
        match platform.system():
            case 'Windows':
                subprocess.call(['explorer', path])
            case 'Linux':
                subprocess.call(['nautilus', '--browser', path])

    @staticmethod
    def open_in_system_terminal(path):
        match platform.system():
            case 'Windows':
                os.system(f"start cmd /K cd {path}")

    def create_directory(self):
        self.create_file(directory=True)

    def create_file(self, directory=False, base_path=None, extension=''):
        if base_path is None:
            base_path = self.sm.project.path()
        self.dialog = RenameFileDialog('', self.tm)
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
            self.update_files_list()

    def delete_file(self, *args):
        if self.files_list.currentItem() is None:
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
            self.setIcon(QIcon(self.tm.get_image('directory')))
            # self.setText('▲ ..')
            self.file_type = 'dir'
            self.priority = 0
        else:
            self.name = os.path.basename(path)
            self.setText(self.name)
            if os.path.isdir(self.path):
                # self.setText(f"▼ {self.name}")
                self.file_type = 'dir'
                self.setIcon(QIcon(self.tm.get_image('directory')))
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
            self.setIcon(QIcon(self.tm.get_image('directory', color=color)))
        elif '.' in self.name:
            self.setIcon(QIcon(self.tm.get_image(self.name.split('.')[1], 'unknown_file', color=color)))
        else:
            self.setIcon(QIcon(self.tm.get_image('unknown_file', color=color)))
        self.setFont(self.tm.font_medium)


class DeleteFileDialog(QDialog):
    def __init__(self, message, tm):
        super().__init__()

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

        self.setStyleSheet(tm.bg_style_sheet)
        for el in [self.button_cancel, self.button_ok]:
            tm.auto_css(el)


class RenameFileDialog(QDialog):
    def __init__(self, name, tm):
        super().__init__()

        self.setWindowTitle("Переименование файла" if name else "Создание файла")

        self.layout = QVBoxLayout()
        label = QLabel("Введите новое имя файла:" if name else "Введите имя файла:")
        label.setFont(tm.font_medium)
        self.layout.addWidget(label)

        self.line_edit = QLineEdit()
        self.line_edit.setText(name)
        self.layout.addWidget(self.line_edit)
        self.line_edit.selectAll()

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

        self.setStyleSheet(tm.bg_style_sheet)
        for el in [self.button_ok, self.button_cancel, self.line_edit]:
            tm.auto_css(el)

        self.resize(280, 50)
