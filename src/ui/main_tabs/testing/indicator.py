from PyQt6.QtCore import Qt
from PyQtUIkit.widgets import KitLabel

from src.backend.backend_types import FuncTest


class TestCountIndicator(KitLabel):
    def __init__(self, test_type: FuncTest.Type):
        super().__init__()
        self._type = test_type
        self._name = 'POS' if self._type == FuncTest.Type.POS else 'NEG'

        self.setFixedSize(125, 26)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._count = 0
        self._passed = 0
        self._completed = 0

    @property
    def count(self):
        return self._count

    @property
    def passed(self):
        return self._passed

    @property
    def completed(self):
        return self._completed

    def set_text(self):
        self.setText(f"{self._name}: {self._passed}/{self._count}")
        if self._passed == self._count:
            self.main_palette = 'Success'
        elif self._passed < self._completed:
            self.main_palette = 'Danger'
        else:
            self.main_palette = 'Main'
        self._apply_theme()

    def set_count(self, count):
        self._passed = 0
        self._completed = 0
        self._count = count
        self.set_text()

    def add_test(self, status: FuncTest.Status):
        self._completed += 1
        if status == FuncTest.Status.PASSED:
            self._passed += 1
        self.set_text()
