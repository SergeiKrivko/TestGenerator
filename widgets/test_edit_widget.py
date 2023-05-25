from PyQt5.QtWidgets import QTextEdit, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class TestEditWidget(QWidget):
    def __init__(self, tm):
        super(TestEditWidget, self).__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.tm = tm
        self.labels = []

        h_layout1 = QHBoxLayout()
        layout.addLayout(h_layout1)
        h_layout1.addWidget(label := QLabel("Описание теста"))
        self.labels.append(label)
        self.test_name_edit = QLineEdit()
        h_layout1.addWidget(self.test_name_edit)

        h_layout2 = QHBoxLayout()
        layout.addLayout(h_layout2)
        h_layout2.addWidget(label := QLabel("Аргументы"))
        self.labels.append(label)
        self.cmd_args_edit = QLineEdit()
        h_layout2.addWidget(self.cmd_args_edit)

        h_layout2.addWidget(label := QLabel("Код возврата"))
        self.labels.append(label)
        self.exit_code_edit = QLineEdit()
        self.exit_code_edit.setMaximumWidth(80)
        self.exit_code_edit_text = ""
        self.exit_code_edit.textChanged.connect(self.exit_code_edit_triggered)
        h_layout2.addWidget(self.exit_code_edit)

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        layout1 = QVBoxLayout()
        h_layout.addLayout(layout1, 1)
        label = QLabel("Входные данные")
        self.labels.append(label)
        label.setFixedHeight(20)
        layout1.addWidget(label)
        self.test_in_edit = QTextEdit()
        layout1.addWidget(self.test_in_edit)

        layout2 = QVBoxLayout()
        h_layout.addLayout(layout2, 1)
        layout_h2 = QHBoxLayout()
        layout2.addLayout(layout_h2)
        layout_h2.addWidget(label := QLabel("Выходные данные"))
        self.labels.append(label)
        self.button_generate = QPushButton()
        self.button_generate.setText("Сгенерировать")
        self.button_generate.setFixedHeight(20)
        layout_h2.addWidget(self.button_generate)
        self.test_out_edit = QTextEdit()
        layout2.addWidget(self.test_out_edit)

    def exit_code_edit_triggered(self):
        if not self.exit_code_edit.text().strip():
            self.exit_code_edit.setText("")
            self.exit_code_edit_text = ""
        else:
            try:
                int(self.exit_code_edit.text().strip())
            except ValueError:
                self.exit_code_edit.setText(self.exit_code_edit_text)
            else:
                self.exit_code_edit_text = self.exit_code_edit.text()

    def open_test(self, description, data_in, data_out, cmd_args="", exit_code=None):
        self.test_name_edit.setText(description)
        self.test_in_edit.setText(data_in)
        self.test_out_edit.setText(data_out)
        self.cmd_args_edit.setText(cmd_args)
        self.exit_code_edit.setText(exit_code if exit_code else "")

        self.test_in_edit.setDisabled(False)
        self.test_out_edit.setDisabled(False)
        self.test_name_edit.setDisabled(False)
        self.cmd_args_edit.setDisabled(False)
        self.exit_code_edit.setDisabled(False)
        self.button_generate.setDisabled(False)

    def set_disabled(self):
        self.test_in_edit.setDisabled(True)
        self.test_out_edit.setDisabled(True)
        self.test_name_edit.setDisabled(True)
        self.cmd_args_edit.setDisabled(True)
        self.exit_code_edit.setDisabled(True)
        self.button_generate.setDisabled(True)
        self.test_in_edit.setText("")
        self.test_out_edit.setText("")
        self.test_name_edit.setText("")

    def set_theme(self):
        self.test_name_edit.setStyleSheet(self.tm.style_sheet)
        self.test_name_edit.setFont(self.tm.font_small)
        self.test_in_edit.setStyleSheet(self.tm.text_edit_style_sheet)
        self.test_in_edit.setFont(self.tm.code_font)
        self.test_out_edit.setStyleSheet(self.tm.text_edit_style_sheet)
        self.test_out_edit.setFont(self.tm.code_font)
        self.cmd_args_edit.setStyleSheet(self.tm.style_sheet)
        self.cmd_args_edit.setFont(self.tm.code_font)
        self.exit_code_edit.setStyleSheet(self.tm.style_sheet)
        self.exit_code_edit.setFont(self.tm.font_small)
        self.button_generate.setStyleSheet(self.tm.buttons_style_sheet)
        self.button_generate.setFont(self.tm.font_small)
        for label in self.labels:
            label.setFont(self.tm.font_small)


