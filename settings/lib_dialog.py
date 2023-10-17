import os.path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QVBoxLayout, QListWidget, \
    QListWidgetItem, QTextEdit, QPushButton, QComboBox, QLineEdit, QLabel, QMessageBox, QWidget

from settings.remote_libs import ListReader, FileReader
from ui.message_box import MessageBox


class LibWidget(QWidget):
    def __init__(self, sm, tm):
        super(LibWidget, self).__init__()
        self.sm = sm
        self.tm = tm

        self.new_lib_dialog = NewLibDialog("Библиотеки автозавершения кода", self.tm)

        vertical_layout = QVBoxLayout()
        main_layout = QHBoxLayout()

        lib_layout = QVBoxLayout()
        lib_layout.setContentsMargins(0, 0, 0, 0)

        self.button_add_lib = QPushButton()
        self.button_add_lib.setText("Добавить")
        self.button_add_lib.setFixedSize(180, 30)
        self.button_add_lib.clicked.connect(self.add_lib)
        lib_layout.addWidget(self.button_add_lib)

        self.lib_list_widget = QListWidget()
        self.lib_list_widget.setFixedWidth(180)
        self.global_libs_dir = f"{self.sm.app_data_dir}/global_libs"
        self.local_libs_dir = f"{self.sm.app_data_dir}/custom_libs"

        os.makedirs(self.global_libs_dir, exist_ok=True)
        os.makedirs(self.local_libs_dir, exist_ok=True)

        for el in os.listdir(self.global_libs_dir):
            self.lib_list_widget.addItem(CustomLib(el, CustomLib.GLOBAL, self.tm, f"{self.global_libs_dir}/{el}"))
        for el in os.listdir(self.local_libs_dir):
            self.lib_list_widget.addItem(CustomLib(el, CustomLib.LOCAL, self.tm, f"{self.local_libs_dir}/{el}"))
        self.lib_list_widget.currentRowChanged.connect(self.open_lib)

        lib_layout.addWidget(self.lib_list_widget)

        main_layout.addLayout(lib_layout, 1)

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)

        actions_layout = QHBoxLayout()
        actions_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.lib_name_edit = QLineEdit()
        self.lib_name_edit.editingFinished.connect(self.rename_lib)
        actions_layout.addWidget(self.lib_name_edit)

        self.button_update = QPushButton("Обновить")
        self.button_update.setFixedSize(80, 20)
        self.button_update.clicked.connect(self.update_lib)
        actions_layout.addWidget(self.button_update)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setFixedSize(80, 20)
        self.delete_button.clicked.connect(self.delete_lib)
        actions_layout.addWidget(self.delete_button)

        right_layout.addLayout(actions_layout)

        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.modify_lib)
        self.text_edit.setFont(QFont("Courier", 10))
        right_layout.addWidget(self.text_edit, 2)

        main_layout.addLayout(right_layout)
        vertical_layout.addLayout(main_layout)
        self.setLayout(vertical_layout)

        self.dialog = None
        self.open_lib()

    def set_theme(self):
        for el in [self.lib_list_widget, self.button_add_lib, self.text_edit, self.delete_button, self.button_update,
                   self.lib_name_edit, self.new_lib_dialog]:
            self.tm.auto_css(el)
        for i in range(self.lib_list_widget.count()):
            item = self.lib_list_widget.item(i)
            item.setForeground(self.tm['HFile'] if item.lib_type == CustomLib.GLOBAL else self.tm['CFile'])

    def add_lib(self):
        if self.new_lib_dialog.exec():
            if self.new_lib_dialog.mode_combo_box.currentIndex() == CustomLib.LOCAL:
                self.lib_list_widget.addItem(CustomLib(
                    self.new_lib_dialog.local_line_edit.text(), CustomLib.LOCAL, self.tm,
                    path := f"{self.local_libs_dir}/{self.new_lib_dialog.local_line_edit.text()}"))
                open(path, 'w').close()
            elif self.new_lib_dialog.mode_combo_box.currentIndex() == CustomLib.GLOBAL:
                lib_name = self.new_lib_dialog.global_list_widget.currentItem().text()
                for i in range(self.lib_list_widget.count()):
                    if self.lib_list_widget.item(i).name == lib_name:
                        dlg = CustomDialog(" ", "Данная библиотека уже установлена. Вы хотите загрузить ее заново?",
                                           self.tm)
                        if dlg.exec():
                            self.start_loading_lib(lib_name, self.lib_list_widget.item(i))
                        break
                else:
                    self.start_loading_lib(lib_name, lib_name)

    def start_loading_lib(self, lib_name, item):
        self.remote_file_reader = FileReader(lib_name)
        self.remote_file_reader.complete.connect(lambda s: self.after_file_reading(s, item))

        self.dialog = LoadFileDialog(lib_name, self.tm)
        self.dialog.rejected.connect(self.remote_file_reader.terminate)

        self.remote_file_reader.error.connect(lambda: (self.dialog.accept(), QMessageBox.warning(
            self, "Ошибка", "Не удалось загрузить библиотеку. Проверьте подключение к интернету")))
        self.remote_file_reader.start()
        self.dialog.exec()

    def after_file_reading(self, s, item):
        if isinstance(item, str):
            self.lib_list_widget.addItem(item := CustomLib(item, CustomLib.GLOBAL, self.tm,
                                                           f"{self.global_libs_dir}/{item}"))
        if self.dialog:
            self.dialog.accept()
        with open(item.file, 'w', encoding='utf-8') as f:
            f.write(s)
        self.open_lib()

    def modify_lib(self):
        item = self.lib_list_widget.currentItem()
        if isinstance(item, CustomLib):
            with open(item.file, 'w', encoding='utf-8') as f:
                f.write(self.text_edit.toPlainText())

    def open_lib(self):
        self.lib_name_edit.hide()
        self.button_update.hide()
        self.delete_button.hide()
        if item := self.lib_list_widget.currentItem():
            with open(item.file, encoding='utf-8') as f:
                self.text_edit.setText(f.read())
            if item.lib_type == CustomLib.GLOBAL:
                self.delete_button.show()
                self.button_update.show()
            elif item.lib_type == CustomLib.LOCAL:
                self.delete_button.show()
                self.lib_name_edit.show()
                self.lib_name_edit.setText(item.name)

    def rename_lib(self):
        item = self.lib_list_widget.currentItem()
        if isinstance(item, CustomLib) and item.lib_type == CustomLib.LOCAL:
            path = f"{self.local_libs_dir}/{item.text()}"
            if os.path.isfile(path):
                try:
                    os.rename(path, f"{self.local_libs_dir}/{self.lib_name_edit.text()}")
                except Exception as ex:
                    MessageBox(MessageBox.Warning, "Ошибка", str(ex), self.tm)
                else:
                    item.name = self.lib_name_edit.text()
                    item.setText(self.lib_name_edit.text())
                    item.file = f"{self.local_libs_dir}/{self.lib_name_edit.text()}"
                    
    def update_lib(self):
        item = self.lib_list_widget.currentItem()
        if isinstance(item, CustomLib):
            self.start_loading_lib(item.name, item)

    def delete_lib(self):
        item = self.lib_list_widget.currentItem()
        if isinstance(item, CustomLib):
            self.dialog = CustomDialog("Удаление библиотеки",
                                       f"Вы действительно хотите удалить библиотеку {item.name}?", self.tm)
            if self.dialog.exec():
                path = f"{self.global_libs_dir if item.lib_type == CustomLib.GLOBAL else self.local_libs_dir}/" \
                       f"{item.text()}"
                if os.path.isfile(path):
                    os.remove(path)
                self.lib_list_widget.takeItem(self.lib_list_widget.currentRow())


