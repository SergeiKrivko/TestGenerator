import os
import shutil

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLineEdit, \
    QPushButton, QDialog, QLabel, QListWidgetItem, QTreeWidget, QTreeWidgetItem

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

        super().__init__([self.name], QTreeWidgetItem.DontShowIndicatorWhenChildless)

        self.setIcon(0, QIcon(self.tm.get_image(self.file_type, 'unknown_file')))
        self.setFont(0, self.tm.font_medium)


class TreeDirectory(QTreeWidgetItem):
    def __init__(self, path, tm):
        super().__init__()
        self.tm = tm
        self.path = path
        self.name = os.path.basename(self.path)
        self.file_type = 'directory'

        super().__init__([self.name], QTreeWidgetItem.DontShowIndicatorWhenChildless)

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


class FilesWidget(SidePanelWidget):
    renameFile = pyqtSignal(str)
    ignore_files = []

    def __init__(self, sm, bm: BackendManager, tm):
        super(FilesWidget, self).__init__(sm, tm, 'Файлы', ['add', 'delete', 'rename', 'update'])
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
        self.files_list.setFocusPolicy(False)
        self.files_list.setHeaderHidden(True)
        files_layout.addWidget(self.files_list)

        self.files_list.doubleClicked.connect(self.open_file)
        self.buttons['add'].clicked.connect(self.create_file)
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
        if item := self.files_list.currentItem() is None:
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
        print('open task', self.path)
        self.update_files_list()

    def create_file(self, *args):
        self.dialog = RenameFileDialog(
            f"main{languages[self.sm.get('language', 'C')]['files'][0]}"
            if self.path == self.path and not os.path.isfile(
                f"{self.path}/main{languages[self.sm.get('language', 'C')]['files'][0]}") else '', self.tm)
        if self.dialog.exec():
            os.makedirs(self.path, exist_ok=True)
            if not self.dialog.line_edit.text():
                MessageBox(MessageBox.Warning, "Ошибка", "Невозможно создать файл: имя файла не задано", self.tm)
                return
            try:
                open(f"{self.path}/{self.dialog.line_edit.text()}", 'x').close()
            except FileExistsError:
                MessageBox(MessageBox.Warning, "Ошибка",
                           "Невозможно создать файл: файл с таким именем уже существует", self.tm)
            except PermissionError:
                MessageBox(MessageBox.Warning, "Ошибка", "Невозможно создать файл: недостаточно прав", self.tm)
            except Exception as ex:
                MessageBox(MessageBox.Warning, "Ошибка",
                           f"Невозможно создать файл: {ex.__class__.__name__}: {ex}", self.tm)
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
        button_layout.setAlignment(Qt.AlignRight)
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
        button_layout.setAlignment(Qt.AlignRight)

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
