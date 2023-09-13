from PyQt5.QtCore import QThread, QObject, pyqtSignal
from pywtdlib.client import Client
from pywtdlib.enum import Update, AuthorizationState

import config


class TelegramObject(QObject):
    def __init__(self, data: dict):
        super().__init__()
        self._dict = data

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def __str__(self):
        return str(self._dict)


class TelegramManager(QThread):
    newChat = pyqtSignal(TelegramObject)
    requestAuthentication = pyqtSignal(str, bool, str, str)

    def __init__(self, sm):
        super().__init__()
        self._sm = sm

        self._tg = Client(api_id=config.TELEGRAM_API_KEY,
                          api_hash=config.TELEGRAM_API_HASH,
                          use_chat_info_database=True,
                          use_file_database=True,
                          use_message_database=True,
                          )
        self._tg.database_directory = f"{self._sm.app_data_dir}/Telegram/tdlib"
        self._tg.set_update_handler(self._update_handler)

        self._users = dict()
        self._chats = dict()

        self._options = dict()

    def send(self, query: dict):
        self._tg.tdjson.send(query)

    def get_messages(self, chat_id):
        if isinstance(chat_id, str):
            chat_id = int(chat_id)
        if chat_id not in self._chats:
            return
        chat = self._chats[chat_id]
        message_id = chat.first_message_id()
        if message_id is not None:
            self.send({'@type': 'getChatHistory', 'chat_id': chat_id, 'limit': Update.LIMIT_CHATS,
                       'from_message_id': message_id})
        else:
            self.send({'@type': 'getChatHistory', 'chat_id': chat_id, 'limit': Update.LIMIT_CHATS})
        # self._tg.tdjson.send({'@type': 'getChatHistory', 'chat_id': chat_id, 'limit': Update.LIMIT_CHATS})

    def __getitem__(self, item):
        return self._options[item]

    def __setitem__(self, key, value):
        self._options[key] = value

    def get(self, key, default=None):
        return self._options.get(key, default)

    def get_chat(self, chat_id):
        return self._chats[chat_id]

    def authenticate_user(self, event: dict) -> None:
        # process authorization states
        if event["@type"] == AuthorizationState.AUTHORIZATION:
            auth_state = event["authorization_state"]["@type"]

            # if client is closed, we need to destroy it and create new client
            if auth_state == AuthorizationState.CLOSED:
                self._tg.logger.critical(event)
                raise ValueError(event)

            # set TDLib parameters
            # you MUST obtain your own api_id and api_hash at https://my.telegram.org
            # and use them in the setTdlibParameters call
            if auth_state == AuthorizationState.WAIT_TDLIB_PARAMETERS:
                self._tg.send_tdlib_parameters()

            # enter phone number to log in
            if auth_state == AuthorizationState.WAIT_PHONE_NUMBER:
                self.requestAuthentication.emit("Please enter your phone number: ", False,
                                                "setAuthenticationPhoneNumber", "phone_number")
                # self.send_phone_number()

            # wait for authorization code
            if auth_state == AuthorizationState.WAIT_CODE:
                self.requestAuthentication.emit("Please enter the authentication code you received: ", True,
                                                "checkAuthenticationCode", "code")
                # self.send_auth_code()

            # wait for first and last name for new users
            if auth_state == AuthorizationState.WAIT_REGISTRATION:
                self._tg.register_user()

            # wait for password if present
            if auth_state == AuthorizationState.WAIT_PASSWORD:
                self.requestAuthentication.emit("Please enter your password: ", True,
                                                "checkAuthenticationPassword", "password")
                # self.send_password()

            # enter email address to log in
            if auth_state == AuthorizationState.WAIT_EMAIL_ADDRESS:
                self.requestAuthentication.emit("Please enter your email address: ", False,
                                                "setAuthenticationEmailAddress", "email_address")
                # self.send_email()

            # wait for email authorization code
            if auth_state == AuthorizationState.WAIT_EMAIL_CODE:
                # self.requestAuthentication.emit("Please enter the email authentication code you received: ", True,
                #                                 "checkAuthenticationPassword", "password")
                self._tg.send_email_code()

            # user authenticated
            if auth_state == AuthorizationState.READY:
                # get all chats
                self._tg.get_all_chats()

                self._tg.authorized = True
                self._tg.logger.info("User authorized")

    def _update_handler(self, event):
        if event.get('@type') == "updateOption":
            if event['value']['@type'] == 'optionValueInteger':
                self[event['name']] = int(event['value'].get('value'))
            else:
                self[event['name']] = event['value'].get('value')

        if not self._tg.authorized:
            self.authenticate_user(event)
        elif event.get('@type') == "updateUser":
            self._users[event['user']['id']] = TelegramUser(event['user'])
        elif event.get('@type') == "updateNewChat":
            chat = TelegramChat(event['chat'])
            chat.chatHistoryRequest.connect(self.get_messages)
            self._chats[event['chat']['id']] = chat
            self.newChat.emit(chat)
        elif event.get('@type') == "updateNewMessage":
            message = TelegramChat(event['message'])
            if message['chat_id'] in self._chats:
                self._chats[message['chat_id']].add_message(message)
        elif event.get('@type') == "messages":
            message = None
            for el in event['messages']:
                message = TelegramMessage(el)
                if message['chat_id'] in self._chats:
                    self._chats[message['chat_id']].insert_message(message)
            if message is not None:
                self._chats[message['chat_id']].loading_finished()
        else:
            print(event)

    def users(self):
        return self._users

    def send_message(self, text: str, chat_id: int):
        self._tg.tdjson.send(
            {"@type": Update.SEND_MESSAGE,
             "chat_id": chat_id,
             "input_message_content": {'@type': 'inputMessageText', 'text': {'@type': 'formattedText', 'text': text}}})

    def run(self):
        self._tg.start()


