from PyQt5.QtWidgets import QDialog, QWidget


class SideBarDialog(QDialog):
    def __init__(self, bm, sm, tm):
        super().__init__()
        self.sm = sm
        self.bm = bm
        self.tm = tm

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
