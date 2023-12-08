import os

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QFileDialog, \
    QLabel, QLineEdit, QCheckBox, QMessageBox, QComboBox

from backend.backend_manager import BackendManager
from backend.backend_types.project import Project
from backend.settings_manager import SettingsManager
from language.languages import PROJECT_LANGUAGES, languages
from ui.custom_dialog import CustomDialog
from ui.message_box import MessageBox
from ui.options_window import OptionsWidget
from ui.side_panel_widget import SidePanelWidget

LANGUAGES = PROJECT_LANGUAGES
LANGUAGE_ICONS = {key: f"files/{languages[key]['files'][0][1:]}" for key in PROJECT_LANGUAGES}
LANGUAGE_ICONS[None] = 'icons/unknown_file'


class ProjectWidget(SidePanelWidget):
    jump_to_code = pyqtSignal(str)

    def __init__(self, sm: SettingsManager, bm: BackendManager, tm):
        super(ProjectWidget, self).__init__(sm, tm, 'Проекты', ['add', 'delete', 'rename', 'to_zip', 'from_zip'])
        self.bm = bm

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self.open_project)
        left_layout.addWidget(self.list_widget)

        self.buttons['add'].clicked.connect(self.new_project)
        self.buttons['delete'].clicked.connect(self.delete_project)
        self.buttons['rename'].clicked.connect(self.rename_project)
        self.buttons['to_zip'].clicked.connect(self.project_to_zip)
        self.buttons['from_zip'].clicked.connect(self.project_from_zip)

        self.setLayout(left_layout)

        self.dialog = None

        self.bm.finishChangingProject.connect(self.update_projects)
        self._opening_project = False

        self.update_projects()

    def select_project(self, project: Project):
        for i in range(self.list_widget.count()):
            if self.list_widget.item(i).project == project:
                self.list_widget.setCurrentRow(i)
                break

    def find_project(self, path):
        path, _ = os.path.split(path)
        while True:
            for key, item in self.sm.projects.items():
                if not os.path.isdir(item.name()):
                    continue
                if os.path.samefile(path, item):
                    self.select_project(key)
                    return True
            if path == (path := os.path.split(path)[0]):
                break
        return False

    def update_projects(self):
        self._opening_project = True
        self.list_widget.clear()
        for pr in self.sm.projects.values():
            item = ProjectListWidgetItem(pr, self.tm, LANGUAGE_ICONS.get(pr.get('language'), 'icons/unknown_file'))
            item.setFont(self.tm.font_medium)
            item.set_icon()
            self.list_widget.addItem(item)
            if self.sm.project == pr:
                self.list_widget.setCurrentItem(item)
        self.list_widget.sortItems()
        self._opening_project = False
        self.select_project(self.sm.main_project)

    def rename_project(self):
        self.dialog = RenameProjectDialog(self.sm.project.name(), self.tm)
        if self.dialog.exec():
            new_name = self.dialog.line_edit.text()
            if new_name in self.sm.projects:
                MessageBox(MessageBox.Icon.Warning, "Переименование проекта",
                           f"Проект {new_name} уже существует. Переименование невозможно", self.tm)
            else:
                self.sm.rename_project(new_name)
                self.update_projects()

    def delete_project(self):
        dialog = DeleteProjectDialog(self.sm.main_project.name(), self.tm)
        if dialog.exec():
            self.sm.delete_main_project(directory=dialog.result() == DeleteProjectDialog.DELETE_ALL,
                                        data=dialog.result() == DeleteProjectDialog.DELETE_DATA)
            self.update_projects()

    def new_project(self):
        dialog = NewProjectDialog(self.sm, self.tm)
        if dialog.exec():
            project_name = dialog.options_widget['Название проекта:']
            path = dialog.dir_edit.text()
            if not dialog.checkbox.isChecked():
                path = os.path.join(path, project_name)
                os.makedirs(path, exist_ok=True)

            project = self.sm.add_main_project(path)
            self.update_projects()
            self.select_project(project)

            project['language'] = dialog.options_widget.widgets["Язык:"].currentText()
            project['func_tests_in_project'] = dialog.options_widget["Сохранять тесты в папке проекта"]
            self.update_projects()

    def open_project(self, forced=False):
        if self._opening_project:
            return
        if self.list_widget.currentItem() is None:
            return
        if self.list_widget.currentItem().project == self.sm.main_project:
            return
        print(f"ProjectWidget: open({repr(self.list_widget.currentItem().project.path())})")
        self.bm.open_main_project(self.list_widget.currentItem().project)

    def project_to_zip(self):
        path, _ = QFileDialog.getSaveFileName(None, "Выберите путь", self.sm.project.path() + '.TGProject.7z',
                                              'TestGenerator ZIP projects (*.TGProject.7z)')
        if not path:
            return
        if not path.endswith('.TGProject.7z'):
            path += '.TGProject.7z'

        self.bm.project_to_zip(path)

    def project_from_zip(self, path=''):
        if not os.path.isfile(path):
            path, _ = QFileDialog.getOpenFileName(
                None, "Выберите проект для распаковки",
                self.sm.get_general('zip_path', self.sm.project.path() if self.sm.project else os.getcwd()),
                '7zip (*.TGProject.7z)')
        if not path or not os.path.isfile(path):
            return
        self.sm.set_general('zip_path', os.path.split(path)[0])
        dialog = ProjectFromZipDialog(
            os.path.basename(path)[:-len('.TGProject.7z')],
            os.path.split(self.sm.project.path() if self.sm.project else os.getcwd())[0], self.tm)
        if dialog.exec():
            if dialog.line_edit.text() in self.sm.projects:
                MessageBox(MessageBox.Icon.Warning, 'Распаковка проекта',
                           f"Проект {dialog.line_edit.text()} уже существует. "
                           f"Невозможно создать новый проект с таким же именем.", self.tm)
            elif dialog.path_edit.text() in self.sm.projects:
                MessageBox(MessageBox.Icon.Warning, 'Распаковка проекта',
                           f"Директория {dialog.path_edit.text()} не существует. Невозможно создать проект.", self.tm)
            else:
                project_path = f"{dialog.path_edit.text()}/{dialog.line_edit.text()}"

                self.bm.project_from_zip(path, project_path, True)

    def command(self, zip=None):
        if zip is not None:
            self.project_from_zip(zip)

    def set_theme(self):
        super().set_theme()
        self.list_widget.setStyleSheet(self.tm.list_widget_css('Main'))
        for i in range(self.list_widget.count()):
            self.list_widget.item(i).set_icon()

    def remove_temp_projects(self):
        pass
        # for el in self.temp_project:
        #     self.sm.delete_project(el, main_dir=False)
        # self.temp_project.clear()
        # self.sm.set_general('temp_projects', '[]')


