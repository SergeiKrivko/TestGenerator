import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QFileDialog, \
    QDialog, QLabel, QLineEdit, QCheckBox

from widgets.message_box import MessageBox
from widgets.options_window import OptionsWidget


class ProjectWidget(QWidget):
    def __init__(self, sm, tm, disable_menu_func):
        super(ProjectWidget, self).__init__()
        self.sm = sm
        self.tm = tm
        self.disable_menu_func = disable_menu_func

        layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        self.button_new_project = QPushButton("Новый проект")
        self.button_new_project.setFixedSize(200, 50)
        self.button_new_project.clicked.connect(self.new_project)
        left_layout.addWidget(self.button_new_project)

        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(200)
        self.list_widget.currentRowChanged.connect(self.open_project)
        left_layout.addWidget(self.list_widget)

        buttons_layout = QHBoxLayout()

        self.button_rename_project = QPushButton("Переименовать")
        self.button_rename_project.setFixedHeight(24)
        self.button_rename_project.clicked.connect(self.rename_project)
        buttons_layout.addWidget(self.button_rename_project)

        self.button_delete_project = QPushButton("Удалить")
        self.button_delete_project.setFixedHeight(24)
        self.button_delete_project.clicked.connect(self.delete_project)
        buttons_layout.addWidget(self.button_delete_project)

        left_layout.addLayout(buttons_layout)
        layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop)
        right_layout.setContentsMargins(20, 20, 20, 20)

        testing_checkbox_layout = QHBoxLayout()
        testing_checkbox_layout.setAlignment(Qt.AlignLeft)
        self.testing_checkbox = QCheckBox()
        testing_checkbox_layout.addWidget(self.testing_checkbox)
        self.label = QLabel("Настройки тестирования по умолчанию")
        testing_checkbox_layout.addWidget(self.label)
        self.testing_checkbox.clicked.connect(self.testing_checkbox_triggered)
        if self.sm.path:
            self.testing_checkbox.setChecked(self.sm.get('default_testing_settings', True))
        right_layout.addLayout(testing_checkbox_layout)

        self.options_widget = OptionsWidget({
            "Компилятор": {'type': str, 'width': 400},
            "Ключ -lm": {'type': bool, 'name': OptionsWidget.NAME_RIGHT},
            "Компаратор для позитивных тестов:": {'type': 'combo', 'name': OptionsWidget.NAME_LEFT, 'values': [
                'Числа', 'Числа как текст', 'Текст после подстроки', 'Слова после подстроки', 'Текст', 'Слова']},
            "Компаратор для негативных тестов:": {'type': 'combo', 'name': OptionsWidget.NAME_LEFT, 'values': [
                'Нет', 'Числа', 'Числа как текст', 'Текст после подстроки', 'Слова после подстроки', 'Текст', 'Слова']},
            'Погрешность сравнения чисел:': {'type': float, 'name': OptionsWidget.NAME_LEFT},
            'Подстрока для позитивных тестов': {'type': str, 'name': OptionsWidget.NAME_RIGHT},
            'Подстрока для негативных тестов': {'type': str, 'name': OptionsWidget.NAME_RIGHT},
            "Coverage": {'type': bool, 'name': OptionsWidget.NAME_RIGHT},
            "Тестирование по памяти": {'type': bool, 'name': OptionsWidget.NAME_RIGHT},
            "Ограничение по времени:": {'type': float, 'min': 0.01, 'max': 600, 'name': OptionsWidget.NAME_LEFT},
        }, margins=(5, 5, 5, 5))
        self.options_widget.setDisabled(True)
        self.options_widget.clicked.connect(self.save_settings)
        right_layout.addWidget(self.options_widget)

        layout.addLayout(right_layout)
        self.setLayout(layout)

        self.opening_project = False
        self.dialog = None

        self.update_projects()
        self.open_project()

    def testing_checkbox_triggered(self, value):
        self.sm.set('default_testing_settings', value)
        self.sm.repair_settings()
        if value:
            self.options_widget.hide()
        else:
            self.options_widget.show()

    def update_projects(self):
        self.list_widget.clear()
        for pr in self.sm.get_general('projects', set()):
            item = ProjectListWidgetItem(pr)
            self.list_widget.addItem(item)
            if self.sm.path == pr:
                self.list_widget.setCurrentItem(item)
        self.list_widget.sortItems()

    def rename_project(self):
        self.dialog = RenameProjectDialog(self.sm.path, self.tm)
        if self.dialog.exec():
            new_path = f"{os.path.split(self.sm.path)[0]}/{self.dialog.line_edit.text()}"
            if os.path.isdir(new_path):
                MessageBox(MessageBox.Warning, "Переименование проекта",
                           f"Папка {new_path} уже существует. Переименование невозможно", self.tm)
            else:
                os.rename(self.sm.path, new_path)
                projects_set = self.sm.get_general('projects', set())
                projects_set.remove(self.sm.path)
                projects_set.add(new_path)
                self.sm.set_general(new_path, self.sm.get_general(self.sm.path, dict()))
                self.sm.remove(self.sm.path)
                self.sm.set_general('projects', projects_set)
                self.sm.set_general('__project__', new_path)
                self.sm.repair_settings()
                self.update_projects()

    def delete_project(self):
        self.dialog = DeleteProjectDialog(self.sm.path, self.tm)
        if self.dialog.exec():
            projects_set = self.sm.get_general('projects', set())
            projects_set.remove(self.sm.path)
            self.sm.remove(self.sm.path)
            self.sm.set_general('projects', projects_set)
            self.sm.set_general('__project__', None)
            self.update_projects()
            if not self.list_widget.count():
                self.disable_menu_func(True)

    def new_project(self):
        path = QFileDialog.getExistingDirectory(directory=self.sm.get_general('__project__', os.getcwd()))
        if path:
            projects_set = self.sm.get_general('projects', set())
            projects_set.add(path)
            self.sm.set_general('projects', projects_set)
            self.sm.repair_settings()
            self.update_projects()
            self.disable_menu_func(False)

    def open_project(self):
        self.opening_project = True
        if self.list_widget.currentItem() is None:
            self.options_widget.setDisabled(True)
            return
        path = self.list_widget.currentItem().path
        self.options_widget.setDisabled(False)
        self.sm.set_general('__project__', path)
        self.sm.repair_settings()
        self.testing_checkbox.setChecked(flag := self.sm.get('default_testing_settings', True))
        if flag:
            self.options_widget.hide()
        else:
            self.options_widget.show()
        self.options_widget.widgets['Компилятор'].setText(self.sm.get('compiler', 'gcc -std=c99 -Wall -Werror'))
        self.options_widget.widgets['Ключ -lm'].setChecked(bool(self.sm.get('-lm', True)))
        self.options_widget.widgets['Компаратор для позитивных тестов:'].setCurrentIndex(int(
            self.sm.get('pos_comparator', 0)))
        self.options_widget.widgets['Компаратор для негативных тестов:'].setCurrentIndex(int(
            self.sm.get('neg_comparator', 0)))
        self.options_widget.widgets['Погрешность сравнения чисел:'].setValue(int(self.sm.get('epsilon', 0)))
        self.options_widget.widgets['Подстрока для позитивных тестов'].setText(self.sm.get('pos_substring', 'Result:'))
        self.options_widget.widgets['Подстрока для негативных тестов'].setText(self.sm.get('neg_substring', 'Error:'))
        self.options_widget.widgets['Coverage'].setChecked(bool(self.sm.get('coverage', False)))
        self.options_widget.widgets['Тестирование по памяти'].setChecked(bool(self.sm.get('memory_testing', False)))
        self.options_widget.widgets['Ограничение по времени:'].setValue(int(self.sm.get('time_limit', 3)))
        self.opening_project = False

    def save_settings(self):
        if self.opening_project:
            return
        if not self.testing_checkbox.isChecked():
            print(f'save project {self.sm.path} settings')
            dct = self.options_widget.values
            self.sm.set('compiler', dct['Компилятор'])
            self.sm.set('-lm', dct['Ключ -lm'])
            self.sm.set('pos_comparator', dct['Компаратор для позитивных тестов:'])
            self.sm.set('neg_comparator', dct['Компаратор для негативных тестов:'])
            self.sm.set('memory_testing', dct['Тестирование по памяти'])
            self.sm.set('coverage', dct['Coverage'])
            self.sm.set('epsilon', dct['Погрешность сравнения чисел:'])
            self.sm.set('pos_substring', dct['Подстрока для позитивных тестов'])
            self.sm.set('neg_substring', dct['Подстрока для негативных тестов'])
            self.sm.set('time_limit', dct['Ограничение по времени:'])

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        self.button_new_project.setStyleSheet(self.tm.buttons_style_sheet)
        self.button_new_project.setFont(self.tm.font_big)
        self.list_widget.setStyleSheet(self.tm.list_widget_style_sheet)
        self.tm.set_theme_to_list_widget(self.list_widget, self.tm.font_medium)
        self.button_delete_project.setStyleSheet(self.tm.buttons_style_sheet)
        self.button_delete_project.setFont(self.tm.font_small)
        self.button_rename_project.setStyleSheet(self.tm.buttons_style_sheet)
        self.button_rename_project.setFont(self.tm.font_small)
        self.options_widget.setFont(self.tm.font_small)
        self.label.setFont(self.tm.font_small)
        self.options_widget.widgets['Компилятор'].setStyleSheet(self.tm.style_sheet)
        self.options_widget.widgets['Компаратор для позитивных тестов:'].setStyleSheet(self.tm.combo_box_style_sheet)
        self.options_widget.widgets['Компаратор для негативных тестов:'].setStyleSheet(self.tm.combo_box_style_sheet)
        self.options_widget.widgets['Погрешность сравнения чисел:'].setStyleSheet(self.tm.double_spin_box_style_sheet)
        self.options_widget.widgets['Подстрока для позитивных тестов'].setStyleSheet(self.tm.style_sheet)
        self.options_widget.widgets['Подстрока для негативных тестов'].setStyleSheet(self.tm.style_sheet)
        self.options_widget.widgets['Ограничение по времени:'].setStyleSheet(self.tm.double_spin_box_style_sheet)

    def show(self) -> None:
        self.open_project()
        super(ProjectWidget, self).show()


