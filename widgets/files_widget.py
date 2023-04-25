import os

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLineEdit, \
    QPushButton, QDialogButtonBox, QDialog, QLabel, QListWidgetItem


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

        self.file_name = QLineEdit()
        files_layout.addWidget(self.file_name)

        buttons_layout = QHBoxLayout()
        files_layout.addLayout(buttons_layout)
        self.button_add_file = QPushButton()
        self.button_add_file.setText("+")
        buttons_layout.addWidget(self.button_add_file)
        self.button_delete_file = QPushButton()
        self.button_delete_file.setText("✕")
        buttons_layout.addWidget(self.button_delete_file)

        self.files_list = QListWidget()
        files_layout.addWidget(self.files_list)

        self.files_list.currentRowChanged.connect(self.open_file)
        self.file_name.editingFinished.connect(self.rename_file)
        self.button_add_file.clicked.connect(self.create_file)
        self.button_delete_file.clicked.connect(self.delete_file)

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
        if self.files_list.currentRow() != -1:
            self.file_name.setText(self.files_list.currentItem().text())

    def rename_file(self):
        if self.files_list.currentItem() is None:
            return
        if not os.path.isfile(f"{self.path}/{self.file_name.text()}"):
            os.rename(f"{self.path}/{self.files_list.currentItem().text()}", f"{self.path}/{self.file_name.text()}")
        self.update_files_list()
        self.renameFile.emit(self.file_name.text())

    def get_path(self):
        self.path = self.sm.lab_path()

    def create_file(self, *args):
        self.get_path()
        os.makedirs(self.path, exist_ok=True)
        if not os.path.isfile(f"{self.path}/new_file.c"):
            open(f"{self.path}/new_file.c", 'w').close()
        else:
            i = 1
            while os.path.isfile(f"{self.path}/new_file_{i}.c"):
                i += 1
            open(f"{self.path}/new_file_{i}.c", 'w').close()
        self.update_files_list()

    def delete_file(self, *args):
        if self.files_list.currentRow() == -1:
            return
        dlg = CustomDialog(f"Вы уверены, что хотите удалить файл {self.files_list.currentItem().text()}?")
        if dlg.exec():
            os.remove(f"{self.path}/{self.files_list.currentItem().text()}")
            self.update_files_list()

    def set_theme(self):
        self.file_name.setStyleSheet(self.tm.style_sheet)
        self.button_add_file.setStyleSheet(self.tm.style_sheet)
        self.button_delete_file.setStyleSheet(self.tm.style_sheet)
        self.files_list.setStyleSheet(self.tm.style_sheet)


class CustomDialog(QDialog):
    def __init__(self, message):
        super().__init__()

        self.setWindowTitle("Удаление файла")

        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(message))
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


