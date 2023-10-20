from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar

from backend.backend_types.project import Project
from backend.backend_manager import BackendManager


class ProgressDialog(QDialog):
    def __init__(self, bm: BackendManager, tm, project: Project):
        super().__init__()
        self._tm = tm
        self._bm = bm

        self.setWindowTitle(f"Загрузка проекта")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self._label = QLabel(f"Открытие проекта\n{project.path()}")
        self._label.setWordWrap(True)
        layout.addWidget(self._label)

        self._progress_bar = QProgressBar()
        self._progress_bar.setFixedHeight(30)
        layout.addWidget(self._progress_bar)

        self.setFixedSize(320, 125)

        self._bm.updateProgress.connect(self.update_progress)
        self._bm.finishChangingProject.connect(self._on_loading_complete)

        self.set_theme()

    def _on_loading_complete(self):
        super().accept()

    def update_progress(self, current, maximum):
        self._progress_bar.setMaximum(maximum)
        self._progress_bar.setValue(current)

    def accept(self) -> None:
        pass

    def reject(self) -> None:
        pass

    def set_theme(self):
        self.setStyleSheet(self._tm.bg_style_sheet)
        for el in [self._progress_bar, self._label]:
            self._tm.auto_css(el)
