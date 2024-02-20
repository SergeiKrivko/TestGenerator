from src.backend.backend_types.unit_tests_suite import UnitTestsSuite


class UnitTestsModule:
    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self._suits = []

    def name(self):
        return self._name

    def suits(self):
        for el in self._suits:
            yield el

    def add_suite(self, suite: UnitTestsSuite):
        self._suits.append(suite)

    def insert_suite(self, suite: UnitTestsSuite, index: int):
        self._suits.insert(index, suite)

    def delete_suite(self, index):
        self._suits.pop(index)

    def has_suits(self):
        return bool(len(self._suits))
