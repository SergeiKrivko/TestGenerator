import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QFileDialog
from PyQtUIkit.core import KitFont
from PyQtUIkit.themes import ThemeManager
from PyQtUIkit.widgets import *
from qasync import asyncSlot

from src.backend.backend_types.project import Project
from src.backend.language.languages import LANGUAGES, PROJECT_LANGUAGES
from src.backend.managers import BackendManager


class ProjectsWidget(KitLayoutButton):
    WIDTH = 190

    def __init__(self, bm: BackendManager):
        super().__init__()
        self._bm = bm
        self._bm.projects.recentChanged.connect(self._load_current)

        self.main_palette = 'Menu'
        self.border = 0
        self.padding = 5
        self.radius = 8
        self.setFixedSize(ProjectsWidget.WIDTH, 32)

        self._icon_widget = KitIconWidget('line-help')
        self._icon_widget.setFixedSize(24, 24)
        self.addWidget(self._icon_widget)

        self._menu = _ProjectsMenu(self, self._bm)
        self.setMenu(self._menu)

        self._label = KitLabel()
        self.addWidget(self._label)

        icon = KitIconWidget('line-chevron-down')
        icon.setFixedSize(18, 18)
        self.addWidget(icon)

    def _load_current(self):
        lang = LANGUAGES.get(self._bm.projects.current.get('language', '').lower())
        self._icon_widget.icon = 'line-help' if lang is None else lang.icon
        self._label.text = self._bm.projects.current.name()


class _ProjectsMenu(KitMenu):
    HEIGHT = 600

    def __init__(self, parent, bm: BackendManager):
        super().__init__(parent)
        self._bm = bm
        self._bm.projects.recentChanged.connect(self._load_projects)
        self.setFixedWidth(350)
        self.setMaximumHeight(_ProjectsMenu.HEIGHT)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._scroll_area = KitScrollArea()
        self._scroll_area.radius = 6
        self._scroll_area.border = 1
        layout.addWidget(self._scroll_area, 100)

        scroll_layout = KitVBoxLayout()
        scroll_layout.padding = 5
        scroll_layout.spacing = 3
        self._scroll_area.setWidget(scroll_layout)

        self._button_new = _Button('Новый проект', 'line-document')
        self._button_new.border = 0
        self._button_new.on_click = lambda: self._new_project()
        scroll_layout.addWidget(self._button_new)

        self._button_open = _Button('Открыть проект', 'line-folder')
        self._button_open.border = 0
        self._button_open.on_click = lambda: self._open_project()
        scroll_layout.addWidget(self._button_open)

        self._button_light_edit = _Button('LightEdit', 'line-text')
        self._button_light_edit.border = 0
        # self._button_light_edit.on_click = lambda: self._open_project()
        scroll_layout.addWidget(self._button_light_edit)

        scroll_layout.addWidget(KitHSeparator())

        self._projects_layout = KitVBoxLayout()
        scroll_layout.addWidget(self._projects_layout)

        self._load_projects()

    def _load_projects(self):
        self.close()
        self._projects_layout.clear()
        self._scroll_area.setFixedHeight(10)
        for proj in self._bm.projects.recent:
            self._projects_layout.addWidget(item := _ProjectItem(self._bm, proj))
            if self._bm.projects.current and proj.path() == self._bm.projects.current.path():
                item.setChecked(True)
        self._scroll_area.setFixedHeight(min(_ProjectsMenu.HEIGHT, self._scroll_area.height() +
                                             self._scroll_area.verticalScrollBar().maximum()))

    @asyncSlot()
    async def _new_project(self):
        dialog = NewProjectDialog(self, self._bm)
        if dialog.exec():
            proj = await self._bm.projects.new(dialog.path)
            proj.set('func_tests_in_project', dialog.func_tests_in_project)
            proj.set('name', dialog.proj_name)
            proj.set('language', dialog.language)

    @asyncSlot()
    async def _open_project(self):
        project_path = '~' if self._bm.projects.current is None else self._bm.projects.current.path()
        path = os.path.abspath(QFileDialog.getExistingDirectory(directory=project_path))
        if not path:
            return
        if path in [proj.path() for proj in self._bm.projects.recent]:
            await self._bm.projects.open(path)
        elif os.path.isdir(os.path.join(path, Project.TEST_GENERATOR_DIR) or
                           KitDialog.question(self, f"Создать новый проект \"{path}\"?")) == 'Yes':
            await self._bm.projects.new(path, language=self._detect_project_lang(path))

    @staticmethod
    def _detect_project_lang(path):
        for lang_name in PROJECT_LANGUAGES:
            lang = LANGUAGES.get(lang_name)
            if os.path.isfile(f'{path}/main{lang.extensions[0]}'):
                return lang.name

        counts = {lang_name: 0 for lang_name in PROJECT_LANGUAGES}
        for _, _, files in os.walk(path):
            for filename in files:
                for lang_name in PROJECT_LANGUAGES:
                    lang = LANGUAGES.get(lang_name)
                    if filename.endswith(lang.extensions[0]):
                        counts[lang_name] += 1
                        break

        return max(counts, key=counts.get)

    def _apply_theme(self):
        super()._apply_theme()
        self._scroll_area._apply_theme()
        self._scroll_area.setFixedHeight(min(_ProjectsMenu.HEIGHT, self._scroll_area.height() +
                                             self._scroll_area.verticalScrollBar().maximum()))

    def _apply_lang(self):
        self._scroll_area._apply_lang()

    def _set_tm(self, tm: ThemeManager):
        super()._set_tm(tm)
        self._scroll_area._set_tm(tm)


