class Field:
    TYPE_STR = 0
    TYPE_INT = 1
    TYPE_FLOAT = 2
    TYPE_INT_RANGE = 3
    TYPE_FLOAT_RANGE = 4

    def __init__(self, field_type):
        self.type = field_type

    def str(self, value):
        return ''


class FieldStr(Field):
    def __init__(self, values: list[str]):
        super().__init__(Field.TYPE_STR)
        self._values = values

    def __getitem__(self, item):
        return self._values[item]

    def __iter__(self):
        for el in self._values:
            yield el

    def str(self, value):
        return value


class FieldInt(Field):
    def __init__(self, name, values: list[int]):
        super().__init__(Field.TYPE_INT)
        self.name = name
        self._values = values

    def __getitem__(self, item):
        return self._values[item]

    def __iter__(self):
        for el in self._values:
            yield el

    def str(self, value):
        return f"{self.name} = {value}"


class FieldFloat(Field):
    def __init__(self, name, values: list[float]):
        super().__init__(Field.TYPE_INT)
        self.name = name
        self._values = values

    def __getitem__(self, item):
        return self._values[item]

    def __iter__(self):
        for el in self._values:
            yield el

    def str(self, value):
        return f"{self.name} = {value}"


class FieldIntRange(Field):
    def __init__(self, name, start: int, stop: int, step: int):
        super().__init__(Field.TYPE_INT)
        self.name = name
        self._start = start
        self._stop = stop
        self._step = step

    def __getitem__(self, item):
        return self._start + self._step * item

    def __iter__(self):
        return range(self._start, self._stop, self._step)

    def str(self, value):
        return f"{self.name} = {value}"


class FieldFloatRange(Field):
    def __init__(self, name, start: int, stop: int, step: int):
        super().__init__(Field.TYPE_INT)
        self.name = name
        self._start = start
        self._stop = stop
        self._step = step

    def __getitem__(self, item):
        return self._start + self._step * item

    def __iter__(self):
        item = self._start
        while item < self._stop + self._step / 2:
            yield item
            item += self._step

    def str(self, value):
        return f"{self.name} = {value}"
