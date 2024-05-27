import json
import os.path
import sys
import zipfile
from urllib.parse import quote

import requests

from src import config

token = ""
headers = dict()


def auth():
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    r = requests.post(rest_api_url,
                      params={"key": config.FIREBASE_API_KEY},
                      json={"email": os.getenv("ADMIN_EMAIL"),
                            "password": os.getenv("ADMIN_PASSWORD"),
                            "returnSecureToken": True})
    if not r.ok:
        raise Exception("Can not authorize")
    res = r.json()
    global token
    token = res['idToken']
    headers['Authorization'] = 'Bearer ' + token


def upload_file(path, name=''):
    if name and '.' not in name:
        name += '.' + path.split('.')[-1]
    url = f"https://firebasestorage.googleapis.com/v0/b/testgenerator-bf37c.appspot.com/o/" \
          f"{quote(f'releases/{name or os.path.basename(path)}', safe='')}"
    with open(path, 'br') as f:
        resp = requests.post(url, data=f.read(), headers=headers)
        if not resp.ok:
            raise Exception(resp.text)


def download_file(name):
    url = f"https://firebasestorage.googleapis.com/v0/b/testgenerator-bf37c.appspot.com/o/" \
          f"{quote(f'releases/{name}', safe='')}?alt=media"
    resp = requests.get(url, stream=True, headers=headers)
    if resp.ok:
        return b''.join(resp).decode('utf-8')
    else:
        return ''


def get_system():
    match sys.platform:
        case 'win32':
            return 'windows'
        case 'linux':
            return 'linux'
        case 'darwin':
            return 'macos'


def get_arch():
    return os.getenv('ARCHITECTURE')


def release_file():
    match sys.platform:
        case 'win32':
            return r"dist\TestGeneratorSetup.exe"
        case 'linux':
            return f"testgenerator_{config.APP_VERSION}_amd64.deb"
        case 'darwin':
            return f"TestGenerator.dmg"


def version_file():
    return f"{get_system()}-{get_arch()}.json"


def upload_version(name=None):
    url = f"https://firebasestorage.googleapis.com/v0/b/testgenerator-bf37c.appspot.com/o/" \
          f"{quote(f'releases/{name or version_file()}', safe='')}"
    resp = requests.post(url, data=json.dumps({
        'version': config.APP_VERSION,
        'size': os.path.getsize(release_file()),
    }, indent=2).encode('utf-8'), headers=headers)
    if not resp.ok:
        raise Exception(resp.text)


def compress_to_zip(path):
    archive = zipfile.ZipFile(path + '.zip', 'w')
    archive.write(path, os.path.basename(path))
    archive.close()
    return path + '.zip'


def main():
    auth()
    upload_file(compress_to_zip(release_file()), f"{get_system()}-{get_arch()}.zip")
    upload_version()


if __name__ == '__main__':
    main()
