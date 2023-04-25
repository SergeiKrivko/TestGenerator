from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class TestEditWidget(QWidget):
    def __init__(self, tm):
        super(TestEditWidget, self).__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.tm = tm

        h_layout1 = QHBoxLayout()
        layout.addLayout(h_layout1)
        h_layout1.addWidget(QLabel("Описание теста"))
        self.test_name_edit = QLineEdit()
        self.test_name_edit.setFont(QFont("Calibri", 10))
        h_layout1.addWidget(self.test_name_edit)

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        layout1 = QVBoxLayout()
        h_layout.addLayout(layout1, 1)
        label = QLabel("Входные данные")
        label.setFixedHeight(20)
        layout1.addWidget(label)
        self.test_in_edit = QTextEdit()
        self.test_in_edit.setFont(QFont("Courier", 10))
        layout1.addWidget(self.test_in_edit)

        layout2 = QVBoxLayout()
        h_layout.addLayout(layout2, 1)
        layout_h2 = QHBoxLayout()
        layout2.addLayout(layout_h2)
        layout_h2.addWidget(QLabel("Выходные данные"))
        self.button_generate = QPushButton()
        self.button_generate.setText("Сгенерировать")
        self.button_generate.setFixedHeight(20)
        layout_h2.addWidget(self.button_generate)
        self.test_out_edit = QTextEdit()
        self.test_out_edit.setFont(QFont("Courier", 10))
        layout2.addWidget(self.test_out_edit)

    def open_test(self, description, data_in, data_out):
        self.test_name_edit.setText(description)
        self.test_in_edit.setText(data_in)
        self.test_out_edit.setText(data_out)

        self.test_in_edit.setDisabled(False)
        self.test_out_edit.setDisabled(False)
        self.test_name_edit.setDisabled(False)
        self.button_generate.setDisabled(False)

    def set_disabled(self):
        self.test_in_edit.setDisabled(True)
        self.test_out_edit.setDisabled(True)
        self.test_name_edit.setDisabled(True)
        self.button_generate.setDisabled(True)
        self.test_in_edit.setText("")
        self.test_out_edit.setText("")
        self.test_name_edit.setText("")

    def set_theme(self):
        self.test_name_edit.setStyleSheet(self.tm.style_sheet)
        self.test_in_edit.setStyleSheet(self.tm.style_sheet)
        self.test_out_edit.setStyleSheet(self.tm.style_sheet)
        self.button_generate.setStyleSheet(self.tm.style_sheet)


