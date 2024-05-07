from uuid import UUID

from PyQt6.QtCore import Qt
from PyQtUIkit.widgets import *

from src.backend.managers import BackendManager
from src.ui.side_tabs.builds.build_box import BuildBox


class CommandsList(KitVBoxLayout):
    TYPE_BUILD = 0
    TYPE_CMD = 1
    TYPE_UTIL = 2

    def __init__(self, bm: BackendManager, name="", fixed_type=None):
        super().__init__()
        self.sm = bm.sm
        self.bm = bm
        self._fixed_type = fixed_type

        self.spacing = 6

        top_layout = KitHBoxLayout()
        top_layout.spacing = 6
        self.addWidget(top_layout)

        self._label = KitLabel(name)
        top_layout.addWidget(self._label)

        self.button_add = KitIconButton('line-add')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(40)
        self.button_add.clicked.connect(self.add_scenario)
        top_layout.addWidget(self.button_add, 1)

        self.button_delete = KitIconButton('line-trash')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(40)
        self.button_delete.clicked.connect(self.delete_scenario)
        top_layout.addWidget(self.button_delete, 1)

        self.button_up = KitIconButton('line-chevron-up')
        self.button_up.setFixedHeight(22)
        self.button_up.setMaximumWidth(40)
        self.button_up.clicked.connect(self.move_scenario_up)
        top_layout.addWidget(self.button_up, 1)

        self.button_down = KitIconButton('line-chevron-up')
        self.button_down.setFixedHeight(22)
        self.button_down.setMaximumWidth(40)
        self.button_down.clicked.connect(self.move_scenario_down)
        top_layout.addWidget(self.button_down, 1)

        self._list_widget = KitListWidget()
        self.addWidget(self._list_widget)

    def add_scenario(self):
        dialog = NewCommandDialog(self, self.bm, self._fixed_type)
        if dialog.exec():
            scenario_type, data = dialog.get_result()
            if data is None:
                return
            self._list_widget.addItem(_ListWidgetItem(self.bm, scenario_type, data))

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
            command_type = el['type']
            data = el['data']
            if command_type == CommandsList.TYPE_UTIL and data not in self.bm.utils.all:
                continue
            if command_type == CommandsList.TYPE_BUILD:
                data = UUID(data)
                if data not in self.bm.builds.all:
                    continue
            self._list_widget.addItem(_ListWidgetItem(self.bm, command_type, data))


class NewCommandDialog(KitDialog):
    def __init__(self, parent, bm: BackendManager, fixed_type=None):
        super().__init__(parent)
        self.name = "Новая команда"
        self.sm = bm.sm
        self.bm = bm
        self._fixed_type = fixed_type

        self.setFixedWidth(300)

        main_layout = KitVBoxLayout()
        main_layout.spacing = 6
        main_layout.padding = 10
        self.setWidget(main_layout)

        self._type_box = KitComboBox()
        self._type_box.addItem(KitComboBoxItem("Конфигурация запуска", CommandsList.TYPE_BUILD))
        self._type_box.addItem(KitComboBoxItem("Команда", CommandsList.TYPE_CMD))
        self._type_box.addItem(KitComboBoxItem("Утилита", CommandsList.TYPE_BUILD))
        self._type_box.currentIndexChanged.connect(self._on_type_changed)
        main_layout.addWidget(self._type_box)

        self._line_edit = KitLineEdit()
        self._line_edit.font = 'mono'
        main_layout.addWidget(self._line_edit)
        self._line_edit.hide()

        self._build_box = BuildBox(self.bm)
        main_layout.addWidget(self._build_box)

        self._utils_box = KitComboBox()
        self._utils_box.hide()
        # self._utils_box.addItems([item.get('name', '') for item in self.bm.utils.values()])
        self._utils = list(self.bm.utils.all.keys())
        main_layout.addWidget(self._utils_box)

        buttons_layout = KitHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(buttons_layout)

        self._button = KitButton("Ок")
        self._button.setFixedSize(80, 24)
        self._button.clicked.connect(self.accept)
        buttons_layout.addWidget(self._button)

        self._build_box.load_data()
        if self._fixed_type is not None:
            self._type_box.setCurrentIndex(self._fixed_type)
            self._type_box.hide()

    def _on_type_changed(self):
        match self._type_box.currentValue():
            case CommandsList.TYPE_BUILD:
                self._line_edit.hide()
                self._utils_box.hide()
                self._build_box.show()
            case CommandsList.TYPE_CMD:
                self._build_box.hide()
                self._utils_box.hide()
                self._line_edit.show()
            case CommandsList.TYPE_UTIL:
                self._build_box.hide()
                self._line_edit.hide()
                self._utils_box.show()

    def get_result(self):
        match self._type_box.currentValue():
            case CommandsList.TYPE_CMD:
                res = self._line_edit.text
            case CommandsList.TYPE_BUILD:
                res = self._build_box.current()
            case CommandsList.TYPE_UTIL:
                try:
                    res = self._utils[self._utils_box.currentIndex()]
                except IndexError:
                    res = None
            case _:
                raise IndexError
        return self._type_box.currentValue(), res


class _ListWidgetItem(KitListWidgetItem):
    def __init__(self, bm, type, data):
        super().__init__('')
        self.bm = bm
        self._type = type
        self._data = data

        match self._type:
            case CommandsList.TYPE_CMD:
                self.setText(self._data)
                self.icon = 'custom-shell'
            case CommandsList.TYPE_BUILD:
                self.setText(self.bm.builds.get(self._data).get('name', '-'))
                self.icon = 'line-hammer'
            case CommandsList.TYPE_UTIL:
                self.setText(self.bm.get_util(self._data).get('name', '-'))
                self.icon = 'line-checkmark'

    def store(self):
        return {'type': self._type, 'data': str(self._data)}
