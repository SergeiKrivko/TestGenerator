import os
import shutil

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLineEdit, \
    QPushButton, QDialog, QLabel, QListWidgetItem, QTreeWidget, QTreeWidgetItem

from language.languages import languages
from ui.message_box import MessageBox
from ui.side_panel_widget import SidePanelWidget


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
        self.setFont(0, self.tm.font_small)


class TreeDirectory(QTreeWidgetItem):
    def __init__(self, path, tm):
        super().__init__()
        self.tm = tm
        self.path = path
        self.name = os.path.basename(self.path)
        self.file_type = 'directory'

        super().__init__([self.name], QTreeWidgetItem.DontShowIndicatorWhenChildless)

        self.setIcon(0, QIcon(self.tm.get_image(self.file_type, 'unknown_file')))
        self.setFont(0, self.tm.font_small)

        for el in os.listdir(self.path):
            if os.path.isdir(path := os.path.join(self.path, el)):
                self.addChild(TreeDirectory(path, self.tm))
        for el in os.listdir(self.path):
            if os.path.isfile(path := os.path.join(self.path, el)):
                self.addChild(TreeFile(path, self.tm))


class FilesWidget(SidePanelWidget):
    renameFile = pyqtSignal(str)
    openFile = pyqtSignal(str)
    ignore_files = []

    def __init__(self, sm, cm, tm):
        super(FilesWidget, self).__init__(sm, tm, 'Файлы', ['add', 'delete', 'rename', 'update'])
        self.cm = cm

        # self.setFixedWidth(225)
        files_layout = QVBoxLayout()
        files_layout.setSpacing(3)
        files_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(files_layout)
        self.path = ''
        self.current_path = ''

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

    def update_files_list(self):
        self.files_list.clear()
        if not self.current_path or not os.path.isdir(self.current_path):
            return

        for el in os.listdir(self.path):
            if os.path.isdir(path := os.path.join(self.path, el)):
                self.files_list.addTopLevelItem(TreeDirectory(path, self.tm))
        for el in os.listdir(self.path):
            if os.path.isfile(path := os.path.join(self.path, el)):
                self.files_list.addTopLevelItem(TreeFile(path, self.tm))

    def rename_file(self, flag=True):
        if self.files_list.currentItem() is None:
            return
        if (item := self.files_list.currentItem()).file_type == 'dir' and flag:
            if item.name == '..':
                self.current_path = os.path.split(self.current_path)[0]
            else:
                self.current_path = f"{self.current_path}/{item.name}"
            self.update_files_list()
        else:
            self.dialog = RenameFileDialog(item.name, self.tm)
            if self.dialog.exec():
                if not os.path.isfile(f"{self.current_path}/{self.dialog.line_edit.text()}"):
                    os.rename(self.files_list.currentItem().path,
                              f"{self.current_path}/{self.dialog.line_edit.text()}")
                    self.update_files_list()
                    self.renameFile.emit(self.dialog.line_edit.text())
                else:
                    MessageBox(MessageBox.Warning, "Ошибка", "Невозможно переименовать файл", self.tm)

    def open_task(self):
        self.path = self.sm.lab_path()
        self.current_path = self.path
        self.update_files_list()

    def create_file(self, *args):
        self.dialog = RenameFileDialog(
            f"main{languages[self.sm.get('language', 'C')]['files'][0]}"
            if self.path == self.current_path and not os.path.isfile(
                f"{self.path}/main{languages[self.sm.get('language', 'C')]['files'][0]}") else '', self.tm)
        if self.dialog.exec():
            os.makedirs(self.current_path, exist_ok=True)
            if not self.dialog.line_edit.text():
                MessageBox(MessageBox.Warning, "Ошибка", "Невозможно создать файл: имя файла не задано", self.tm)
                return
            try:
                open(f"{self.current_path}/{self.dialog.line_edit.text()}", 'x').close()
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
            if item.file_type == 'directory':
                self.openFile.emit('')
            else:
                self.openFile.emit(item.path)

    def set_theme(self):
        super().set_theme()
        self.files_list.setStyleSheet(self.tm.tree_widget_css('Main'))
        self.update_files_list()


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
        self.setFont(self.tm.font_small)


class DeleteFileDialog(QDialog):
    def __init__(self, message, tm):
        super().__init__()

        self.setWindowTitle("Удаление файла")

        self.layout = QVBoxLayout()
        label = QLabel(message)
        label.setFont(tm.font_small)
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
        label.setFont(tm.font_small)
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
