import requests
from urllib.parse import quote
from PyQt5.QtCore import QThread, pyqtSignal


def get_files_list():
    resp = requests.get('https://testgenerator-bf37c-default-rtdb.europe-west1.firebasedatabase.app/libs_list.json')
    if resp.status_code == 200:
        return resp.json()
    return []


def download_file(name, save_as='temp'):
    url = f"https://firebasestorage.googleapis.com/v0/b/testgenerator-bf37c.appspot.com/o/" \
          f"{quote(f'lib/{name}', safe='')}?alt=media"
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        with open(save_as, 'wb') as f:
            for chunk in resp:
                f.write(chunk)
    

class ListReader(QThread):
    complete = pyqtSignal(list)
    
    def run(self) -> None:
        lst = get_files_list()
        self.complete.emit(lst)


class FileReader(QThread):
    complete = pyqtSignal()
    
    def __init__(self, file_name, save_as='temp'):
        super(FileReader, self).__init__()
        self.file_name = file_name
        self.save_as = save_as

    def run(self) -> None:
        download_file(self.file_name, self.save_as)
        self.complete.emit()
