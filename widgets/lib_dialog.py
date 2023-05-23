import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QVBoxLayout, QListWidget, \
    QListWidgetItem, QTextEdit, QPushButton, QComboBox, QLineEdit, QLabel, QMessageBox, QWidget

from other.remote_libs import ListReader, FileReader


class LibWidget(QWidget):
    def __init__(self, sm, tm):
        super(LibWidget, self).__init__()

        self.new_lib_dialog = NewLibDialog(self, "Библиотеки автозавершения кода")
        self.sm = sm
        self.tm = tm

        vertical_layout = QVBoxLayout()
        main_layout = QHBoxLayout()

        lib_layout = QVBoxLayout()
        lib_layout.setContentsMargins(0, 0, 0, 0)

        self.button_add_lib = QPushButton()
        self.button_add_lib.setText("Добавить")
        self.button_add_lib.clicked.connect(self.add_lib)
        lib_layout.addWidget(self.button_add_lib)

        self.lib_list_widget = QListWidget()
        self.global_libs_dir = f"{self.sm.app_data_dir}/global_libs"
        self.local_libs_dir = f"{self.sm.app_data_dir}/custom_libs"

        os.makedirs(self.global_libs_dir, exist_ok=True)
        os.makedirs(self.local_libs_dir, exist_ok=True)

        for el in os.listdir(self.global_libs_dir):
            self.lib_list_widget.addItem(CustomLib(el, CustomLib.GLOBAL, f"{self.global_libs_dir}/{el}"))
        for el in os.listdir(self.local_libs_dir):
            self.lib_list_widget.addItem(CustomLib(el, CustomLib.LOCAL, f"{self.local_libs_dir}/{el}"))
        self.lib_list_widget.currentRowChanged.connect(self.open_lib)
        self.lib_list_widget.doubleClicked.connect(self.open_lib_dialog)

        lib_layout.addWidget(self.lib_list_widget)

        main_layout.addLayout(lib_layout, 1)

        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.modify_lib)
        self.text_edit.setFont(QFont("Courier", 10))
        main_layout.addWidget(self.text_edit, 2)

        vertical_layout.addLayout(main_layout)
        self.setLayout(vertical_layout)

    def set_theme(self):
        self.lib_list_widget.setStyleSheet(self.tm.list_widget_style_sheet)
        self.button_add_lib.setStyleSheet(self.tm.buttons_style_sheet)
        self.text_edit.setStyleSheet(self.tm.text_edit_style_sheet)

    def add_lib(self):
        if self.new_lib_dialog.exec():
            if self.new_lib_dialog.mode_combo_box.currentIndex() == CustomLib.LOCAL:
                self.lib_list_widget.addItem(CustomLib(
                    self.new_lib_dialog.local_line_edit.text(), CustomLib.LOCAL,
                    f"{self.global_libs_dir}/{self.new_lib_dialog.local_line_edit.text()}"))
            elif self.new_lib_dialog.mode_combo_box.currentIndex() == CustomLib.GLOBAL:
                lib_name = self.new_lib_dialog.global_list_widget.currentItem().text()
                for i in range(self.lib_list_widget.count()):
                    if self.lib_list_widget.item(i).name == lib_name:
                        dlg = CustomDialog(" ", "Данная библиотека уже установлена. Вы хотите загрузить ее заново?",
                                           self)
                        if dlg.exec():
                            self.remote_file_reader = FileReader(
                                self.new_lib_dialog.global_list_widget.currentItem().text())
                            self.remote_file_reader.complete.connect(lambda s: self.after_file_reading(
                                s, self.lib_list_widget.item(i)))
                            self.remote_file_reader.start()
                            self.remote_file_reader.error.connect(lambda: QMessageBox.warning(
                                self, "Ошибка", "Не удалось загрузить библиотеку. Проверьте подключение к интернету"))
                        break
                else:
                    self.lib_list_widget.addItem(item := CustomLib(
                        lib_name, CustomLib.GLOBAL,
                        f"{self.global_libs_dir}/{lib_name}"))
                    self.remote_file_reader = FileReader(self.new_lib_dialog.global_list_widget.currentItem().text())
                    self.remote_file_reader.complete.connect(lambda s: self.after_file_reading(s, item))
                    self.remote_file_reader.error.connect(lambda: QMessageBox.warning(
                        self, "Ошибка", "Не удалось загрузить библиотеку. Проверьте подключение к интернету"))
                    self.remote_file_reader.start()

    def after_file_reading(self, s, item):
        with open(item.file, 'w', encoding='utf-8') as f:
            f.write(s)

    def modify_lib(self):
        item = self.lib_list_widget.currentItem()
        if isinstance(item, CustomLib):
            with open(item.file, 'w', encoding='utf-8') as f:
                f.write(self.text_edit.toPlainText())

    def open_lib(self):
        if item := self.lib_list_widget.currentItem():
            with open(item.file, encoding='utf-8') as f:
                self.text_edit.setText(f.read())

    def open_lib_dialog(self):
        item = self.lib_list_widget.currentItem()
        if isinstance(item, CustomLib):
            if item.lib_type == CustomLib.GLOBAL:
                self.lib_dialog = GlobalLibDialog(item.name, self)
                if self.lib_dialog.exec():
                    if self.lib_dialog.status == GlobalLibDialog.DELETE:
                        self.sm.remove(item.name)
                        self.lib_list_widget.takeItem(self.lib_list_widget.currentRow())
            elif item.lib_type == CustomLib.LOCAL:
                self.lib_dialog = LocalLibDialog(item.name, self)
                if self.lib_dialog.exec():
                    if self.lib_dialog.status == LocalLibDialog.DELETE:
                        self.sm.remove(item.name)
                        self.lib_list_widget.takeItem(self.lib_list_widget.currentRow())