class TelegramUser(TelegramObject):
    def __init__(self, data: dict):
        super().__init__(data)


class TelegramMessage(TelegramObject):
    def __init__(self, data):
        super().__init__(data)


class TelegramChat(TelegramObject):
    insertMessage = pyqtSignal(TelegramMessage)
    newMessage = pyqtSignal(TelegramMessage)
    chatHistoryRequest = pyqtSignal(str)
    loadingFinished = pyqtSignal()

    def __init__(self, data: dict):
        super().__init__(data)
        self._messages = dict()
        self._list = []
        self._loading = False

    def add_message(self, message: TelegramMessage):
        self._messages[message['id']] = message
        self._list.append(message['id'])
        self.newMessage.emit(message)

    def insert_message(self, message: TelegramMessage):
        self._messages[message['id']] = message
        self._list.insert(0, message['id'])
        self.insertMessage.emit(message)

    def first_message_id(self):
        if len(self._list) == 0:
            return None
        return self._list[0]

    def last_message_id(self):
        if len(self._list) == 0:
            return None
        return self._list[-1]

    def message_list(self):
        return self._list

    def load_messages(self):
        if self._loading:
            return
        self._loading = True
        self.chatHistoryRequest.emit(str(self['id']))

    def loading_finished(self):
        self._loading = False
        self.loadingFinished.emit()


dct = {'@type': 'message',
       'id': 9288286208,
       'sender_id': {'@type': 'messageSenderUser', 'user_id': 5202599233},
       'chat_id': 5202599233,
       'is_outgoing': True,
       'is_pinned': False,
       'can_be_edited': True,
       'can_be_forwarded': True,
       'can_be_saved': True,
       'can_be_deleted_only_for_self': True,
       'can_be_deleted_for_all_users': False,
       'can_get_added_reactions': False,
       'can_get_statistics': False,
       'can_get_message_thread': False,
       'can_get_viewers': False,
       'can_get_media_timestamp_links': False,
       'can_report_reactions': False,
       'has_timestamped_media': True,
       'is_channel_post': False, 'is_topic_message': False,
       'contains_unread_mention': False,
       'date': 1694536273,
       'edit_date': 0,
       'unread_reactions': [],
       'reply_in_chat_id': 0,
       'reply_to_message_id': 0,
       'message_thread_id': 0, 'ttl': 0,
       'ttl_expires_in': 0.0,
       'via_bot_user_id': 0,
       'author_signature': '',
       'media_album_id': '0',
       'restriction_reason': '',
       'content': {'@type': 'messageText', 'text': {'@type': 'formattedText', 'text': '1', 'entities': []}}}

