import os

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QWidget, \
    QLineEdit

from src.backend.backend_types.build import Build
from src.backend.managers import BackendManager
from src.language.languages import languages
from src.language.utils import get_files
from src.ui.button import Button
from src.ui.side_panel_widget import SidePanelWidget
from src.ui.tree_widget import TreeWidget, TreeWidgetItemCheckable


class BuildPanel(SidePanelWidget):
    def __init__(self, sm, bm: BackendManager, tm):
        super().__init__(sm, tm, "Сценарии сборки", [])
        self.bm = bm

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(buttons_layout)

        self.button_add = Button(self.tm, 'buttons/plus', css='Main')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(40)
        self.button_add.clicked.connect(self.add_scenario)
        buttons_layout.addWidget(self.button_add, 1)

        self.button_delete = Button(self.tm, 'buttons/delete', css='Main')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(40)
        self.button_delete.clicked.connect(self.delete_scenario)
        buttons_layout.addWidget(self.button_delete, 1)

        self.button_up = Button(self.tm, 'buttons/button_up', css='Main')
        self.button_up.setFixedHeight(22)
        self.button_up.setMaximumWidth(40)
        self.button_up.clicked.connect(self.move_scenario_up)
        buttons_layout.addWidget(self.button_up, 1)

        self.button_down = Button(self.tm, 'buttons/button_down', css='Main')
        self.button_down.setFixedHeight(22)
        self.button_down.setMaximumWidth(40)
        self.button_down.clicked.connect(self.move_scenario_down)
        buttons_layout.addWidget(self.button_down, 1)

        self._list_widget = QListWidget()
        self._list_widget.currentItemChanged.connect(self.select_build)
        main_layout.addWidget(self._list_widget, 2)

        self._scenario_edit = ScenarioEdit(self.sm, self.bm, self.tm)
        main_layout.addWidget(self._scenario_edit, 4)

        self.bm.builds.onLoad.connect(lambda lst: [self._on_add_build(el) for el in lst])
        self.bm.builds.onAdd.connect(self._on_add_build)
        self.bm.builds.onDelete.connect(self._on_build_deleted)
        self.bm.builds.onClear.connect(self._on_builds_clear)
        self.bm.builds.onRename.connect(self._on_build_renamed)

    def _on_builds_clear(self):
        self._list_widget.clear()

    def _on_add_build(self, build: Build):
        self._list_widget.addItem(ListWidgetItem(build, self.tm))

    def _on_build_deleted(self, build: Build):
        for i in range(self._list_widget.count()):
            if isinstance(item := self._list_widget.item(i), ListWidgetItem) and item.build == build:
                self._list_widget.takeItem(i)
                break

    def _on_build_renamed(self, build, new_name):
        for i in range(self._list_widget.count()):
            if isinstance(item := self._list_widget.item(i), ListWidgetItem) and item.build == build:
                item.setText(new_name)
                break

    def select_build(self, item):
        if isinstance(item, ListWidgetItem):
            self._scenario_edit.load_scenario(item.build)

    def add_scenario(self):
        self.bm.builds.add(Build(''))

    def delete_scenario(self):
        item = self._list_widget.currentItem()
        if isinstance(item, ListWidgetItem):
            self.bm.builds.delete(item.build.name)

    def move_scenario_up(self):
        index = self._list_widget.currentRow()
        if index == 0:
            return
        item = self._list_widget.takeItem(index)
        index -= 1
        self._list_widget.insertItem(index, item)
        self._list_widget.setCurrentRow(index)

    def move_scenario_down(self):
        index = self._list_widget.currentRow()
        if index == self._list_widget.count() - 1:
            return
        item = self._list_widget.takeItem(index)
        index += 1
        self._list_widget.insertItem(index, item)
        self._list_widget.setCurrentRow(index)

    def set_theme(self):
        super().set_theme()
        for el in [self._list_widget]:
            self.tm.auto_css(el)
        for el in [self.button_add, self.button_delete, self.button_up, self.button_down, self._scenario_edit]:
            el.set_theme()


class ListWidgetItem(QListWidgetItem):
    def __init__(self, build: Build, tm):
        super().__init__()
        self._tm = tm
        self.build = build
        self.setFont(self._tm.font_medium)
        self.update_name()

    def update_name(self):
        self.setText(self.build.name)


class ScenarioEdit(QWidget):
    def __init__(self, sm, bm: BackendManager, tm):
        super().__init__()
        self._sm = sm
        self._bm = bm
        self._tm = tm
        self._scenario = None

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self._name_edit = QLineEdit()
        self._name_edit.editingFinished.connect(self._on_name_changed)
        main_layout.addWidget(self._name_edit)

        self._keys_edit = QLineEdit()
        self._keys_edit.setPlaceholderText("Ключи компилятора")
        self._keys_edit.editingFinished.connect(lambda: self._scenario.set_keys(self._keys_edit.text()))
        main_layout.addWidget(self._keys_edit)

        self._linker_keys_edit = QLineEdit()
        self._linker_keys_edit.setPlaceholderText("Ключи компоновки")
        self._linker_keys_edit.editingFinished.connect(lambda: self._scenario.set_lkeys(self._linker_keys_edit.text()))
        main_layout.addWidget(self._linker_keys_edit)

        self._tree_widget = TreeWidget(self._tm, TreeWidget.CHECKABLE)
        main_layout.addWidget(self._tree_widget)

    def _on_name_changed(self):
        self._bm.rename_build(self._scenario.name, self._name_edit.text())

    def load_scenario(self, scenario: Build):
        self._scenario = scenario
        if not isinstance(self._scenario, Build):
            return
        self._name_edit.setText(self._scenario.name)
        self.update_tree()
        self._keys_edit.setText(self._scenario.keys)

    def update_tree(self):
        self._tree_widget.clear()
        for el in get_files(lab_dir := self._sm.project.path(), languages[self._scenario.language]['files']):
            el = os.path.relpath(el, lab_dir).replace('\\', '/')
            lst = el.split('/')[:-1]
            tree_elem = TreeElement(self._tm, el)
            self._tree_widget.add_item(tree_elem, key=lst)
            self._connect_tree_elem(tree_elem, el)
            if el in self._scenario.files:
                tree_elem.set_checked(True)
            for key in self._scenario.files:
                if not os.path.isfile(f"{lab_dir}/{el}"):
                    self._scenario.files.remove(key)
        self._tree_widget.set_theme()

    def _connect_tree_elem(self, elem: 'TreeElement', path):
        elem.stateChanged.connect(lambda flag: self._scenario.set_file_status(path, flag))

    def set_theme(self):
        for el in [self._name_edit, self._keys_edit, self._linker_keys_edit]:
            self._tm.auto_css(el)
        self._tree_widget.set_theme()


class TreeElement(TreeWidgetItemCheckable):
    def __init__(self, tm, path):
        super().__init__(tm, os.path.basename(path))
        self.path = path

    def set_checked(self, flag):
        if self._checkbox.isChecked() == flag:
            return
        self._checkbox.setChecked(flag)

    def set_theme(self):
        super().set_theme()
