import os
import shutil

from language.build.make_command import MakeCommand
from language.utils import get_files


def c_compile(path, cm, sm, data, coverage=False):
    if os.name == 'nt' and sm.get_smart("C_wsl", False):
        compiler = "wsl -e gcc"
    else:
        compiler = sm.get_smart('gcc', 'gcc')

    temp_dir = f"{sm.temp_dir()}/build"
    try:
        os.remove(f"{sm.temp_dir()}/app.exe")
    except FileNotFoundError:
        pass
    os.makedirs(temp_dir, exist_ok=True)

    c_files = []
    h_dirs = set()
    for key in data['files']:
        if key.endswith('.c'):
            c_files.append(os.path.join(path, key))
        else:
            h_dirs.add(os.path.join(path, os.path.split(key)[0]))
    o_files = [f"{temp_dir}/{os.path.basename(el)[:-2]}.o" for el in c_files]

    h_dirs = '-I ' + ' -I '.join(h_dirs)
    errors = []
    code = True

    compiler_keys = data.get('keys', '')
    for c_file, o_file in zip(c_files, o_files):
        command = f"{compiler} {compiler_keys} {'--coverage' if coverage else ''} {h_dirs} -c -o {o_file} {c_file}"
        res = cm.cmd_command(command)
        if res.returncode:
            code = False
        errors.append(res.stderr)

    if code:
        command = f"{compiler} {compiler_keys} {'--coverage' if coverage else ''} -o {path}/app.exe " \
                  f"{' '.join(o_files)} {data.get('linker_keys', '')}"
        res = cm.cmd_command(command)
        if res.returncode:
            code = False
        errors.append(res.stderr)

    shutil.rmtree(temp_dir)
    return code, ''.join(errors)


def c_run(path, sm, args='', coverage=False):
    # temp_dir = sm.temp_dir()
    if os.name == 'nt' and sm.get_smart("C_wsl", False):
        return f"wsl -e {path}/app.exe {args}"
    return f"{os.path.join(path, 'app.exe')} {args}"


def c_clear_coverage_files(path):
    if not os.path.isdir(path):
        return
    for file in get_files(path, '.gcda'):
        os.remove(file)
    for file in get_files(path, '.gcno'):
        os.remove(file)
    for file in get_files(path, 'temp.txt'):
        os.remove(file)
    for file in get_files(path, '.gcov'):
        os.remove(file)


def c_collect_coverage(path, sm, cm):
    total_count = 0
    count = 0

    temp_dir = f"{sm.temp_dir()}/build"

    for file in get_files(path, '.c'):
        if os.name == 'nt' and sm.get_smart("C_wsl", False):
            res = cm.cmd_command(f"wsl -e gcov {file} -o {temp_dir}", shell=True)
        else:
            res = cm.cmd_command(f"{sm.get_smart('gcov', 'gcov')} {file} -o {temp_dir}", shell=True)

        for line in res.stdout.split('\n'):
            if "Lines executed:" in line:
                p, _, c = line.split(":")[1].split()
                total_count += int(c)
                count += round(float(p[:-1]) / 100 * int(c))
                break

    if total_count == 0:
        return 0
    return count / total_count * 100


def convert_make(sm, data: dict):
    c_files = []
    h_dirs = set()
    for key in data['files']:
        if key.endswith('.c'):
            c_files.append(key)
        else:
            h_dirs.add(os.path.split(key)[0])
    o_files = [f"{sm.get('temp_files_dir', '')}/{os.path.basename(el)[:-2]}.o" for el in c_files]

    if os.name == 'nt' and sm.get_smart("C_wsl", False):
        compiler = "wsl -e gcc"
    else:
        compiler = sm.get_smart('gcc', 'gcc')
    compiler_keys = sm.get_smart('c_compiler_keys', '')

    res = [MakeCommand(data['name'], o_files, f"{compiler} --coverage -g {' '.join(o_files)} -o {data['name']} "
                                              f"{data['keys']}")]
    for c_file, o_file in zip(c_files, o_files):
        res.append(MakeCommand(
            o_file, c_file, f"{compiler} {compiler_keys} {' '.join(map(lambda s: '-I ' + s, h_dirs))} "
                            f"--coverage -g -c {c_file} -o {o_file}"))
    return res
