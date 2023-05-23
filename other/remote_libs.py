import requests
from urllib.parse import quote
from PyQt5.QtCore import QThread, pyqtSignal


def get_files_list():
    resp = requests.get('https://testgenerator-bf37c-default-rtdb.europe-west1.firebasedatabase.app/libs_list.json')
    if resp.status_code == 200:
        return resp.json()
    return []


def download_file(name):
    url = f"https://firebasestorage.googleapis.com/v0/b/testgenerator-bf37c.appspot.com/o/" \
          f"{quote(f'lib/{name}', safe='')}?alt=media"
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        return b''.join(resp).decode('utf-8')
    else:
        return ''
    

class ListReader(QThread):
    complete = pyqtSignal(list)
    error = pyqtSignal(Exception)
    
    def run(self) -> None:
        try:
            lst = get_files_list()
            self.complete.emit(lst)
        except Exception:
            pass


class FileReader(QThread):
    complete = pyqtSignal(str)
    error = pyqtSignal(Exception)
    
    def __init__(self, file_name):
        super(FileReader, self).__init__()
        self.file_name = file_name

    def run(self) -> None:
        try:
            res = download_file(self.file_name)
            self.complete.emit(res)
        except Exception as ex:
            self.error.emit(ex)
