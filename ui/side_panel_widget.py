from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout

from ui.button import Button


class SidePanelWidget(QWidget):
    __Buttons = {
        'add': lambda tm: SidePanelButton(tm, 'plus', tooltip='Создать'),
        'delete': lambda tm: SidePanelButton(tm, 'button_delete', tooltip='Удалить'),
        'rename': lambda tm: SidePanelButton(tm, 'button_rename', tooltip='Переименовать'),
        'to_zip': lambda tm: SidePanelButton(tm, 'button_to_zip', tooltip='Сжать в zip'),
        'from_zip': lambda tm: SidePanelButton(tm, 'button_from_zip', tooltip='Распаковать из zip'),
        'run': lambda tm: SidePanelButton(tm, 'run', tooltip='Запустить'),
        'pull': lambda tm: SidePanelButton(tm, 'button_pull', tooltip='Pull'),
        'commit': lambda tm: SidePanelButton(tm, 'button_commit', tooltip='Commit'),
        'push': lambda tm: SidePanelButton(tm, 'button_push', tooltip='Push'),
        'minimize': lambda tm: SidePanelButton(tm, 'delete'),
    }

    def __init__(self, sm, tm, name, buttons):
        super().__init__()
        self.sm = sm
        self.tm = tm

        __main_layout = QVBoxLayout()
        __main_layout.setContentsMargins(0, 0, 0, 0)

        __top_layout = QHBoxLayout()

        self.__name_label = QLabel(name)
        __top_layout.addWidget(self.__name_label)

        self.buttons = dict()

        for el in buttons:
            button = self.__Buttons[el](self.tm)
            self.buttons[el] = button
            __top_layout.addWidget(button)

        __main_layout.addLayout(__top_layout)

        self.__main_widget = QWidget()
        __main_layout.addWidget(self.__main_widget)
        super().setLayout(__main_layout)

    def setLayout(self, a0) -> None:
        self.__main_widget.setLayout(a0)

    def set_theme(self):
        self.tm.auto_css(self.__name_label)
        for el in self.buttons.values():
            el.set_theme()


class SidePanelButton(Button):
    def __init__(self, tm, image, tooltip=''):
        super().__init__(tm, image, css='Main', tooltip=tooltip)
        self.setFixedSize(24, 24)
