import json
import struct
import time
from typing import Literal

from src.side_tabs.chat import database
from src.side_tabs.chat.message import GPTMessage


class GPTChat:
    SIMPLE = 0
    TRANSLATE = 1
    SUMMARY = 2

    def __init__(self, db: database.Database, chat_id: int):
        self._id = chat_id
        self._db = db

        self._first_message = None

    @property
    def id(self):
        return self._id

    @property
    def message_ids(self):
        self._db.cursor.execute(f'SELECT id FROM Messages{self.id} WHERE deleted = 0')
        chats = self._db.cursor.fetchall()
        for el in chats:
            yield el[0]

    @property
    def messages(self):
        for el in self.message_ids:
            yield GPTMessage(self._db, self.id, el)

    def load_messages(self, limit=10, to_message=None):
        if to_message is not None:
            self._db.cursor.execute(f"""SELECT id FROM Messages{self.id} WHERE deleted = 0 AND 
            id < {self._first_message} AND id >= {to_message} ORDER BY id DESC""")
            chats = self._db.cursor.fetchall()
        elif self._first_message is None:
            self._db.cursor.execute(f'SELECT id FROM Messages{self.id} WHERE deleted = 0 ORDER BY id DESC')
            chats = self._db.cursor.fetchmany(limit)
        else:
            self._db.cursor.execute(
                f'SELECT id FROM Messages{self.id} WHERE deleted = 0 AND id < {self._first_message} ORDER BY id DESC')
            chats = self._db.cursor.fetchmany(limit)
        for el in chats:
            self._first_message = el[0]
            yield GPTMessage(self._db, self.id, el[0])

    def drop_messages(self, from_message):
        self._db.cursor.execute(
            f'SELECT id FROM Messages{self.id} WHERE deleted = 0 AND id < {from_message} AND '
            f'id >= {self._first_message} ORDER BY id')
        chats = self._db.cursor.fetchall()
        for el in chats:
            yield GPTMessage(self._db, self.id, el[0])
        self._first_message = from_message

    def get_message(self, message_id):
        return GPTMessage(self._db, self.id, message_id)

    @property
    def type(self):
        self._db.cursor.execute(f"""SELECT type from Chats WHERE id = {self._id}""")
        type = self._db.cursor.fetchone()[0]
        return type

    @type.setter
    def type(self, type):
        self._db.cursor.execute(f"""UPDATE Chats SET type = ? WHERE id = {self._id}""", (type,))

    @property
    def type_data(self):
        self._db.cursor.execute(f"""SELECT type_data from Chats WHERE id = {self._id}""")
        try:
            type_data = json.loads(self._db.cursor.fetchone()[0])
        except json.JSONDecodeError:
            type_data = dict()
        except TypeError:
            type_data = dict()
        return type_data

    @type_data.setter
    def type_data(self, type_data):
        self._db.cursor.execute(f"""UPDATE Chats SET type_data = ? WHERE id = {self._id}""", (json.dumps(type_data),))

    @property
    def name(self):
        self._db.cursor.execute(f"""SELECT chat_name from Chats WHERE id = {self._id}""")
        name = self._db.cursor.fetchone()[0]
        return name

    @name.setter
    def name(self, name):
        self._db.cursor.execute(f"""UPDATE Chats SET chat_name = ? WHERE id = {self._id}""", (name,))

    @property
    def ctime(self):
        self._db.cursor.execute(f"""SELECT ctime from Chats WHERE id = {self._id}""")
        ctime = self._db.cursor.fetchone()[0]
        return ctime

    @ctime.setter
    def ctime(self, ctime):
        self._db.cursor.execute(f"""UPDATE Chats SET ctime = ? WHERE id = {self._id}""", (ctime,))

    @property
    def utime(self):
        self._db.cursor.execute(f"""SELECT utime from Chats WHERE id = {self._id}""")
        utime = self._db.cursor.fetchone()[0]
        return utime

    @utime.setter
    def utime(self, utime):
        self._db.cursor.execute(f"""UPDATE Chats SET utime = ? WHERE id = {self._id}""", (utime,))

    @property
    def pinned(self):
        self._db.cursor.execute(f"""SELECT pinned from Chats WHERE id = {self._id}""")
        pinned = bool(self._db.cursor.fetchone()[0])
        return pinned

    @pinned.setter
    def pinned(self, pinned):
        self._db.cursor.execute(f"""UPDATE Chats SET pinned = {1 if pinned else 0} WHERE id = {self._id}""")

    @property
    def used_messages(self):
        self._db.cursor.execute(f"""SELECT used_messages from Chats WHERE id = {self._id}""")
        used_messages = self._db.cursor.fetchone()[0]
        return used_messages

    @used_messages.setter
    def used_messages(self, used_messages):
        self._db.cursor.execute(f"""UPDATE Chats SET used_messages = {used_messages} WHERE id = {self._id}""")

    @property
    def saved_messages(self):
        self._db.cursor.execute(f"""SELECT saved_messages from Chats WHERE id = {self._id}""")
        saved_messages = self._db.cursor.fetchone()[0]
        return saved_messages

    @saved_messages.setter
    def saved_messages(self, saved_messages):
        self._db.cursor.execute(f"""UPDATE Chats SET saved_messages = {saved_messages} WHERE id = {self._id}""")

    @property
    def temperature(self):
        self._db.cursor.execute(f"""SELECT temperature from Chats WHERE id = {self._id}""")
        temperature = self._db.cursor.fetchone()[0]
        return temperature

    @temperature.setter
    def temperature(self, temperature):
        self._db.cursor.execute(f"""UPDATE Chats SET temperature = {float(temperature)} WHERE id = {self._id}""")

    @property
    def model(self):
        self._db.cursor.execute(f"""SELECT model from Chats WHERE id = {self._id}""")
        model = self._db.cursor.fetchone()[0]
        return model

    @model.setter
    def model(self, model):
        self._db.cursor.execute(f"""UPDATE Chats SET model = ? WHERE id = {self._id}""", (model,))

    def add_message(self, role: Literal['user', 'assistant', 'system'], content="", reply=tuple()):
        t = time.time()
        self._db.cursor.execute(f"""INSERT INTO Messages{self._id} (
                role, content, replys, replied_count, deleted, ctime) 
                VALUES (?, ?, ?, 0, 0, {t})""", (role, content, struct.pack(f'{len(reply)}q', *reply)))
        message_id = self._db.cursor.lastrowid
        self.utime = t

        self._db.commit()
        return GPTMessage(self._db, self.id, message_id)

    def delete_message(self, message_id):
        message = GPTMessage(self._db, self.id, message_id)
        for el in message.replys:
            el.replied_count -= 1
        message.deleted = True
        self._db.commit()

    def get_sort_key(self):
        res = self.utime
        if res <= 0:
            res = self.ctime
        if self.pinned:
            res += 10000000000
        return res

    @property
    def last_message(self):
        self._db.cursor.execute(f"""SELECT MAX(id) FROM Messages{self.id}""")
        message_id = self._db.cursor.fetchone()[0]
        if message_id is None:
            return None
        return GPTMessage(self._db, self.id, message_id)

    def messages_to_prompt(self, reply: list[int] = tuple()):
        messages = list(self.message_ids)
        ind = min(len(messages), self.used_messages)
        ids = messages[-ind:]
        for el in reversed(reply):
            if el not in ids:
                ids.insert(0, el)

        return self.system_prompts() + [GPTMessage(self._db, self.id, message_id).to_json() for message_id in ids]

    def delete(self):
        self._db.cursor.execute(f"""DELETE FROM Chats WHERE id = {self._id}""")
        self._db.cursor.execute(f"""DROP TABLE IF EXISTS Messages{self._id}""")
        self._db.commit()

    def system_prompts(self):
        match self.type:
            case GPTChat.SIMPLE:
                return []
            case GPTChat.TRANSLATE:
                return [{'role': 'system', 'content': f"You translate messages from {self.type_data['language1']} to "
                                                      f"{self.type_data['language2']} or vice versa. ONLY TRANSLATE!"}]
            case GPTChat.SUMMARY:
                return [{'role': 'system', 'content': "You compose a summary of the messages sent to you using"
                                                      " russian language"}]
