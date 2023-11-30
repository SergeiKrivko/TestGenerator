import os

from PyQt6.QtCore import QThread, pyqtSignal

import config
from side_tabs.telegram.telegram_api import TgClient, tg


class TgChat(tg.Chat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._messages = dict()
        self.first_message = None
        self.last_message = None
        self.last_message_count = 0

    def append_message(self, message: tg.Message):
        self._messages[message.id] = message
        self.set_last_message(message)
        if self.first_message is None:
            self.set_first_message(message)

    def insert_message(self, message: tg.Message):
        self._messages[message.id] = message
        self.set_first_message(message)

    def set_first_message(self, message: tg.Message):
        self.first_message = message

    def set_last_message(self, message: tg.Message):
        self.last_message = message

    def get_message(self, message_id):
        return self._messages[message_id]

    def message_count(self):
        return len(self._messages)


class TelegramManager(QThread):
    authorization = pyqtSignal(object)

    chatsLoaded = pyqtSignal(list)
    updateChat = pyqtSignal(str)
    addMessage = pyqtSignal(tg.Message)
    insertMessage = pyqtSignal(tg.Message)
    loadingFinished = pyqtSignal(TgChat)
    updateFolders = pyqtSignal(dict)
    messageInterationInfoChanged = pyqtSignal(object, object)
    deleteMessages = pyqtSignal(object, list)

    updateUserStatus = pyqtSignal(str)

    updateFile = pyqtSignal(tg.File)

    def __init__(self, sm):
        super().__init__()
        self._sm = sm
        self._client = TgClient(api_id=config.TELEGRAM_API_KEY,
                                api_hash=config.TELEGRAM_API_HASH,
                                use_chat_info_database=True,
                                use_file_database=True,
                                use_message_database=True)
        self._client.database_directory = f"{self._sm.app_data_dir}/Telegram/tdlib"
        self._client.set_update_handler(self._handler)
        self._client.set_error_handler(self.error_handler)
        self._client.console_authentication = False
        self._client.set_authorization_handler(self.authorization.emit)

        self.temp_path = f"{self._sm.app_data_dir}/Telegram/files"
        os.makedirs(self.temp_path, exist_ok=True)

        self._options = dict()
        self._files = dict()
        self._chats = dict()
        self._users = dict()
        self._chat_lists = {'All': tg.ChatListMain(), 'Archive': tg.ChatListArchive()}
        self._messages_to_get_reactions = []
        self._search_reactions_now = None

    def __getitem__(self, item):
        return self._options[item]

    def __setitem__(self, key, value):
        self._options[key] = value

    def get(self, key, default=None):
        return self._options.get(key, default)

    def get_chat(self, chat_id: int) -> TgChat:
        return self._chats[chat_id]

    def get_user(self, user_id: int) -> tg.User:
        return self._users[user_id]

    def update_chat(self, chat: TgChat):
        if chat.id not in self._chats:
            self._chats[chat.id] = chat

    def update_file(self, file: tg.File):
        if file.id not in self._files:
            self._files[file.id] = file

    # COMMANDS

    def send_message(self, text, chat_id):
        self._client.send({"@type": "sendMessage", "chat_id": chat_id, "input_message_content": {
            "@type": "inputMessageText", "text": {"@type": "@formattedText", "text": text}}})

    def send_file_message(self, text, path, chat_id):
        self._client.send({"@type": "sendMessage", "chat_id": chat_id, "input_message_content": {
            "@type": "inputMessageDocument", "caption": {"@type": "@formattedText", "text": text},
            "document": {"@type": "inputFileLocal", "path": path}}})

    def load_messages(self, chat: TgChat, max_count=100):
        if chat.first_message is None:
            self._client.send({'@type': 'getChatHistory', 'chat_id': chat.id, 'limit': max_count})
        else:
            self._client.send({'@type': 'getChatHistory', 'chat_id': chat.id, 'limit': max_count,
                               'from_message_id': chat.first_message.id})

    def view_messages(self, chat_id: int, message_ids: list):
        self._client.send({'@type': "viewMessages", 'chat_id': chat_id, 'message_ids': message_ids})

    def open_chat(self, chat_id: int):
        self._client.send({'@type': 'openChat', 'chat_id': chat_id})

    def close_chat(self, chat_id: int):
        self._client.send({'@type': 'closeChat', 'chat_id': chat_id})

    def get_reactions(self, message: tg.Message):
        self._messages_to_get_reactions.append(message)
        if self._search_reactions_now is None:
            message = self._messages_to_get_reactions.pop(0)
            self._search_reactions_now = message
            tg.getMessageAddedReactions(message.chat_id, message.id, limit=500)

    def authenticate_user(self, str1, str2):
        self._client.send_authentication(str1, str2)

    def _handler(self, event):
        # event = events.convert_event(event_dict, self)
        # OPTIONS

        if isinstance(event, tg.UpdateOption):
            self._options[event.name] = event.value.value

        # CHATS

        elif isinstance(event, tg.UpdateNewChat):
            self._chats[event.chat.id] = TgChat(**tg.to_json(event.chat))
            self.updateChat.emit(str(event.chat.id))
        elif isinstance(event, tg.UpdateChatReadInbox):
            self._chats[event.chat_id].unread_count = event.unread_count
            self.updateChat.emit(str(event.chat_id))
        elif isinstance(event, tg.Chats):
            for chat_id in event.chat_ids:
                if chat_id not in self._chats:
                    tg.getChat(chat_id)
            self.chatsLoaded.emit(event.chat_ids)
        elif isinstance(event, tg.UpdateChatFolders):
            for el in event.chat_folders:
                self._chat_lists[el.title] = tg.ChatListFolder(chat_folder_id=el.id)
            self.updateFolders.emit(self._chat_lists)

        # MESSAGES

        elif isinstance(event, tg.UpdateNewMessage):
            chat = self.get_chat(event.message.chat_id)
            if chat.last_message is None or event.message.id != chat.last_message.id:
                chat.append_message(event.message)
                self.addMessage.emit(event.message)
        elif isinstance(event, tg.UpdateChatLastMessage):
            if event.last_message is not None:
                chat = self.get_chat(event.chat_id)
                chat.set_last_message(event.last_message)
        elif isinstance(event, tg.UpdateDeleteMessages):
            self.deleteMessages.emit(event.chat_id, event.message_ids)
        elif isinstance(event, tg.Messages):
            el = None
            for el in event.messages:
                self.get_chat(el.chat_id).insert_message(el)
                self.insertMessage.emit(el)
            if el is not None and self.get_chat(el.chat_id).last_message_count < self.get_chat(
                    el.chat_id).message_count():
                self.get_chat(el.chat_id).last_message_count = self.get_chat(el.chat_id).message_count()
                self.loadingFinished.emit(self.get_chat(el.chat_id))
        elif isinstance(event, tg.UpdateMessageInteractionInfo):
            self.get_chat(event.chat_id).get_message(event.message_id).interaction_info = event.interaction_info
            self.messageInterationInfoChanged.emit(event.chat_id, event.message_id)

        # USERS

        elif isinstance(event, tg.UpdateUser):
            self._users[event.user.id] = event.user
        elif isinstance(event, tg.UpdateUserStatus):
            self.get_user(event.user_id).status = event.status
            self.updateUserStatus.emit(str(event.user_id))

        # FILES

        elif isinstance(event, tg.UpdateFile):
            if event.file.id not in self._files:
                self._files[event.file.id] = event.file
            tg.update_object(file := self._files[event.file.id], event.file)
            self.updateFile.emit(file)
        # else:
        #     print(tg.to_json(event))

    def error_handler(self, error: dict):
        error = tg.get_object(error)
        if not isinstance(error, tg.Error):
            return

        if error.code == 400 and error.message == 'MSG_ID_INVALID':
            if self._messages_to_get_reactions:
                self._search_reactions_now = self._messages_to_get_reactions.pop(0)
                tg.getMessageAddedReactions(self._search_reactions_now.chat_id,
                                            self._search_reactions_now.id, limit=500)
            else:
                self._search_reactions_now = None

    def run(self):
        self._client.execute()
