from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QVBoxLayout, QListWidget, \
    QListWidgetItem, QTextEdit, QPushButton, QComboBox, QLineEdit


class LibDialog(QDialog):
    def __init__(self, parent, name, q_settings: QSettings):
        super(LibDialog, self).__init__(parent)

        self.setWindowTitle(name)
        self.new_lib_dialog = NewLibDialog(self, "Библиотеки автозавершения кода")
        self.q_settings = q_settings

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.save_libs)
        self.buttonBox.rejected.connect(self.reject)

        vertical_layout = QVBoxLayout()
        main_layout = QHBoxLayout()

        lib_layout = QVBoxLayout()
        lib_layout.setContentsMargins(0, 0, 0, 0)

        self.button_add_lib = QPushButton()
        self.button_add_lib.setText("Добавить")
        self.button_add_lib.clicked.connect(self.add_lib)
        lib_layout.addWidget(self.button_add_lib)

        self.lib_list_widget = QListWidget()
        libs = q_settings.value("lib")
        if isinstance(libs, str):
            for lib_info in libs.split(';'):
                lib_name, lib_type = lib_info.split(':')
                lib_type = int(lib_type)
                lib_data = q_settings.value(lib_name)
                self.lib_list_widget.addItem(CustomLib(lib_name, lib_type, lib_data if lib_data else ""))
        self.lib_list_widget.currentRowChanged.connect(self.open_lib)

        lib_layout.addWidget(self.lib_list_widget)

        main_layout.addLayout(lib_layout, 1)

        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.modify_lib)
        self.text_edit.setFont(QFont("Courier", 10))
        main_layout.addWidget(self.text_edit, 2)

        vertical_layout.addLayout(main_layout)
        vertical_layout.addWidget(self.buttonBox)

        self.setLayout(vertical_layout)

    def save_libs(self):
        libs_list = []
        for i in range(self.lib_list_widget.count()):
            item = self.lib_list_widget.item(i)
            libs_list.append(f"{item.name}:{item.lib_type}")
            self.q_settings.setValue(item.name, item.data)
        self.q_settings.setValue("lib", ';'.join(libs_list))
        self.accept()

    def add_lib(self):
        if self.new_lib_dialog.exec():
            if self.new_lib_dialog.mode_combo_box.currentIndex() == CustomLib.LOCAL:
                self.lib_list_widget.addItem(CustomLib(self.new_lib_dialog.local_line_edit.text(), CustomLib.LOCAL))

    def modify_lib(self):
        item = self.lib_list_widget.currentItem()
        if item:
            item.data = self.text_edit.toPlainText()

    def open_lib(self):
        if self.lib_list_widget.currentItem():
            self.text_edit.setText(self.lib_list_widget.currentItem().data)


class NewLibDialog(QDialog):
    def __init__(self, parent, name):
        super(NewLibDialog, self).__init__(parent)
        self.setWindowTitle(name)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
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
        main_layout.addWidget(self.global_list_widget)

        main_layout.addWidget(self.buttonBox)
        self.setLayout(main_layout)

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


class CustomLib(QListWidgetItem):
    GLOBAL = 0
    LOCAL = 1

    def __init__(self, name: str, lib_type, data=None):
        super(CustomLib, self).__init__(name)
        self.name = name
        self.lib_type = lib_type
        self.data = data if data else ""

