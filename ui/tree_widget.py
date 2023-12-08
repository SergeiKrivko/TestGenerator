from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QVBoxLayout, QPushButton, QScrollArea

from ui.button import Button


class TreeWidgetItem(QWidget):
    def __init__(self, name: str):
        super().__init__()
        self._name = name

    def set_name(self, name: str):
        self._name = name

    def name(self):
        return self._name


class TreeWidgetItemCheckable(TreeWidgetItem):
    stateChanged = pyqtSignal(bool)

    def __init__(self, tm, name):
        super().__init__(name)
        self._tm = tm
        self._color = 'TextColor'

        self._layout = QHBoxLayout()
        self._layout.setSpacing(2)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._layout.setContentsMargins(25, 3, 3, 3)

        self._checkbox = QCheckBox()
        self._checkbox.stateChanged.connect(self.stateChanged.emit)
        self._layout.addWidget(self._checkbox)

        self._label = QLabel(self._name)
        self._layout.addWidget(self._label)

        self.setLayout(self._layout)

    def set_name(self, name: str):
        super().set_name(name)
        self._label.setText(self._name)

    def set_color(self, color):
        self._color = color
        self.set_theme()

    def set_theme(self):
        self._tm.auto_css(self._checkbox)
        color = self._tm[self._color]
        if isinstance(color, QColor):
            color = color.name()
        self._label.setStyleSheet(f"color: {color};")
        self._label.setFont(self._tm.font_medium)


class TreeBranch(QWidget):
    stateChanged = pyqtSignal(bool)
    clicked = pyqtSignal()

    def __init__(self, tm, name, icon: str = None, maximize=False, checkbox=False, palette='Main'):
        super().__init__()
        self.tm = tm
        self._name = name
        self._icon = icon
        self._checkbox_enabled = checkbox
        self.parent = None
        self._palette = palette
        self._maximize = maximize

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self._top_layout = QHBoxLayout()
        self._top_layout.setSpacing(5)
        self._top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._top_layout.setContentsMargins(3, 3, 3, 3)
        if not self._maximize:
            main_layout.addLayout(self._top_layout)

        self._button_maximize = Button(self.tm, 'buttons/button_maximize')
        self._button_maximize.setFixedSize(17, 17)
        self._button_maximize.clicked.connect(self.maximize)
        self._top_layout.addWidget(self._button_maximize)

        self._button_minimize = Button(self.tm, 'buttons/button_minimize')
        self._button_minimize.setFixedSize(17, 17)
        self._button_minimize.clicked.connect(self.minimize)
        self._button_minimize.hide()
        self._top_layout.addWidget(self._button_minimize)

        self._checkbox = QCheckBox()
        self._checkbox.stateChanged.connect(self.stateChanged.emit)
        self._top_layout.addWidget(self._checkbox)
        if not self._checkbox_enabled:
            self._checkbox.hide()

        self._label = QLabel(name)
        self._top_layout.addWidget(self._label)

        self.items_layout = QVBoxLayout()
        self.items_layout.setContentsMargins(5 if maximize else 15, 0, 0, 0)
        self.items_layout.setSpacing(0)
        main_layout.addLayout(self.items_layout)

        self.child_widgets = dict()

    def set_name(self, name: str):
        self._name = name
        self._label.setText(name)

    def name(self):
        return self._name

    def __getitem__(self, item: str | tuple | list):
        if isinstance(item, str):
            item = (item,)
        dct = self
        for el in item:
            dct = dct.child_widgets[el]
        return dct

    def _parse_key(self, key: str | tuple | list = None, add_branches=False):
        branch = self
        if key is not None:
            if isinstance(key, str):
                key = (key,)
            for el in key:
                if add_branches and el not in branch.child_widgets:
                    branch.add_branch(el)
                branch = branch.child_widgets[el]
        return branch

    def add_branch(self, item, key: str | tuple | list = None):
        if isinstance(item, str):
            item = TreeBranch(self.tm, item)
        if not isinstance(item, TreeBranch):
            raise TypeError(f"Argument 2 has unexpected type {item.__class__.__name__}")

        branch = self._parse_key(key, add_branches=True)

        if branch != self:
            branch.add_branch(item)
            return False

        self.items_layout.addWidget(item)
        item.parent = self
        self.child_widgets[item.name()] = item
        if not self._maximize:
            item.hide()
        return True

    def add_item(self, item: TreeWidgetItem, key: str | tuple | list = None):
        branch = self._parse_key(key, add_branches=True)

        if branch != self:
            branch.add_item(item)
            return False

        self.items_layout.addWidget(item)
        self.child_widgets[item.name()] = item
        if not self._maximize:
            item.hide()
        return True

    def maximize(self):
        for el in self.child_widgets.values():
            el.show()
        self._button_maximize.hide()
        self._button_minimize.show()

    def minimize(self):
        for el in self.child_widgets.values():
            el.hide()
        self._button_minimize.hide()
        self._button_maximize.show()

    def clear(self):
        self.child_widgets.clear()
        for i in reversed(range(self.items_layout.count())):
            item = self.items_layout.takeAt(i)
            item.widget().hide()

    def set_theme(self):
        for el in [self._button_minimize, self._button_maximize, self._checkbox, self._label]:
            self.tm.auto_css(el)
        for el in self.child_widgets.values():
            el.set_theme()


