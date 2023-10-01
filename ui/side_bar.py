from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from ui.button import Button
from ui.side_panel_widget import SidePanelWidget


class SidePanel(QWidget):
    def __init__(self, sm, bm, tm, cm):
        super().__init__()
        self.sm = sm
        self.bm = bm
        self.tm = tm
        self.cm = cm

        strange_layout = QHBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)
        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        self._layout = QHBoxLayout()
        self._layout.setSpacing(5)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setAlignment(Qt.AlignTop)
        strange_widget.setLayout(self._layout)

        self.tabs: dict[str: SidePanelWidget] = dict()

        self.resizing = False
        self.current_tab: SidePanelWidget | None = None
        self.current_tab_key = None
        self.mouse_x = None

        self.hide()

    def add_tab(self, key, widget: SidePanelWidget):
        self.tabs[key] = widget
        widget.hide()
        widget.startResizing.connect(self.start_resizing)
        self._layout.addWidget(widget)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.resizing and isinstance(self.current_tab, QWidget):
            if self.mouse_x is not None:
                self.setMaximumWidth(max(200, self.width() + a0.x() - self.mouse_x))
                self.current_tab.side_panel_width = self.maximumWidth()
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
        self.setMaximumWidth(self.current_tab.side_panel_width)

    def tab_command(self, tab, args, kwargs):
        self.tabs[tab].command(*args, **kwargs)

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

        self._layout = QVBoxLayout()
        self._layout.setSpacing(5)
        self._layout.setContentsMargins(5, 5, 5, 5)
        self._layout.setAlignment(Qt.AlignTop)
        strange_widget.setLayout(self._layout)

        self.buttons = dict()

    def add_tab(self, widget: SidePanelWidget, name: str):
        button = SideBarButton(self.tm, name, f'button_{name}')
        self._layout.addWidget(button)
        button.clicked.connect(lambda flag: self.button_clicked(button.name, flag))
        self.buttons[name] = button
        self.side_panel.add_tab(name, widget)

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

    def set_theme(self):
        self.setStyleSheet(f"background-color: {self.tm['MenuColor']}; "
                           f"border-right: 1px solid {self.tm['BorderColor']};")
        for el in self.buttons.values():
            el.set_theme(self.tm)


class SideBarButton(Button):
    def __init__(self, tm, name, image):
        super().__init__(tm, image, css='Menu', color='TextColor')
        self.name = name
        self.setFixedSize(30, 30)
        self.setCheckable(True)
