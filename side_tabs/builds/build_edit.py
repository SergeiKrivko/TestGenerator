from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget

from backend.types.build import Build
from side_tabs.builds.build_fields import *


class BuildEdit(QScrollArea):
    def __init__(self, bm, sm, tm):
        super().__init__()
        self.bm = bm
        self.sm = sm
        self.tm = tm
        self._build = None
        self._widgets = []

        scroll_widget = QWidget()
        self.setWidget(scroll_widget)
        self.setWidgetResizable(True)

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignTop)
        self._layout.setContentsMargins(0, 0, 0, 0)
        scroll_widget.setLayout(self._layout)

    def clear(self):
        for _ in range(self._layout.count()):
            self._layout.takeAt(0)
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
                    LineField(self.tm, 'name', '-', "Название:"),
                    LineField(self.tm, 'keys', '', "Ключи компилятора:"),
                    LineField(self.tm, 'linker_keys', '', "Ключи компоновки:"),
                    LineField(self.tm, 'app_file', 'app.exe', "Исполняемый файл:"),
                    TreeField(self.tm, 'files', self.sm.project.path(), ('.c', '.h'), "Файлы:"))

    def set_theme(self):
        self.setStyleSheet(self.tm.scroll_area_css(palette='Bg', border=False))
        for el in self._widgets:
            el.set_theme()


