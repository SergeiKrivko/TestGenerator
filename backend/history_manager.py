class HistoryManager:
    def __init__(self):
        self._undo: list[HistoryRecord] = []
        self._redo: list[HistoryRecord] = []

    def add_record(self, record_type, data=None):
        self._redo.clear()
        record = HistoryRecord(record_type, data)
        self._undo.append(record)
        return record

    def _add_redo_record(self, record: 'HistoryRecord'):
        self._redo.append(record)

    def _add_undo_record(self, record: 'HistoryRecord'):
        self._undo.append(record)

    def get_undo(self):
        if not self._undo:
            return None
        record = self._undo[-1]
        self._undo.pop()
        self._add_redo_record(record)
        return record

    def get_redo(self):
        if not self._redo:
            return None
        record = self._redo[-1]
        self._redo.pop()
        self._add_undo_record(record)
        return record

    def clear(self):
        self._undo.clear()
        self._redo.clear()


class HistoryRecord:
    def __init__(self, action_type: str, data=None):
        self.type = action_type
        self.data = []
        if data:
            self.data.append(data)

    def add_data(self, data):
        self.data.insert(0, data)

    def __iter__(self):
        return iter(self.data)

    def clear(self):
        self.data.clear()
