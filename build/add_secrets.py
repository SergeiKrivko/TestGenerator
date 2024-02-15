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


def write_secrets():
    with open("config/secret.py", 'w', encoding='utf-8') as f:
        for key in ['TELEGRAM_API_KEY', 'TELEGRAM_API_HASH', 'CONVERTIO_API_KEY']:
            f.write(f"{key} = {os.getenv(key)}\n")


def write_build_config():
    with open("config/build.py", 'w', encoding='utf-8') as f:
        for key in ['USE_WEB_ENGINE', 'USE_TELEGRAM']:
            f.write(f"{key} = {os.getenv(key, 'True').capitalize()}\n")


def fix_version():
    import config

    with open(r"build/setup.iss", encoding='utf-8') as f:
        text = f.read()

        index = text.index('#define MyAppVersion ') + len('#define MyAppVersion ')
        text = text[:index] + f'"{config.APP_VERSION}"' + text[index:][text[index:].index('\n'):]

    with open(r"build/setup.iss", 'w', encoding='utf-8') as f:
        f.write(text)


if sys.platform == 'win32':
    download_zip('lib_win.zip', r"venv\Lib\site-packages\pywtdlib\lib\Windows\AMD64")
    download_zip('libcairo_win.zip', r"venv\Lib\site-packages\cairocffi\dlls")

try:
    write_secrets()
except Exception as ex:
    print(ex.__class__.__name__)
write_build_config()

fix_version()