class NewLibDialog(QDialog):
    def __init__(self, name, tm):
        super(NewLibDialog, self).__init__()
        self.setWindowTitle(name)
        self.tm = tm

        QBtn = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.return_pressed)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setFixedSize(80, 20)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.mode_combo_box = QComboBox()
        self.mode_combo_box.addItems(["Глобальная", "Локальная"])
        self.mode_combo_box.currentIndexChanged.connect(self.change_mode)
        main_layout.addWidget(self.mode_combo_box)

        self.local_line_edit = QLineEdit()
        main_layout.addWidget(self.local_line_edit)
        self.local_line_edit.hide()

        self.global_list_widget = QListWidget()
        self.global_list_widget.doubleClicked.connect(self.return_pressed)
        main_layout.addWidget(self.global_list_widget)

        main_layout.addWidget(self.buttonBox)
        self.setLayout(main_layout)

        self.remote_files_list_reader = ListReader()
        self.remote_files_list_reader.start()
        self.remote_files_list_reader.complete.connect(self.set_files_list)
        self.remote_files_list_reader.error.connect(lambda: QMessageBox.warning(
            self, "Ошибка", "Не удалось загрузить список библиотек. Проверьте подключение к интернету"))
        self.set_theme()

    def change_mode(self):
        if self.mode_combo_box.currentIndex() == CustomLib.LOCAL:
            self.global_list_widget.hide()
            self.local_line_edit.show()
        elif self.mode_combo_box.currentIndex() == CustomLib.GLOBAL:
            self.local_line_edit.hide()
            self.global_list_widget.show()

    def return_pressed(self):
        if self.mode_combo_box.currentIndex() == CustomLib.GLOBAL and self.global_list_widget.currentItem():
            self.accept()
        elif self.mode_combo_box.currentIndex() == CustomLib.LOCAL and self.local_line_edit.text():
            self.accept()

    def set_files_list(self, lst):
        for el in lst:
            self.global_list_widget.addItem(el)

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        for el in [self.mode_combo_box, self.local_line_edit, self.global_list_widget,
                   self.buttonBox.button(QDialogButtonBox.StandardButton.Ok)]:
            self.tm.auto_css(el)

    def exec(self) -> int:
        self.global_list_widget.clear()
        self.remote_files_list_reader = ListReader()
        self.remote_files_list_reader.start()
        self.remote_files_list_reader.complete.connect(self.set_files_list)
        return super(NewLibDialog, self).exec()


