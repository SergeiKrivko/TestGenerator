from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QTextEdit, QLabel, QWidget, QHBoxLayout


class PreviewWidget(QWidget):
    def __init__(self, sm, tm, path=None):
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

        self.web_engine = QWebEngineView()
        self.web_engine.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web_engine.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        layout.addWidget(self.web_engine)

        self.setLayout(layout)
        self.theme_apply = False
        self.file = ''

        if path is not None:
            self.open(path)

    def open(self, file: str):
        self.text_edit.hide()
        self.web_engine.hide()
        self.label.hide()
        self.file = file

        try:
            if file.endswith('.md'):
                with open(file, encoding='utf-8') as f:
                    self.text_edit.setMarkdown(f.read())
                self.text_edit.show()
            if file.endswith('.html') or file.endswith('.pdf'):
                file = file.replace('\\', '/')
                self.web_engine.setUrl(QUrl(f"file:///{file}"))
                self.web_engine.show()
            if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.bmp'):
                self.label.setPixmap(QPixmap(file))
                self.label.show()
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")

    def set_theme(self):
        if self.isHidden():
            return
        self.theme_apply = True
        for widget in [self.text_edit]:
            self.tm.auto_css(widget)
        self.label.setStyleSheet(self.tm.style_sheet)

    def show(self) -> None:
        super().show()
        self.set_theme()
        if not self.file.endswith('.pdf'):
            self.open(self.file)
