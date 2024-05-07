import json
import typing
from enum import Enum

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQtUIkit.widgets import *

from src.backend.backend_types import FuncTest
from src.backend.managers import BackendManager

BUTTONS_MAX_WIDTH = 30


class TestListWidget(KitVBoxLayout):

    testSelected = pyqtSignal(FuncTest)

    def __init__(self, bm: BackendManager, test_type: FuncTest.Type):
        super().__init__()
        self._bm = bm
        self._test_type = test_type
        self.spacing = 6

        buttons_layout = KitHBoxLayout()
        buttons_layout.spacing = 6
        self.addWidget(buttons_layout)

        buttons_layout.addWidget(KitLabel(
            f"{'Позитивные' if self._test_type == FuncTest.Type.POS else 'Негативные'} тесты"))

        self.add_button = KitIconButton('line-add')
        self.add_button.setFixedHeight(22)
        self.add_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.add_button.on_click = self._new_test
        buttons_layout.addWidget(self.add_button)

        self.delete_button = KitIconButton('line-trash')
        self.delete_button.setFixedHeight(22)
        self.delete_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.delete_button.on_click = self._delete_tests
        buttons_layout.addWidget(self.delete_button)

        self.button_up = KitIconButton('line-chevron-up')
        self.button_up.setFixedHeight(22)
        self.button_up.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_up.on_click = self._move_up
        buttons_layout.addWidget(self.button_up)

        self.button_down = KitIconButton('line-chevron-down')
        self.button_down.setFixedHeight(22)
        self.button_down.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_down.on_click = self._move_down
        buttons_layout.addWidget(self.button_down)

        self.button_copy = KitIconButton('line-copy')
        self.button_copy.setFixedHeight(22)
        self.button_copy.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_copy.on_click = self._copy_tests
        buttons_layout.addWidget(self.button_copy)

        self.button_cut = KitIconButton('line-cut')
        self.button_cut.setFixedHeight(22)
        self.button_cut.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_cut.on_click = self._cut_tests
        buttons_layout.addWidget(self.button_cut)

        self.button_paste = KitIconButton('line-clipboard')
        self.button_paste.setFixedHeight(22)
        self.button_paste.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.button_paste.on_click = self._paste_tests
        buttons_layout.addWidget(self.button_paste)

        self.list_widget = KitListWidget()
        self.list_widget.currentItemChanged.connect(self._on_current_changed)
        self.list_widget.setSelectionMode(KitListWidget.SelectionMode.ExtendedSelection)
        self.addWidget(self.list_widget)

        comparator_layout = KitHBoxLayout()
        comparator_layout.spacing = 6
        comparator_layout.addWidget(KitLabel('Компаратор:'))

        self.comparator_widget = KitComboBox()
        self.comparator_widget.addItem(KitComboBoxItem('По умолчанию', FuncTest.Comparator.DEFAULT))
        if self._test_type == FuncTest.Type.NEG:
            self.comparator_widget.addItem(KitComboBoxItem('Нет', FuncTest.Comparator.NONE))
        self.comparator_widget.addItem(KitComboBoxItem('Числа', FuncTest.Comparator.NUMBERS))
        self.comparator_widget.addItem(KitComboBoxItem('Числа как текст', FuncTest.Comparator.NUMBERS_AS_STRING))
        self.comparator_widget.addItem(KitComboBoxItem('Текст после подстроки', FuncTest.Comparator.TEXT_AFTER))
        self.comparator_widget.addItem(KitComboBoxItem('Слова после подстроки', FuncTest.Comparator.WORDS_AFTER))
        self.comparator_widget.addItem(KitComboBoxItem('Текст', FuncTest.Comparator.TEXT))
        self.comparator_widget.addItem(KitComboBoxItem('Слова', FuncTest.Comparator.WORDS))

        self.comparator_widget.setMaximumWidth(200)
        self.comparator_widget.currentValueChanged.connect(self._save_comparator)
        comparator_layout.addWidget(self.comparator_widget)
        self.addWidget(comparator_layout)

        self._bm.func_tests.onAdd.connect(self._on_test_added)
        self._bm.func_tests.onDelete.connect(self._on_test_deleted)
        self._bm.func_tests.onClear.connect(self.list_widget.clear)

        self.ctrl_pressed = False
        self.shift_pressed = False

        self.tests_changed = False

    def _on_test_added(self, test: FuncTest, index: int):
        if test.type != self._test_type:
            return
        item = TestListWidgetItem(test)
        self.list_widget.insertItem(index, item)
        self.list_widget.clearSelection()
        self.list_widget.setCurrentRow(index)

    def _on_test_deleted(self, test: FuncTest, index):
        if test.type != self._test_type:
            return
        self.list_widget.takeItem(index)
        self.list_widget.setCurrentRow(min(index, self.list_widget.count() - 1))

    def _on_current_changed(self, item):
        if isinstance(item, TestListWidgetItem):
            self.testSelected.emit(item.test)

    def clear_selection(self):
        self.list_widget.setCurrentItem(None)
        self.list_widget.clearSelection()

    def update_test_name(self):
        item = self.list_widget.currentItem()
        if isinstance(item, TestListWidgetItem):
            item.update_name()

    def _new_test(self):
        self.tests_changed = True
        if self.list_widget.currentItem():
            index = self.list_widget.currentRow() + 1
        else:
            index = self.list_widget.count()
        self._bm.func_tests.new(self._test_type, index)

    def _delete_tests(self):
        self.tests_changed = True
        self._bm.func_tests.delete_some(self._test_type, [index.row() for index in self.list_widget.selectedIndexes()])

    def _copy_tests(self):
        items = self.list_widget.selectedItems()
        mime_data = QMimeData()
        mime_data.setData(f'TestGeneratorFuncTests',
                          json.dumps([item.test.to_dict() for item in items]).encode('utf-8'))
        KitApplication.clipboard().setMimeData(mime_data)

    def _paste_tests(self):
        index = self.list_widget.currentRow() + 1
        if index == 0:
            index = self.list_widget.count()

        tests = KitApplication.clipboard().mimeData().data(f'TestGeneratorFuncTests')
        if tests:
            try:
                tests = json.loads(tests.data().decode('utf-8'))
                self._bm.func_tests.add_some(self._test_type, {i + index: el for i, el in enumerate(tests)})
            except UnicodeDecodeError:
                pass
            except json.JSONDecodeError:
                pass

    def _cut_tests(self):
        self._copy_tests()
        self._delete_tests()

    def _move_down(self):
        if self.list_widget.currentRow():
            self.tests_changed = True
            self._bm.func_tests.move(self._test_type, 'down', self.list_widget.currentRow())

    def _move_up(self):
        if self.list_widget.currentRow():
            self.tests_changed = True
            self._bm.func_tests.move(self._test_type, 'up', self.list_widget.currentRow())

    def _save_comparator(self, value):
        self._bm.sm.set_data(f'{self._test_type.value}_comparator', value.value)

    def _undo(self):
        pass

    def _redo(self):
        pass

    def keyPressEvent(self, a0: typing.Optional[QtGui.QKeyEvent]) -> None:
        match a0.key():
            case Qt.Key.Key_X:
                if self.ctrl_pressed:
                    self._cut_tests()
            case Qt.Key.Key_C:
                if self.ctrl_pressed:
                    self._copy_tests()
            case Qt.Key.Key_V:
                if self.ctrl_pressed:
                    self._paste_tests()
            case Qt.Key.Key_Z:
                if self.ctrl_pressed:
                    if self.shift_pressed:
                        self._redo()
                    else:
                        self._undo()
            case Qt.Key.Key_Control:
                self.ctrl_pressed = True
            case Qt.Key.Key_Shift:
                self.shift_pressed = True
            case Qt.Key.Key_Delete:
                self._delete_tests()

    def keyReleaseEvent(self, a0: typing.Optional[QtGui.QKeyEvent]) -> None:
        if a0.key() == Qt.Key.Key_Control:
            self.ctrl_pressed = False
        if a0.key() == Qt.Key.Key_Shift:
            self.shift_pressed = False


class TestListWidgetItem(KitListWidgetItem):
    def __init__(self, test: FuncTest):
        super().__init__(test.description)
        self.test = test

    def update_name(self):
        self.setText(self.test.description)
