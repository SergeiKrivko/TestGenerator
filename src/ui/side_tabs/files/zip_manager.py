import os.path
from zipfile import ZipFile, ZIP_DEFLATED


class ZipManager:
    def __init__(self):
        pass

    @staticmethod
    def compress(path, files: list[str]):
        f = ZipFile(path, mode='w', compression=ZIP_DEFLATED)
        for el in files:
            f.write(el, os.path.relpath(el, os.path.split(path)[0]))
        f.close()

    @staticmethod
    def extract(path, *args):
        f = ZipFile(path, 'r')
        f.extractall(os.path.split(path)[0])
