import os.path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMenu, QCheckBox

from backend.backend_types.project import Project
from backend.settings_manager import SettingsManager
from backend.managers import BackendManager
from ui.custom_dialog import CustomDialog


class LabWidget(QPushButton):
    def __init__(self, tm, sm: SettingsManager, bm: BackendManager):
        super().__init__()
        self.tm = tm
        self.bm = bm
        self.sm = sm

        self.setFixedHeight(26)
        self.setMinimumWidth(200)

        self._project = None
        self._menu = QMenu()

        self.sm.mainProjectChanged.connect(self.full_update)
        self.sm.projectChanged.connect(self.update_current)

    def full_update(self):
        self._project = self.sm.main_project
        if not isinstance(self._project, Project):
            return
        self._menu = ProjectMenu(self.tm, self.bm, self._project, self)
        self._menu.setMaximumWidth(200)
        self._menu.updateRequested.connect(self.full_update)
        self.set_theme()
        self.setMenu(self._menu)

    def update_current(self):
        self.setText(os.path.relpath(self.sm.project.path(), self._project.path()))

    def set_theme(self):
        self.tm.auto_css(self, palette='Bg', border=True, padding=True)
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
            self._delete_action.triggered.connect(self.delete_subproject)
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

    def delete_subproject(self):
        dialog = DeleteSubProjectDialog(self._tm, self._project)
        if dialog.exec():
            self._bm._sm.delete_project(self._project, directory=dialog.checkbox.isChecked())
            self.updateRequested.emit()

    def set_theme(self):
        self.setFont(self._tm.font_medium)
        self._tm.auto_css(self, palette='Bg')
        for el in self._menu:
            el.set_theme()


class NewSubProjectDialog(CustomDialog):
    def __init__(self, tm):
        super().__init__(tm, "Создание подпроекта", True)
        super().set_theme()

        layout = QVBoxLayout()

        self.label = QLabel("Название подпроекта:")
        layout.addWidget(self.label)

        self.line_edit = QLineEdit()
        self.line_edit.setMinimumSize(200, 24)
        layout.addWidget(self.line_edit)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
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


class DeleteSubProjectDialog(CustomDialog):
    def __init__(self, tm, project):
        super().__init__(tm, "Удаление подпроекта", True)
        super().set_theme()
        self.project = project

        self.setFixedSize(340, 140)

        layout = QVBoxLayout()

        self.checkbox = QCheckBox()
        self.checkbox.setText("Удалить папку подпроекта")
        layout.addWidget(self.checkbox)

        self.label = QLabel("Эта операция приведет к безвозвратному удалению данных подпроекта. Вы действительно "
                            f"хотите удалить подпроект \"{project.name()}\"?")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
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
        for el in [self.label, self.button_cancel, self.button_ok, self.checkbox]:
            self.tm.auto_css(el)
