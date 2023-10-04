import json
import os
import subprocess


def cmd_command(args, **kwargs):
    if os.name == 'nt':
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return subprocess.run(args, capture_output=True, text=True, startupinfo=si, **kwargs)
    else:
        return subprocess.run(args, capture_output=True, text=True, **kwargs)


def read_file(path, default=None) -> str:
    try:
        file = open(path, encoding='utf-8')
        res = file.read()
        file.close()
        return res
    except Exception as ex:
        if default is not None:
            return default
        raise ex


def read_binary(path, default=None) -> bytes:
    try:
        file = open(path, 'br', encoding='utf-8')
        res = file.read()
        file.close()
        return res
    except Exception as ex:
        if default is not None:
            return default
        raise ex


def read_json(path: str, expected_type: type = dict):
    try:
        res = json.loads(read_file(path))
        if not isinstance(res, expected_type):
            res = expected_type()
    except json.JSONDecodeError:
        res = expected_type()
    return res


def write_file(path: str, text: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def get_sorted_jsons(path: str):
    lst = list(filter(lambda s: s.rstrip('.json').isdigit(), os.listdir(path)))
    lst.sort(key=lambda el: int(el.rstrip('.json')))
    return lst
