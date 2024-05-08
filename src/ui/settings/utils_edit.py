from PyQt6.QtCore import pyqtSignal, Qt
from PyQtUIkit.widgets import *

from src.backend.backend_types.util import Util


class UtilsEdit(KitHBoxLayout):
    def __init__(self, bm):
        super().__init__()
        self.bm = bm
        self.padding = 10
        self.spacing = 6

        right_layout = KitVBoxLayout()
        self.addWidget(right_layout)

        buttons_layout = KitHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(buttons_layout)

        self.button_add = KitIconButton('line-add')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(40)
        self.button_add.clicked.connect(self.new_util)
        buttons_layout.addWidget(self.button_add, 1)

        self.button_delete = KitIconButton('line-trash')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(40)
        self.button_delete.clicked.connect(self._on_delete_pressed)
        buttons_layout.addWidget(self.button_delete, 1)

        self._list_widget = KitListWidget()
        self._list_widget.currentItemChanged.connect(self._on_util_selected)
        self._list_widget.setFixedWidth(225)
        right_layout.addWidget(self._list_widget)

        self._util_edit = UtilOptionsEdit(self.tm)
        self._util_edit.nameChanged.connect(self._update_item_text)
        self.addWidget(self._util_edit)

        self.bm.addUtil.connect(self.add_util)
        self.bm.deleteUtil.connect(self.delete_util)
        self.bm.clearUtils.connect(self.clear)

    def add_util(self, util):
        self._list_widget.addItem(ListWidgetItem(util))

    def clear(self):
        self._list_widget.clear()
        self._util_edit.store_util()

    def delete_util(self, util):
        for i in range(self._list_widget.count()):
            if self._list_widget.item(i).util == util:
                self._list_widget.takeItem(i)
                break

    def _on_util_selected(self):
        item = self._list_widget.currentItem()
        if not isinstance(item, ListWidgetItem):
            return
        self._util_edit.open_util(item.util)

    def _update_item_text(self):
        item = self._list_widget.currentItem()
        if not isinstance(item, ListWidgetItem):
            return
        item.setText(item.util['name'])

    def new_util(self):
        util = Util(self.bm.generate_util_id())
        self.bm.add_util(util)

    def _on_delete_pressed(self):
        item = self._list_widget.currentItem()
        if not isinstance(item, ListWidgetItem):
            return
        self.bm.delete_util(item.util.id)

    def closeEvent(self, a0) -> None:
        self._util_edit.store_util()


class ListWidgetItem(KitListWidgetItem):
    def __init__(self, util: Util):
        super().__init__('')
        self.util = util

    def update_name(self):
        self.setText(self.util.get('name', '-'))


class UtilOptionsEdit(KitVBoxLayout):
    nameChanged = pyqtSignal()

    def __init__(self, tm):
        super().__init__()
        self.tm = tm
        self._util = None
        self.spacing = 6

        self.addWidget(KitLabel("Название:"))

        self._name_edit = KitLineEdit()
        self._name_edit.textEdited.connect(self._on_name_changed)
        self.addWidget(self._name_edit)

        self.addWidget(KitLabel("Строка запуска:"))

        self._command_edit = KitLineEdit()
        self.addWidget(self._command_edit)

        layout = KitHBoxLayout()
        layout.spacing = 6
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addWidget(layout)

        layout.addWidget(KitLabel("Тип:"))

        self._type_edit = KitComboBox()
        self._type_edit.addItems(['Перед тестированием', 'Для теста'])
        layout.addWidget(self._type_edit)

        layout = KitHBoxLayout()
        layout.spacing = 6
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addWidget(layout)

        layout.addWidget(KitLabel("Тип вывода:"))

        self._output_edit = KitComboBox()
        self._output_edit.addItems(['STDOUT', 'STDERR', 'Файл {dist}'])
        layout.addWidget(self._output_edit)

        self._checkbox1 = KitCheckBox("Ненулевой код возврата считается отрицательным результатом")
        self.addWidget(self._checkbox1)

        self._checkbox2 = KitCheckBox("Наличие вывода считается отрицательным результатом")
        self.addWidget(self._checkbox2)

        self.hide()

    def open_util(self, util: Util):
        self.store_util()
        self._util = util
        if not isinstance(self._util, Util):
            self.hide()
            return
        self.show()
        self._name_edit.setText(util.get('name', '-'))
        self._command_edit.setText(util.get('command', ''))
        self._type_edit.setCurrentIndex(util.get('type', 0))
        self._output_edit.setCurrentIndex(util.get('output', 0))
        self._checkbox1.setChecked(util.get('returncode_res', False))
        self._checkbox2.setChecked(util.get('output_res', False))

    def _on_name_changed(self):
        if not isinstance(self._util, Util):
            return
        self._util['name'] = self._name_edit.text()
        self.nameChanged.emit()

    def store_util(self):
        if not isinstance(self._util, Util):
            return
        self._util['name'] = self._name_edit.text()
        self._util['command'] = self._command_edit.text()
        self._util['type'] = self._type_edit.currentIndex()
        self._util['output'] = self._output_edit.currentIndex()
        self._util['returncode_res'] = self._checkbox1.isChecked()
        self._util['output_res'] = self._checkbox2.isChecked()

    def hideEvent(self, a0) -> None:
        self.store_util()
