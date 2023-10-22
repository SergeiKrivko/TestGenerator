import json
import os
import subprocess


def get_si():
    if os.name == 'nt':
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return si
    else:
        return None


def cmd_command(args, **kwargs):
    if 'encoding' not in kwargs:
        kwargs['encoding'] = 'utf-8'
    return subprocess.run(args, capture_output=True, text=True, startupinfo=get_si(), **kwargs)


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


def wsl_path(path: str, build):
    if not build.get('wsl'):
        return path
    path = path.replace('\\', '/')
    if len(path) <= 2:
        return path
    if path[1] == ':':
        path = f"/mnt/{path[0].lower()}{path[2:]}"
    return path
