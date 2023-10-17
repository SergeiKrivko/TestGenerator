import os

from PyQt6.QtCore import QThread, pyqtSignal

import config
from side_tabs.telegram.telegram_api import TgClient, types
from side_tabs.telegram.telegram_api import events


class TelegramManager(QThread):
    authorization = pyqtSignal(object)

    newChat = pyqtSignal(types.TgChat)
    updateChat = pyqtSignal(str)
    addMessage = pyqtSignal(types.TgMessage)
    insertMessage = pyqtSignal(types.TgMessage)
    loadingFinished = pyqtSignal(types.TgChat)

    updateUserStatus = pyqtSignal(str)

    updateFile = pyqtSignal(types.TgFile)

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
        self._client.console_authentication = False
        self._client.set_authorization_handler(self.authorization.emit)

        self.temp_path = f"{self._sm.app_data_dir}/Telegram/files"
        os.makedirs(self.temp_path, exist_ok=True)

        self._options = dict()
        self._files = dict()
        self._chats = dict()
        self._users = dict()
        self._handlers = dict()

    def __getitem__(self, item):
        return self._options[item]

    def __setitem__(self, key, value):
        self._options[key] = value

    def get(self, key, default=None):
        return self._options.get(key, default)

    def get_chat(self, chat_id: int) -> types.TgChat:
        return self._chats[chat_id]

    def get_user(self, user_id: int) -> types.TgUser:
        return self._users[user_id]

    def update_chat(self, chat: types.TgChat):
        if chat.id not in self._chats:
            self._chats[chat.id] = chat

    def update_file(self, file: types.TgFile):
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

    def load_messages(self, chat: types.TgChat):
        self._client.load_messages(chat, max_count=50)

    def download_file(self, file: types.TgFile):
        self._client.download_file(file)

    def view_messages(self, chat_id: int, message_ids: list):
        # return
        self._client.send({'@type': "viewMessages", 'chat_id': chat_id, 'message_ids': message_ids})

    def open_chat(self, chat_id: int):
        self._client.send({'@type': 'openChat', 'chat_id': chat_id})

    def close_chat(self, chat_id: int):
        self._client.send({'@type': 'closeChat', 'chat_id': chat_id})

    def authenticate_user(self, str1, str2):
        self._client.send_authentication(str1, str2)

    def _handler(self, event_dict: dict):
        event = events.convert_event(event_dict, self)
        # OPTIONS

        if isinstance(event, events.TgUpdateOption):
            self._options[event.name] = event.value.value

        # CHATS

        elif isinstance(event, events.TgUpdateNewChat):
            self._chats[event.chat.id] = event.chat
            self.newChat.emit(event.chat)
        elif isinstance(event, events.TgUpdateChatReadInbox):
            self._chats[event.chat_id].unread_count = event.unread_count
            self.updateChat.emit(str(event.chat_id))

        # MESSAGES

        elif isinstance(event, events.TgUpdateNewMessage):
            chat = self.get_chat(event.message.chat_id)
            if chat.last_message is None or event.message.id != chat.last_message.id:
                chat.append_message(event.message)
                # print(event_dict)
                self.addMessage.emit(event.message)
        elif isinstance(event, events.TgUpdateChatLastMessage):
            if event.last_message is not None:
                chat = self.get_chat(event.chat_id)
                chat.set_last_message(event.last_message)
        elif isinstance(event, events.TgMessages):
            el = None
            for el in map(lambda message: types.TgMessage(message, self), event.messages):
                self.get_chat(el.chat_id).insert_message(el)
                self.insertMessage.emit(el)
            if el is not None and self.get_chat(el.chat_id).last_message_count < self.get_chat(
                    el.chat_id).message_count():
                self.get_chat(el.chat_id).last_message_count = self.get_chat(el.chat_id).message_count()
                self.loadingFinished.emit(self.get_chat(el.chat_id))

        # USERS

        elif isinstance(event, events.TgUpdateUser):
            self._users[event.user.id] = event.user
        elif isinstance(event, events.TgUpdateUserStatus):
            self.get_user(event.user_id).set_status(event.status)
            self.updateUserStatus.emit(str(event.user_id))

        # FILES

        elif isinstance(event, events.TgUpdateFile):
            types.update_object(file := self._files[event.file.id], event.file)
            self.updateFile.emit(file)
        # else:
        #     print(event)

    def run(self):
        self._client.execute()
