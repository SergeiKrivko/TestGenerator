class HistoryManager:
    def __init__(self):
        self._undo: list[_HistoryRecord] = []
        self._redo: list[_HistoryRecord] = []

    def add_record(self, record_type, data=None):
        self._redo.clear()
        record = _HistoryRecord(record_type, data)
        self._undo.append(record)
        return record

    def _add_redo_record(self, record: '_HistoryRecord'):
        self._redo.append(record)

    def _add_undo_record(self, record: '_HistoryRecord'):
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


class _HistoryRecord:
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


class _EmptyRecord(_HistoryRecord):
    def __init__(self):
        super().__init__('')

    def add_data(self, data):
        pass


EMPTY_RECORD = _EmptyRecord()
