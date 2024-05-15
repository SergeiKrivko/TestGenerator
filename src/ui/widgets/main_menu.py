from PyQt6.QtCore import pyqtSignal, Qt, QPoint
from PyQtUIkit.widgets import *

from src.ui.widgets.projects import ProjectsWidget


class MainMenu(KitHBoxLayout):
    tab_changed = pyqtSignal(str)

    def __init__(self, bm):
        super().__init__()
        self.bm = bm

        self.setFixedHeight(44)
        self.padding = 10, 7, 10, 7
        self.border = 0
        self.main_palette = 'Menu'
        self.spacing = 35

        self._projects_widget = ProjectsWidget(self.bm)
        self.addWidget(self._projects_widget)

        self._buttons = dict()
        self._buttons_layout = KitHBoxLayout()
        self._buttons_layout.setSpacing(5)
        self.addWidget(self._buttons_layout)

        self.addWidget(KitHBoxLayout(), 100)

        right_layout = KitHBoxLayout()
        right_layout.setSpacing(5)
        self.addWidget(right_layout)

        self.button_settings = _Button('line-settings')
        right_layout.addWidget(self.button_settings)

        self.current_tab = ''
        self.last_pos = None
        self.moving = False
        self.maximized = False

    def add_tab(self, identifier: str, name: str):
        button = KitButton(name)
        button.border = 0
        button.radius = 6
        button.main_palette = 'Menu'
        button.setFixedHeight(26)
        button.setCheckable(True)
        button.clicked.connect(lambda flag: self.select_tab(identifier, flag))
        self._buttons_layout.addWidget(button, 1, Qt.AlignmentFlag.AlignLeft)

        self._buttons[identifier] = button

    def remove_tab(self, identifier):
        self._buttons_layout.removeWidget(self._buttons[identifier])
        self._buttons.pop(identifier)

    def set_tab_hidden(self, key, hidden):
        self._buttons[key].setHidden(hidden)

    def mousePressEvent(self, a0) -> None:
        if a0.button() == Qt.MouseButton.LeftButton and not self.maximized:
            self.moving = True
            self.last_pos = a0.pos()

    def select_tab(self, triggered_key, flag):
        for key, item in self._buttons.items():
            if triggered_key != key:
                item.setChecked(False)
            elif not flag:
                item.setChecked(True)
        if triggered_key != self.current_tab:
            self.current_tab = triggered_key
            self.tab_changed.emit(triggered_key)


class _Button(KitIconButton):
    def __init__(self, icon):
        super().__init__(icon)
        self.size = 30
        self.radius = 6
        self.border = 0
        self.main_palette = 'Menu'
