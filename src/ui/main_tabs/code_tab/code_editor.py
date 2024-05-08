import os

from PyQt6.QtGui import QFontMetrics
from PyQt6.Qsci import QsciScintilla, QsciLexer
from PyQtUIkit.core import *
from PyQtUIkit.widgets import KitScintilla
from PyQtUIkit.widgets._widget import _KitWidget

from src.backend.language.languages import LANGUAGES


class CodeEditor(KitScintilla):
    def __init__(self, language):
        super().__init__(language)
        self.main_palette = 'CodeBg'


class CodeFileEditor(CodeEditor):
    fileDeleted = pyqtSignal()

    def __init__(self, path: str):
        self._path = path
        super().__init__(self._detect_language())

        self._mtime = os.path.getmtime(self._path)
        self.textChanged.connect(self._save_file)

        self._file_deleted = False

        self._load_file()

    @property
    def path(self):
        return self._path

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
            self.setText(f.read())

    def _save_file(self):
        if self._file_deleted:
            return
        with open(self._path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(self.text())

    def _check_file_deleted(self):
        self._file_deleted = not os.path.isfile(self._path)

    def _check_file_modified(self):
        if self._file_deleted:
            return
        mtime = os.path.getmtime(self._path)
        if mtime > self._mtime:
            self._mtime = mtime
            self._load_file()

    def showEvent(self, a0):
        super().showEvent(a0)
        self._check_file_deleted()
        self._check_file_modified()
