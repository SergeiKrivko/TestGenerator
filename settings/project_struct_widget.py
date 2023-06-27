from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QLineEdit, QComboBox


class ProjectStructWidget(QWidget):
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
        self.struct_combo_box.addItems(['Лаба - задание - вариант', 'Без структуры'])
        self.struct_combo_box.setFixedSize(300, 24)
        self.struct_combo_box.currentIndexChanged.connect(lambda value: self.sm.set('struct', value))
        main_layout.addWidget(self.struct_combo_box)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        self.checkbox = QCheckBox()
        self.checkbox.stateChanged.connect(lambda value: self.sm.set('func_tests_in_project', value))
        self.struct_combo_box.currentIndexChanged.connect(lambda value: self.sm.set('struct', value))
        layout.addWidget(self.checkbox)
        self.compiler_label = QLabel("Сохранять тесты в папке проекта")
        self.labels.append(self.compiler_label)
        layout.addWidget(self.compiler_label)
        main_layout.addLayout(layout)

        # main_layout.addWidget(label := QLabel("Файлы с входными данными"))
        # self.labels.append(label)
        # self.test_in_edit = QLineEdit()
        # self.test_in_edit.setFixedSize(300, 24)
        # main_layout.addWidget(self.test_in_edit)
        #
        # main_layout.addWidget(label := QLabel("Файлы с выходными данными"))
        # self.labels.append(label)
        # self.test_out_edit = QLineEdit()
        # self.test_out_edit.setFixedSize(300, 24)
        # main_layout.addWidget(self.test_out_edit)
        #
        # main_layout.addWidget(label := QLabel("Файлы с аргументами"))
        # self.labels.append(label)
        # self.test_args_edit = QLineEdit()
        # self.test_args_edit.setFixedSize(300, 24)
        # main_layout.addWidget(self.test_args_edit)
        #
        # main_layout.addWidget(label := QLabel("Входные файлы"))
        # self.labels.append(label)
        # self.test_in_files_edit = QLineEdit()
        # self.test_in_files_edit.setFixedSize(300, 24)
        # main_layout.addWidget(self.test_in_files_edit)
        #
        # main_layout.addWidget(label := QLabel("Выходные файлы"))
        # self.labels.append(label)
        # self.test_out_files_edit = QLineEdit()
        # self.test_out_files_edit.setFixedSize(300, 24)
        # main_layout.addWidget(self.test_out_files_edit)
        #
        # main_layout.addWidget(label := QLabel("Файлы проверки состояния входных"))
        # self.labels.append(label)
        # self.test_check_files_edit = QLineEdit()
        # self.test_check_files_edit.setFixedSize(300, 24)
        # main_layout.addWidget(self.test_check_files_edit)

        self.setLayout(main_layout)
        self.apply_values()

    def apply_values(self):
        self.struct_combo_box.setCurrentIndex(self.sm.get('struct', 0))
        self.checkbox.setChecked(bool(self.sm.get('func_tests_in_project', True)))

    def set_theme(self):
        for label in self.labels:
            self.tm.auto_css(label)
        for widget in [self.struct_combo_box, self.checkbox]:
            self.tm.auto_css(widget)

