import os
import shutil

from PyQt5.QtCore import pyqtSignal, Qt, QThread
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLineEdit, \
    QPushButton, QDialog, QLabel, QListWidgetItem, QDialogButtonBox

from ui.button import Button
from ui.message_box import MessageBox
from language.languages import languages
from ui.resources import resources


class FilesWidget(QWidget):
    renameFile = pyqtSignal(str)
    openFile = pyqtSignal(str)
    ignore_files = [".exe", ".o", "temp.txt"]

    def __init__(self, sm, cm, tm):
        super(FilesWidget, self).__init__()
        self.sm = sm
        self.cm = cm
        self.tm = tm

        self.setMaximumWidth(175)
        files_layout = QVBoxLayout()
        files_layout.setContentsMargins(0, 5, 0, 0)
        self.setLayout(files_layout)
        self.path = ''
        self.current_path = ''

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(3)
        files_layout.addLayout(buttons_layout)

        self.button_add_file = Button(self.tm, 'plus')
        self.button_add_file.setFixedHeight(22)
        buttons_layout.addWidget(self.button_add_file)

        self.button_delete_file = Button(self.tm, 'delete')
        self.button_delete_file.setFixedHeight(22)
        buttons_layout.addWidget(self.button_delete_file)

        self.button_run = Button(self.tm, 'run')
        self.button_run.setFixedHeight(22)
        buttons_layout.addWidget(self.button_run)

        self.button_search = Button(self.tm, 'search')
        self.button_search.setFixedHeight(22)
        buttons_layout.addWidget(self.button_search)

        self.files_list = QListWidget()
        files_layout.addWidget(self.files_list)

        self.files_list.currentItemChanged.connect(self.open_file)
        self.button_add_file.clicked.connect(self.create_file)
        self.button_delete_file.clicked.connect(self.delete_file)
        self.files_list.doubleClicked.connect(self.rename_file)
        self.button_run.clicked.connect(self.run_file)
        self.button_run.setDisabled(True)

        self.dialog = None

    def update_files_list(self):
        self.files_list.clear()
        if not self.current_path or not os.path.isdir(self.current_path):
            return

        items = []
        if self.current_path != self.path:
            items.append(FileListWidgetItem('..', self.tm, self.sm))

        for file in os.listdir(self.current_path):
            for el in FilesWidget.ignore_files:
                if file.endswith(el):
                    break
            else:
                items.append(FileListWidgetItem(f"{self.current_path}/{file}", self.tm, self.sm))

        items.sort(key=lambda it: it.priority)
        for item in items:
            self.files_list.addItem(item)

    def rename_file(self):
        if self.files_list.currentItem() is None:
            return
        if (item := self.files_list.currentItem()).file_type == 'dir':
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
        if self.files_list.currentRow() == -1:
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
        if isinstance(item, FileListWidgetItem):
            if item.file_type == 'dir':
                self.openFile.emit('')
            else:
                self.openFile.emit(item.path)
                for language in languages.values():
                    if language.get('fast_run', False):
                        for el in language['files']:
                            if item.path.endswith(el):
                                self.button_run.setDisabled(False)
                                return
            self.button_run.setDisabled(True)

    def run_file(self):
        if not self.files_list.currentItem():
            return
        for language in languages.values():
            if language.get('fast_run', False):
                for el in language['files']:
                    if self.files_list.currentItem().path.endswith(el):
                        old_dir = os.getcwd()
                        os.chdir(self.current_path)
                        looper = FileRunner(language['run'], self.files_list.currentItem().path, self.sm, self.cm)
                        dialog = RunDialog(self.tm, os.path.basename(self.files_list.currentItem().path))
                        dialog.rejected.connect(looper.terminate)
                        looper.finished.connect(dialog.accept)
                        looper.start()
                        if dialog.exec() and looper.res:
                            if looper.res.stderr:
                                MessageBox(MessageBox.Information, "STDERR", looper.res.stderr, self.tm)
                            if looper.res.stdout:
                                MessageBox(MessageBox.Information, "STDOUT", looper.res.stdout, self.tm)

                        os.chdir(old_dir)
                        return

    def set_theme(self):
        for el in [self.button_add_file, self.button_delete_file, self.button_run, self.button_search]:
            self.tm.auto_css(el)
        self.files_list.setStyleSheet(self.tm.list_widget_style_sheet)
        for i in range(self.files_list.count()):
            self.files_list.item(i).set_theme()


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
            self.setIcon(QIcon(self.tm.get_image('parent_dir')))
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
        color = None
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
            self.setForeground(QColor(self.tm['TextColor']))
        if color:
            self.setForeground(color)

        if self.file_type == 'dir':
            if self.name == '..':
                self.setIcon(QIcon(self.tm.get_image('parent_dir', color=color)))
            else:
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
        self.button_ok.setStyleSheet(tm.buttons_style_sheet)
        self.button_ok.setFont(tm.font_small)
        self.button_cancel.setStyleSheet(tm.buttons_style_sheet)
        self.button_cancel.setFont(tm.font_small)


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
        self.button_ok.setStyleSheet(tm.buttons_style_sheet)
        self.button_ok.setFont(tm.font_small)
        self.button_cancel.setStyleSheet(tm.buttons_style_sheet)
        self.button_cancel.setFont(tm.font_small)
        self.line_edit.setStyleSheet(tm.style_sheet)
        self.line_edit.setFont(tm.font_small)

        self.resize(280, 50)


class FileRunner(QThread):
    def __init__(self, func, path, sm, cm):
        super().__init__()
        self.func = func
        self.path = path
        self.sm = sm
        self.cm = cm
        self.res = None

    def run(self):
        self.res = self.func(self.path, self.sm, self.cm, scip_timeout=True)


class RunDialog(QDialog):
    def __init__(self, tm, path):
        super().__init__()
        self.tm = tm

        self.setWindowTitle(path)

        layout = QVBoxLayout()
        label = QLabel(f"Идет выполнение скрипта \"{path}\"")
        label.setWordWrap(True)
        label.setFont(self.tm.font_small)

        QBtn = QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.Cancel).setStyleSheet(self.tm.buttons_style_sheet)
        self.buttonBox.button(QDialogButtonBox.Cancel).setFixedSize(80, 24)

        layout.addWidget(label)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