class TreeBranchCheckable(TreeBranch):
    is_checkable = pyqtSignal()

    def __init__(self, tm, name, icon=None, maximize=False):
        super().__init__(tm, name, icon, maximize=maximize, checkbox=True)

        self._checkbox.clicked.connect(lambda: self.set_checked(self._checkbox.isChecked()))
        self.checkable_items = 0
        self.checked_items = 0

    def add_branch(self, item: TreeBranch | str, key: str | tuple | list = None):
        if isinstance(item, str):
            item = TreeBranchCheckable(self.tm, item)

        if super().add_branch(item, key):
            item.is_checkable.connect(self._new_checkable_item)
            item._checkbox.stateChanged.connect(self._child_widget_state_changed)

    def add_item(self, item: TreeWidgetItemCheckable | str, key: str | tuple | list = None):
        if isinstance(item, str):
            item = TreeWidgetItemCheckable(self.tm, item)
        if super().add_item(item, key):
            self._new_checkable_item()
            item.stateChanged.connect(self._child_widget_state_changed)

    def _new_checkable_item(self):
        if self._checkbox.isHidden() and not self._maximize:
            self._checkbox.show()
            self.is_checkable.emit()
        self.checkable_items += 1

    def set_checked(self, flag):
        self._checkbox.setChecked(flag)
        for el in self.child_widgets.values():
            el.set_checked(flag)

    def _child_widget_state_changed(self, state):
        self.checked_items += (1 if state else -1)
        if self.checked_items >= self.checkable_items:
            self.checked_items = self.checkable_items
            self._checkbox.setChecked(True)
        else:
            self._checkbox.setChecked(False)
            if self.checked_items < 0:
                self.checked_items = 0


class TreeWidget(QScrollArea):
    ABSTRACT = 0
    CHECKABLE = 1
    SELECTABLE = 2

    _BRANCHES = {0: TreeBranch, 1: TreeBranchCheckable}
    _ITEMS = {0: QWidget, 1: TreeWidgetItemCheckable}

    def __init__(self, tm, type=0):
        super().__init__()
        self.tm = tm
        self.type = type
        self.main_widget = self._BRANCHES[type](self.tm, '__tree_widget_main_branch__', maximize=True)

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

    def add_branch(self, item: TreeBranch, key: str | tuple | list = None):
        if isinstance(item, str):
            item = self._BRANCHES[self.type](self.tm, item)

        self.main_widget.add_branch(item, key)
        if key is None:
            item.show()

    def add_item(self, item: QWidget | str, key: str | tuple | list = None):
        if isinstance(item, str):
            item = self._ITEMS[self.type](self.tm, item)

        self.main_widget.add_item(item, key)
        if key is None:
            item.show()

    def clear(self):
        self.main_widget.clear()

    def __getitem__(self, item: str | tuple | list):
        return self.main_widget[item]

    def get(self, key: str | tuple | list):
        return self[key]

    def set_theme(self, palette='Main'):
        self.tm.auto_css(self, palette)
        self.main_widget.set_theme()