class NewLibDialog(QDialog):
    def __init__(self, parent, name):
        super(NewLibDialog, self).__init__(parent)
        self.setWindowTitle(name)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.return_pressed)
        self.buttonBox.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

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
        elif self.mode_combo_box.currentIndex() == CustomLib.LOCAL:
            self.accept()

    def set_files_list(self, lst):
        for el in lst:
            self.global_list_widget.addItem(el)

    def exec(self) -> int:
        self.global_list_widget.clear()
        self.remote_files_list_reader = ListReader()
        self.remote_files_list_reader.start()
        self.remote_files_list_reader.complete.connect(self.set_files_list)
        return super(NewLibDialog, self).exec()


class GlobalLibDialog(QDialog):
    DELETE = 1

    def __init__(self, name, parent=None):
        super(GlobalLibDialog, self).__init__(parent)
        self.setWindowTitle(name)
        self.status = 0

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        main_layout = QVBoxLayout()

        self.button_delete = QPushButton()
        self.button_delete.setText("Удалить")
        self.button_delete.clicked.connect(self.delete_lib)
        main_layout.addWidget(self.button_delete)

        main_layout.addWidget(self.buttonBox)
        self.setLayout(main_layout)

    def delete_lib(self):
        self.status = GlobalLibDialog.DELETE
        self.accept()


class LocalLibDialog(QDialog):
    DELETE = 1

    def __init__(self, name, parent=None):
        super(LocalLibDialog, self).__init__(parent)
        self.setWindowTitle(name)
        self.status = 0

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        main_layout = QVBoxLayout()

        self.button_delete = QPushButton()
        self.button_delete.setText("Удалить")
        self.button_delete.clicked.connect(self.delete_lib)
        main_layout.addWidget(self.button_delete)

        main_layout.addWidget(self.buttonBox)
        self.setLayout(main_layout)

    def delete_lib(self):
        self.status = LocalLibDialog.DELETE
        self.accept()


class CustomLib(QListWidgetItem):
    GLOBAL = 0
    LOCAL = 1

    def __init__(self, name: str, lib_type, file=None):
        super(CustomLib, self).__init__(name)
        self.name = name
        self.lib_type = lib_type
        self.file = file
        if self.lib_type == CustomLib.GLOBAL:
            self.setForeground(Qt.blue)
        elif self.lib_type == CustomLib.LOCAL:
            self.setForeground(Qt.red)


class CustomDialog(QDialog):
    def __init__(self, name, message, parent=None):
        super(CustomDialog, self).__init__(parent)
        self.setWindowTitle(name)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
