import os
import shutil

from backend.commands import cmd_command
from language.utils import get_files


def c_compile(project, build, sm, coverage=False):
    if os.name == 'nt' and project.get("C_wsl", False):
        compiler = "wsl -e gcc"
    else:
        compiler = project.get('gcc', 'gcc')

    temp_dir = f"{sm.temp_dir()}/build"
    path = project.path()
    try:
        os.remove(f"{sm.temp_dir()}/{build.get('app_file')}")
    except FileNotFoundError:
        pass
    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    c_files = []
    h_dirs = set()
    print(build.get('name'), build.get('files', []))
    for key in build.get('files', []):
        if key.endswith('.c'):
            c_files.append(os.path.join(path, key))
        else:
            h_dirs.add(os.path.join(path, os.path.split(key)[0]))
    o_files = [f"{temp_dir}/{os.path.basename(el)[:-2]}.o" for el in c_files]

    h_dirs = '-I ' + ' -I '.join(h_dirs)
    errors = []
    code = True

    compiler_keys = build.get('keys', '')
    for c_file, o_file in zip(c_files, o_files):
        command = f"{compiler} {compiler_keys} {'--coverage' if coverage else ''} {h_dirs} -c -o {o_file} {c_file}"
        res = cmd_command(command, shell=True)
        if res.returncode:
            code = False
        errors.append(res.stderr)

    if code:
        command = f"{compiler} {compiler_keys} {'--coverage' if coverage else ''} -o {path}/{build.get('app_file')} " \
                  f"{' '.join(o_files)} {build.get('linker_keys', '')}"
        res = cmd_command(command, shell=True)
        if res.returncode:
            code = False
        errors.append(res.stderr)

    return code, ''.join(errors)


def c_run(project, build, args=''):
    # temp_dir = sm.temp_dir()
    if os.name == 'nt' and project.get("C_wsl", False):
        return f"wsl -e {project.path()}/{build.get('app_file')} {args}"
    return f"{os.path.join(project.path(), build.get('app_file'))} {args}"


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
        if os.name == 'nt' and sm.get("C_wsl", False):
            res = cm.cmd_command(f"wsl -e gcov {file} -o {temp_dir}", shell=True)
        else:
            res = cm.cmd_command(f"{sm.get('gcov', 'gcov')} {file} -o {temp_dir}", shell=True)

        for line in res.stdout.split('\n'):
            if "Lines executed:" in line:
                p, _, c = line.split(":")[1].split()
                total_count += int(c)
                count += round(float(p[:-1]) / 100 * int(c))
                break

    if total_count == 0:
        return 0
    return count / total_count * 100
