import os
import platform
import shutil
import subprocess

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFileDialog, QVBoxLayout

from src.side_tabs.telegram.telegram_api import tg
from src.ui.button import Button
from src.ui.message_box import MessageBox
from src.ui.resources import resources


class DocumentWidget(QWidget):

    TYPE_DOCUMENT = 10
    TYPE_PROJECT = 11

    def __init__(self, tm, document: tg.Document, manager):
        super().__init__()
        self._tm = tm
        self._document = document
        self._manager = manager
        self._path = ''
        self._type = DocumentWidget.TYPE_DOCUMENT
        self._importing = False

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(5, 0, 5, 5)
        self.setLayout(main_layout)

        file_name = self._document.file_name
        self._extension = 'icons/unknown_file' if '.' not in self._document.file_name else \
            self._document.file_name[self._document.file_name.rindex('.') + 1:]
        if self._extension not in resources:
            icon = 'icons/unknown_file'
        else:
            icon = self._extension

        if file_name.endswith('.TGProject.7z'):
            self._type = DocumentWidget.TYPE_PROJECT
            icon = 'icons/projects'
            file_name = self._document.file_name[:-len('.TGProject.7z')]

        self._button = Button(self._tm, icon, css='Menu')
        self._button.setFixedSize(20, 20)
        main_layout.addWidget(self._button)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(layout)

        self._type_label = QLabel()
        layout.addWidget(self._type_label)
        self._type_label.hide()

        self._name_label = QLabel(file_name)
        layout.addWidget(self._name_label)
        self._name_label.setMinimumWidth(100)

        match self._type:
            case DocumentWidget.TYPE_PROJECT:
                self._type_label.setText("Проект")
                self._type_label.show()
                self._button.setFixedSize(32, 32)
                self._button.clicked.connect(self.save_project)

        self._manager.updateFile.connect(self._on_file_updated)

    def download(self):
        if not self._document.document.local.is_downloading_completed and \
                not self._document.document.local.is_downloading_active:
            self._button.image_name = 'button_import'
            self._button.set_theme()
            tg.downloadFile(self._document.document.id, 1)

    def save(self, path=None):
        if not self._document.document.local.is_downloading_completed:
            return
        if path is None:
            if '.' in self._document.file_name:
                extension = '.' + self._document.file_name.split('.')[-1]
            else:
                extension = ''
            self._path = QFileDialog.getSaveFileName(caption="Сохранение файла", filter=extension)[0]
            if self._path and not self._path.endswith(extension):
                self._path += extension
        else:
            self._path = path

        if self._path:
            try:
                shutil.copy(self._document.document.local.path, self._path)
            except Exception as ex:
                MessageBox(MessageBox.Icon.Warning, "Ошибка", f"Не удалось сохранить файл {self._document.file_name}:\n"
                                                              f"{ex.__class__.__name__}: {ex}", self._tm)

    def open_file(self):
        if not self._document.document.local.is_downloading_completed:
            return
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', self._document.document.local.path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(self._document.document.local.path)
        else:  # linux variants
            subprocess.call(('xdg-open', self._document.document.local.path))

    def save_project(self):
        if not self._document.document.local.is_downloading_completed:
            return
        self._manager.load_zip_project(self._document.document.local.path)

    def show_in_folder(self):
        if not self._document.document.local.is_downloading_completed:
            return
        match platform.system():
            case 'Windows':
                subprocess.call(['explorer', os.path.split(self._document.document.local.path)[0]])
            case 'Linux':
                subprocess.call(['nautilus', '--browser', os.path.split(self._document.document.local.path)[0]])

    def _on_file_updated(self, file: tg.File):
        if file.id == self._document.document.id:
            self._document.document = file
            if self._document.document.local.is_downloading_completed:
                self._button.image_name = self._extension
                self._button.set_theme()

    def set_theme(self):
        self.setStyleSheet("border: none;")
        for el in [self._button, self._name_label, self._type_label]:
            self._tm.auto_css(el)
