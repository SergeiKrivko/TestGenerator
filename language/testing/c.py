import os

from backend.commands import cmd_command
from language.utils import get_files


def c_compile(project, build, sm):
    coverage = build.get('coverage', False)
    compiler = build.get('compiler')
    if compiler is None:
        compiler = project.get('gcc', 'gcc')

    path = project.path()
    temp_dir = f"{sm.temp_dir()}/build{build.id}"
    os.makedirs(temp_dir, exist_ok=True)

    c_files = []
    h_dirs = set()
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


def c_collect_coverage(sm, build):
    total_count = 0
    count = 0

    temp_dir = f"{sm.temp_dir()}/build{build.id}"

    for file in build.get('files', []):
        res = cmd_command(f"{sm.get('gcov', 'gcov')} {file} -o {temp_dir}", shell=True, cwd=temp_dir)

        for line in res.stdout.split('\n'):
            if "Lines executed:" in line:
                p, _, c = line.split(":")[1].split()
                total_count += int(c)
                count += round(float(p[:-1]) / 100 * int(c))
                break

    if total_count == 0:
        return 0
    return count / total_count * 100
