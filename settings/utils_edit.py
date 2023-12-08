from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QListWidget, QVBoxLayout, QListWidgetItem, QLabel, QLineEdit, \
    QComboBox, QCheckBox

from backend.backend_types.util import Util
from ui.button import Button


class UtilsEdit(QWidget):
    def __init__(self, bm, tm):
        super().__init__()
        self.bm = bm
        self.tm = tm

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        right_layout = QVBoxLayout()
        layout.addLayout(right_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addLayout(buttons_layout)

        self.button_add = Button(self.tm, 'buttons/plus', css='Main')
        self.button_add.setFixedHeight(22)
        self.button_add.setMaximumWidth(40)
        self.button_add.clicked.connect(self.new_util)
        buttons_layout.addWidget(self.button_add, 1)

        self.button_delete = Button(self.tm, 'buttons/delete', css='Main')
        self.button_delete.setFixedHeight(22)
        self.button_delete.setMaximumWidth(40)
        self.button_delete.clicked.connect(self._on_delete_pressed)
        buttons_layout.addWidget(self.button_delete, 1)

        self._list_widget = QListWidget()
        self._list_widget.currentItemChanged.connect(self._on_util_selected)
        self._list_widget.setFixedWidth(225)
        right_layout.addWidget(self._list_widget)

        self._util_edit = UtilOptionsEdit(self.tm)
        self._util_edit.nameChanged.connect(self._update_item_text)
        layout.addWidget(self._util_edit)

        self.bm.addUtil.connect(self.add_util)
        self.bm.deleteUtil.connect(self.delete_util)
        self.bm.clearUtils.connect(self.clear)

    def add_util(self, util):
        self._list_widget.addItem(ListWidgetItem(self.tm, util))

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

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        self._util_edit.set_theme()
        for el in [self.button_add, self.button_delete, self._list_widget]:
            self.tm.auto_css(el)

    def closeEvent(self, a0) -> None:
        self._util_edit.store_util()


class ListWidgetItem(QListWidgetItem):
    def __init__(self, tm, util: Util):
        super().__init__()
        self.tm = tm
        self.util = util
        self.set_theme()

    def update_name(self):
        self.setText(self.util.get('name', '-'))

    def set_theme(self):
        self.update_name()
        self.setFont(self.tm.font_medium)
        # self.setIcon(QIcon(self.tm.get_image(BuildTypeDialog.IMAGES.get(self.util.get('type')), 'unknown_file')))


class UtilOptionsEdit(QWidget):
    nameChanged = pyqtSignal()

    def __init__(self, tm):
        super().__init__()
        self.tm = tm
        self._util = None

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self._labels = []

        label = QLabel("Название:")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._name_edit = QLineEdit()
        self._name_edit.textEdited.connect(self._on_name_changed)
        main_layout.addWidget(self._name_edit)

        label = QLabel("Строка запуска:")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._command_edit = QLineEdit()
        main_layout.addWidget(self._command_edit)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(layout)

        label = QLabel("Тип:")
        self._labels.append(label)
        layout.addWidget(label)

        self._type_edit = QComboBox()
        self._type_edit.addItems(['Перед тестированием', 'Для теста'])
        layout.addWidget(self._type_edit)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(layout)

        label = QLabel("Тип вывода:")
        self._labels.append(label)
        layout.addWidget(label)

        self._output_edit = QComboBox()
        self._output_edit.addItems(['STDOUT', 'STDERR', 'Файл {dist}'])
        layout.addWidget(self._output_edit)

        self._checkbox1 = QCheckBox("Ненулевой код возврата считается отрицательным результатом")
        main_layout.addWidget(self._checkbox1)

        self._checkbox2 = QCheckBox("Наличие вывода считается отрицательным результатом")
        main_layout.addWidget(self._checkbox2)

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

    def set_theme(self):
        for el in [self._name_edit, self._command_edit, self._type_edit, self._output_edit, self._checkbox1,
                   self._checkbox2]:
            self.tm.auto_css(el)
        for el in self._labels:
            self.tm.auto_css(el)