class _Button(KitLayoutButton):
    HEIGHT = 24

    def __init__(self, text: str, icon: str):
        super().__init__()
        self.setFixedHeight(_Button.HEIGHT)
        self._text = text
        self.padding = 3
        self.border = 0

        self._icon_widget = KitIconWidget(icon)
        self._icon_widget.setFixedSize(_Button.HEIGHT - 6, _Button.HEIGHT - 6)
        self.addWidget(self._icon_widget)

        self._name_label = KitLabel(self._text)
        self.addWidget(self._name_label)


class _ProjectItem(KitLayoutButton):
    HEIGHT = 40

    def __init__(self, bm: BackendManager, project: Project):
        super().__init__()
        self._bm = bm
        self.setFixedHeight(_ProjectItem.HEIGHT)
        self._project = project
        self.setCheckable(True)
        self.on_click = lambda: self._on_clicked()
        self.padding = 4
        self.border = 0

        lang = LANGUAGES.get(self._project.get('language', '').lower())
        self._icon_widget = KitIconWidget('line-help' if lang is None else lang.icon)
        self._icon_widget.setFixedSize(_ProjectItem.HEIGHT - 8, _ProjectItem.HEIGHT - 8)
        self.addWidget(self._icon_widget)

        right_layout = KitVBoxLayout()
        right_layout.spacing = 3
        self.addWidget(right_layout)

        self._name_label = KitLabel(self._project.name())
        right_layout.addWidget(self._name_label)

        self._path_label = KitLabel(self._project.path())
        self._path_label.font_size = KitFont.Size.SMALL
        right_layout.addWidget(self._path_label)

    @asyncSlot()
    async def _on_clicked(self):
        self.setChecked(True)
        await self._bm.projects.open(self._project)


class NewProjectDialog(KitDialog):
    def __init__(self, parent, bm: BackendManager):
        super().__init__(parent)
        self._bm = bm
        self.name = 'Новый проект'
        self.button_close = False
        self.setFixedWidth(300)

        main_layout = KitVBoxLayout()
        main_layout.padding = 10
        main_layout.spacing = 6
        self.setWidget(main_layout)
        self.labels = []

        self.checkbox = KitCheckBox("Из существующей папки")
        main_layout.addWidget(self.checkbox)

        layout = KitHBoxLayout()
        layout.spacing = 2
        self.dir_edit = KitLineEdit()
        self.dir_edit.setFixedHeight(22)
        layout.addWidget(self.dir_edit)

        self.dir_button = KitButton("Обзор")
        self.dir_button.on_click = self.set_path
        self.dir_button.setFixedSize(50, 22)
        layout.addWidget(self.dir_button)
        main_layout.addWidget(layout)

        label = KitLabel("Название проекта:")
        self.labels.append(label)
        main_layout.addWidget(label)

        self.proj_name_edit = KitLineEdit()
        main_layout.addWidget(self.proj_name_edit)

        layout = KitHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(layout)

        label = KitLabel("Язык:")
        self.labels.append(label)
        layout.addWidget(label)

        self.lang_edit = KitComboBox()
        self.lang_edit.addItems(PROJECT_LANGUAGES)
        layout.addWidget(self.lang_edit)

        self.save_tests_checkbox = KitCheckBox("Сохранять тесты в папке проекта")
        main_layout.addWidget(self.save_tests_checkbox)

        button_layout = KitHBoxLayout()
        button_layout.spacing = 6
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(button_layout)

        self.button_ok = KitButton("Ок")
        self.button_ok.setDisabled(True)
        self.dir_edit.textChanged.connect(lambda: self.button_ok.setDisabled(not os.path.isdir(self.dir_edit.text)))
        self.button_ok.setFixedSize(70, 24)
        self.button_ok.clicked.connect(self.accept)
        button_layout.addWidget(self.button_ok)

        self.button_cancel = KitButton("Отмена")
        self.button_cancel.setFixedSize(70, 24)
        self.button_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.button_cancel)

    def set_path(self):
        project_path = '~' if self._bm.projects.current.path() is None else self._bm.projects.current.path()
        path = QFileDialog.getExistingDirectory(directory=self.dir_edit.text if os.path.isdir(
            self.dir_edit.text) else project_path)
        self.dir_edit.setText(path)
        if self.checkbox.isChecked():
            self.proj_name_edit.setText(os.path.basename(path))

    @property
    def path(self):
        if self.checkbox.isChecked():
            return self.dir_edit.text
        return os.path.join(self.dir_edit.text, self.proj_name_edit.text)

    @property
    def language(self):
        return self.lang_edit.currentValue()

    @property
    def proj_name(self):
        return self.proj_name_edit.text

    @property
    def func_tests_in_project(self):
        return self.save_tests_checkbox.state
