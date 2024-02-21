import json
import os.path
import sys
import zipfile
from urllib.parse import quote

import requests

from src import config


match os.getenv('BUILD_TYPE'):
    case 'Lite':
        build_suffix = '-lite'
    case _:
        build_suffix = ''


def upload_file(path, name=''):
    if name and '.' not in name:
        name += '.' + path.split('.')[-1]
    url = f"https://firebasestorage.googleapis.com/v0/b/testgenerator-bf37c.appspot.com/o/" \
          f"{quote(f'releases/{name or os.path.basename(path)}', safe='')}"
    with open(path, 'br') as f:
        resp = requests.post(url, data=f.read())
        if not resp.ok:
            raise Exception(resp.text)


def download_file(name):
    url = f"https://firebasestorage.googleapis.com/v0/b/testgenerator-bf37c.appspot.com/o/" \
          f"{quote(f'releases/{name}', safe='')}?alt=media"
    resp = requests.get(url, stream=True)
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


def release_file():
    match sys.platform:
        case 'win32':
            return r"dist\TestGeneratorSetup.exe"
        case 'linux':
            return f"testgenerator_{config.APP_VERSION}_amd64.deb"
        case 'darwin':
            return "TestGenerator.dmg"


def version_file():
    return f"{get_system()}{build_suffix}.json"


def upload_info(zip_file):
    url = f"https://firebasestorage.googleapis.com/v0/b/testgenerator-bf37c.appspot.com/o/" \
          f"{quote(f'releases/{version_file()}', safe='')}"
    resp = requests.post(url, data=json.dumps({
        'version': config.APP_VERSION,
        'file_size': os.path.getsize(zip_file),
    }, indent=2).encode('utf-8'))
    if not resp.ok:
        raise Exception(resp.text)


def compress_to_zip(path):
    zip_path = f"{os.path.dirname(path) or '.'}/{get_system()}{build_suffix}.zip"
    archive = zipfile.ZipFile(zip_path, 'w')
    archive.write(path, os.path.basename(path))
    archive.close()
    return zip_path


def main():
    zip_file = compress_to_zip(release_file())
    upload_file(zip_file, f"{get_system()}{build_suffix}")
    upload_info(zip_file)


if __name__ == '__main__':
    main()
