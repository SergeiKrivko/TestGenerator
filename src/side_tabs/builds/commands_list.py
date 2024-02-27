from uuid import UUID

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QComboBox, \
    QLineEdit, QPushButton

from src.backend.settings_manager import SettingsManager
from src.side_tabs import builds as builds
from src.ui.button import Button
from src.ui.custom_dialog import CustomDialog


class CommandsList(QWidget):
    TYPE_BUILD = 0
    TYPE_CMD = 1
    TYPE_UTIL = 2

    def __init__(self, sm, bm, tm, name="", fixed_type=None):
        super().__init__()
        self.sm = sm
        self.bm = bm
        self.tm = tm
        self._fixed_type = fixed_type

        mail_layout = QVBoxLayout()
        mail_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mail_layout)

        top_layout = QHBoxLayout()
        mail_layout.addLayout(top_layout)

        self._label = QLabel(name)
        top_layout.addWidget(self._label)

        self.button_add = Button(self.tm, 'buttons/plus', css='Main')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(40)
        self.button_add.clicked.connect(self.add_scenario)
        top_layout.addWidget(self.button_add, 1)

        self.button_delete = Button(self.tm, 'buttons/delete', css='Main')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(40)
        self.button_delete.clicked.connect(self.delete_scenario)
        top_layout.addWidget(self.button_delete, 1)

        self.button_up = Button(self.tm, 'buttons/button_up', css='Main')
        self.button_up.setFixedHeight(22)
        self.button_up.setMaximumWidth(40)
        self.button_up.clicked.connect(self.move_scenario_up)
        top_layout.addWidget(self.button_up, 1)

        self.button_down = Button(self.tm, 'buttons/button_down', css='Main')
        self.button_down.setFixedHeight(22)
        self.button_down.setMaximumWidth(40)
        self.button_down.clicked.connect(self.move_scenario_down)
        top_layout.addWidget(self.button_down, 1)

        self._list_widget = QListWidget()
        mail_layout.addWidget(self._list_widget)

    def add_scenario(self):
        dialog = NewCommandDialog(self.sm, self.bm, self.tm, self._fixed_type)
        if dialog.exec():
            scenario_type, data = dialog.get_result()
            if data is None:
                return
            self._list_widget.addItem(_ListWidgetItem(self.bm, self.tm, scenario_type, data))

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
            if el['type'] == CommandsList.TYPE_UTIL and el['data'] not in self.bm.utils:
                continue
            if el['type'] == CommandsList.TYPE_BUILD and el['data'] not in self.bm._builds:
                continue
            self._list_widget.addItem(_ListWidgetItem(self.bm, self.tm, el['type'], el['data']))

    def set_theme(self):
        for el in [self._label, self.button_add, self.button_delete, self.button_up, self.button_down,
                   self._list_widget]:
            self.tm.auto_css(el)


class NewCommandDialog(CustomDialog):
    def __init__(self, sm, bm, tm, fixed_type=None):
        super().__init__(tm, "Новая команда", True)
        self.sm = sm
        self.bm = bm
        self._fixed_type = fixed_type

        self.setFixedWidth(300)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self._type_box = QComboBox()
        self._type_box.addItems(["Конфигурация запуска", "Команда", "Утилита"])
        self._type_box.currentIndexChanged.connect(self._on_type_changed)
        main_layout.addWidget(self._type_box)

        self._line_edit = QLineEdit()
        main_layout.addWidget(self._line_edit)
        self._line_edit.hide()

        self._make_box = ScenarioBox(self.sm, self.bm, self.tm)
        main_layout.addWidget(self._make_box)

        self._utils_box = QComboBox()
        self._utils_box.hide()
        self._utils_box.addItems([item.get('name', '') for item in self.bm.utils.values()])
        self._utils = list(self.bm.utils.keys())
        main_layout.addWidget(self._utils_box)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
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
            case CommandsList.TYPE_BUILD:
                self._line_edit.hide()
                self._utils_box.hide()
                self._make_box.show()
            case CommandsList.TYPE_CMD:
                self._make_box.hide()
                self._utils_box.hide()
                self._line_edit.show()
            case CommandsList.TYPE_UTIL:
                self._make_box.hide()
                self._line_edit.hide()
                self._utils_box.show()

    def get_result(self):
        match self._type_box.currentIndex():
            case CommandsList.TYPE_CMD:
                res = self._line_edit.text()
            case CommandsList.TYPE_BUILD:
                res = self._make_box.current_scenario()
            case CommandsList.TYPE_UTIL:
                try:
                    res = self._utils[self._utils_box.currentIndex()]
                except IndexError:
                    res = None
            case _:
                raise IndexError
        return self._type_box.currentIndex(), res

    def set_theme(self):
        super().set_theme()
        for el in [self._type_box, self._line_edit, self._make_box, self._utils_box, self._button]:
            self.tm.auto_css(el)


class ScenarioBox(QComboBox):
    currentChanged = pyqtSignal(int)

    def __init__(self, sm: SettingsManager, bm, tm, default=False):
        super().__init__()
        self._sm = sm
        self._bm = bm
        self._tm = tm
        self._builds = []
        self._loading = 0
        self._default = default
        if self._default:
            self.addItem("")
        self.setMinimumWidth(150)
        self.load_data()
        self.currentIndexChanged.connect(self._on_index_changed)
        self._loading = False
        self._bm.builds.onLoad.connect(self.load_data)
        self._bm.builds.onAdd.connect(self.load_data)
        self._bm.builds.onDelete.connect(self.load_data)
        self._bm.builds.onRename.connect(self.load_data)
        # self._bm.builds.onClear.connect(self.load_data)

    def load_data(self):
        text = self.currentText()
        self._loading = True
        self.clear()
        self._builds = list(self._bm.builds.all.keys())
        if self._default:
            self._builds.insert(0, None)
            self.addItem("")
        self.addItems([item.get('name') for item in self._bm.builds.all.values()])
        self._loading = False
        self.setCurrentText(text)
        self.set_theme()

    def _on_index_changed(self):
        if not self._loading:
            self.currentChanged.emit(self.current_scenario())

    def load(self, value):
        if isinstance(value, str):
            value = UUID(value)
        self.load_data()
        try:
            self.setCurrentIndex(self._builds.index(value))
        except ValueError:
            pass

    def current_scenario(self) -> str | None:
        return str(self._builds[self.currentIndex()])

    def set_theme(self):
        self._tm.auto_css(self)
        for i, build in enumerate(self._builds):
            if build is not None:
                build = self._bm.builds.get(build)
                self.setItemIcon(i, QIcon(self._tm.get_image(builds.BuildTypeDialog.IMAGES.get(build.get('type')),
                                                             'icons/unknown_file')))


class _ListWidgetItem(QListWidgetItem):
    def __init__(self, bm, tm, type, data):
        super().__init__()
        self._tm = tm
        self.bm = bm
        self._type = type
        self._data = data

        match self._type:
            case CommandsList.TYPE_CMD:
                self.setText(self._data)
                self.setIcon(QIcon(self._tm.get_image('files/cmd')))
            case CommandsList.TYPE_BUILD:
                self.setText(self.bm.builds.get(self._data).get('name', '-'))
                self.setIcon(QIcon(self._tm.get_image('icons/build')))
            case CommandsList.TYPE_UTIL:
                self.setText(self.bm.get_util(self._data).get('name', '-'))
                self.setIcon(QIcon(self._tm.get_image('icons/passed')))

    def store(self):
        return {'type': self._type, 'data': self._data}