class ProjectListWidgetItem(QListWidgetItem):
    def __init__(self, project: Project, tm, icon):
        super(ProjectListWidgetItem, self).__init__()
        self.project = project
        self.setText(str(os.path.basename(self.project.name())))
        self._tm = tm
        self._icon = icon

    def set_icon(self):
        self.setIcon(QIcon(self._tm.get_image(self._icon)))


class RenameProjectDialog(CustomDialog):
    def __init__(self, path, tm):
        super(RenameProjectDialog, self).__init__(tm, "Переименование проекта")
        self.path = path

        self.setFixedWidth(220)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(label := QLabel(f"Переименовать проект {os.path.basename(self.path)} в:"))

        self.line_edit = QLineEdit()
        self.line_edit.setText(os.path.basename(self.path))
        self.line_edit.setFixedHeight(24)
        self.line_edit.setMinimumWidth(200)
        layout.addWidget(self.line_edit)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(5)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.button_ok = QPushButton("Ok")
        self.button_ok.setFixedSize(80, 24)
        buttons_layout.addWidget(self.button_ok)
        self.button_ok.clicked.connect(self.accept)
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.setFixedSize(80, 24)
        buttons_layout.addWidget(self.button_cancel)
        self.button_cancel.clicked.connect(self.reject)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        super().set_theme()
        for el in [self.line_edit, self.button_ok, self.button_cancel, label]:
            tm.auto_css(el)


class DeleteProjectDialog(CustomDialog):
    DELETE_FROM_LIST = 0
    DELETE_DATA = 1
    DELETE_ALL = 2

    def __init__(self, name, tm):
        super(DeleteProjectDialog, self).__init__(tm, "Удаление проекта")
        self.name = name
        self.setFixedSize(350, 170)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        self._combo_box = QComboBox()
        self._combo_box.addItems(['Удалить проект из списка', 'Удалить данные проекта', 'Полностью удалить проект'])
        self._combo_box.currentIndexChanged.connect(self._on_item_changed)
        layout.addWidget(self._combo_box)
        tm.auto_css(self._combo_box)

        self._label = QLabel()
        self._label.setWordWrap(True)
        self._label.setFont(tm.font_medium)
        layout.addWidget(self._label)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(5)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.button_yes = QPushButton("Да")
        self.button_yes.setFixedSize(80, 24)
        buttons_layout.addWidget(self.button_yes)
        self.button_yes.clicked.connect(self.accept)
        self.button_no = QPushButton("Нет")
        self.button_no.setFixedSize(80, 24)
        buttons_layout.addWidget(self.button_no)
        self.button_no.clicked.connect(self.reject)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        super().set_theme()
        self.button_yes.setStyleSheet(tm.button_css())
        self.button_no.setFont(tm.font_medium)
        self.button_no.setStyleSheet(tm.button_css())
        self.button_no.setFont(tm.font_medium)

        self._on_item_changed()

    def _on_item_changed(self):
        match self._combo_box.currentIndex():
            case DeleteProjectDialog.DELETE_FROM_LIST:
                self._label.setText(f"Проект пропадет из списка, но все данные будут сохранены. Вы сможете снова "
                                    f"добавить этот проект.\nУдалить проект {self.name}?")
            case DeleteProjectDialog.DELETE_DATA:
                self._label.setText(f"Эта операция приведет к безвозвратному удалению папки .TestGenerator из этого "
                                    f"проекта. Все прочие файлы останутся доступны.\nУдалить проект {self.name}?")
            case DeleteProjectDialog.DELETE_ALL:
                self._label.setText(f"Эта операция приведет к безвозвратному удалению папки проекта."
                                    f"\nУдалить проект {self.name}?")

    def result(self):
        return self._combo_box.currentIndex()


