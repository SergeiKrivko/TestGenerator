from PyQt5.QtWidgets import QVBoxLayout, QTreeWidget, QTreeWidgetItem

from ui.side_panel_widget import SidePanelWidget
from ui.tree_widget import TreeWidget


class TODOPanel(SidePanelWidget):
    def __init__(self, sm, cm, tm):
        super().__init__(sm, tm, 'TODO', ['add', 'delete'])
        self.cm = cm
        # self.setFixedWidth(300)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        layout.addWidget(self.tree)

        self.setLayout(layout)

        # self.sm.project_changed.connect(self.update_tree)

    def update_tree(self):
        self.tree.clear()
        item = QTreeWidgetItem(['item1'], QTreeWidgetItem.DontShowIndicatorWhenChildless)
        item.addChild(QTreeWidgetItem(['item3'], QTreeWidgetItem.DontShowIndicatorWhenChildless))
        self.tree.addTopLevelItem(item)
        item = QTreeWidgetItem(['item2'], QTreeWidgetItem.DontShowIndicatorWhenChildless)
        self.tree.addTopLevelItem(item)
        self.set_theme()

    def set_theme(self):
        super().set_theme()


class TODORecord:
    CODE_TODO = 0
    TG_TODO = 1

    def __init__(self, type, desc, path=None, line=None):
        self.type = type
        self.desc = desc
        self.path = path
        self.line = line
