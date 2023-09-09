from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton

from ui.button import Button


class SidePanelWidget(QWidget):
    startResizing = pyqtSignal()
    __Buttons = {
        'add': lambda tm: SidePanelButton(tm, 'plus', tooltip='Создать'),
        'delete': lambda tm: SidePanelButton(tm, 'button_delete', tooltip='Удалить'),
        'rename': lambda tm: SidePanelButton(tm, 'button_rename', tooltip='Переименовать'),
        'to_zip': lambda tm: SidePanelButton(tm, 'button_to_zip', tooltip='Сжать в zip'),
        'from_zip': lambda tm: SidePanelButton(tm, 'button_from_zip', tooltip='Распаковать из zip'),
        'run': lambda tm: SidePanelButton(tm, 'run', tooltip='Запустить'),
        'preview': lambda tm: SidePanelButton(tm, 'button_preview', tooltip='Предпросмотр'),
        'pull': lambda tm: SidePanelButton(tm, 'button_pull', tooltip='Pull'),
        'commit': lambda tm: SidePanelButton(tm, 'button_commit', tooltip='Commit'),
        'push': lambda tm: SidePanelButton(tm, 'button_push', tooltip='Push'),
        'save': lambda tm: SidePanelButton(tm, 'button_save', tooltip='Сохранить'),
        'load': lambda tm: SidePanelButton(tm, 'button_load', tooltip='Открыть'),
        'update': lambda tm: SidePanelButton(tm, 'update', tooltip='Обновить'),
        'cancel': lambda tm: SidePanelButton(tm, 'button_cancel', tooltip='Отменить'),
        'close': lambda tm: SidePanelButton(tm, 'delete', tooltip='Закрыть'),
    }

    def __init__(self, sm, tm, name, buttons):
        super().__init__()
        self.sm = sm
        self.tm = tm

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 0, 5)
        layout.setSpacing(5)
        main_layout.addLayout(layout)

        __top_layout = QHBoxLayout()
        __top_layout.setSpacing(2)

        self.__name_label = QLabel(name)
        __top_layout.addWidget(self.__name_label)

        self.buttons = dict()

        for el in buttons:
            button = self.__Buttons[el](self.tm)
            self.buttons[el] = button
            __top_layout.addWidget(button)

        layout.addLayout(__top_layout)

        self._resize_widget = _ResizeWidget(self.tm)
        self._resize_widget.pressed.connect(self.startResizing.emit)
        main_layout.addWidget(self._resize_widget)

        self.__main_widget = QWidget()
        layout.addWidget(self.__main_widget)
        super().setLayout(main_layout)

    def setLayout(self, a0) -> None:
        self.__main_widget.setLayout(a0)

    def setFixedWidth(self, w: int) -> None:
        self._resize_widget.setDisabled(True)
        super().setFixedWidth(w)

    def set_theme(self):
        self._resize_widget.set_theme()
        self.setStyleSheet(f"border: none;")
        self.tm.auto_css(self.__name_label)
        for el in self.buttons.values():
            el.set_theme()

    def get_button(self, key):
        return self.buttons.get(key)


class SidePanelButton(Button):
    def __init__(self, tm, image, tooltip=''):
        super().__init__(tm, image, css='Main', tooltip=tooltip)
        self.setFixedSize(24, 24)


class _ResizeWidget(QPushButton):
    pressed = pyqtSignal()

    def __init__(self, tm):
        super().__init__()
        self.tm = tm
        self.setMaximumHeight(10000)
        self.setFixedWidth(5)

        self.setCursor(QCursor(Qt.SizeHorCursor))

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            self.pressed.emit()

    def set_theme(self):
        self.setStyleSheet(f"""
        QPushButton {{
            background-color: {self.tm['MainColor']};
            border-right: 1px solid {self.tm['BorderColor']};
        }}
        """)
