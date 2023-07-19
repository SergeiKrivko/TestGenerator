from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, tm, image, color=None, css='Main', tooltip=''):
        super().__init__()
        self.tm = tm
        self.css = css
        self.image_name = image
        self.color = color
        if tooltip:
            self.setToolTip(tooltip)

    def set_theme(self, tm=None):
        if tm is not None:
            self.tm = tm
        self.setStyleSheet(self.tm.button_css(self.css))
        self.setIcon(QIcon(self.tm.get_image(self.image_name, color=self.tm.get(self.color))))
