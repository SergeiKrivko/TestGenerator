from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea

from backend.types.build import Build
from side_tabs.builds.build_fields import *


class BuildEdit(QScrollArea):
    nameChanged = pyqtSignal(str)

    def __init__(self, bm, sm, tm):
        super().__init__()
        self.bm = bm
        self.sm = sm
        self.tm = tm
        self._build = None
        self._widgets = []

        self._scroll_widget = QWidget()
        self.setWidget(self._scroll_widget)
        self.setWidgetResizable(True)

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignTop)
        self._scroll_widget.setLayout(self._layout)

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self._scroll_widget.setFixedWidth(self.width() - 20)

    def clear(self):
        for el in self._widgets:
            el.setParent(None)
        self._widgets.clear()

    def open(self, build: Build | None):
        self.store_build()
        self._build = build
        if self._build is None:
            return
        self._select_struct()
        for el in self._widgets:
            el.load(build)

    def store_build(self):
        if self._build is not None:
            for el in self._widgets:
                el.store(self._build)

    def _load_struct(self, *args: BuildField):
        self.clear()
        for widget in args:
            self._widgets.append(widget)
            self._layout.addWidget(widget)
        self.set_theme()

    def _select_struct(self):
        match self._build.get('type', 'C'):
            case 'C':
                self._load_struct(
                    name_edit := LineField(self.tm, 'name', '-', "Название:"),
                    LineField(self.tm, 'keys', '', "Ключи компилятора:"),
                    LineField(self.tm, 'linker_keys', '', "Ключи компоновки:"),
                    CheckboxField(self.tm, 'coverage', False, "Coverage"),
                    LineField(self.tm, 'app_file', 'app.exe', "Исполняемый файл:"),
                    ProgramField(self.sm, self.tm, 'compiler', "Компилятор", 'gcc.exe'),
                    TreeField(self.tm, 'files', self.sm.project.path(), ('.c', '.h'), "Файлы:"))
            case 'python':
                self._load_struct(
                    name_edit := LineField(self.tm, 'name', '-', "Название:"),
                    ProgramField(self.sm, self.tm, 'interpreter', "Интерпретатор", 'python.exe'),
                    LineField(self.tm, 'file', '', "Файл:"),
                )
            case 'python_coverage':
                self._load_struct(
                    name_edit := LineField(self.tm, 'name', '-', "Название:"),
                    ProgramField(self.sm, self.tm, 'interpreter', "Интерпретатор", 'coverage.exe'),
                    LineField(self.tm, 'file', '', "Файл:"),
                )
            case 'script':
                self._load_struct(
                    name_edit := LineField(self.tm, 'name', '-', "Название:"),
                    LineField(self.tm, 'file', '', "Файл:"),
                )
            case 'bash':
                self._load_struct(
                    name_edit := LineField(self.tm, 'name', '-', "Название:"),
                    LineField(self.tm, 'file', '', "Файл:"),
                )
            case 'command':
                self._load_struct(
                    name_edit := LineField(self.tm, 'name', '-', "Название:"),
                    LineField(self.tm, 'command', '', "Команда:"),
                )
            case _:
                self._load_struct(name_edit := LineField(self.tm, 'name', '-', "Название:"))
        if name_edit is not None:
            name_edit.valueChanged.connect(self.nameChanged.emit)

    def set_theme(self):
        self.setStyleSheet(self.tm.scroll_area_css(palette='Bg', border=False))
        for el in self._widgets:
            el.set_theme()


