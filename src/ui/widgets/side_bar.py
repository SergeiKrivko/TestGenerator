from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQtUIkit.widgets import KitHBoxLayout, KitIconButton, KitTabLayout, KitVBoxLayout, KitVSeparator, KitMenu, \
    KitButton
from TestGeneratorPluginLib import SideTab

from src.ui.widgets.side_bar_window import SideBarDialog
from src.ui.widgets.side_panel_widget import SidePanelWidget


class SideBar(KitHBoxLayout):
    SPACING = 5
    WIDTH = 40
    BUTTON_SIZE = 30

    def __init__(self, bm):
        super().__init__()
        self.bm = bm

        self._layout = KitVBoxLayout()
        self._layout.main_palette = 'Menu'
        self._layout.setSpacing(SideBar.SPACING)
        self._layout.padding = 5
        self._layout.radius = 0
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.setFixedWidth(SideBar.WIDTH)
        self.addWidget(self._layout)

        self._button_more = SideBarButton('solid-ellipsis-horizontal', 'more')
        self._button_more.hide()
        self._button_more.setCheckable(False)
        self._layout.addWidget(self._button_more)

        self._menu = SideBarMenu(self)
        self._menu.activated.connect(self.move_menu)
        self._button_more.setMenu(self._menu)

        self.addWidget(KitVSeparator())
        self._tab_layout = KitTabLayout()
        self._tab_layout.hide()
        self._tab_layout.main_palette = 'Main'
        self._tab_layout.radius = 0
        self.addWidget(self._tab_layout)

        self.buttons = dict()
        self.actions = dict()
        self.desc = dict()
        self._tabs = dict()
        self._children = dict()
        self._apply_width(0)

    def move_menu(self):
        pos = self.mapToGlobal(self._button_more.pos())
        self._menu.move(pos.x() + SideBar.BUTTON_SIZE + 5, pos.y())

    def add_tab(self, name: str, widget: SidePanelWidget | SideTab | SideBarDialog, icon: str, desc: str = ''):
        button = SideBarButton(icon, desc)
        self.buttons[name] = button
        self._layout.insertWidget(self._layout.count() - 1, button)
        self.desc[name] = desc
        if desc:
            button.setToolTip(desc)

        action = self._menu.addAction(desc, icon)
        self.actions[name] = action
        action.setVisible(False)

        if isinstance(widget, (SidePanelWidget, SideTab)):
            button.clicked.connect(lambda flag: self.button_clicked(name, flag))
            action.triggered.connect(lambda: self.button_clicked(name, True))
            widget.resized.connect(self._apply_width)

            index = len(self._tabs)
            self._tab_layout.addWidget(widget)
            self._tabs[name] = index

        elif isinstance(widget, SideBarDialog):
            button.setCheckable(False)
            button.clicked.connect(lambda flag: self.window_button_clicked(name))
            action.triggered.connect(lambda flag: self.window_button_clicked(name))

        self._children[name] = widget

    def remove_tab(self, name):
        self._layout.removeWidget(self.buttons[name])
        self.buttons.pop(name)
        self.desc.pop(name)
        self._tab_layout.removeWidget(self._tabs[name])
        self._tabs.pop(name)

    def _apply_width(self, width):
        self.setMaximumWidth(SideBar.WIDTH + width)

    def calc_visible_buttons(self):
        count = 0
        hidden = 0
        for key, item in self.buttons.items():
            if item.isChecked() or self.bm.sm.get_general(f'side_button_{key}', True):
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
            if count <= (max_visible - 1) and (item.isChecked() or self.bm.sm.get_general(f'side_button_{key}', True)):
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
        super().resizeEvent(a0)
        self.show_buttons()

    def button_clicked(self, key: str, flag: bool):
        for _key, item in self.buttons.items():
            if _key != key:
                item.setChecked(False)

        self._tab_layout.setHidden(not flag)
        if not flag:
            self._apply_width(0)
        self._tab_layout.setCurrent(self._tabs[key])
        if key in self.buttons:
            if flag:
                self.buttons[key].setChecked(True)
        self.show_buttons()

    def window_button_clicked(self, key):
        self._children[key].show()

    def select_tab(self, key):
        if key in self._tabs:
            for _key, item in self.buttons.items():
                if _key != key:
                    item.setChecked(False)
                else:
                    item.setChecked(True)

            self._tab_layout.show()
            self._tab_layout.setCurrent(self._tabs[key])
        elif key in self._children:
            self._tab_layout.hide()
            self._children[key].exec()

    def tab_command(self, key, args, kwargs):
        if key in self._tabs:
            self._children[key].command(*args, **kwargs)


class SideBarButton(KitIconButton):
    def __init__(self, icon, name):
        super().__init__(icon)
        self.name = name
        self.size = SideBar.BUTTON_SIZE
        self.main_palette = 'Menu'
        self.border = 0
        self.radius = 6
        self.setCheckable(True)


class SideBarMenu(KitMenu):
    activated = pyqtSignal()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.activated.emit()
