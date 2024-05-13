from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog

from src.backend.backend_types.build import Build
from src.backend.backend_types.program import PROGRAMS
from src.backend.managers import BackendManager
from src.ui.side_tabs.builds.build_fields import *
from src.ui.side_tabs.builds.commands_list import CommandsList


class BuildEdit(KitScrollArea):
    nameChanged = pyqtSignal(str)

    def __init__(self, bm: BackendManager):
        super().__init__()
        self.bm = bm
        self.sm = bm.sm
        self._build = None
        self._widgets = []

        self.main_palette = 'Bg'
        self.border = 0

        scroll_layout = KitVBoxLayout()
        scroll_layout.spacing = 6
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(scroll_layout)

        self._layout = KitVBoxLayout()
        self._layout.spacing = 6
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_layout.addWidget(self._layout)

        self._cwd_label = KitLabel("Рабочая директория:")
        self._cwd_label.hide()
        scroll_layout.addWidget(self._cwd_label)

        cwd_layout = KitHBoxLayout()
        cwd_layout.spacing = 6
        scroll_layout.addWidget(cwd_layout)

        self._cwd_line = KitLineEdit()
        self._cwd_line.editingFinished.connect(self._on_cwd_changed)
        self._cwd_line.hide()
        cwd_layout.addWidget(self._cwd_line)

        self._cwd_button = KitButton("Обзор")
        self._cwd_button.setFixedSize(60, 24)
        self._cwd_button.clicked.connect(self._select_cwd)
        self._cwd_button.hide()
        cwd_layout.addWidget(self._cwd_button)

        self._utils_widget = CommandsList(self.bm, "Утилиты:", fixed_type=CommandsList.TYPE_UTIL)
        self._utils_widget.setFixedHeight(200)
        self._utils_widget.hide()
        scroll_layout.addWidget(self._utils_widget)

        self._preproc_widget = CommandsList(self.bm, "Перед выполнением:")
        self._preproc_widget.setFixedHeight(200)
        self._preproc_widget.hide()
        scroll_layout.addWidget(self._preproc_widget)

        self._postproc_widget = CommandsList(self.bm, "После выполнения:")
        self._postproc_widget.setFixedHeight(200)
        self._postproc_widget.hide()
        scroll_layout.addWidget(self._postproc_widget)

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self.widget().setFixedWidth(self.width() - 20)

    def clear(self):
        self._layout.clear()
        self._widgets.clear()

    @property
    def current_build(self):
        return self._build

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

    def _load_struct(self, *args: BuildField):
        self.clear()
        for widget in args:
            self._widgets.append(widget)
            self._layout.addWidget(widget)

    def _select_struct(self):
        match self._build.get('type', 'C'):
            case Build.Type.C_EXE:
                self._load_struct(
                    name_edit := LineField('name', '-', "Название:"),
                    LineField('keys', '', "Ключи компилятора:"),
                    LineField('linker_keys', '', "Ключи компоновки:"),
                    CheckboxField('coverage', False, "Coverage"),
                    LineField('app_file', 'app.exe', "Исполняемый файл:"),
                    ProgramField(self.bm, PROGRAMS['gcc'], "Компилятор", checkbox=True),
                    ProgramField(self.bm, PROGRAMS['gcov'], "Gcov", checkbox=True),
                    TreeField('files', self.sm.project.path(), ('.c', '.h'), "Файлы:")
                )
            case Build.Type.C_LIB:
                self._load_struct(
                    name_edit := LineField('name', '-', "Название:"),
                    LineField('keys', '', "Ключи компилятора:"),
                    LineField('linker_keys', '', "Ключи компоновки:"),
                    CheckboxField('dynamic', False, 'Динамическая библиотека'),
                    LineField('lib_file', 'lib.a', "Файл библиотеки:"),
                    ProgramField(self.bm, PROGRAMS['gcc'], "Компилятор", checkbox=True),
                    # TreeField('files', self.sm.project.path(), ('.c', '.h'), "Файлы:")
                )
            case Build.Type.CPP_EXE:
                self._load_struct(
                    name_edit := LineField('name', '-', "Название:"),
                    LineField('keys', '', "Ключи компилятора:"),
                    LineField('linker_keys', '', "Ключи компоновки:"),
                    CheckboxField('coverage', False, "Coverage"),
                    LineField('app_file', 'app.exe', "Исполняемый файл:"),
                    ProgramField(self.bm, PROGRAMS['g++'], "Компилятор", checkbox=True),
                    ProgramField(self.bm, PROGRAMS['gcov'], "Gcov", checkbox=True),
                    # TreeField('files', self.sm.project.path(), ('.cpp', '.h'), "Файлы:")
                )
            case Build.Type.PYTHON:
                self._load_struct(
                    name_edit := LineField('name', '-', "Название:"),
                    ProgramField(self.bm, PROGRAMS['python'], "Интерпретатор"),
                    LineField('file', '', "Файл:"),
                    CheckboxField('coverage', False, "Coverage"),
                )
            case Build.Type.BASH:
                self._load_struct(
                    name_edit := LineField('name', '-', "Название:"),
                    LineField('file', '', "Файл:"),
                )
            case Build.Type.COMMAND:
                self._load_struct(
                    name_edit := LineField('name', '-', "Название:"),
                    LineField('command', '', "Команда:"),
                )
            # case 'report':
            #     self._load_struct(
            #         name_edit := LineField('name', '-', "Название:"),
            #         LineField('file', '', "Файл:"),
            #         LineField('output', '', "Выходной файл:"),
            #     )
            case _:
                self._load_struct(name_edit := LineField('name', '-', "Название:"))

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

        if name_edit is not None:
            name_edit.valueChanged.connect(self.nameChanged.emit)

    def _on_cwd_changed(self):
        if not os.path.isdir(self._cwd_line.text) if os.path.isabs(self._cwd_line.text) else \
                not os.path.isdir(f"{self.sm.project.path()}/{self._cwd_line.text}"):
            self._cwd_line.setText(self._build.get('cwd', '.'))
            if not os.path.isdir(self._cwd_line.text) if os.path.isabs(self._cwd_line.text) else \
                    not os.path.isdir(f"{self.sm.project.path()}/{self._cwd_line.text}"):
                self._cwd_line.setText('.')
        else:
            self._build['cwd'] = self._cwd_line.text

    def _select_cwd(self):
        path = QFileDialog.getExistingDirectory(
            caption="Выберите директорию", directory=os.path.join(self.sm.project.path(), self._cwd_line.text))
        if os.path.isdir(path):
            path = os.path.relpath(path, self.sm.project.path())
            self._build['cwd'] = path
            self._cwd_line.setText(path)
