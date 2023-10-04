import json

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QScrollArea

from other.report.docx_converter import DocxConverter
from other.report.widgets import ReportMainDocument
from ui.message_box import MessageBox
from ui.side_bar_window import SideBarWindow


class ReportWindow(SideBarWindow):
    def __init__(self, bm, sm, tm):
        super().__init__(bm, sm, tm)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 0, 10)
        self.setLayout(main_layout)
        self.resize(800, 500)

        self._main_document = ReportMainDocument(self.tm)
        self._main_document.set_margins(0, 0, 10, 0)

        self._scroll_area = QScrollArea()
        main_layout.addWidget(self._scroll_area)
        self._scroll_area.setWidget(self._main_document)
        self._scroll_area.setWidgetResizable(True)

    def show(self) -> None:
        super().show()
        self.load_file()
        self.set_theme()

    def save_file(self):
        with open(f"{self.sm.project.data_path()}/report.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._main_document.store()))

    def convert_file(self):
        print(f"{self.sm.project.path()}/report.docx")
        converter = DocxConverter(self._main_document.store(), f"{self.sm.project.path()}/report.docx")
        converter.convert()

    def load_file(self):
        try:
            with open(f"{self.sm.project.data_path()}/report.json", encoding='utf-8') as f:
                self._main_document.load(json.loads(f.read()))
        except FileNotFoundError:
            pass
        except Exception as ex:
            MessageBox(MessageBox.Warning, "Ошибка", f"Не удалось загрузить файл:\n{ex.__class__.__name__}: {ex}",
                       self.tm)

    def closeEvent(self, a0) -> None:
        super().closeEvent(a0)
        self.save_file()
        self.convert_file()

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        self.tm.auto_css(self._scroll_area, palette='Bg', border=False)
        self._main_document.set_theme()
