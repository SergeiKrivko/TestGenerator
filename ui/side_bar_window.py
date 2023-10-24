from PyQt6.QtWidgets import QWidget

from ui.custom_dialog import CustomDialog


class SideBarDialog(CustomDialog):
    def __init__(self, bm, sm, tm):
        super().__init__(tm)
        self.sm = sm
        self.bm = bm

    def command(self, *args, **kwargs):
        pass


class SideBarWindow(QWidget):
    def __init__(self, bm, sm, tm):
        super().__init__()
        self.sm = sm
        self.bm = bm
        self.tm = tm

    def command(self, *args, **kwargs):
        pass
