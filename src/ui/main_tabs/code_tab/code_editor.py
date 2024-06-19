import os
import time

from PyQt6.QtCore import Qt
from PyQtUIkit.core import *
from PyQtUIkit.widgets import KitScintilla, KitVBoxLayout

from src.backend.language.languages import LANGUAGES
from src.ui.main_tabs.code_tab import SearchPanel


class CodeEditor(KitScintilla):
    searchRequested = pyqtSignal(bool)

    def __init__(self, language):
        super().__init__(language)
        self.main_palette = 'CodeBg'

    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        if e.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if e.key() == Qt.Key.Key_F:
                self.searchRequested.emit(True)
        elif e.key() == Qt.Key.Key_Escape:
            self.searchRequested.emit(False)
            
    def dragEnterEvent(self, e):
        e.ignore()


class CodeFileEditor(KitVBoxLayout):
    fileDeleted = pyqtSignal()
    searchRequested = pyqtSignal(bool)

    def __init__(self, path: str):
        self._path = path
        super().__init__()

        self._editor = CodeEditor(self._detect_language())
        self._editor.searchRequested.connect(self._on_search_requested)

        self.search_panel = SearchPanel(self._editor)
        self.search_panel.hide()
        self.addWidget(self.search_panel)
        self.addWidget(self._editor)

        self._mtime = os.path.getmtime(self._path)
        self._editor.textChanged.connect(self._save_file)

        self._file_deleted = False

        self._load_file()

    @property
    def path(self):
        return self._path

    @property
    def searching(self):
        return not self.search_panel.isHidden()

    @searching.setter
    def searching(self, value):
        self.search_panel.setHidden(not value)

    def _detect_language(self):
        for lang in LANGUAGES.values():
            for ext in lang.extensions:
                if self._path.endswith(ext):
                    return lang.name
        return 'txt'

    def _load_file(self):
        if self._file_deleted:
            return
        with open(self._path, encoding='utf-8') as f:
            self._editor.setText(f.read())

    def _save_file(self):
        if self._file_deleted:
            return
        with open(self._path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(self._editor.text())
        self._mtime = time.time()

    def _check_file_deleted(self):
        self._file_deleted = not os.path.isfile(self._path)
        if self._file_deleted:
            self.fileDeleted.emit()

    def _check_file_modified(self):
        if self._file_deleted:
            return
        mtime = os.path.getmtime(self._path)
        if mtime > self._mtime:
            self._mtime = mtime
            print(f"Reloading {self.path} from disk")
            self._load_file()

    def _on_search_requested(self, flag):
        if flag and self._editor.hasSelectedText():
            self.search_panel.search(self._editor.selectedText())
        self.searchRequested.emit(flag)

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self._check_file_deleted()
        self._check_file_modified()

    def showEvent(self, a0):
        super().showEvent(a0)
        self._check_file_deleted()
        self._check_file_modified()
