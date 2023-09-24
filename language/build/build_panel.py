import json
import os

from PyQt5.QtWidgets import QTabBar, QVBoxLayout, QComboBox, QHBoxLayout, QListWidget, QListWidgetItem, QWidget, \
    QLineEdit

from language.build.make_convert import MakeConverter
from language.languages import languages
from language.utils import get_files
from ui.button import Button
from ui.side_panel_widget import SidePanelWidget
from ui.tree_widget import TreeWidget, TreeWidgetItemCheckable


class BuildPanel(SidePanelWidget):
    def __init__(self, sm, tm):
        super().__init__(sm, tm, "Сценарии сборки", [])

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(buttons_layout)

        self.button_add = Button(self.tm, 'plus', css='Main')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(40)
        self.button_add.clicked.connect(self.add_scenario)
        buttons_layout.addWidget(self.button_add, 1)

        self.button_delete = Button(self.tm, 'delete', css='Main')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(40)
        self.button_delete.clicked.connect(self.delete_scenario)
        buttons_layout.addWidget(self.button_delete, 1)

        self.button_up = Button(self.tm, 'button_up', css='Main')
        self.button_up.setFixedHeight(22)
        self.button_up.setMaximumWidth(40)
        self.button_up.clicked.connect(self.move_scenario_up)
        buttons_layout.addWidget(self.button_up, 1)

        self.button_down = Button(self.tm, 'button_down', css='Main')
        self.button_down.setFixedHeight(22)
        self.button_down.setMaximumWidth(40)
        self.button_down.clicked.connect(self.move_scenario_down)
        buttons_layout.addWidget(self.button_down, 1)

        self._list_widget = QListWidget()
        self._list_widget.currentItemChanged.connect(lambda item: self._scenario_edit.load_scenario(item))
        main_layout.addWidget(self._list_widget, 2)

        self._scenario_edit = ScenarioEdit(self.sm, self.tm)
        main_layout.addWidget(self._scenario_edit, 4)

        self.data_dir = ""
        self.temp_file_index = 0
        self.sm.finishChangeTask.connect(self.open_task)
        self.sm.startChangeTask.connect(self.store_task)
        self._files = dict()

    def open_task(self):
        self.data_dir = f"{self.sm.data_lab_path()}/scenarios/make"
        self.temp_file_index = 0
        self._files.clear()
        self.load_scenarios()

    def load_scenarios(self):
        self._list_widget.clear()
        if not os.path.isdir(self.data_dir):
            return
        for el in os.listdir(self.data_dir):
            if el.endswith('.json'):
                path = os.path.join(self.data_dir, el)
                sc = Scenario(path)
                self._files[path] = sc
                self._list_widget.addItem(sc)

    def store_task(self):
        if not self._list_widget.count():
            return
        converter = MakeConverter(self.sm)
        for i in range(self._list_widget.count()):
            item = self._list_widget.item(i)
            if not isinstance(item, Scenario):
                continue
            path = f"{self.data_dir}/{i}.json"
            if item.path != path:
                if path in self._files:
                    self._files[item.path].rename_file(self.create_temp_file())
                item.rename_file(path)
            with open(path, encoding='utf-8') as f:
                converter.add_scenario(json.loads(f.read()))
        converter.run()
        
    def hide(self) -> None:
        self.store_task()
        super().hide()

    def add_scenario(self):
        self._list_widget.addItem(Scenario(self.create_temp_file()))

    def delete_scenario(self):
        item = self._list_widget.takeItem(self._list_widget.currentRow())
        try:
            os.remove(item.path)
        except FileNotFoundError:
            pass

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

    def create_temp_file(self):
        path = f"{self.data_dir}/temp_{self.temp_file_index}"
        self.temp_file_index += 1
        return path

    def set_theme(self):
        super().set_theme()
        for el in [self._list_widget]:
            self.tm.auto_css(el)
        for el in [self.button_add, self.button_delete, self.button_up, self.button_down, self._scenario_edit]:
            el.set_theme()