class CustomLib(QListWidgetItem):
    GLOBAL = 0
    LOCAL = 1

    def __init__(self, name: str, lib_type, tm, file=None):
        super(CustomLib, self).__init__(name)
        self.name = name
        self.lib_type = lib_type
        self.file = file
        if self.lib_type == CustomLib.GLOBAL:
            self.setForeground(tm['HFile'])
        elif self.lib_type == CustomLib.LOCAL:
            self.setForeground(tm['CFile'])


class CustomDialog(QDialog):
    def __init__(self, name, message, tm):
        super(CustomDialog, self).__init__()
        self.setWindowTitle(name)

        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.setStyleSheet(tm.bg_style_sheet)
        tm.auto_css(self.buttonBox.button(QDialogButtonBox.Yes))
        self.buttonBox.button(QDialogButtonBox.Yes).setFixedSize(80, 24)
        tm.auto_css(self.buttonBox.button(QDialogButtonBox.No))
        self.buttonBox.button(QDialogButtonBox.No).setFixedSize(80, 24)


class LoadFileDialog(QDialog):
    def __init__(self, lib_name, tm):
        super(LoadFileDialog, self).__init__()
        self.setWindowTitle("Загрузка библиотеки")

        QBtn = QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Загрузка библиотеки \"{lib_name}\". Пожалуйста, подождите."))
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        self.setModal(False)

        self.setStyleSheet(tm.bg_style_sheet)
        tm.auto_css(self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel))
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setFixedSize(80, 24)
