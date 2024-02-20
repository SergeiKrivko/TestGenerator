import os
import sqlite3
from time import time

from src.backend.commands import read_json
from src.side_tabs.chat import chat
from src.backend.settings_manager import SettingsManager


class Database:
    def __init__(self, sm: SettingsManager):
        self._sm = sm
        os.makedirs(self._sm.app_data_dir, exist_ok=True)
        need_loading = not os.path.isfile(f"{self._sm.app_data_dir}/database.db") and \
                       os.path.isdir(f"{self._sm.app_data_dir}/dialogs")
        self._connection = sqlite3.connect(f"{self._sm.app_data_dir}/database.db")
        # self._connection = sqlite3.connect("database.db")

        self.cursor = self._connection.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Chats (
        id INTEGER PRIMARY KEY,
        type INTEGER NOT NULL,
        type_data TEXT,
        chat_name TEXT,
        ctime REAL NOT NULL,
        utime REAL NOT NULL,
        pinned INTEGER NOT NULL,
        used_messages INTEGER NOT NULL,
        saved_messages INTEGER NOT NULL,
        temperature REAL NOT NULL,
        model TEXT NOT NULL,
        scrolling_pos INTEGER
        )''')

        for chat_id in self.chat_ids:
            self._create_chat_table(chat_id)

        if need_loading:
            for file in os.listdir(f"{self._sm.app_data_dir}/dialogs"):
                self.from_json_file(os.path.join(f"{self._sm.app_data_dir}/dialogs", file))

        self._connection.commit()

    def _create_chat_table(self, chat_id):
        self.cursor.execute(f'''
                            CREATE TABLE IF NOT EXISTS Messages{chat_id} (
                            id INTEGER PRIMARY KEY,
                            role TEXT,
                            content TEXT,
                            replys BLOB,
                            replied_count INTEGER,
                            deleted INTEGER NOT NULL,
                            ctime REAL
                            )''')

    @property
    def chat_ids(self):
        self.cursor.execute('SELECT id FROM Chats')
        chats = self.cursor.fetchall()
        for el in chats:
            yield el[0]

    @property
    def chats(self):
        for el in self.chat_ids:
            yield chat.GPTChat(self, el)

    def add_chat(self):
        self.cursor.execute(f"""INSERT INTO Chats (
        type, ctime, utime, pinned, used_messages, saved_messages, temperature, model, scrolling_pos) 
        VALUES ({chat.GPTChat.SIMPLE}, {time()}, {time()}, 0, 1, 1000, 0.5, "default", 0)""")
        chat_id = self.cursor.lastrowid
        self._create_chat_table(chat_id)
        self._connection.commit()
        return chat.GPTChat(self, chat_id)

    def from_json_file(self, path):
        data = read_json(path)
        new_chat = self.add_chat()

        new_chat.name = data.get('name')
        new_chat.type = data.get('type')
        new_chat.type_data = data.get('data')
        new_chat.model = data.get('model', 'default')
        new_chat.ctime = data.get('time')
        new_chat.utime = data.get('utime')
        new_chat.pinned = data.get('pinned', False)
        new_chat.used_messages = data.get('used_messages')
        new_chat.saved_messages = data.get('saved_messages')
        new_chat.temperature = data.get('temperature')
        for message in data.get('messages'):
            new_chat.add_message(message['role'], message['content'])

    def commit(self):
        self._connection.commit()

    def __del__(self):
        self._connection.commit()
        self._connection.close()


if __name__ == '__main__':
    db = Database(None)
    # db.add_chat()
    # db.add_chat()
    for el in db.chats:
        print(list(el.messages))
        # if el.id == 2:
        #     el.delete_message(3)
            # el.add_message('user')
            # el.add_message('assistant')
