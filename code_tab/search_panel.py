from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QLabel

from ui.button import Button


class SearchPanel(QWidget):
    selectText = pyqtSignal(int, int, int, int)

    def __init__(self, sm, tm):
        super().__init__()
        self._sm = sm
        self._tm = tm
        self.text = ''
        self.pos = (0, 0)

        strange_layout = QVBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)
        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        strange_widget.setLayout(main_layout)

        line_edit_layout = QVBoxLayout()
        line_edit_layout.setContentsMargins(0, 0, 0, 0)
        line_edit_layout.setSpacing(0)
        main_layout.addLayout(line_edit_layout)

        self.search_line_edit = QLineEdit()
        self.search_line_edit.setFixedHeight(25)
        self.search_line_edit.setMaximumWidth(400)
        line_edit_layout.addWidget(self.search_line_edit)

        self.replace_line_edit = QLineEdit()
        self.replace_line_edit.setFixedHeight(24)
        self.replace_line_edit.setMaximumWidth(400)
        line_edit_layout.addWidget(self.replace_line_edit)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(4)
        right_layout.setContentsMargins(0, 0, 8, 0)
        main_layout.addLayout(right_layout)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft)
        top_layout.setContentsMargins(0, 2, 0, 0)
        right_layout.addLayout(top_layout)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.label)
        self.label.setFixedWidth(120)

        self.button_up = Button(self._tm, 'button_up', css='Main')
        self.button_up.setFixedSize(20, 20)
        self.button_up.clicked.connect(self.search_previous)
        top_layout.addWidget(self.button_up)

        self.button_down = Button(self._tm, 'button_down', css='Main')
        self.button_down.setFixedSize(20, 20)
        self.button_down.clicked.connect(self.search_next)
        top_layout.addWidget(self.button_down)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 2)
        bottom_layout.setAlignment(Qt.AlignLeft)
        right_layout.addLayout(bottom_layout)

        self.button_replace = QPushButton("Заменить")
        bottom_layout.addWidget(self.button_replace)

        self.button_replace_all = QPushButton("Заменить все")
        bottom_layout.addWidget(self.button_replace_all)
        
    def search_next(self):
        try:
            if word := self.search_line_edit.text():
                current_line, current_symbol = self.pos
                text = self.text.split('\n')
                self.update_label(text)
                if word in text[current_line][current_symbol:]:
                    index = text[current_line][current_symbol:].index(word) + current_symbol
                    self.selectText.emit(current_line, index, current_line, index + len(word))
                    return True
                else:
                    for i in range(current_line + 1, len(text)):
                        if word in text[i]:
                            index = text[i].index(word)
                            self.selectText.emit(i, index, i, index + len(word))
                            return True
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")
        return False

    def search_previous(self):
        try:
            if word := self.search_line_edit.text():
                current_line, current_symbol = self.pos
                text = self.text.split('\n')
                self.update_label(text)
                if word in text[current_line][:current_symbol - 1]:
                    index = text[current_line][:current_symbol - 1].rindex(word)
                    self.selectText.emit(current_line, index, current_line, index + len(word))
                    return True
                else:
                    for i in range(current_line - 1, -1, -1):
                        if word in text[i]:
                            index = text[i].rindex(word)
                            self.selectText.emit(i, index, i, index + len(word))
                            return True
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")
        return False

    def update_label(self, text):
        count = 0
        word = self.search_line_edit.text()
        for i in range(len(text)):
            if i < self.pos[0]:
                count += text[i].count(word)
            else:
                try:
                    line = text[i][:self.pos[1] + len(word)]
                except IndexError:
                    line = text[i]
                count += line.count(word)
                break
        self.label.setText(f"{count}/{self.text.count(word)}")

    def set_theme(self):
        self.setStyleSheet(f"background-color: {self._tm['MainColor']}; "
                           f"border-bottom: 1px solid {self._tm['BorderColor']};")
        css = f"background-color: {self._tm['MainColor']}; color: {self._tm['TextColor']}; " \
              f"border-bottom: none; border-right: 1px solid {self._tm['BorderColor']};" \
              f"border-left: none; border-top: none;"
        self.replace_line_edit.setStyleSheet(css)
        self.search_line_edit.setStyleSheet(css.replace('border-bottom: none',
                                                        f"border-bottom: 1px solid {self._tm['BorderColor']}"))
        self.search_line_edit.setFont(self._tm.font_small)
        self.replace_line_edit.setFont(self._tm.font_small)
        for el in [self.button_up, self.button_down, self.button_replace, self.button_replace_all, self.label]:
            self._tm.auto_css(el)