dct = {'@type': 'message',
       'id': 9296674816,
       'sender_id': {'@type': 'messageSenderUser', 'user_id': 5202599233},
       'chat_id': 547732104,
       'is_outgoing': True,
       'is_pinned': False,
       'can_be_edited': True,
       'can_be_forwarded': True,
       'can_be_saved': True,
       'can_be_deleted_only_for_self': True,
       'can_be_deleted_for_all_users': True,
       'can_get_added_reactions': False,
       'can_get_statistics': False,
       'can_get_message_thread': False,
       'can_get_viewers': False,
       'can_get_media_timestamp_links': False,
       'can_report_reactions': False,
       'has_timestamped_media': True,
       'is_channel_post': False,
       'is_topic_message': False,
       'contains_unread_mention': False,
       'date': 1694542260, 'edit_date': 0,
       'unread_reactions': [],
       'reply_in_chat_id': 0,
       'reply_to_message_id': 0,
       'message_thread_id': 0,
       'ttl': 0,
       'ttl_expires_in': 0.0,
       'via_bot_user_id': 0,
       'author_signature': '',
       'media_album_id': '0',
       'restriction_reason': '',
       'content': {'@type': 'messagePhoto', 'photo': {
           '@type': 'photo', 'has_stickers': False,
           'minithumbnail': {'@type': 'minithumbnail', 'width': 25,
                             'height': 40,
                             'data': '/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDACgcHiMeGSgjISMtKygwPGRBPDc3PHtYXUlkkYCZlo+AjIqgtObDoKrarYqMyP/L2u71////m8H////6/+b9//j/2wBDASstLTw1PHZBQXb4pYyl+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj/wAARCAAoABkDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDPBx6flR+BoH1xSk/7VACUzzG9f0p2STz0qOgCXBHUYoo3FuSc0UwCoqlqKkBIOlLRRQAAZqKiigD/2Q=='},
           'sizes': [{'@type': 'photoSize', 'type': 'm',
                      'photo': {'@type': 'file', 'id': 1436, 'size': 9945,
                                'expected_size': 9945,
                                'local': {'@type': 'localFile', 'path': '',
                                          'can_be_downloaded': True,
                                          'can_be_deleted': False,
                                          'is_downloading_active': False,
                                          'is_downloading_completed': False,
                                          'download_offset': 0,
                                          'downloaded_prefix_size': 0,
                                          'downloaded_size': 0},
                                'remote': {'@type': 'remoteFile',
                                           'id': 'AgACAgIAAxkDAAIiomUAAam0cTnbCF1h0tOTWUccuaqW-QAC8c0xG2WMCUibI0zd1ZnWrwEAAwIAA20AAywE',
                                           'unique_id': 'AQAD8c0xG2WMCUhy',
                                           'is_uploading_active': False,
                                           'is_uploading_completed': True,
                                           'uploaded_size': 9945}},
                      'width': 204, 'height': 320, 'progressive_sizes': []},
                     {'@type': 'photoSize', 'type': 'x',
                      'photo': {'@type': 'file', 'id': 1437, 'size': 21972,
                                'expected_size': 21972,
                                'local': {'@type': 'localFile', 'path': '',
                                          'can_be_downloaded': True,
                                          'can_be_deleted': False,
                                          'is_downloading_active': False,
                                          'is_downloading_completed': False,
                                          'download_offset': 0,
                                          'downloaded_prefix_size': 0,
                                          'downloaded_size': 0},
                                'remote': {'@type': 'remoteFile',
                                           'id': 'AgACAgIAAxkDAAIiomUAAam0cTnbCF1h0tOTWUccuaqW-QAC8c0xG2WMCUibI0zd1ZnWrwEAAwIAA3gAAywE',
                                           'unique_id': 'AQAD8c0xG2WMCUh9',
                                           'is_uploading_active': False,
                                           'is_uploading_completed': True,
                                           'uploaded_size': 21972}},
                      'width': 355, 'height': 558,
                      'progressive_sizes': [2321, 4941, 11474, 15888]}]},
                   'caption': {'@type': 'formattedText', 'text': 'Отправлено из Telegram Desktop', 'entities': []},
                   'is_secret': False}}
