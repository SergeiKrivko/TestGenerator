import os

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLineEdit, \
    QPushButton, QDialog, QLabel, QListWidgetItem

from widgets.message_box import MessageBox


class FilesWidget(QWidget):
    renameFile = pyqtSignal(str)
    ignore_files = [".exe", ".o", "temp.txt"]

    def __init__(self, sm, tm):
        super(FilesWidget, self).__init__()
        self.sm = sm
        self.tm = tm

        self.setMaximumWidth(175)
        files_layout = QVBoxLayout()
        files_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(files_layout)
        self.path = ''

        buttons_layout = QHBoxLayout()
        files_layout.addLayout(buttons_layout)
        self.button_add_file = QPushButton()
        self.button_add_file.setText("+")
        self.button_add_file.setFixedHeight(20)
        buttons_layout.addWidget(self.button_add_file)
        self.button_delete_file = QPushButton()
        self.button_delete_file.setText("✕")
        self.button_delete_file.setFixedHeight(20)
        buttons_layout.addWidget(self.button_delete_file)

        self.files_list = QListWidget()
        files_layout.addWidget(self.files_list)

        self.files_list.currentRowChanged.connect(self.open_file)
        self.button_add_file.clicked.connect(self.create_file)
        self.button_delete_file.clicked.connect(self.delete_file)
        self.files_list.doubleClicked.connect(self.rename_file)

        self.dialog = None

    def update_files_list(self):
        self.get_path()
        self.files_list.clear()

        if not os.path.isdir(self.path):
            return

        for file in os.listdir(self.path):
            for el in FilesWidget.ignore_files:
                if file.endswith(el):
                    break
            else:
                if '.' in file:
                    item = QListWidgetItem(file)
                    if file.endswith("main.c"):
                        item.setForeground(self.tm['MainC'])
                    elif file.endswith(".c"):
                        item.setForeground(self.tm['CFile'])
                    elif file.endswith(".h"):
                        item.setForeground(self.tm['HFile'])
                    elif file.endswith(".txt"):
                        item.setForeground(self.tm['TxtFile'])
                    elif file.endswith(".md"):
                        item.setForeground(self.tm['MdFile'])
                    self.files_list.addItem(item)

    def open_file(self):
        pass
        # if self.files_list.currentRow() != -1:
        #     self.file_name.setText(self.files_list.currentItem().text())

    def rename_file(self):
        if self.files_list.currentItem() is None:
            return
        self.dialog = RenameFileDialog(self.files_list.currentItem().text(), self.tm)
        if self.dialog.exec():
            if not os.path.isfile(f"{self.path}/{self.dialog.line_edit.text()}"):
                os.rename(f"{self.path}/{self.files_list.currentItem().text()}",
                          f"{self.path}/{self.dialog.line_edit.text()}")
                self.update_files_list()
                self.renameFile.emit(self.dialog.line_edit.text())
            else:
                MessageBox(MessageBox.Warning, "Ошибка", "Невозможно переименовать файл", self.tm)

    def get_path(self):
        self.path = self.sm.lab_path()

    def create_file(self, *args):
        self.dialog = RenameFileDialog('main.c' if not os.path.isfile(f"{self.path}/main.c") else '', self.tm)
        if self.dialog.exec():
            self.get_path()
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
        if self.files_list.currentRow() == -1:
            return
        dlg = DeleteFileDialog(f"Вы уверены, что хотите удалить файл {self.files_list.currentItem().text()}?", self.tm)
        if dlg.exec():
            os.remove(f"{self.path}/{self.files_list.currentItem().text()}")
            self.update_files_list()

    def set_theme(self):
        self.button_add_file.setStyleSheet(self.tm.buttons_style_sheet)
        self.button_delete_file.setStyleSheet(self.tm.buttons_style_sheet)
        self.files_list.setStyleSheet(self.tm.list_widget_style_sheet)


class DeleteFileDialog(QDialog):
    def __init__(self, message, tm):
        super().__init__()

        self.setWindowTitle("Удаление файла")

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(message))

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
        self.button_cancel.setStyleSheet(tm.buttons_style_sheet)


class RenameFileDialog(QDialog):
    def __init__(self, name, tm):
        super().__init__()

        self.setWindowTitle("Переименование файла" if name else "Создание файла")

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Введите новое имя файла:" if name else "Введите имя файла:"))

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
        self.button_cancel.setStyleSheet(tm.buttons_style_sheet)
        self.line_edit.setStyleSheet(tm.style_sheet)

        self.resize(280, 50)
