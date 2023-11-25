import encodings
import json
import os
import pathlib
import subprocess
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.environ["PYMORPHY2_DICT_PATH"] = str(pathlib.Path(sys._MEIPASS).joinpath('pymorphy3_dicts_ru/data'))
import pymorphy3


def get_si():
    if os.name == 'nt':
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return si
    else:
        return None


ENCODINGS = ['utf-8', 'utf-16', 'ansi', 'ascii', 'charmap']


def cmd_command(args, **kwargs):
    if isinstance(text := kwargs.get('input', b''), str):
        kwargs['input'] = text.encode(kwargs.get('encoding', 'utf-8'))
    res = subprocess.run(args, capture_output=True, startupinfo=get_si(), **kwargs)
    for encoding in ENCODINGS:
        try:
            res.stdout = res.stdout.decode(encoding)
            break
        except UnicodeDecodeError:
            pass
    else:
        raise UnicodeDecodeError
    for encoding in ENCODINGS:
        try:
            res.stderr = res.stderr.decode(encoding)
            break
        except UnicodeDecodeError:
            pass
    else:
        raise UnicodeDecodeError
    return res


def cmd_command_pipe(command, stdout=True, stderr=False, **kwargs):
    try:
        proc = subprocess.Popen(command, startupinfo=get_si(), text=True,
                                stdout=subprocess.PIPE if stdout else None,
                                stderr=subprocess.STDOUT if stderr and stdout else None,
                                **kwargs)
        for line in iter(proc.stdout.readline, ''):
            yield line
    except Exception as ex:
        raise subprocess.CalledProcessError(1, f"{ex.__class__.__name__}: {ex}")

    proc.stdout.close()
    exit_code = proc.poll()
    if exit_code:
        raise subprocess.CalledProcessError(exit_code, command)


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
        res = json.loads(read_file(path, ''))
        if not isinstance(res, expected_type):
            res = expected_type()
    except json.JSONDecodeError:
        res = expected_type()
    return res


def write_file(path: str, text: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def get_sorted_jsons(path: str):
    if not os.path.isdir(path):
        return []
    lst = list(filter(lambda s: s.rstrip('.json').isdigit(), os.listdir(path)))
    lst.sort(key=lambda el: int(el.rstrip('.json')))
    return lst


def wsl_path(path: str, build=None):
    if build and not build.get('wsl'):
        return path
    path = path.replace('\\', '/')
    if len(path) <= 2:
        return path
    if path[1] == ':':
        path = f"/mnt/{path[0].lower()}{path[2:]}"
    return path


morph = pymorphy3.MorphAnalyzer()


def inflect(text: str, case='nomn'):
    res = []
    for word in text.split(' '):
        upper, capitalize = False, False
        if word.upper() == word:
            upper = True
        elif word.lower() != word:
            capitalize = True
        if not word:
            res.append(word)
        else:
            try:
                p = morph.parse(word)[0]
                if p.inflect({'nomn'}).word == word.lower():
                    new_word = p.inflect({case}).word
                    if upper:
                        new_word = new_word.upper()
                    elif capitalize:
                        new_word = new_word.capitalize()
                    res.append(new_word)
                else:
                    res.append(word)
            except AttributeError:
                res.append(word)
    return ' '.join(res)


def check_files_mtime(file, dependencies):
    for el in dependencies:
        if os.path.getmtime(el) > os.path.getmtime(file):
            return False
    return True
