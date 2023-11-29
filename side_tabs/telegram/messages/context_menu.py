from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMenu

from side_tabs.telegram.telegram_api import tg


class ContextMenu(QMenu):
    DELETE = 1
    SAVE = 2
    IMPORT = 3
    OPEN_FILE = 4
    SHOW_IN_FOLDER = 5

    def __init__(self, message: tg.Message, tm):
        super().__init__()
        self.tm = tm
        self.action = 0

        action = self.addAction(QIcon(self.tm.get_image('button_delete')), "Удалить")
        action.triggered.connect(lambda: self.set_action(ContextMenu.DELETE))

        self.addSeparator()

        if isinstance(message.content, tg.MessageDocument):
            action = self.addAction("Открыть")
            action.triggered.connect(lambda: self.set_action(ContextMenu.OPEN_FILE))

            action = self.addAction(QIcon(self.tm.get_image('directory')), "Показать в папке")
            action.triggered.connect(lambda: self.set_action(ContextMenu.SHOW_IN_FOLDER))

            action = self.addAction(QIcon(self.tm.get_image('button_save')), "Сохранить")
            action.triggered.connect(lambda: self.set_action(ContextMenu.SAVE))

            action = self.addAction(QIcon(self.tm.get_image('button_import')), "Импортировать в проект")
            action.triggered.connect(lambda: self.set_action(ContextMenu.IMPORT))

        self.tm.auto_css(self)

    def set_action(self, action):
        self.action = action
