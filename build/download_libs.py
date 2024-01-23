import os
import shutil
import sys

import requests
from urllib.parse import quote
import zipfile


def download_zip(name: str, dst: str = None):
    url = f"https://firebasestorage.googleapis.com/v0/b/testgenerator-bf37c.appspot.com/o/" \
              f"{quote(f'telegram_lib/{name}', safe='')}?alt=media"
    resp = requests.get(url)
    if not resp.ok:
        raise Exception(resp.text)
    with open(name, 'wb') as f:
        f.write(resp.content)

    if dst is None:
        dst = name[:-4]
    if os.path.isdir(dst):
        shutil.rmtree(dst)

    zip_file = zipfile.ZipFile(name, 'r')
    zip_file.extractall(dst)
    zip_file.close()
    os.remove(name)


if sys.platform == 'win32':
    download_zip('lib_win.zip', r"..\venv\Lib\site-packages\pywtdlib\lib\Windows\AMD64")
    download_zip('libcairo_win.zip', r"..\venv\Lib\site-packages\cairocffi\dlls")
