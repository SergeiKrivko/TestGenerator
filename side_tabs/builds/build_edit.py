import os

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QScrollArea, QPushButton, QFileDialog

from backend.backend_types.build import Build
from backend.backend_types.program import PROGRAMS
from side_tabs.builds.build_fields import *
from side_tabs.builds.commands_list import CommandsList


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

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._scroll_widget.setLayout(layout)

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self._layout)

        self._cwd_label = QLabel("Рабочая директория:")
        self._cwd_label.hide()
        layout.addWidget(self._cwd_label)

        cwd_layout = QHBoxLayout()
        layout.addLayout(cwd_layout)

        self._cwd_line = QLineEdit()
        self._cwd_line.editingFinished.connect(self._on_cwd_changed)
        self._cwd_line.hide()
        cwd_layout.addWidget(self._cwd_line)

        self._cwd_button = QPushButton("Обзор")
        self._cwd_button.setFixedSize(60, 22)
        self._cwd_button.clicked.connect(self._select_cwd)
        self._cwd_button.hide()
        cwd_layout.addWidget(self._cwd_button)

        self._utils_widget = CommandsList(self.sm, self.bm, self.tm, "Утилиты:", fixed_type=CommandsList.TYPE_UTIL)
        self._utils_widget.setFixedHeight(200)
        self._utils_widget.set_theme()
        self._utils_widget.hide()
        layout.addWidget(self._utils_widget)

        self._preproc_widget = CommandsList(self.sm, self.bm, self.tm, "Перед выполнением:")
        self._preproc_widget.setFixedHeight(200)
        self._preproc_widget.set_theme()
        self._preproc_widget.hide()
        layout.addWidget(self._preproc_widget)

        self._postproc_widget = CommandsList(self.sm, self.bm, self.tm, "После выполнения:")
        self._postproc_widget.setFixedHeight(200)
        self._postproc_widget.set_theme()
        self._postproc_widget.hide()
        layout.addWidget(self._postproc_widget)

        self._wsl_widget = CheckboxField(self.tm, 'wsl', False, "Использовать WSL")
        self._wsl_widget.hide()
        layout.addWidget(self._wsl_widget)

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
            self._build['utils'] = self._utils_widget.store()
            self._build['preproc'] = self._preproc_widget.store()
            self._build['postproc'] = self._postproc_widget.store()
            if os.name == 'nt':
                self._wsl_widget.store(self._build)

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
                    ProgramField(self.sm, self.tm, PROGRAMS['gcc'], "Компилятор", checkbox=True),
                    ProgramField(self.sm, self.tm, PROGRAMS['gcov'], "Gcov", checkbox=True),
                    TreeField(self.tm, 'files', self.sm.project.path(), ('.c', '.h'), "Файлы:"))
            case 'C++':
                self._load_struct(
                    name_edit := LineField(self.tm, 'name', '-', "Название:"),
                    LineField(self.tm, 'keys', '', "Ключи компилятора:"),
                    LineField(self.tm, 'linker_keys', '', "Ключи компоновки:"),
                    CheckboxField(self.tm, 'coverage', False, "Coverage"),
                    LineField(self.tm, 'app_file', 'app.exe', "Исполняемый файл:"),
                    ProgramField(self.sm, self.tm, PROGRAMS['g++'], "Компилятор", checkbox=True),
                    ProgramField(self.sm, self.tm, PROGRAMS['gcov'], "Gcov", checkbox=True),
                    TreeField(self.tm, 'files', self.sm.project.path(), ('.cpp', '.h'), "Файлы:"))
            case 'python':
                self._load_struct(
                    name_edit := LineField(self.tm, 'name', '-', "Название:"),
                    ProgramField(self.sm, self.tm, PROGRAMS['python'], "Интерпретатор"),
                    LineField(self.tm, 'file', '', "Файл:"),
                )
            case 'python_coverage':
                self._load_struct(
                    name_edit := LineField(self.tm, 'name', '-', "Название:"),
                    ProgramField(self.sm, self.tm, PROGRAMS['python_coverage'], "Интерпретатор"),
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
            case 'report':
                self._load_struct(
                    name_edit := LineField(self.tm, 'name', '-', "Название:"),
                    LineField(self.tm, 'file', '', "Файл:"),
                    LineField(self.tm, 'output', '', "Выходной файл:"),
                )
            case _:
                self._load_struct(name_edit := LineField(self.tm, 'name', '-', "Название:"))

        self._cwd_label.show()
        self._cwd_line.show()
        self._cwd_button.show()
        self._utils_widget.show()
        self._preproc_widget.show()
        self._postproc_widget.show()
        # if os.name == 'nt':
        #     self._wsl_widget.show()

        self._cwd_line.setText(self._build.get('cwd', '.'))
        self._utils_widget.load(self._build.get('utils', []))
        self._preproc_widget.load(self._build.get('preproc', []))
        self._postproc_widget.load(self._build.get('postproc', []))
        self._wsl_widget.load(self._build)

        if name_edit is not None:
            name_edit.valueChanged.connect(self.nameChanged.emit)

    def _on_cwd_changed(self):
        if not os.path.isdir(self._cwd_line.text()) if os.path.isabs(self._cwd_line.text()) else \
                not os.path.isdir(f"{self.sm.project.path()}/{self._cwd_line.text()}"):
            self._cwd_line.setText(self._build.get('cwd', '.'))
            if not os.path.isdir(self._cwd_line.text()) if os.path.isabs(self._cwd_line.text()) else \
                    not os.path.isdir(f"{self.sm.project.path()}/{self._cwd_line.text()}"):
                self._cwd_line.setText('.')
        else:
            self._build['cwd'] = self._cwd_line.text()

    def _select_cwd(self):
        path = QFileDialog.getExistingDirectory(
            caption="Выберите директорию", directory=os.path.join(self.sm.project.path(), self._cwd_line.text()))
        if os.path.isdir(path):
            path = os.path.relpath(path, self.sm.project.path())
            self._build['cwd'] = path
            self._cwd_line.setText(path)

    def set_theme(self):
        self.setStyleSheet(self.tm.scroll_area_css(palette='Bg', border=False))
        for el in self._widgets:
            el.set_theme()
        for el in [self._cwd_button, self._cwd_line, self._cwd_label]:
            self.tm.auto_css(el)
        self._preproc_widget.set_theme()
        self._postproc_widget.set_theme()
        self._wsl_widget.set_theme()
