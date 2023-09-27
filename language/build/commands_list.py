import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QDialog, QComboBox, \
    QLineEdit, QPushButton

from ui.button import Button


class CommandsList(QWidget):
    TYPE_MAKE = 0
    TYPE_CMD = 1

    def __init__(self, sm, tm, name="", fixed_type=None):
        super().__init__()
        self.sm = sm
        self.tm = tm
        self._fixed_type = fixed_type

        mail_layout = QVBoxLayout()
        mail_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mail_layout)

        top_layout = QHBoxLayout()
        mail_layout.addLayout(top_layout)

        self._label = QLabel(name)
        top_layout.addWidget(self._label)

        self.button_add = Button(self.tm, 'plus', css='Main')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(40)
        self.button_add.clicked.connect(self.add_scenario)
        top_layout.addWidget(self.button_add, 1)

        self.button_delete = Button(self.tm, 'delete', css='Main')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(40)
        self.button_delete.clicked.connect(self.delete_scenario)
        top_layout.addWidget(self.button_delete, 1)

        self.button_up = Button(self.tm, 'button_up', css='Main')
        self.button_up.setFixedHeight(22)
        self.button_up.setMaximumWidth(40)
        self.button_up.clicked.connect(self.move_scenario_up)
        top_layout.addWidget(self.button_up, 1)

        self.button_down = Button(self.tm, 'button_down', css='Main')
        self.button_down.setFixedHeight(22)
        self.button_down.setMaximumWidth(40)
        self.button_down.clicked.connect(self.move_scenario_down)
        top_layout.addWidget(self.button_down, 1)

        self._list_widget = QListWidget()
        mail_layout.addWidget(self._list_widget)

    def add_scenario(self):
        dialog = NewCommandDialog(self.sm, self.tm, self._fixed_type)
        if dialog.exec():
            self._list_widget.addItem(_ListWidgetItem(self.tm, *dialog.get_result()))

    def delete_scenario(self):
        item = self._list_widget.takeItem(self._list_widget.currentRow())

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

    def store(self):
        return [self._list_widget.item(i).store() for i in range(self._list_widget.count())]

    def load(self, data: list):
        self._list_widget.clear()
        for el in data:
            self._list_widget.addItem(_ListWidgetItem(self.tm, el['type'], el['data']))

    def set_theme(self):
        for el in [self._label, self.button_add, self.button_delete, self.button_up, self.button_down,
                   self._list_widget]:
            self.tm.auto_css(el)


class NewCommandDialog(QDialog):
    def __init__(self, sm, tm, fixed_type=None):
        super().__init__()
        self.sm = sm
        self.tm = tm
        self._fixed_type = fixed_type

        self.setFixedSize(300, 100)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self._type_box = QComboBox()
        self._type_box.addItems(["Сценарий Make", "Команда"])
        self._type_box.currentIndexChanged.connect(self._on_type_changed)
        main_layout.addWidget(self._type_box)

        self._line_edit = QLineEdit()
        main_layout.addWidget(self._line_edit)
        self._line_edit.hide()

        self._make_box = MakeScenarioBox(self.sm)
        main_layout.addWidget(self._make_box)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignRight)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(buttons_layout)

        self._button = QPushButton("Ок")
        self._button.setFixedSize(80, 22)
        self._button.clicked.connect(self.accept)
        buttons_layout.addWidget(self._button)

        self._make_box.load_data()
        if self._fixed_type is not None:
            self._type_box.setCurrentIndex(self._fixed_type)
            self._type_box.hide()
        self.set_theme()

    def _on_type_changed(self):
        match self._type_box.currentIndex():
            case CommandsList.TYPE_MAKE:
                self._line_edit.hide()
                self._make_box.show()
            case CommandsList.TYPE_CMD:
                self._make_box.hide()
                self._line_edit.show()

    def get_result(self):
        match self._type_box.currentIndex():
            case CommandsList.TYPE_CMD:
                res = self._line_edit.text()
            case CommandsList.TYPE_MAKE:
                res = self._make_box.current_scenario()['data']
            case _:
                raise IndexError
        return self._type_box.currentIndex(), res

    def set_theme(self):
        for el in [self._type_box, self._line_edit, self._make_box, self._button]:
            self.tm.auto_css(el)


class MakeScenarioBox(QComboBox):
    def __init__(self, sm, default=False):
        super().__init__()
        self._sm = sm
        self._make_commands = dict()
        self._default = default
        if self._default:
            self.addItem("")
            self._make_commands[''] = None
        self.setMinimumWidth(150)

    def _load_make(self):
        self._make_commands.clear()
        self.clear()
        data_dir = f"{self._sm.data_lab_path()}/scenarios/make"
        for el in os.listdir(data_dir):
            if el.endswith('.json'):
                path = os.path.join(data_dir, el)
                try:
                    with open(path, encoding='utf-8') as f:
                        data = json.loads(f.read())
                        self._make_commands[data['name']] = data
                        self.addItems([data['name']])
                except FileNotFoundError:
                    pass
                except json.JSONDecodeError:
                    pass
                except KeyError:
                    pass

    def load_data(self):
        try:
            self._load_make()
        except FileNotFoundError:
            pass

    def load(self, data: dict | None):
        self.load_data()
        if data is None:
            self.setCurrentText("")
        elif 'data' in data and 'name' in data['data'] and data['data']['name'] in self._make_commands:
            self.setCurrentText(data['data']['name'])

    def current_scenario(self) -> dict | None:
        if self.currentText() not in self._make_commands:
            return None
        return {'type': CommandsList.TYPE_MAKE, 'data': self._make_commands[self.currentText()]}


class _ListWidgetItem(QListWidgetItem):
    def __init__(self, tm, type, data):
        super().__init__()
        self._tm = tm
        self._type = type
        self._data = data

        match self._type:
            case CommandsList.TYPE_CMD:
                self.setText(self._data)
                self.setIcon(QIcon(self._tm.get_image('cmd')))
            case CommandsList.TYPE_MAKE:
                self.setText(self._data['name'])
                self.setIcon(QIcon(self._tm.get_image('icon_build')))

    def store(self):
        return {'type': self._type, 'data': self._data}
