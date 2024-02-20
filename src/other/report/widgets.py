from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QDialog, QComboBox, \
    QPushButton

from src.ui.button import Button


def get_widget(data: dict):
    if data['__class__'] == "ReportMainDocument":
        return ReportMainDocument
    if data['__class__'] == "ReportSection":
        return ReportSection
    if data['__class__'] == "ReportSubSection":
        return ReportSubSection
    if data['__class__'] == "ReportTextEdit":
        return ReportTextEdit
    if data['__class__'] == "ReportCodeEdit":
        return ReportCodeEdit
    if data['__class__'] == "ReportListWidgetItem":
        return ReportListWidgetItem
    if data['__class__'] == "ReportListWidget":
        return ReportListWidget


class ReportWidget(QWidget):
    WIDGET_HEIGHT = 22
    NAME = ""

    deleteRequested = pyqtSignal(QWidget)
    moveUpRequested = pyqtSignal(QWidget)
    moveDownRequested = pyqtSignal(QWidget)

    def __init__(self, tm, widget_name='', children: list | tuple = tuple()):
        super().__init__()
        self.tm = tm
        self.children_list = children

        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        super().setLayout(self._main_layout)

        self._top_layout = QHBoxLayout()
        self._top_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addLayout(self._top_layout)

        self._name_label = QLabel(widget_name)
        self._top_layout.addWidget(self._name_label)

        self._button_up = Button(self.tm, 'buttons/button_up')
        self._button_up.setFixedSize(ReportWidget.WIDGET_HEIGHT, ReportWidget.WIDGET_HEIGHT)
        self._button_up.clicked.connect(lambda: self.moveUpRequested.emit(self))
        self._top_layout.addWidget(self._button_up)

        self._button_down = Button(self.tm, 'buttons/button_down')
        self._button_down.setFixedSize(ReportWidget.WIDGET_HEIGHT, ReportWidget.WIDGET_HEIGHT)
        self._button_down.clicked.connect(lambda: self.moveDownRequested.emit(self))
        self._top_layout.addWidget(self._button_down)

        self._button_delete = Button(self.tm, 'buttons/delete')
        self._button_delete.setFixedSize(ReportWidget.WIDGET_HEIGHT, ReportWidget.WIDGET_HEIGHT)
        self._button_delete.clicked.connect(lambda: self.deleteRequested.emit(self))
        self._top_layout.addWidget(self._button_delete)

        self._button_plus = Button(self.tm, 'buttons/plus')
        self._button_plus.setFixedSize(ReportWidget.WIDGET_HEIGHT, ReportWidget.WIDGET_HEIGHT)
        self._button_plus.clicked.connect(self.select_child)
        self._top_layout.addWidget(self._button_plus)
        if not self.children_list:
            self._button_plus.hide()

        self._children_layout = QVBoxLayout()
        self._children_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._children_layout.setContentsMargins(20, 0, 0, 0)

        self._children = []

    def set_margins(self, left, top, right, bottom):
        self._main_layout.setContentsMargins(left, top, right, bottom)

    def select_child(self):
        if not self.children_list:
            return
        if len(self.children_list) == 1:
            self.add_child(self.children_list[0](self.tm))
            return

        dialog = SelectChildDialog(self.tm, self)
        if dialog.exec():
            self.add_child(self.children_list[dialog.current_index()](self.tm))

    def add_child(self, widget: 'ReportWidget'):
        self._children.append(widget)
        self._children_layout.addWidget(widget)
        widget.moveUpRequested.connect(self.move_child_up)
        widget.moveDownRequested.connect(self.move_child_down)
        widget.deleteRequested.connect(self.delete_child)
        if hasattr(widget, 'set_theme'):
            widget.set_theme()

    def delete_child(self, widget: QWidget):
        if widget in self._children:
            self._children.remove(widget)
        widget.setParent(None)

    def move_child_up(self, widget: 'ReportWidget'):
        if widget in self._children:
            index = self._children.index(widget)
            if index == 0:
                return
            self._children.pop(index)
            self._children.insert(index - 1, widget)
            self._children_layout.takeAt(index)
            self._children_layout.insertWidget(index - 1, widget)

    def move_child_down(self, widget: 'ReportWidget'):
        if widget in self._children:
            index = self._children.index(widget)
            if index == len(self._children) - 1:
                return
            self._children.pop(index)
            self._children.insert(index + 1, widget)
            self._children_layout.takeAt(index)
            self._children_layout.insertWidget(index + 1, widget)

    def store(self):
        return dict()

    def load(self, data: dict):
        pass

    def setLayout(self, a0) -> None:
        self._main_layout.addLayout(a0)

    def set_theme(self):
        for el in [self._button_up, self._button_down, self._button_delete, self._button_plus, self._name_label]:
            self.tm.auto_css(el)


