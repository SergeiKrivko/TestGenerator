from uuid import UUID

from PyQt6.QtCore import pyqtSignal
from PyQtUIkit.widgets import KitComboBox, KitComboBoxItem

from src.backend.managers import BackendManager
from src.ui.side_tabs.builds.build_icons import IMAGES


class BuildBox(KitComboBox):
    currentChanged = pyqtSignal(object)

    def __init__(self, bm: BackendManager, default=False):
        super().__init__()
        self._sm = bm.sm
        self._bm = bm
        self._default = default
        if self._default:
            self.addItem("")
        self.setMinimumWidth(150)
        self._loading = False

        self.load_data()
        self.currentIndexChanged.connect(self._on_index_changed)

        self._bm.builds.onLoad.connect(self.load_data)
        self._bm.builds.onAdd.connect(self.load_data)
        self._bm.builds.onDelete.connect(self.load_data)
        self._bm.builds.onRename.connect(self.load_data)
        # self._bm.builds.onClear.connect(self.load_data)

    def load_data(self):
        value = self.currentValue()
        self._loading = True
        self.clear()

        if self._default:
            self.addItem(KitComboBoxItem('', ''))
        for key, item in self._bm.builds.all.items():
            self.addItem(KitComboBoxItem(item.name, item.id, IMAGES.get(item.type, 'line-help')))

        self._loading = False
        self.setCurrentValue(value)

    def _on_index_changed(self):
        if not self._loading:
            self.currentChanged.emit(self.current())

    def load(self, value):
        if isinstance(value, str):
            value = UUID(value)
        self.load_data()
        try:
            self.setCurrentValue(value)
        except ValueError:
            pass

    def current(self) -> str | None:
        return self.currentValue()
