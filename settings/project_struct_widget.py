from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QLineEdit, QComboBox


class TestingSettingsWidget(QWidget):
    def __init__(self, sm, tm):
        super().__init__()
        self.sm = sm
        self.tm = tm

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.labels = []

        main_layout.addWidget(label := QLabel("Файлы с входными данными"))
        self.labels.append(label)
        self.struct_combo_box = QComboBox()
        self.struct_combo_box.addItems('Лаба - задание - вариант', 'Без структуры')
        self.struct_combo_box.setFixedSize(300, 24)
        main_layout.addWidget(self.struct_combo_box)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        self.compiler_checkbox = QCheckBox()
        self.compiler_checkbox.stateChanged.connect(self.compiler_checkbox_triggered)
        layout.addWidget(self.compiler_checkbox)
        self.compiler_label = QLabel("Сохранять тесты в папке проекта")
        layout.addWidget(self.compiler_label)
        main_layout.addLayout(layout)

        main_layout.addWidget(label := QLabel("Файлы с входными данными"))
        self.labels.append(label)
        self.test_in_edit = QLineEdit()
        self.test_in_edit.setFixedSize(300, 24)
        main_layout.addWidget(self.test_in_edit)

        main_layout.addWidget(label := QLabel("Файлы с выходными данными"))
        self.labels.append(label)
        self.test_out_edit = QLineEdit()
        self.test_out_edit.setFixedSize(300, 24)
        main_layout.addWidget(self.test_out_edit)

        main_layout.addWidget(label := QLabel("Файлы с аргументами"))
        self.labels.append(label)
        self.test_args_edit = QLineEdit()
        self.test_args_edit.setFixedSize(300, 24)
        main_layout.addWidget(self.test_args_edit)

        main_layout.addWidget(label := QLabel("Входные файлы"))
        self.labels.append(label)
        self.test_in_files_edit = QLineEdit()
        self.test_in_files_edit.setFixedSize(300, 24)
        main_layout.addWidget(self.test_in_files_edit)

        main_layout.addWidget(label := QLabel("Выходные файлы"))
        self.labels.append(label)
        self.test_out_files_edit = QLineEdit()
        self.test_out_files_edit.setFixedSize(300, 24)
        main_layout.addWidget(self.test_out_files_edit)

        main_layout.addWidget(label := QLabel("Файлы проверки состояния входных"))
        self.labels.append(label)
        self.test_check_files_edit = QLineEdit()
        self.test_check_files_edit.setFixedSize(300, 24)
        main_layout.addWidget(self.test_check_files_edit)

