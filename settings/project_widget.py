import os
import shutil

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QFileDialog, \
    QDialog, QLabel, QLineEdit, QCheckBox, QTabWidget, QGridLayout, QMessageBox
import py7zr

from ui.message_box import MessageBox
from ui.options_window import OptionsWidget


class ProjectWidget(QWidget):
    def __init__(self, sm, tm, disable_menu_func):
        super(ProjectWidget, self).__init__()
        self.sm = sm
        self.tm = tm
        self.disable_menu_func = disable_menu_func

        layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        self.button_new_project = QPushButton("Новый проект")
        self.button_new_project.setFixedSize(225, 50)
        self.button_new_project.clicked.connect(self.new_project)
        left_layout.addWidget(self.button_new_project)

        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(225)
        self.list_widget.currentRowChanged.connect(self.open_project)
        left_layout.addWidget(self.list_widget)

        buttons_layout = QGridLayout()
        buttons_layout.setColumnMinimumWidth(0, 110)
        buttons_layout.setColumnMinimumWidth(1, 110)

        self.button_rename_project = QPushButton("Переименовать")
        self.button_rename_project.setFixedSize(110, 24)
        self.button_rename_project.clicked.connect(self.rename_project)
        buttons_layout.addWidget(self.button_rename_project)

        self.button_delete_project = QPushButton("Удалить")
        self.button_delete_project.setFixedSize(110, 24)
        self.button_delete_project.clicked.connect(self.delete_project)
        buttons_layout.addWidget(self.button_delete_project)

        self.button_to_zip = QPushButton("В zip")
        self.button_to_zip.setFixedSize(110, 24)
        self.button_to_zip.clicked.connect(self.project_to_zip)
        buttons_layout.addWidget(self.button_to_zip)

        self.button_from_zip = QPushButton("Из zip")
        self.button_from_zip.setFixedSize(110, 24)
        self.button_from_zip.clicked.connect(self.project_from_zip)
        buttons_layout.addWidget(self.button_from_zip)

        left_layout.addLayout(buttons_layout)
        layout.addLayout(left_layout)

        self.tab_widget = QTabWidget()

        self.struct_settings_widget = OptionsWidget({
            'Структура проекта': {'type': 'combo', 'name': OptionsWidget.NAME_LEFT, 'width': 200,
                                  'values': ['Лаба - задание - вариант', 'Лаба - вариант', 'Лаба', 'Без структуры']},
            'Название папки с лабой': {'type': str, 'width': 250, 'name': OptionsWidget.NAME_RIGHT,
                                       'initial': self.sm.get('dir_format', '')},
            'Описание тестов': {'type': str, 'initial': self.sm.get('readme', 'func_tests/readme.md'),
                                'width': 250, 'name': OptionsWidget.NAME_RIGHT},
            'Входные данные для позитивных тестов': {
                'type': str, 'width': 250, 'initial': self.sm.get('pos_in', ''),
                'name': OptionsWidget.NAME_RIGHT},
            'Входные данные для негативных тестов': {
                'type': str, 'width': 250, 'initial': self.sm.get('pos_in', ''),
                'name': OptionsWidget.NAME_RIGHT},
        }, margins=(25, 25, 25, 25))
        self.tab_widget.addTab(self.struct_settings_widget, 'Структура проекта')

        widget = QWidget()
        testing_settings_layout = QVBoxLayout()
        widget.setLayout(testing_settings_layout)
        testing_settings_layout.setAlignment(Qt.AlignTop)
        testing_settings_layout.setContentsMargins(20, 20, 20, 20)

        testing_checkbox_layout = QHBoxLayout()
        testing_checkbox_layout.setAlignment(Qt.AlignLeft)
        self.testing_checkbox = QCheckBox()
        testing_checkbox_layout.addWidget(self.testing_checkbox)
        self.label = QLabel("Настройки тестирования по умолчанию")
        testing_checkbox_layout.addWidget(self.label)
        self.testing_checkbox.clicked.connect(self.testing_checkbox_triggered)
        if self.sm.data_path:
            self.testing_checkbox.setChecked(self.sm.get('default_testing_settings', True))
        testing_settings_layout.addLayout(testing_checkbox_layout)

        self.testing_settings_widget = OptionsWidget({
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
        self.testing_settings_widget.setDisabled(True)
        self.testing_settings_widget.clicked.connect(self.save_settings)
        testing_settings_layout.addWidget(self.testing_settings_widget)

        # self.tab_widget.addTab(widget, 'Тестирование')

        layout.addWidget(widget)
        self.setLayout(layout)

        self.opening_project = False
        self.dialog = None

        self.disable_menu_func(True)
        self.update_projects()
        self.looper = None

    def testing_checkbox_triggered(self, value):
        self.sm.set('default_testing_settings', value)
        self.sm.repair_settings()
        if value:
            self.testing_settings_widget.hide()
        else:
            self.testing_settings_widget.show()

    def update_projects(self):
        self.list_widget.clear()
        for pr in self.sm.projects.keys():
            item = ProjectListWidgetItem(pr)
            item.setFont(self.tm.font_medium)
            self.list_widget.addItem(item)
            if self.sm.project == pr:
                self.list_widget.setCurrentItem(item)
        self.list_widget.sortItems()

    def rename_project(self):
        self.dialog = RenameProjectDialog(self.sm.data_path, self.tm)
        if self.dialog.exec():
            new_name = self.dialog.line_edit.text()
            if new_name in self.sm.projects:
                MessageBox(MessageBox.Warning, "Переименование проекта",
                           f"Проект {new_name} уже существует. Переименование невозможно", self.tm)
            else:
                os.rename(self.sm.data_path, f"{os.path.split(self.sm.data_path)[0]}/{new_name}")
                self.sm.projects[new_name] = self.sm.projects[self.sm.project]
                self.sm.projects.pop(self.sm.project)
                self.sm.project = new_name
                self.sm.repair_settings()
                self.update_projects()

    def delete_project(self):
        print(self.sm.data_path)
        self.dialog = DeleteProjectDialog(self.sm.data_path, self.tm)
        if self.dialog.exec():
            try:
                if os.path.isdir(self.sm.path) and self.dialog.check_box.isChecked():
                    shutil.rmtree(self.sm.path)
            except PermissionError:
                pass
            try:
                if os.path.isdir(self.sm.data_path):
                    shutil.rmtree(self.sm.data_path)
            except PermissionError:
                pass
            self.sm.projects.pop(self.sm.project)
            self.update_projects()
            self.disable_menu_func(True)

    def new_project(self):
        path = QFileDialog.getExistingDirectory(directory=self.sm.path)
        if path:
            self.sm.projects[os.path.basename(path)] = path
            self.update_projects()
            self.disable_menu_func(False)

    def open_project(self, forced=False):
        if self.list_widget.currentItem() is None:
            self.testing_settings_widget.setDisabled(True)
            return
        project = self.list_widget.currentItem().text()
        if project == self.sm.project and not forced:
            return
        self.opening_project = True
        self.testing_settings_widget.setDisabled(False)
        self.sm.set_project(project)
        self.sm.repair_settings()
        self.testing_checkbox.setChecked(flag := self.sm.get('default_testing_settings', True))
        if flag:
            self.testing_settings_widget.hide()
        else:
            self.testing_settings_widget.show()

        self.struct_settings_widget.widgets['Структура проекта'].setCurrentIndex(self.sm.get(
            'struct', 0))
        self.struct_settings_widget.widgets['Название папки с лабой'].setText(self.sm.get(
            'dir_format', 'lab_{lab:0>2}_{task:0>2}_{var:0>2}'))
        self.struct_settings_widget.widgets['Описание тестов'].setText(self.sm.get(
            'readme', 'func_tests/readme.md'))
        self.struct_settings_widget.widgets['Входные данные для позитивных тестов'].setText(self.sm.get(
            'pos_in', 'func_tests/data/pos_{:0>2}_in.txt'))
        self.struct_settings_widget.widgets['Входные данные для негативных тестов'].setText(self.sm.get(
            'neg_in', 'func_tests/data/neg_{:0>2}_in.txt'))

        self.testing_settings_widget.widgets['Компилятор'].setText(
            self.sm.get('compiler', 'gcc -std=c99 -Wall -Werror'))
        self.testing_settings_widget.widgets['Ключ -lm'].setChecked(bool(self.sm.get('-lm', True)))
        self.testing_settings_widget.widgets['Компаратор для позитивных тестов:'].setCurrentIndex(int(
            self.sm.get('pos_comparator', 0)))
        self.testing_settings_widget.widgets['Компаратор для негативных тестов:'].setCurrentIndex(int(
            self.sm.get('neg_comparator', 0)))
        self.testing_settings_widget.widgets['Погрешность сравнения чисел:'].setValue(int(self.sm.get('epsilon', 0)))
        self.testing_settings_widget.widgets['Подстрока для позитивных тестов'].setText(
            self.sm.get('pos_substring', 'Result:'))
        self.testing_settings_widget.widgets['Подстрока для негативных тестов'].setText(
            self.sm.get('neg_substring', 'Error:'))
        self.testing_settings_widget.widgets['Coverage'].setChecked(bool(self.sm.get('coverage', False)))
        self.testing_settings_widget.widgets['Тестирование по памяти'].setChecked(
            bool(self.sm.get('memory_testing', False)))
        self.testing_settings_widget.widgets['Ограничение по времени:'].setValue(int(self.sm.get('time_limit', 3)))
        self.opening_project = False
        self.disable_menu_func(False)

    def project_to_zip(self):
        path, _ = QFileDialog.getSaveFileName(None, "Выберите путь", self.sm.path + '.7z', '7z (*.7z)')
        if not path:
            return
        if not path.endswith('.7z'):
            path += '.7z'

        self.sm.store()
        if os.path.isdir(self.sm.path) and os.path.isdir(self.sm.data_path):
            looper = ProjectPacker(path, self.sm.path, self.sm.data_path)
            looper.start()
            dialog = ProgressDialog("Запаковка проекта", "Идет запаковка проекта. Пожалуйста, подождите", self.tm)
            looper.finished.connect(dialog.reject)
            if dialog.exec():
                looper.cancel()
        else:
            MessageBox(MessageBox.Warning, "Ошибка", "Неизвестная ошибка. Сжатие проекта невозможно", self.tm)

    def project_from_zip(self, path=''):
        if not os.path.isfile(path):
            path, _ = QFileDialog.getOpenFileName(
                None, "Выберите проект для распаковки",
                self.sm.get_general('zip_path', self.sm.path if self.sm.path else os.getcwd()), '7z (*.7z)')
        if not path or not os.path.isfile(path):
            return
        self.sm.set_general('zip_path', os.path.split(path)[0])
        dialog = ProjectFromZipDialog(os.path.basename(path).rstrip('.7z'),
                                      os.path.split(self.sm.path if self.sm.path else os.getcwd())[0], self.tm)
        if dialog.exec():
            if dialog.line_edit.text() in self.sm.projects:
                MessageBox(MessageBox.Warning, 'Распаковка проекта',
                           f"Проект {dialog.line_edit.text()} уже существует. "
                           f"Невозможно создать новый проект с таким же именем.", self.tm)
            elif dialog.path_edit.text() in self.sm.projects:
                MessageBox(MessageBox.Warning, 'Распаковка проекта',
                           f"Директория {dialog.path_edit.text()} не существует. Невозможно создать проект.", self.tm)
            else:
                main_path = f"{dialog.path_edit.text()}/{dialog.line_edit.text()}"
                data_path = f"{self.sm.app_data_dir}/projects/{dialog.line_edit.text()}"

                looper = ProjectUnpacker(path, main_path, data_path, self.sm.app_data_dir)
                looper.start()
                progress_dialog = ProgressDialog("Распаковка проекта", "Идет распаковка проекта. Пожалуйста, подождите",
                                                 self.tm)
                looper.finished.connect(progress_dialog.reject)
                if progress_dialog.exec():
                    looper.cancel()
                else:
                    self.sm.projects[dialog.line_edit.text()] = main_path
                    self.sm.set_project(dialog.line_edit.text())
                    self.update_projects()

                # with py7zr.SevenZipFile(path, mode='r') as archive:
                #     archive.extractall(f"{self.sm.app_data_dir}/temp")
                # if os.path.isdir(main_path):
                #     shutil.rmtree(main_path)
                # if os.path.isdir(data_path):
                #     shutil.rmtree(data_path)
                # os.rename(f"{self.sm.app_data_dir}/temp/main", main_path)
                # os.rename(f"{self.sm.app_data_dir}/temp/data", data_path)
                # shutil.rmtree(f"{self.sm.app_data_dir}/temp")

    def save_settings(self):
        if self.opening_project:
            return
        if not self.testing_checkbox.isChecked():
            dct = self.struct_settings_widget.values
            self.sm.set('struct', dct['Структура проекта'])
            self.sm.set('dir_format', dct['Название папки с лабой'])
            self.sm.set('readme', dct['Описание тестов'])
            self.sm.set('pos_in', dct['Входные данные для позитивных тестов'])
            self.sm.set('neg_in', dct['Входные данные для негативных тестов'])

            dct = self.testing_settings_widget.values
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
        for el in [self.button_delete_project, self.button_rename_project, self.button_to_zip, self.button_from_zip]:
            self.tm.auto_css(el)
        self.button_new_project.setStyleSheet(self.tm.buttons_style_sheet)
        self.button_new_project.setFont(self.tm.font_big)
        self.list_widget.setStyleSheet(self.tm.list_widget_style_sheet)
        self.tm.set_theme_to_list_widget(self.list_widget, self.tm.font_medium)

        self.tab_widget.setStyleSheet(self.tm.tab_widget_style_sheet.replace('width: 50px', 'width: 120px'))
        self.tab_widget.setFont(self.tm.font_small)

        for widget in [self.struct_settings_widget, self.testing_settings_widget]:
            widget.setFont(self.tm.font_small)
            for el in widget.widgets.values():
                self.tm.auto_css(el)
            for label in widget.labels.values():
                label.setFont(self.tm.font_small)

    def show(self) -> None:
        if self.isHidden():
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

        h_layout = QHBoxLayout()
        h_layout.setAlignment(Qt.AlignLeft)
        self.check_box = QCheckBox()
        self.check_box.setChecked(True)
        h_layout.addWidget(self.check_box)

        label = QLabel("Удалить папку проекта")
        label.setFont(tm.font_small)
        h_layout.addWidget(label)

        layout = QVBoxLayout()
        layout.addLayout(h_layout)
        layout.setSpacing(15)
        label = QLabel(f"Эта операция приведет к безвозвратному удалению всех данных проекта. "
                       f"Удалить проект {os.path.basename(self.path)}?")
        label.setWordWrap(True)
        label.setFont(tm.font_small)
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
        self.button_no.setFont(tm.font_small)
        self.button_no.setStyleSheet(tm.buttons_style_sheet)
        self.button_no.setFont(tm.font_small)


class ProjectFromZipDialog(QDialog):
    def __init__(self, name: str, directory: str, tm):
        super().__init__()

        self.setWindowTitle("Распаковка проекта")

        self.layout = QVBoxLayout()

        label = QLabel("Выберите директорию:")
        label.setFont(tm.font_small)
        self.layout.addWidget(label)

        h_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setText(directory)
        self.path_edit.setStyleSheet(tm.style_sheet)
        h_layout.addWidget(self.path_edit)
        self.path_button = QPushButton("Обзор")
        self.path_button.setStyleSheet(tm.buttons_style_sheet)
        self.path_button.setFixedSize(50, 20)
        self.path_button.clicked.connect(self.get_dir)
        h_layout.addWidget(self.path_button)
        self.layout.addLayout(h_layout)

        label = QLabel("Введите имя проекта:")
        label.setFont(tm.font_small)
        self.layout.addWidget(label)

        self.line_edit = QLineEdit()
        self.line_edit.setText(name)
        self.layout.addWidget(self.line_edit)
        self.line_edit.selectAll()

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setAlignment(Qt.AlignRight)

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

        self.setStyleSheet(tm.bg_style_sheet)
        self.button_ok.setStyleSheet(tm.buttons_style_sheet)
        self.button_ok.setFont(tm.font_small)
        self.button_cancel.setStyleSheet(tm.buttons_style_sheet)
        self.button_cancel.setFont(tm.font_small)
        self.line_edit.setStyleSheet(tm.style_sheet)
        self.line_edit.setFont(tm.font_small)

        self.resize(280, 50)

    def get_dir(self):
        path = QFileDialog.getExistingDirectory(None, "Выберите директорию", self.path_edit.text())
        if os.path.isdir(path):
            self.path_edit.setText(path)


class ProgressDialog(QMessageBox):
    def __init__(self, title, message, tm):
        super().__init__(None)

        self.setIcon(QMessageBox.Information)
        self.setText(message)
        self.setWindowTitle(title)
        self.setFont(tm.font_small)

        self.setStyleSheet(tm.bg_style_sheet)
        self.addButton(QMessageBox.Cancel)
        button = self.button(QMessageBox.Cancel)
        button.setFont(tm.font_small)
        button.setStyleSheet(tm.buttons_style_sheet)
        button.setFixedSize(70, 24)


class ProjectPacker(QThread):
    def __init__(self, path, main_path, data_path):
        super().__init__()
        self.path = path
        self.main_path = main_path
        self.data_path = data_path

    def run(self):
        with py7zr.SevenZipFile(self.path, mode='w') as archive:
            archive.writeall(self.main_path, arcname='main')
            archive.writeall(self.data_path, arcname='data')

    def cancel(self):
        self.terminate()


class ProjectUnpacker(QThread):
    def __init__(self, path, main_path, data_path, app_data_dir):
        super().__init__()
        self.path = path
        self.main_path = main_path
        self.data_path = data_path
        self.app_data_dir = app_data_dir

    def run(self):
        with py7zr.SevenZipFile(self.path, mode='r') as archive:
            archive.extractall(f"{self.app_data_dir}/temp")

        if os.path.isdir(self.main_path):
            shutil.rmtree(self.main_path)
        if os.path.isdir(self.data_path):
            shutil.rmtree(self.data_path)
        os.rename(f"{self.app_data_dir}/temp/main", self.main_path)
        os.rename(f"{self.app_data_dir}/temp/data", self.data_path)
        shutil.rmtree(f"{self.app_data_dir}/temp")

    def cancel(self):
        self.terminate()
        shutil.rmtree(self.main_path, ignore_errors=True)
        shutil.rmtree(self.data_path, ignore_errors=True)