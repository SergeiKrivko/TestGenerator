from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMenu

from src.ui.button import Button
from src.ui.side_bar_window import SideBarDialog, SideBarWindow
from src.ui.side_panel_widget import SidePanelWidget


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
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
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
                self.setMaximumWidth(max(200, self.width() + a0.pos().x() - self.mouse_x))
                self.current_tab.side_panel_width = self.maximumWidth()
            self.mouse_x = a0.pos().x()

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
    SPACING = 5
    BUTTON_SIZE = 30

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
        self._layout.setSpacing(SideBar.SPACING)
        self._layout.setContentsMargins(5, 5, 5, 5)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        strange_widget.setLayout(self._layout)

        self._button_more = SideBarButton(tm, 'more', 'buttons/button_more')
        self._button_more.hide()
        self._button_more.setCheckable(False)
        self._layout.addWidget(self._button_more)

        self._menu = SideBarMenu()
        self._menu.activated.connect(self.move_menu)
        self._button_more.setMenu(self._menu)

        self.buttons = dict()
        self.actions = dict()
        self.desc = dict()
        self._windows = dict()

    def move_menu(self):
        pos = self.mapToGlobal(self._button_more.pos())
        self._menu.move(pos.x() + SideBar.BUTTON_SIZE + 5, pos.y())

    def add_tab(self, name: str, widget: SidePanelWidget | SideBarWindow | SideBarDialog, desc: str = ''):
        button = SideBarButton(self.tm, name, f'icons/{name}')
        self.buttons[name] = button
        self.desc[name] = desc
        if desc:
            button.setToolTip(desc)

        action = self._menu.addAction(QIcon(self.tm.get_image(f'icons/{name}')), desc)
        self.actions[name] = action
        action.setVisible(False)

        self._layout.insertWidget(self._layout.count() - 1, button)
        if isinstance(widget, SidePanelWidget):
            button.clicked.connect(lambda flag: self.button_clicked(button.name, flag))
            action.triggered.connect(lambda: self.button_clicked(button.name, True))
            self.side_panel.add_tab(name, widget)
        elif isinstance(widget, SideBarWindow):
            button.setCheckable(False)
            button.clicked.connect(lambda flag: self.window_button_clicked(button.name))
            action.triggered.connect(lambda flag: self.window_button_clicked(button.name))
            self._windows[name] = widget

    def calc_visible_buttons(self):
        count = 0
        hidden = 0
        for key, item in self.buttons.items():
            if item.isChecked() or self.sm.get_general(f'side_button_{key}', True):
                count += 1
            else:
                hidden += 1
        return count, hidden

    def calc_max_buttons_count(self):
        return (self.height() + SideBar.SPACING) / (SideBar.BUTTON_SIZE + SideBar.SPACING)

    def show_buttons(self):
        visible, hidden = self.calc_visible_buttons()
        max_visible = self.calc_max_buttons_count()
        if max_visible < visible or hidden:
            max_visible -= 1
            self._button_more.show()
        else:
            self._button_more.hide()

        count = 0
        last_key = None
        for key, item in self.buttons.items():
            if count <= (max_visible - 1) and (item.isChecked() or self.sm.get_general(f'side_button_{key}', True)):
                item.show()
                last_key = key
                count += 1
                self.actions[key].setVisible(False)
            elif item.isChecked() and last_key:
                self.buttons[last_key].hide()
                self.actions[last_key].setVisible(True)
                item.show()
                self.actions[key].setVisible(False)
            else:
                item.hide()
                self.actions[key].setVisible(True)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.show_buttons()

    def button_clicked(self, key: str, flag: bool):
        for _key, item in self.buttons.items():
            if _key != key:
                item.setChecked(False)

        if key in self.buttons:
            if flag:
                self.buttons[key].setChecked(True)
                self.side_panel.show_tab(key)
            else:
                self.side_panel.hide()
        self.show_buttons()

    def window_button_clicked(self, key):
        self._windows[key].show()

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
        self._button_more.set_theme()
        self.tm.auto_css(self._menu, palette='Menu')
        for el in self._windows.values():
            el.set_theme()
        self._menu.setStyleSheet(f"""
QMenu {{
    color: {self.tm['TextColor']};
    background-color: {self.tm['MenuColor']};
    border: 1px solid {self.tm['BorderColor']};
    border-radius: 6px;
    spacing: 5px;
    padding: 5px;
}}

QMenu::item {{
    border: 0px solid {self.tm['BorderColor']};
    background-color: transparent;
    border-radius: 8px;
    height: 30px;
    padding: 0px 8px;
    alignment: left;
}}

QMenu::item:selected {{
    background-color: {self.tm['MenuHoverColor']};
}}
QMenu::separator {{
    height: 1px;
    background: {self.tm['BorderColor']};
    margin: 4px 10px;
}}""")


class SideBarButton(Button):
    def __init__(self, tm, name, image):
        super().__init__(tm, image, css='Menu', color='TextColor')
        self.name = name
        self.setFixedSize(SideBar.BUTTON_SIZE, SideBar.BUTTON_SIZE)
        self.setCheckable(True)


class SideBarMenu(QMenu):
    activated = pyqtSignal()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.activated.emit()