class ScenarioEdit(QWidget):
    def __init__(self, sm, tm):
        super().__init__()
        self._sm = sm
        self._tm = tm
        self._scenario = None

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self._name_edit = QLineEdit()
        self._name_edit.editingFinished.connect(lambda: self._scenario.set_name(self._name_edit.text()))
        main_layout.addWidget(self._name_edit)

        self._combo_box = QComboBox()
        self._combo_box.addItems(["Сценарий сборки", "Сценарий Make"])
        self._combo_box.currentIndexChanged.connect(lambda ind: self._scenario.set_type(ind))
        main_layout.addWidget(self._combo_box)

        self._compiler_edit = QLineEdit()
        self._compiler_edit.setPlaceholderText("Компилятор")
        self._compiler_edit.editingFinished.connect(lambda: self._scenario.set_compiler(self._compiler_edit.text()))
        main_layout.addWidget(self._compiler_edit)

        self._keys_edit = QLineEdit()
        self._keys_edit.setPlaceholderText("Ключи компилятора")
        self._keys_edit.editingFinished.connect(lambda: self._scenario.set_keys(self._keys_edit.text()))
        main_layout.addWidget(self._keys_edit)

        self._tree_widget = TreeWidget(self._tm, TreeWidget.CHECKABLE)
        main_layout.addWidget(self._tree_widget)

    def load_scenario(self, scenario: 'Scenario'):
        if isinstance(self._scenario, Scenario):
            self._scenario.store()
        self._scenario = scenario
        if not isinstance(self._scenario, Scenario):
            return
        self._name_edit.setText(self._scenario.name)
        self._combo_box.setCurrentIndex(self._scenario.type)
        match self._scenario.type:
            case Scenario.TYPE_COMPILE:
                self.load_compiler()

    def load_compiler(self):
        for el in [self._compiler_edit, self._keys_edit, self._tree_widget]:
            el.show()
        self.update_tree()
        self._compiler_edit.setText(self._scenario.compiler)
        self._keys_edit.setText(self._scenario.keys)

    def update_tree(self):
        self._tree_widget.clear()
        for el in get_files(lab_dir := self._sm.lab_path(), languages[self._scenario.language]['files'][0]):
            el = os.path.relpath(el, lab_dir).replace('\\', '/')
            lst = el.split('/')[:-1]
            tree_elem = TreeElement(self._tm, el)
            self._tree_widget.add_item(tree_elem, key=lst)
            self._connect_tree_elem(tree_elem, el)
            if el in self._scenario.files:
                tree_elem.set_checked(self._scenario.files[el])
            else:
                self._scenario.files[el] = False
            for key in self._scenario.files:
                if not os.path.isfile(f"{lab_dir}/{el}"):
                    self._scenario.files.pop(key)
        self._tree_widget.set_theme()

    def _connect_tree_elem(self, elem: 'TreeElement', path):
        elem.stateChanged.connect(lambda flag: self._scenario.set_file_status(path, flag))

    def set_theme(self):
        for el in [self._combo_box, self._name_edit, self._keys_edit, self._compiler_edit]:
            self._tm.auto_css(el)
        self._tree_widget.set_theme()


class Scenario(QListWidgetItem):
    TYPE_COMPILE = 0
    TYPE_MAKE = 1

    def __init__(self, path):
        super().__init__()
        self.path = path

        self.name = '-'
        self.type = Scenario.TYPE_COMPILE

        self.language = 'C'
        self.compiler = ''
        self.keys = ''
        self.files = dict()

        self.dependencies = []
        self.commands = []

        self.load()

    def rename_file(self, new_name):
        os.rename(self.path, new_name)
        self.path = new_name

    def set_name(self, name):
        self.name = name
        self.setText(name)

    def set_type(self, new_type):
        self.type = new_type

    def set_language(self, language):
        self.language = language

    def set_compiler(self, compiler):
        self.compiler = compiler

    def set_keys(self, keys):
        self.keys = keys

    def set_file_status(self, file, status):
        self.files[file] = status

    def load(self):
        try:
            with open(self.path, encoding='utf-8') as f:
                data = json.loads(f.read())
                if not isinstance(data, dict):
                    data = dict()
        except FileNotFoundError:
            data = dict()
        except json.JSONDecodeError:
            data = dict()

        self.set_name(data.get('name', ''))
        self.type = data.get('type', Scenario.TYPE_MAKE)
        match self.type:
            case Scenario.TYPE_COMPILE:
                self.language = data.get('language', 'C')
                self.files = data.get('files')
                self.compiler = data.get('compiler', 'C')
                self.keys = data.get('keys')
            case Scenario.TYPE_MAKE:
                self.dependencies = data.get('dependencies', [])
                self.commands = data.get('commands', [])

    def store(self):
        data = {'name': self.name, 'type': self.type}
        match self.type:
            case Scenario.TYPE_COMPILE:
                data['language'] = self.language
                data['files'] = self.files
                data['compiler'] = self.compiler
                data['keys'] = self.keys
            case Scenario.TYPE_MAKE:
                data['dependencies'] = self.dependencies
                data['commands'] = self.commands
        os.makedirs(os.path.split(self.path)[0], exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data))


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
