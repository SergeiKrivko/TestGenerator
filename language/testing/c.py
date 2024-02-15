import os

from backend.backend_types.program import PROGRAMS
from backend.commands import cmd_command, check_files_mtime, remove_files
from language.utils import get_files


def c_compile(project, build, sm, lib=False):
    coverage = build.get('coverage', False)
    compiler = PROGRAMS['gcc'].get(sm, build)

    path = project.path()
    temp_dir = build.temp_dir(sm)
    os.makedirs(temp_dir, exist_ok=True)

    c_files = []
    h_dirs = set()
    for key in build.get('files', []):
        if key.endswith('.c'):
            c_files.append(f"{path}/{key}")
        else:
            h_dirs.add(compiler.convert_path(f"{path}/{os.path.split(key)[0]}"))
    o_files = [f"{temp_dir}/{os.path.basename(el)[:-2]}.o" for el in c_files]

    h_dirs = '-I ' + ' -I '.join(h_dirs) if h_dirs else ''
    errors = []
    code = True

    def get_dependencies(file):
        lst = compiler(f"{h_dirs} -MM {compiler.convert_path(file)}").stdout.split()
        lst.pop(0)
        i = 0
        while i < len(lst):
            if lst[i] == '\\':
                lst.pop(i)
            else:
                lst[i] = compiler.recover_path(lst[i])
                i += 1
        return lst

    compiler_keys = build.get('keys', '')
    for c_file, o_file in zip(c_files, o_files):
        if os.path.isfile(o_file) and check_files_mtime(o_file, get_dependencies(c_file)):
            continue
        res = compiler(f"{compiler_keys} {'--coverage' if coverage else ''} {h_dirs} {'-fPIC' if lib else ''} "
                       f"-c -o {compiler.convert_path(o_file)} {compiler.convert_path(c_file)}", cwd=project.path())
        if res.returncode:
            code = False
        errors.append(res.stderr)

    if code:
        if lib:
            app_file = f"{path}/{build.get('lib_file')}"
        else:
            app_file = f"{path}/{build.get('app_file')}"

        if lib and not build.get('dynamic', False):
            res = cmd_command(f"{compiler.vs_args()} ar cr {compiler.convert_path(app_file)} "
                              f"{' '.join(map(compiler.convert_path, o_files))}", cwd=project.path())
            if not res.returncode:
                res = cmd_command(f"{compiler.vs_args()} ranlib {compiler.convert_path(app_file)}", cwd=project.path())
                if res.returncode:
                    code = False
                errors.append(res.stderr)
            else:
                code = False
                errors.append(res.stderr)

        else:
            res = compiler(f"{'--coverage' if coverage else ''} -o {compiler.convert_path(app_file)}"
                           f"{' -shared' if lib else ''} {' '.join(map(compiler.convert_path, o_files))} "
                           f"{build.get('linker_keys', '')}",
                           cwd=project.path())
            if res.returncode:
                code = False
            errors.append(res.stderr)

    return code, ''.join(map(str, errors))


def c_run(project, sm, build, args=''):
    compiler = PROGRAMS['gcc'].get(sm, build)
    path = compiler.convert_path(os.path.join(project.path(), build.get('app_file')))
    return f"{compiler.vs_args()} {path} {args}"


def c_collect_coverage(sm, build):
    total_count = 0
    count = 0
    gcov = PROGRAMS['gcov'].get(sm, build)

    temp_dir = build.temp_dir(sm)

    for file in build.get('files', []):
        res = gcov(f"{file} -o {gcov.convert_path(temp_dir)}", shell=True, cwd=temp_dir)

        for line in res.stdout.split('\n'):
            if "Lines executed:" in line:
                p, _, c = line.split(":")[1].split()
                total_count += int(c)
                count += round(float(p[:-1]) / 100 * int(c))
                break

    if total_count == 0:
        return 0
    return count / total_count * 100


def c_coverage_html(sm, build):
    temp_dir = build.temp_dir(sm)

    lcov = PROGRAMS['lcov'].get(sm, build)
    genhtml = PROGRAMS['genhtml'].get(sm, build)

    try:
        res = lcov(f"-t \"{build.get('name', '')}\" "
                   f"-o {lcov.convert_path(temp_dir)}/coverage.info -c -d {lcov.convert_path(temp_dir)}", shell=True)
        if res.returncode:
            return None

        res = genhtml(f"-o {lcov.convert_path(temp_dir)}/report {lcov.convert_path(temp_dir)}/coverage.info", shell=True)
        if res.returncode:
            return None
        return f"{temp_dir}/report/index.html"
    except FileNotFoundError:
        return None