class ReportAbstractSection(ReportWidget):
    NAME = ""

    def __init__(self, tm, name, children):
        super().__init__(tm, name, children)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self._line_edit = QLineEdit()
        main_layout.addWidget(self._line_edit)

        main_layout.addLayout(self._children_layout)

    def store(self):
        return {'__class__': self.__class__.__name__, 'name': self._line_edit.text(),
                'children': [el.store() for el in self._children]}

    def load(self, data: dict):
        self._line_edit.setText(data.get('name', ''))
        for el in data.get('children', []):
            widget = get_widget(el)(self.tm)
            widget.load(el)
            self.add_child(widget)

    def set_theme(self):
        super().set_theme()
        self.tm.auto_css(self._line_edit)
        for el in self._children:
            el.set_theme()


class ReportMainDocument(ReportAbstractSection):
    def __init__(self, tm):
        super().__init__(tm, "Документ", [ReportSection])


class ReportSection(ReportAbstractSection):
    NAME = "Раздел"

    def __init__(self, tm):
        super().__init__(tm, "Раздел", [ReportSubSection, ReportTextEdit, ReportCodeEdit, ReportListWidget])


class ReportSubSection(ReportAbstractSection):
    NAME = "Подраздел"

    def __init__(self, tm):
        super().__init__(tm, "Подраздел", [ReportTextEdit, ReportCodeEdit, ReportListWidget])


class ReportTextEdit(ReportWidget):
    NAME = "Абзац"

    def __init__(self, tm, name="Абзац"):
        super().__init__(tm, name)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self._text_edit = TextEdit()
        main_layout.addWidget(self._text_edit)

    def store(self):
        return {'__class__': self.__class__.__name__, 'text': self._text_edit.toPlainText()}

    def load(self, data: dict):
        self._text_edit.setText(data.get('text', ''))

    def set_theme(self):
        super().set_theme()
        self.tm.auto_css(self._text_edit)


class ReportCodeEdit(ReportTextEdit):
    NAME = "Код"

    def __init__(self, tm):
        super().__init__(tm, "Код")


class ReportListWidgetItem(ReportWidget):
    def __init__(self, tm):
        super().__init__(tm, "")

        self._label = QLabel("-")
        self._top_layout.insertWidget(1, self._label)

        self._line_edit = QLineEdit()
        self._top_layout.insertWidget(2, self._line_edit)

    def store(self):
        return {'__class__': self.__class__.__name__, 'text': self._line_edit.text()}

    def load(self, data: dict):
        self._line_edit.setText(data.get('text', ''))

    def set_theme(self):
        super().set_theme()
        self.tm.auto_css(self._line_edit)
        self.tm.auto_css(self._label)
        
        
class ReportListWidget(ReportWidget):
    NAME = "Список"

    def __init__(self, tm):
        super().__init__(tm, "Список", [ReportListWidgetItem])

        self._combo_box = QComboBox()
        self._combo_box.addItems(["Маркированный", "Нумерованный"])
        self._top_layout.insertWidget(1, self._combo_box)

        self.setLayout(self._children_layout)

    def store(self):
        return {'__class__': self.__class__.__name__, 'children': [el.store() for el in self._children],
                'type': self._combo_box.currentIndex()}

    def load(self, data: dict):
        for el in data.get('children', []):
            widget = get_widget(el)(self.tm)
            self._combo_box.setCurrentIndex(data.get('type', 0))
            widget.load(el)
            self.add_child(widget)

    def set_theme(self):
        super().set_theme()
        self.tm.auto_css(self._combo_box)


class TextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(28)
        self.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self):
        height = self.verticalScrollBar().maximum()
        if not height:
            self.setFixedHeight(28)
            height = self.verticalScrollBar().maximum()
        self.setFixedHeight(self.height() + height)


class SelectChildDialog(QDialog):
    def __init__(self, tm, parent: ReportWidget):
        super().__init__()

        self.setFixedSize(200, 76)

        mail_layout = QVBoxLayout()
        self.setLayout(mail_layout)

        self._combo_box = QComboBox()
        for el in parent.children_list:
            self._combo_box.addItems([el.NAME])
        mail_layout.addWidget(self._combo_box)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        mail_layout.addLayout(buttons_layout)

        self._button = QPushButton("Добавить")
        self._button.setFixedSize(100, 22)
        self._button.clicked.connect(self.accept)
        buttons_layout.addWidget(self._button)

        for el in [self._button, self._combo_box]:
            tm.auto_css(el)

    def current_index(self):
        return self._combo_box.currentIndex()
