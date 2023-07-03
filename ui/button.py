from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, tm, image):
        super().__init__()
        self.tm = tm
        self.image_name = image

    def set_theme(self, tm=None):
        if tm:
            self.tm = tm
        self.setStyleSheet(self.tm.buttons_style_sheet)
        self.setIcon(QIcon(self.tm.get_image(self.image_name)))
