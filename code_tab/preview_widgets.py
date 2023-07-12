from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTextEdit, QLabel, QWidget, QHBoxLayout


class PreviewWidget(QWidget):
    def __init__(self, sm, tm):
        super().__init__()
        self.sm = sm
        self.tm = tm

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def open(self, file: str):
        self.text_edit.hide()
        self.label.hide()

        try:
            if file.endswith('.md'):
                with open(file, encoding='utf-8') as f:
                    self.text_edit.setMarkdown(f.read())
                self.text_edit.show()
            if file.endswith('.html'):
                with open(file, encoding='utf-8') as f:
                    self.text_edit.setHtml(f.read())
                self.text_edit.show()
            if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.bmp'):
                self.label.setPixmap(QPixmap(file))
                self.label.show()
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")

    def set_theme(self):
        for widget in [self.text_edit]:
            self.tm.auto_css(widget)
        self.label.setStyleSheet(self.tm.style_sheet)
