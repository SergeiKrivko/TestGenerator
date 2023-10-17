class _TimeMeasureException(Exception):
    def __init__(self, *args):
        self._message = '' if not args else args[0]

    def __str__(self):
        return self._message


class DatabaseError(_TimeMeasureException):
    pass
