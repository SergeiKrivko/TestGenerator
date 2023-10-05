from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem

from backend.types.build import Build
from side_tabs.builds.build_edit import BuildEdit
from ui.button import Button
from ui.side_bar_window import SideBarWindow


class BuildWindow(SideBarWindow):
    def __init__(self, bm, sm, tm):
        super().__init__(bm, sm, tm)

        self.setFixedSize(640, 480)

        layout = QHBoxLayout()
        self.setLayout(layout)

        right_layout = QVBoxLayout()
        layout.addLayout(right_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addLayout(buttons_layout)

        self.button_add = Button(self.tm, 'plus', css='Main')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(40)
        self.button_add.clicked.connect(self.new_build)
        buttons_layout.addWidget(self.button_add, 1)

        self.button_delete = Button(self.tm, 'delete', css='Main')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(40)
        self.button_delete.clicked.connect(self.new_build)
        buttons_layout.addWidget(self.button_delete, 1)

        self._list_widget = QListWidget()
        self._list_widget.currentItemChanged.connect(self._on_build_selected)
        self._list_widget.setFixedWidth(225)
        right_layout.addWidget(self._list_widget)

        self._build_edit = BuildEdit(self.bm, self.sm, self.tm)
        layout.addWidget(self._build_edit)

        self.bm.addBuild.connect(self.add_build)

    def add_build(self, build):
        self._list_widget.addItem(ListWidgetItem(self.tm, build))

    def delete_build(self, build):
        for i in range(self._list_widget.count()):
            if self._list_widget.item(i).build == build:
                self._list_widget.takeItem(i)
                break

    def _on_build_selected(self):
        item = self._list_widget.currentItem()
        self._build_edit.open(item.build)

    def new_build(self):
        build = Build(self.bm.generate_build_id())
        self.bm.add_build(build)

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        self._build_edit.set_theme()
        for el in [self.button_add, self.button_delete, self._list_widget]:
            self.tm.auto_css(el)

    def closeEvent(self, a0) -> None:
        self._build_edit.store_build()


class ListWidgetItem(QListWidgetItem):
    def __init__(self, tm, build: Build):
        super().__init__()
        self.tm = tm
        self.build = build
        self.set_theme()

    def set_theme(self):
        self.setText(self.build.get('name'))
        self.setFont(self.tm.font_medium)
