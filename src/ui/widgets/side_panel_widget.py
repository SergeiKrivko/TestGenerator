from PyQt6.QtCore import pyqtSignal, Qt, QPoint
from PyQt6.QtGui import QCursor
from PyQtUIkit.widgets import KitVBoxLayout, KitHBoxLayout, KitIconButton, KitLabel, KitVSeparator

from src.backend.managers import BackendManager


class SidePanelWidget(KitHBoxLayout):
    startResizing = pyqtSignal()

    def __init__(self, bm: BackendManager, name=''):
        super().__init__()
        self.bm = bm
        self.side_panel_width = 300

        self.__layout = KitVBoxLayout()
        self.__layout.setContentsMargins(5, 5, 0, 5)
        self.__layout.setSpacing(5)
        self.addWidget(self.__layout)

        top_layout = KitHBoxLayout()
        # top_layout.padding = 5
        top_layout.setSpacing(2)

        self._name_label = KitLabel(name)
        top_layout.addWidget(self._name_label)

        self.buttons_layout = KitHBoxLayout()
        self.buttons_layout.spacing = 6
        self.buttons_layout.alignment = Qt.AlignmentFlag.AlignRight
        top_layout.addWidget(self.buttons_layout)

        self.__layout.addWidget(top_layout)

        self._resize_widget = _ResizeWidget()
        self._resize_widget.resized.connect(self._resize)
        self.addWidget(self._resize_widget)

        self.addWidget(KitVSeparator())

        super().setFixedWidth(self.side_panel_width)

    def _resize(self, w):
        width = max(200, self.width() - w)
        super().setFixedWidth(width)

    def setWidget(self, w):
        self.__layout.addWidget(w)

    def setFixedWidth(self, w: int) -> None:
        self._resize_widget.setDisabled(True)
        super().setFixedWidth(w)

    def command(self, *args, **kwargs):
        pass

    def finish_work(self):
        pass


class SidePanelButton(KitIconButton):
    def __init__(self, icon, tooltip=''):
        super().__init__(icon)
        if tooltip:
            self.setToolTip(tooltip)
        self.size = 26


class _ResizeWidget(KitVBoxLayout):
    resized = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setMaximumHeight(10000)
        self.setFixedWidth(5)

        self.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))

        self._last_pos = None

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            self._last_pos = self.mapToParent(e.pos()).x()

    def mouseReleaseEvent(self, e) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            self._last_pos = None

    def mouseMoveEvent(self, a0):
        super().mouseMoveEvent(a0)
        if self._last_pos is None:
            return
        pos = self.mapToParent(a0.pos())
        self.resized.emit(self._last_pos - pos.x())
        self._last_pos = pos.x()
