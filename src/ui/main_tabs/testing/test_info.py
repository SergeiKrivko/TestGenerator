from PyQt6.QtCore import Qt
from PyQtUIkit.widgets import *

from src.backend.backend_types import FuncTest


class SimpleField(KitLabel):
    def __init__(self, name, text):
        super().__init__(f"{name} {text}")


class LineField(KitHBoxLayout):
    def __init__(self, name, text):
        super().__init__()
        self.spacing = 6

        self._label = KitLabel(name)
        self.addWidget(self._label)

        self._line_edit = KitLineEdit()
        self._line_edit.setText(text)
        self._line_edit.setReadOnly(True)
        self.addWidget(self._line_edit)


class TextField(KitVBoxLayout):
    def __init__(self, name, text):
        super().__init__()
        self.spacing = 6

        self._label = KitLabel(name)
        self.addWidget(self._label)

        self._text_edit = KitLabel()
        self._text_edit.font = 'mono'
        self._text_edit.setText(text)
        self._text_edit.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse |
                                                Qt.TextInteractionFlag.TextSelectableByKeyboard)
        self.addWidget(self._text_edit)


class _ListFieldItem(KitListWidgetItem):
    def __init__(self, name, status):
        super().__init__('')
        self._status = status
        self.setText(name)

        self.main_palette = 'Success' if status else 'Danger'
        self.icon = 'line-checkmark' if status else 'line-close'


class ListField(KitVBoxLayout):
    def __init__(self, name, dct: dict):
        super().__init__()
        self.spacing = 6

        self._label = KitLabel(name)
        self.addWidget(self._label)

        self._list_widget = KitListWidget()
        self._list_widget.main_palette = 'Bg'
        self._list_widget.border = 0
        self._list_widget.setSelectionMode(KitListWidget.SelectionMode.NoSelection)
        self._list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._list_widget.setMinimumHeight(len(dct) * 22 + 2)
        self.addWidget(self._list_widget)
        for key, item in dct.items():
            self._list_widget.addItem(_ListFieldItem(key, item))


class TestInfoWidget(KitScrollArea):
    def __init__(self):
        super().__init__()
        self.main_palette = 'Bg'
        self._test: FuncTest | None = None

        self._scroll_layout = KitVBoxLayout()
        self._scroll_layout.spacing = 6
        self._scroll_layout.padding = 10
        self.setWidget(self._scroll_layout)
        self._scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._widgets = []

    def clear(self):
        self._widgets.clear()
        self._scroll_layout.clear()

    def add_widget(self, widget):
        self._scroll_layout.addWidget(widget)
        self._widgets.append(widget)
        if hasattr(widget, 'set_theme'):
            widget.set_theme()

    def open_test_info(self):
        self.clear()
        self.add_widget(LineField("Описание:", self._test.description))
        self.add_widget(LineField("Аргументы:", self._test.args))
        if self._test.status in (FuncTest.Status.PASSED, FuncTest.Status.FAILED):
            if self._test.exit:
                self.add_widget(SimpleField("Код возврата:", f"{self._test.exit} ({self._test.exit})"))
            else:
                self.add_widget(SimpleField("Код возврата:", self._test.exit))
            self.add_widget(SimpleField("Время выполнения:", f"{self._test.res.time:.4g} s"))
            self.add_widget(ListField("Результаты:", self._test.res.results))

            # for key, item in self._test.utils_output.items():
            #     self.add_widget(TextField(key, item))

    def set_test(self, test: FuncTest):
        self._test = test