class ProjectFromZipDialog(CustomDialog):
    def __init__(self, name: str, directory: str, tm):
        super().__init__(tm, "Распаковка проекта")

        self.layout = QVBoxLayout()

        label = QLabel("Выберите директорию:")
        tm.auto_css(label)
        self.layout.addWidget(label)

        h_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setText(directory)
        tm.auto_css(self.path_edit)
        h_layout.addWidget(self.path_edit)
        self.path_button = QPushButton("Обзор")
        tm.auto_css(self.path_button)
        self.path_button.setFixedSize(50, 20)
        self.path_button.clicked.connect(self.get_dir)
        h_layout.addWidget(self.path_button)
        self.layout.addLayout(h_layout)

        label = QLabel("Введите имя проекта:")
        tm.auto_css(label)
        self.layout.addWidget(label)

        self.line_edit = QLineEdit()
        self.line_edit.setText(name)
        self.layout.addWidget(self.line_edit)
        self.line_edit.selectAll()

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.button_ok = QPushButton("Ок")
        self.button_ok.setFixedSize(70, 24)
        self.button_ok.clicked.connect(self.accept)
        button_layout.addWidget(self.button_ok)

        self.button_cancel = QPushButton("Отмена")
        self.button_cancel.setFixedSize(70, 24)
        self.button_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.button_cancel)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        super().set_theme()
        for el in [self.button_ok, self.button_cancel, self.line_edit]:
            tm.auto_css(el)

        self.resize(280, 50)

    def get_dir(self):
        path = QFileDialog.getExistingDirectory(None, "Выберите директорию", self.path_edit.text())
        if os.path.isdir(path):
            self.path_edit.setText(path)


class ProgressDialog(QMessageBox):
    def __init__(self, title, message, tm):
        super().__init__(None)

        self.setIcon(QMessageBox.Icon.Information)
        self.setText(message)
        self.setWindowTitle(title)
        self.setFont(tm.font_medium)

        self.setStyleSheet(tm.bg_style_sheet)
        self.addButton(QMessageBox.StandardButton.Cancel)
        button = self.button(QMessageBox.StandardButton.Cancel)
        tm.auto_css(button)
        button.setFixedSize(70, 24)


class NewProjectDialog(CustomDialog):
    def __init__(self, sm, tm):
        super().__init__(tm, "Новый проект")
        self.sm = sm

        main_layout = QVBoxLayout()
        self.labels = []

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox)
        label = QLabel("Из существующей папки")
        self.labels.append(label)
        layout.addWidget(label)
        main_layout.addLayout(layout)

        layout = QHBoxLayout()
        layout.setSpacing(2)
        self.dir_edit = QLineEdit()
        self.dir_edit.setFixedHeight(22)
        layout.addWidget(self.dir_edit)
        self.dir_button = QPushButton("Обзор")
        self.dir_button.clicked.connect(self.set_path)
        self.dir_button.setFixedSize(50, 22)
        layout.addWidget(self.dir_button)
        main_layout.addLayout(layout)

        self.options_widget = OptionsWidget({
            "Название проекта:": {'type': str, 'width': 300},
            "Язык:": {'type': 'combo', 'values': PROJECT_LANGUAGES, 'name': OptionsWidget.NAME_LEFT},
            "Сохранять тесты в папке проекта": {'type': bool, 'name': OptionsWidget.NAME_RIGHT}
        })
        main_layout.addWidget(self.options_widget)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addLayout(button_layout)

        self.button_ok = QPushButton("Ок")
        self.button_ok.setDisabled(True)
        self.dir_edit.textChanged.connect(lambda: self.button_ok.setDisabled(not os.path.isdir(self.dir_edit.text())))
        self.button_ok.setFixedSize(70, 24)
        self.button_ok.clicked.connect(self.accept)
        button_layout.addWidget(self.button_ok)

        self.button_cancel = QPushButton("Отмена")
        self.button_cancel.setFixedSize(70, 24)
        self.button_cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.button_cancel)

        self.setLayout(main_layout)
        self.set_theme()

    def set_path(self):
        path = QFileDialog.getExistingDirectory(directory=self.dir_edit.text() if os.path.isdir(
            self.dir_edit.text()) else os.getcwd() if self.sm.project is None else self.sm.project.path())
        self.dir_edit.setText(path)
        if self.checkbox.isChecked():
            self.options_widget.set_value("Название проекта:", os.path.basename(path))

    def set_theme(self):
        super().set_theme()
        for el in [self.checkbox, self.dir_edit, self.dir_button, self.button_ok, self.button_cancel]:
            self.tm.auto_css(el)
        for el in self.labels:
            self.tm.auto_css(el)
        self.tm.css_to_options_widget(self.options_widget)
