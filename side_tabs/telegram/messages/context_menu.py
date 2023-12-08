import math

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMenu

from side_tabs.telegram.telegram_api import tg
from side_tabs.telegram.telegram_manager import TelegramManager


class ContextMenu(QMenu):
    DELETE = 1
    SAVE = 2
    IMPORT = 3
    OPEN_FILE = 4
    SHOW_IN_FOLDER = 5
    DELETE_FOR_ALL = 6
    PLAY_VIDEO = 7
    STOP_VIDEO = 8
    PAUSE_VIDEO = 9
    ADD_REACTION = 10
    DOWNLOAD_DOCUMENT = 11
    DOWNLOAD_VIDEO = 12

    def __init__(self, message: tg.Message, chat: tg.Chat, manager: TelegramManager, tm):
        super().__init__()
        self.tm = tm
        self._manager = manager
        self.action = 0
        self.data = None

        action = self.addAction(QIcon(self.tm.get_image('buttons/button_delete')), "Удалить")
        action.triggered.connect(lambda: self.set_action(ContextMenu.DELETE))

        action = self.addAction(QIcon(self.tm.get_image('buttons/button_delete')), "Удалить для всех")
        action.triggered.connect(lambda: self.set_action(ContextMenu.DELETE_FOR_ALL))

        self.addMenu(menu := ReactionsMenu(self.tm, self._manager, chat))
        menu.emojiSelected.connect(lambda emoji: (self.set_action(ContextMenu.ADD_REACTION), self.set_data(emoji)))

        self.addSeparator()

        if isinstance(message.content, tg.MessageDocument):
            if message.content.document.document.local.is_downloading_completed:
                action = self.addAction("Открыть")
                action.triggered.connect(lambda: self.set_action(ContextMenu.OPEN_FILE))

                action = self.addAction(QIcon(self.tm.get_image('icons/directory')), "Показать в папке")
                action.triggered.connect(lambda: self.set_action(ContextMenu.SHOW_IN_FOLDER))

                action = self.addAction(QIcon(self.tm.get_image('buttons/button_save')), "Сохранить")
                action.triggered.connect(lambda: self.set_action(ContextMenu.SAVE))

                # action = self.addAction(QIcon(self.tm.get_image('button_import')), "Импортировать в проект")
                # action.triggered.connect(lambda: self.set_action(ContextMenu.IMPORT))

            else:
                action = self.addAction(QIcon(self.tm.get_image('buttons/button_import')), "Скачать")
                action.triggered.connect(lambda: self.set_action(ContextMenu.DOWNLOAD_DOCUMENT))

        elif isinstance(message.content, tg.MessageVideo):
            print(message.content.video.video.local.path, message.content.video.video.local.is_downloading_completed)
            if message.content.video.video.local.is_downloading_completed:
                action = self.addAction(QIcon(self.tm.get_image('buttons/button_run')), "Запустить")
                action.triggered.connect(lambda: self.set_action(ContextMenu.PLAY_VIDEO))

                action = self.addAction(QIcon(self.tm.get_image('buttons/button_pause')), "Приостановить")
                action.triggered.connect(lambda: self.set_action(ContextMenu.STOP_VIDEO))

                # action = self.addAction(QIcon(self.tm.get_image('button_save')), "Сохранить")
                # action.triggered.connect(lambda: self.set_action(ContextMenu.SAVE_VIDEO))

            else:
                action = self.addAction(QIcon(self.tm.get_image('buttons/button_import')), "Скачать")
                action.triggered.connect(lambda: self.set_action(ContextMenu.DOWNLOAD_VIDEO))

        self.tm.auto_css(self)

    def set_action(self, action):
        self.action = action

    def set_data(self, data):
        self.data = data


class ReactionsMenu(QMenu):
    emojiSelected = pyqtSignal(str)

    def __init__(self, tm, manager: TelegramManager, chat: tg.Chat):
        super().__init__()
        self._tm = tm
        self.reaction = ''
        self._manager = manager
        self._chat = chat

        # self.setFixedHeight(math.ceil(len(self._manager.active_reactions) ** 0.5) * 20)
        # self.setFixedWidth(math.ceil(len(self._manager.active_reactions) ** 0.5) * 20)

        self.setTitle("Добавить реакцию")

        if isinstance(self._chat.available_reactions, tg.ChatAvailableReactionsAll):
            for el in self._manager.active_reactions:
                self.add_reaction(el)
        elif isinstance(self._chat.available_reactions, tg.ChatAvailableReactionsSome):
            for el in self._chat.available_reactions.reactions:
                if isinstance(el, tg.ReactionTypeEmoji):
                    self.add_reaction(el.emoji)

        self.setStyleSheet(self._tm.menu_css(palette='Main', padding='4px 4px'))

    def add_reaction(self, emoji):
        a = self.addAction(QIcon(self._tm.get_image('emoji/' + emoji)), '')
        a.triggered.connect(lambda: self.set_reaction(emoji))

    def set_reaction(self, emoji):
        self.reaction = emoji
        self.emojiSelected.emit(emoji)
