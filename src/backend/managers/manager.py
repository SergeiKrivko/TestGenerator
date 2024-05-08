from PyQt6.QtCore import QObject


class AbstractManager(QObject):
    def __init__(self, bm):
        super().__init__()
        self._bm = bm

    async def load(self):
        pass

    async def close(self):
        pass

    async def indexing(self):
        pass
