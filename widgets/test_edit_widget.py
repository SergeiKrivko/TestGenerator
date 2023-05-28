from PyQt5.QtCore import pyqtSignal, Qt
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

        h_layout3 = QHBoxLayout()
        layout.addLayout(h_layout3)

        h_layout3.addWidget(label := QLabel("Препроцессор:"))
        self.labels.append(label)
        self.preprocessor_line = QLineEdit()
        h_layout3.addWidget(self.preprocessor_line)

        h_layout3.addWidget(label := QLabel("Постпроцессор:"))
        self.labels.append(label)
        self.postprocessor_line = QLineEdit()
        h_layout3.addWidget(self.postprocessor_line)

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
        self.preprocessor_line.setStyleSheet(self.tm.style_sheet)
        self.preprocessor_line.setFont(self.tm.code_font)
        self.postprocessor_line.setStyleSheet(self.tm.style_sheet)
        self.postprocessor_line.setFont(self.tm.code_font)
        self.button_generate.setStyleSheet(self.tm.buttons_style_sheet)
        self.button_generate.setFont(self.tm.font_small)
        for label in self.labels:
            label.setFont(self.tm.font_small)


class InEditWidget(QWidget):
    def __init__(self, tm):
        super(InEditWidget, self).__init__()
        self._tm = tm

        self._layout = QVBoxLayout()

        self._tab_layout = QHBoxLayout()
        self._tab_layout.setContentsMargins(0, 0, 0, 0)
        self._tab_layout.setAlignment(Qt.AlignLeft)
        self._tab_layout.setSpacing(0)

        self._stdin_tab = Tab(self._tm, "STDIN", True)
        self._stdin_tab.clicked.connect(self.select_tab)
        self._tab_layout.addWidget(self._stdin_tab)

        self.plus_button = QPushButton("+")
        self.plus_button.setFixedSize(16, 16)
        self.plus_button.clicked.connect(self.add_tab)
        self._tab_layout.addWidget(self.plus_button)

        self._layout.addLayout(self._tab_layout)

        self.stdin_text_edit = QTextEdit()
        self._layout.addWidget(self.stdin_text_edit)
        self.setLayout(self._layout)

        self._tabs = {'STDIN': self._stdin_tab}
        self._widgets = {'STDIN': self.stdin_text_edit}
        
    def add_tab(self):
        name = 'new_tab'
        tab = Tab(self._tm, name)
        self._tabs[name] = tab
        self._tab_layout.addWidget(tab)
        tab.clicked.connect(self.select_tab)
        
        text_edit = QTextEdit()
        self._layout.addWidget(text_edit)
        self._widgets[name] = text_edit
        
    def select_tab(self, name):
        for widget in self._widgets.values():
            widget.hide()
        for widget in self._tabs.values():
            widget.set_selected(False)
        self._widgets[name].show()
        self._tabs[name].set_selected(True)

    def delete_tab(self, name):
        self._tab_layout.removeWidget(self._tabs[name])
        self._tabs.pop(name)

        self._layout.removeWidget(self._widgets[name])
        self._widgets.pop(name)

    def set_theme(self):
        self.plus_button.setStyleSheet(self._tm.buttons_style_sheet)
        for tab in self._tabs.values():
            tab.set_theme()
        for widget in self._widgets.values():
            widget.setStyleSheet(self._tm.text_edit_style_sheet)


class Tab(QWidget):
    clicked = pyqtSignal(str)
    close = pyqtSignal(str)

    def __init__(self, tm, text: str, closable=False):
        super(Tab, self).__init__()
        self._tm = tm
        self._closable = closable
        self._text = text
        self._selected = False
        self.setFixedHeight(20)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._label = QLabel(text)
        layout.addWidget(self._label)

        if self._closable:
            self._button = QPushButton("✕")
            self._button.setFixedSize(12, 12)
            layout.addWidget(self._button)

        self.setLayout(layout)
        self.set_theme()

        self._button.clicked.connect(lambda: self.close.emit(self._text))

    def set_theme(self):
        self.setStyleSheet(f"""
background-color: {self._tm['ColorSelected' if self._selected else 'MainColor']};
border: 1px solid {self._tm['BorderColor']};
border-top-left-radius: 6;
border-top-right-radius: 6;
""")
        if self._closable:
            self._button.setStyleSheet(self._tm.buttons_style_sheet)
        
    def set_selected(self, selected):
        self._selected = selected
        self.set_theme()

    def mousePressEvent(self, a0) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._text)

