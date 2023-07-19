from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget

from code_tab.files_widget import FilesWidget
from code_tab.terminal_tab import TerminalTab
from other.git_panel import GitPanel
from settings.project_widget import ProjectWidget
from tests.console import ConsolePanel
from tests.testing_panel import TestingPanel
from ui.button import Button
from ui.side_panel_widget import SidePanelWidget


class SidePanel(QWidget):
    def __init__(self, sm, tm, cm):
        super().__init__()
        self.sm = sm
        self.tm = tm
        self.cm = cm

        strange_layout = QVBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)
        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignTop)
        strange_widget.setLayout(layout)

        self.tabs = {
            'projects': ProjectWidget(self.sm, self.tm, lambda *args: None),
            'files': FilesWidget(self.sm, self.cm, self.tm),
            'tests': TestingPanel(self.sm, self.tm),
            'search': SidePanelWidget(self.sm, self.tm, "Поиск", []),
            'todo': SidePanelWidget(self.sm, self.tm, "TODO", []),
            'git': GitPanel(self.sm, self.cm, self.tm),
            'terminal': TerminalTab(self.sm, self.tm),
            'run': ConsolePanel(self.sm, self.tm, self.cm)
        }

        for el in self.tabs.values():
            if isinstance(el, SidePanelWidget):
                el.hide()
                layout.addWidget(el)

        self.hide()

    def show_tab(self, key):
        self.show()
        for el in self.tabs.values():
            el.hide()
        self.tabs[key].show()

    def set_theme(self):
        self.setStyleSheet(f"background-color: {self.tm['MainColor']}; border: 0px solid black;"
                           f"border-top-right-radius: 10px; border-bottom-right-radius: 10px;")
        for el in self.tabs.values():
            if hasattr(el, 'set_theme'):
                el.set_theme()
            else:
                self.tm.auto_css(el)


class SideBar(QWidget):
    def __init__(self, sm, tm, side_panel: SidePanel):
        super().__init__()
        self.sm = sm
        self.tm = tm
        self.side_panel = side_panel
        self.setFixedWidth(40)

        strange_layout = QVBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)
        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignTop)
        strange_widget.setLayout(layout)

        self.buttons = {el: SideBarButton(self.tm, f'button_{el}') for el in ['projects', 'files', 'tests', 'search',
                                                                              'git', 'todo', 'terminal', 'run']}
        for el in self.buttons.values():
            layout.addWidget(el)
            el.clicked.connect(self.connect_button(el))

    def button_clicked(self, key: str, flag: bool):
        for _key, item in self.buttons.items():
            if _key != key:
                item.setChecked(False)

        if key in self.buttons:
            if flag:
                self.side_panel.show_tab(key)
            else:
                self.side_panel.hide()

    def connect_button(self, button):
        return lambda flag: self.button_clicked(button.image_name[7:], flag)

    def set_theme(self):
        self.setStyleSheet(f"background-color: {self.tm['MenuColor']};")
        for el in self.buttons.values():
            el.set_theme(self.tm)


class SideBarButton(Button):
    def __init__(self, tm, image):
        super().__init__(tm, image, css='Menu', color='TextColor')
        self.setFixedSize(30, 30)
        self.setCheckable(True)
