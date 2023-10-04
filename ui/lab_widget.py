import os.path

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QDialog, QLineEdit, \
    QPushButton, QMenuBar, QMenu

from backend.types.project import Project
from backend.settings_manager import SettingsManager
from backend.backend_manager import BackendManager


class LabWidget(QMenuBar):
    def __init__(self, tm, sm: SettingsManager, bm: BackendManager):
        super().__init__()
        self.tm = tm
        self.bm = bm
        self.sm = sm

        self._project = None
        self._menu = QMenu()

        self.sm.mainProjectChanged.connect(self.full_update)
        self.sm.projectChanged.connect(self.update_current)

    def full_update(self):
        self._project = self.sm.main_project
        if not isinstance(self._project, Project):
            return
        self.clear()
        self._menu = ProjectMenu(self.tm, self.bm, self._project, self)
        self._menu.setMaximumWidth(200)
        self._menu.updateRequested.connect(self.full_update)
        self.set_theme()
        self.addMenu(self._menu)

    def update_current(self):
        self._menu.setTitle(os.path.relpath(self.sm.project.path(), self._project.path()))

    def set_theme(self):
        self.setFont(self.tm.font_medium)
        self.setStyleSheet(f"""
QMenuBar {{
    border: none;
}}

QMenuBar::item {{
    {self.tm.base_css(palette='Bg')}
    padding: 4px 16px;
}}

QMenuBar::item:selected {{
    background: {self.tm['BgHoverColor']};
}}

QMenuBar::item:pressed {{
    background: {self.tm['BgSelectedColor']};
}}""")
        if hasattr(self._menu, 'set_theme'):
            self._menu.set_theme()


class ProjectMenu(QMenu):
    updateRequested = pyqtSignal()

    def __init__(self, tm, bm, project: Project, parent):
        super().__init__(parent)

        self._tm = tm
        self._bm = bm
        self._project = project
        self._keys = []
        self._menu = []
        self._projects = []

        self._open_action = self.addAction("Открыть")
        self._open_action.triggered.connect(lambda: self._bm.open_project(self._project))
        self._new_child_action = self.addAction("Новый подпроект")
        self._new_child_action.triggered.connect(self.new_subproject)
        self.setDefaultAction(self._open_action)

        if isinstance(parent, ProjectMenu):
            self.setTitle(os.path.relpath(self._project.path(), parent._project.path()))
            self._delete_action = self.addAction("Удалить")
            self._delete_action.triggered.connect(self.new_subproject)
        else:
            self.setTitle(os.path.basename(self._project.path()))

        self.addSeparator()

        for key, item in project.children().items():
            menu = ProjectMenu(self._tm, self._bm, item, self)
            menu.updateRequested.connect(self.updateRequested.emit)
            self._menu.append(menu)
            self._keys.append(key)
            self._projects.append(item)
            self.addMenu(menu)

    def new_subproject(self):
        dialog = NewSubProjectDialog(self._tm)
        if dialog.exec():
            self._project.add_child(dialog.line_edit.text())
            self.updateRequested.emit()

    def set_theme(self):
        self.setFont(self._tm.font_medium)
        self.setStyleSheet(f"""
QMenu {{
    color: {self._tm['TextColor']};
    background-color: {self._tm['BgColor']};
    border: 1px solid {self._tm['BorderColor']};
    border-radius: 6px;
    spacing: 4px;
    padding: 3px;
}}

QMenu::item {{
    border: 0px solid {self._tm['BorderColor']};
    background-color: transparent;
    border-radius: 8px;
    padding: 4px 16px;
}}

QMenu::item:selected {{
    background-color: {self._tm['BgHoverColor']};
}}
QMenu::separator {{
    height: 1px;
    background: {self._tm['BorderColor']};
    margin: 4px 10px;
}}""")
        for el in self._menu:
            el.set_theme()


class NewSubProjectDialog(QDialog):
    def __init__(self, tm):
        super().__init__()
        self.tm = tm

        layout = QVBoxLayout()

        self.label = QLabel("Название подпроекта:")
        layout.addWidget(self.label)

        self.line_edit = QLineEdit()
        self.line_edit.setMinimumSize(200, 24)
        layout.addWidget(self.line_edit)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)
        layout.addLayout(buttons_layout)

        self.button_ok = QPushButton("Ок")
        self.button_ok.setFixedSize(80, 22)
        self.button_ok.clicked.connect(self.accept)
        buttons_layout.addWidget(self.button_ok)

        self.button_cancel = QPushButton("Отмена")
        self.button_cancel.setFixedSize(80, 22)
        self.button_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(self.button_cancel)

        self.setLayout(layout)
        self.set_theme()

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        for el in [self.label, self.line_edit, self.button_cancel, self.button_ok]:
            self.tm.auto_css(el)

