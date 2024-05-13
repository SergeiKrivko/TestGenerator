import webbrowser

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap
from PyQtUIkit.widgets import KitHBoxLayout, KitTextEdit, KitImageViewer

from src import config


class PreviewWidget(KitHBoxLayout):
    def __init__(self, path):
        super().__init__()
        self._path = path

        self.text_edit = None
        self.image_viewer = None
        self.web_engine = None

        if path.endswith('.md'):
            self.open_markdown()
        elif path.endswith('.html') or path.endswith('.pdf'):
            self.open_web()
        elif (path.endswith('.png') or path.endswith('.jpeg') or path.endswith('.jpg') or path.endswith('.png') or
              path.endswith('.svg')):
            self.open_image()

    def open_markdown(self):
        self.text_edit = KitTextEdit()
        self.text_edit.radius = 0
        self.text_edit.border = 0
        self.text_edit.main_palette = 'Bg'
        self.text_edit.setViewportMargins(30, 10, 30, 10)
        self.text_edit.setReadOnly(True)
        self.addWidget(self.text_edit)

        with open(self._path, encoding='utf-8') as f:
            self.text_edit.setMarkdown(f.read())

    def open_image(self):
        self.image_viewer = KitImageViewer()
        self.image_viewer.min_zoom = 0.125
        self.image_viewer.max_zoom = 16
        self.image_viewer.setPixmap(QPixmap(self._path))
        self.addWidget(self.image_viewer)

    def open_web(self):
        file = self._path.replace('\\', '/')
        if config.USE_WEB_ENGINE:
            from PyQt6.QtWebEngineCore import QWebEngineSettings
            from PyQt6.QtWebEngineWidgets import QWebEngineView

            self.web_engine = QWebEngineView()
            self.web_engine.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
            self.web_engine.settings().setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
            self.addWidget(self.web_engine)
            self.web_engine.setUrl(QUrl.fromLocalFile(file))
            self.web_engine.show()
        else:
            webbrowser.open(f"file:///{file}")
