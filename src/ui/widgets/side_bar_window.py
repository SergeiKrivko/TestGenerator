from PyQtUIkit.widgets import KitDialog

from src.backend.managers import BackendManager


class SideBarDialog(KitDialog):
    def __init__(self, parent, bm: BackendManager):
        super().__init__(parent)
        self.bm = bm

    def command(self, *args, **kwargs):
        pass

