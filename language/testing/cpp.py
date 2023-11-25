import os

from backend.backend_types.program import PROGRAMS
from backend.commands import cmd_command, check_files_mtime
from language.utils import get_files


def cpp_compile(project, build, sm):
    coverage = build.get('coverage', False)
    compiler = PROGRAMS['g++'].get(sm, build)

    path = compiler.convert_path(project.path())
    temp_dir = compiler.convert_path(f"{sm.temp_dir()}/build{build.id}")
    os.makedirs(f"{sm.temp_dir()}/build{build.id}", exist_ok=True)

    c_files = []
    h_dirs = set()
    for key in build.get('files', []):
        if key.endswith('.cpp'):
            c_files.append(f"{path}/{key}")
        else:
            h_dirs.add(f"{path}/{os.path.split(key)[0]}")
    o_files = [f"{temp_dir}/{os.path.basename(el)[:-2]}.o" for el in c_files]

    h_dirs = '-I ' + ' -I '.join(h_dirs) if h_dirs else ''
    errors = []
    code = True

    def get_dependencies(file):
        lst = compiler(f"{h_dirs} -MM {file}").stdout.split()
        lst.pop(0)
        i = 0
        while i < len(lst):
            if lst[i] == '\\':
                lst.pop(i)
            else:
                i += 1
        return lst

    compiler_keys = build.get('keys', '')
    for c_file, o_file in zip(c_files, o_files):
        if os.path.isfile(o_file) and check_files_mtime(o_file, get_dependencies(c_file)):
            continue
        res = compiler(f"{compiler_keys} {'--coverage' if coverage else ''} {h_dirs} -c -o {o_file} {c_file}")
        if res.returncode:
            code = False
        errors.append(res.stderr)

    if code:
        res = compiler(f"{compiler_keys} {'--coverage' if coverage else ''} -o {path}/{build.get('app_file')} "
                       f"{' '.join(o_files)} {build.get('linker_keys', '')}")
        if res.returncode:
            code = False
        errors.append(res.stderr)

    return code, ''.join(map(str, errors))


def cpp_run(project, sm, build, args=''):
    compiler = PROGRAMS['g++'].get(sm, build)
    path = compiler.convert_path(os.path.join(project.path(), build.get('app_file')))
    return f"{path} {args}"


def cpp_collect_coverage(sm, build):
    total_count = 0
    count = 0
    gcov = PROGRAMS['gcov'].get(sm, build)

    temp_dir = f"{sm.temp_dir()}/build{build.id}"
    temp_dir_wsl = gcov.convert_path(f"{sm.temp_dir()}/build{build.id}")

    for file in build.get('files', []):
        res = cmd_command(f"{gcov} {file} -o {temp_dir_wsl}", shell=True, cwd=temp_dir)

        for line in res.stdout.split('\n'):
            if "Lines executed:" in line:
                p, _, c = line.split(":")[1].split()
                total_count += int(c)
                count += round(float(p[:-1]) / 100 * int(c))
                break

    if total_count == 0:
        return 0
    return count / total_count * 100


def cpp_coverage_html(sm, build):
    temp_dir = f"{sm.temp_dir()}/build{build.id}"

    lcov = PROGRAMS['lcov'].get(sm, build)
    genhtml = PROGRAMS['genhtml'].get(sm, build)

    temp_dir_wsl = lcov.convert_path(f"{sm.temp_dir()}/build{build.id}")

    try:
        res = lcov(f"-t \"{build.get('name', '')}\" "
                   f"-o {temp_dir_wsl}/coverage.info -c -d {temp_dir_wsl}", shell=True)
        if res.returncode:
            return None

        res = genhtml(f"-o {temp_dir_wsl}/report {temp_dir_wsl}/coverage.info", shell=True)
        if res.returncode:
            return None
        return f"{temp_dir}/report/index.html"
    except FileNotFoundError:
        return None