class ProjectListWidgetItem(QListWidgetItem):
    def __init__(self, path):
        super(ProjectListWidgetItem, self).__init__()
        self.path = path
        self.setText(str(os.path.basename(self.path)))


class RenameProjectDialog(QDialog):
    def __init__(self, path, tm):
        super(RenameProjectDialog, self).__init__()
        self.path = path
        self.setWindowTitle("Переименовать проект")

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(QLabel(f"Переименовать проект {os.path.basename(self.path)} в:"))

        self.line_edit = QLineEdit()
        self.line_edit.setText(os.path.basename(self.path))
        self.line_edit.setFixedHeight(24)
        self.line_edit.setMinimumWidth(200)
        layout.addWidget(self.line_edit)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(5)
        buttons_layout.setAlignment(Qt.AlignRight)
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

        self.setStyleSheet(tm.bg_style_sheet)
        self.line_edit.setStyleSheet(tm.style_sheet)
        self.button_ok.setStyleSheet(tm.buttons_style_sheet)
        self.button_cancel.setStyleSheet(tm.buttons_style_sheet)


class DeleteProjectDialog(QDialog):
    def __init__(self, path, tm):
        super(DeleteProjectDialog, self).__init__()
        self.path = path
        self.setWindowTitle("Удалить проект")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        label = QLabel(f"Эта операция приведет к удалению из программы всех сведений о данном проекте, а "
                       f"именно факта его существования и всех его настроек. При этом файлы проекта удалены "
                       f"не будут. Удалить проект {os.path.basename(self.path)}?")
        label.setWordWrap(True)
        layout.addWidget(label)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(5)
        buttons_layout.setAlignment(Qt.AlignRight)
        self.button_yes = QPushButton("Ok")
        self.button_yes.setFixedSize(80, 24)
        buttons_layout.addWidget(self.button_yes)
        self.button_yes.clicked.connect(self.accept)
        self.button_no = QPushButton("Cancel")
        self.button_no.setFixedSize(80, 24)
        buttons_layout.addWidget(self.button_no)
        self.button_no.clicked.connect(self.reject)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        self.setStyleSheet(tm.bg_style_sheet)
        self.button_yes.setStyleSheet(tm.buttons_style_sheet)
        self.button_no.setStyleSheet(tm.buttons_style_sheet)
