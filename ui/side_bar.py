from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from code_tab.files_widget import FilesWidget
from code_tab.terminal_tab import TerminalTab
from language.build.build_panel import BuildPanel
from other.chat_widget import ChatPanel
from other.git_panel import GitPanel
from other.telegram.telegram_widget import TelegramWidget
from other.todo_panel import TODOPanel
from settings.project_widget import ProjectWidget
from code_tab.console import ConsolePanel
from tests.generator_window import GeneratorTab
from tests.testing_panel import TestingPanel
from ui.button import Button
from ui.side_panel_widget import SidePanelWidget


class SidePanel(QWidget):
    def __init__(self, sm, tm, cm):
        super().__init__()
        self.sm = sm
        self.tm = tm
        self.cm = cm

        strange_layout = QHBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)
        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        strange_widget.setLayout(layout)

        self.tabs = {
            'projects': ProjectWidget(self.sm, self.tm),
            'files': FilesWidget(self.sm, self.cm, self.tm),
            'build': BuildPanel(self.sm, self.tm),
            'tests': TestingPanel(self.sm, self.tm),
            'todo': TODOPanel(self.sm, self.cm, self.tm),
            'git': GitPanel(self.sm, self.cm, self.tm),
            'generator': GeneratorTab(self.sm, self.cm, self.tm),
            'terminal': TerminalTab(self.sm, self.tm),
            'run': ConsolePanel(self.sm, self.tm, self.cm),
            'chat': ChatPanel(self.sm, self.tm),
            'telegram': TelegramWidget(self.sm, self.tm),
        }
        self.tab_width = {'projects': 225, 'files': 225, 'tests': 225, 'git': 300, 'todo': 300, 'chat': 300,
                          'telegram': 300, 'build': 300}

        for key, el in self.tabs.items():
            if isinstance(el, SidePanelWidget):
                el.hide()
                el.startResizing.connect(self.start_resizing)
                layout.addWidget(el)

        self.resizing = False
        self.current_tab = None
        self.current_tab_key = None
        self.mouse_x = None

        self.hide()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.resizing and isinstance(self.current_tab, QWidget):
            if self.mouse_x is not None:
                self.setMaximumWidth(max(200, self.width() + a0.x() - self.mouse_x))
                self.tab_width[self.current_tab_key] = self.maximumWidth()
            self.mouse_x = a0.x()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.resizing = False
        self.mouse_x = None

    def start_resizing(self):
        self.resizing = True

    def show_tab(self, key):
        self.show()
        for el in self.tabs.values():
            el.hide()
        self.current_tab_key = key
        self.current_tab = self.tabs[key]
        self.current_tab.show()
        if key in self.tab_width:
            self.setMaximumWidth(self.tab_width[key])

    def finish_work(self):
        for el in self.tabs.values():
            el.finish_work()

    def set_theme(self):
        self.setStyleSheet(f"background-color: {self.tm['MainColor']}; "
                           f"border-right: 1px solid {self.tm['BorderColor']};")
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

        self.buttons = {el: SideBarButton(self.tm, f'button_{el}') for el in [
            'projects', 'files', 'build', 'tests', 'git', 'todo', 'generator', 'terminal', 'run', 'chat', 'telegram']}
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

    def select_tab(self, key):
        for _key, item in self.buttons.items():
            if _key != key:
                item.setChecked(False)
            else:
                item.setChecked(True)
        self.side_panel.show_tab(key)

    def connect_button(self, button):
        return lambda flag: self.button_clicked(button.image_name[7:], flag)

    def set_theme(self):
        self.setStyleSheet(f"background-color: {self.tm['MenuColor']}; "
                           f"border-right: 1px solid {self.tm['BorderColor']};")
        for el in self.buttons.values():
            el.set_theme(self.tm)


class SideBarButton(Button):
    def __init__(self, tm, image):
        super().__init__(tm, image, css='Menu', color='TextColor')
        self.setFixedSize(30, 30)
        self.setCheckable(True)
