import os
import platform
import shutil
import subprocess

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFileDialog, QMenu

from side_tabs.telegram.telegram_api import tg
from ui.button import Button
from ui.message_box import MessageBox
from ui.resources import resources


class DocumentWidget(QWidget):
    SAVING = 1
    OPENING = 2

    def __init__(self, tm, document: tg.Document, manager):
        super().__init__()
        self._tm = tm
        self._document = document
        self._manager = manager
        self._saving = 0
        self._path = ''
        self._importing = False

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 5)
        self.setLayout(layout)

        extension = 'unknown_file' if '.' not in self._document.file_name else \
            self._document.file_name[self._document.file_name.rindex('.') + 1:]
        if extension not in resources:
            extension = 'unknown_file'
        self._button = Button(self._tm, extension, css='Menu')
        self._button.setFixedSize(20, 20)
        layout.addWidget(self._button)

        self._name_label = QLabel(self._document.file_name)
        layout.addWidget(self._name_label)
        self._name_label.setMinimumWidth(100)

        self._manager.updateFile.connect(self._on_file_updated)

    def set_theme(self):
        self.setStyleSheet("border: none;")
        for el in [self._button, self._name_label]:
            self._tm.auto_css(el)

    def save(self):
        if '.' in self._document.file_name:
            extension = '.' + self._document.file_name.split('.')[-1]
        else:
            extension = ''
        self._path = QFileDialog.getSaveFileName(caption="Сохранение файла", filter=extension)[0]
        if self._path and not self._path.endswith(extension):
            self._path += extension
        if self._path:
            self._saving = DocumentWidget.SAVING
            if self._document.document.local.is_downloading_completed:
                self._continue_saving()
            else:
                if not self._document.document.local.is_downloading_active:
                    tg.downloadFile(self._document.document.id, 1)

    def open_file(self):
        self._saving = DocumentWidget.OPENING
        if self._document.document.local.is_downloading_completed:
            self._continue_saving()
        else:
            if not self._document.document.local.is_downloading_active:
                tg.downloadFile(self._document.document.id, 1)

    def show_in_folder(self):
        if self._document.document.local.is_downloading_completed:
            self._continue_saving()
        else:
            if not self._document.document.local.is_downloading_active:
                tg.downloadFile(self._document.document.id, 1)
        match platform.system():
            case 'Windows':
                subprocess.call(['explorer', os.path.split(self._document.document.local.path)[0]])
            case 'Linux':
                subprocess.call(['nautilus', '--browser', os.path.split(self._document.document.local.path)[0]])

    def _on_file_updated(self, file: tg.File):
        if file.id == self._document.document.id:
            self._document.document = file
            if self._document.document.local.is_downloading_completed:
                if self._saving:
                    self._continue_saving()

    def _continue_saving(self):
        if self._saving == DocumentWidget.SAVING:
            try:
                shutil.copy(self._document.document.local.path, self._path)
            except Exception as ex:
                MessageBox(MessageBox.Icon.Warning, "Ошибка", f"Не удалось сохранить файл {self._document.file_name}:\n"
                                                              f"{ex.__class__.__name__}: {ex}", self._tm)
        elif self._saving == DocumentWidget.OPENING:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', self._document.document.local.path))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(self._document.document.local.path)
            else:  # linux variants
                subprocess.call(('xdg-open', self._document.document.local.path))
        self._saving = 0

