from pywtdlib.client import Client
from typing import Callable, Optional

import side_tabs.telegram.telegram_api.types as types
import side_tabs.telegram.telegram_api.events as events
from side_tabs.telegram.telegram_api.class_converter import Module


class TgClient(Client):

    def __init__(
            self,
            api_id: int,
            api_hash: str,
            use_file_database: Optional[bool] = False,
            use_chat_info_database: Optional[bool] = False,
            use_message_database: Optional[bool] = False,
            use_secret_chats: Optional[bool] = False,
            use_test_dc: Optional[bool] = False,
            enable_storage_optimizer: Optional[bool] = True,
            wait_timeout: Optional[int] = 1,
            verbosity: Optional[int] = 1,
    ) -> None:
        super().__init__(api_id, api_hash, use_file_database, use_chat_info_database, use_message_database,
                         use_secret_chats, use_test_dc, enable_storage_optimizer, wait_timeout, verbosity)
        self.console_authentication = True
        self._authorization_state = None
        self._authorization_handler = None

        self.module = Module(r"C:\Users\sergi\PycharmProjects\TestGenerator\other\telegram\telegram_api\types.py",
                             r"C:\Users\sergi\PycharmProjects\TestGenerator\other\telegram\telegram_api\events.py")

    def send(self, data: dict):
        self.tdjson.send(data)

    def load_messages(self, chat: types.TgChat, max_count=100):
        if chat.first_message is None:
            self.send({'@type': 'getChatHistory', 'chat_id': chat.id, 'limit': max_count})
        else:
            self.send({'@type': 'getChatHistory', 'chat_id': chat.id, 'limit': max_count,
                       'from_message_id': chat.first_message.id})

    def download_file(self, file: types.TgFile):
        self.send({'@type': 'downloadFile', 'file_id': file.id, 'priority': 10})

    def set_update_handler(self, update_handler: Callable) -> None:
        super().set_update_handler(update_handler)

    def set_error_handler(self, error_handler: Callable) -> None:
        super().set_error_handler(error_handler)

    def set_routine_handler(self, routine_handler: Callable) -> None:
        super().set_error_handler(routine_handler)

    def set_authorization_handler(self, authorization_handler: Callable) -> None:
        self._authorization_handler = authorization_handler

    def authenticate_user(self, event_dict: dict):
        if self.console_authentication:
            super().authenticate_user(event_dict)
            return
        try:
            event = events.convert_event(event_dict, self)
        except Exception:
            return
        if isinstance(event, events.TgUpdateAuthorizationState):
            self._authorization_state = event.authorization_state
            if isinstance(self._authorization_state, types.TgAuthorizationStateWaitTdlibParameters):
                self.send_tdlib_parameters()
            elif isinstance(self._authorization_state, types.TgAuthorizationStateReady):
                self.get_all_chats()
                self.authorized = True
                self.logger.info("User authorized")
            elif self._authorization_state is not None:
                self._authorization_handler(self._authorization_state)

    def send_authentication(self, str1: str, str2: str):
        if isinstance(self._authorization_state, types.TgAuthorizationStateWaitPhoneNumber):
            self.send({"@type": "setAuthenticationPhoneNumber", "phone_number": str1})
        elif isinstance(self._authorization_state, types.TgAuthorizationStateWaitCode):
            self.send({"@type": "checkAuthenticationCode", "code": str1})
        elif isinstance(self._authorization_state, types.TgAuthorizationStateWaitRegistration):
            self.send({"@type": "registerUser", "first_name": str1, "last_name": str2})
        elif isinstance(self._authorization_state, types.TgAuthorizationStateWaitEmailAddress):
            self.send({"@type": "setAuthenticationEmailAddress", "email_address": str1})
        elif isinstance(self._authorization_state, types.TgAuthorizationStateWaitEmailCode):
            self.send({"@type": "checkAuthenticationEmailCode",
                       "code": {"@type": "emailAddressAuthenticationCode", "code": str1}})
        elif isinstance(self._authorization_state, types.TgAuthorizationStateWaitPassword):
            self.send({"@type": "checkAuthenticationPassword", "password": str1})

    def execute(self):
        # start the client by sending request to it
        self.get_authorization_state()

        # main events cycle
        while True:
            event_dict = self.tdjson.receive()
            if event_dict:
                self.module.feed_event(event_dict)
                if not self.authorized:
                    self.authenticate_user(event_dict)

                if hasattr(self, "update_handler"):
                    self.update_handler(event_dict)

                if event_dict["@type"] == "error":
                    self.error_handler(event_dict)

            if hasattr(self, "routine_handler"):
                self.routine_handler(event_dict)
