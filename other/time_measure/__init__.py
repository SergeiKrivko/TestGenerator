from types import FunctionType

from backend.commands import read_json
from other.time_measure.fields import *
from other.time_measure.errors import *


class TimeMeasure:
    def __init__(self,
                 programs: list[str],
                 generator: FunctionType,
                 x_field: Field,
                 fields: list[Field],
                 database='TimeMeasureBase.json',
                 ):
        self.programs = programs
        self.generator = generator
        self.x_field = x_field
        self.fields = fields
        self.database = database

        self._data = dict()

    def load_data(self):
        self._data = read_json(self.database)
        if self._data.get('file') != 'TimeMeasure':
            raise DatabaseError('This file is not a database')
