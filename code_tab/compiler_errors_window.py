from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QWidget, QPushButton, QLabel, QScrollArea


class CompilerErrorWindow(QDialog):
    def __init__(self, text: str, files, tm):
        super().__init__()
        self.setWindowTitle("Ошибка компиляции")
        self.setStyleSheet(tm.bg_style_sheet)
        self.tm = tm

        main_layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.scroll_area.setWidget(scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(tm.scroll_area_style_sheet)
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setSpacing(1)
        # self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        scroll_widget.setLayout(self.scroll_layout)
        main_layout.addWidget(self.scroll_area)

        for line in text.split('\n'):
            if len(line.split()) and line.split()[0].count(':') >= 2:
                lst = line.split()[0].split(':')
                if lst[0] in files and lst[1].isdigit() and lst[2].isdigit():
                    button = QPushButton(f"{lst[0]} {lst[1]}:{lst[2]}")
                    button.setStyleSheet(tm.buttons_style_sheet)
                    button.setFont(tm.font_small)
                    button.setFixedWidth(150)
                    self.connect_button(button, lst[0], (lst[1], lst[2]))
                    self.scroll_layout.addWidget(button)
                    self.add_label(line[line.index(' ') + 1:])
                else:
                    self.add_label(line)
            else:
                self.add_label(line)

        # self.text_edit = QTextEdit()
        # self.text_edit.setStyleSheet(tm.text_edit_style_sheet)
        # self.text_edit.setFont(tm.code_font)
        # self.text_edit.setText(text)
        # self.text_edit.setReadOnly(True)
        # main_layout.addWidget(self.text_edit)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.button(QDialogButtonBox.Ok).setStyleSheet(tm.buttons_style_sheet)
        self.buttonBox.button(QDialogButtonBox.Ok).setFont(tm.font_small)
        self.buttonBox.button(QDialogButtonBox.Ok).setFixedSize(80, 20)
        main_layout.addWidget(self.buttonBox)

        self.setLayout(main_layout)
        self.resize(600, 520)
        self.goto = None

    def add_label(self, text):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setFont(self.tm.code_font)
        self.scroll_layout.addWidget(label)

    def connect_button(self, widget, file, pos):
        widget.clicked.connect(lambda: self.button_triggered(file, pos))

    def button_triggered(self, file, pos):
        self.goto = file, int(pos[0]), int(pos[1])
        self.accept()
