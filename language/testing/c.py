import os

from backend.commands import cmd_command, wsl_path
from language.utils import get_files


def c_compile(project, build, sm):
    coverage = build.get('coverage', False)
    compiler = build.get('compiler')
    if compiler is None:
        compiler = project.get('gcc', 'gcc')
    if build.get('wsl') and not compiler.startswith('wsl -e'):
        compiler = 'wsl -e ' + compiler

    path = wsl_path(project.path(), build)
    temp_dir = wsl_path(f"{sm.temp_dir()}/build{build.id}", build)
    os.makedirs(f"{sm.temp_dir()}/build{build.id}", exist_ok=True)

    c_files = []
    h_dirs = set()
    for key in build.get('files', []):
        if key.endswith('.c'):
            c_files.append(f"{path}/{key}")
        else:
            h_dirs.add(f"{path}/{os.path.split(key)[0]}")
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
    path = wsl_path(project.path(), build)
    return f"{'wsl -e ' if build.get('wsl') else ''}{path}/{build.get('app_file')} {args}"


def c_collect_coverage(sm, build):
    total_count = 0
    count = 0
    gcov = sm.get('gcov', 'gcov')
    if build.get('wsl') and not gcov.startswith('wsl -e'):
        gcov = 'wsl -e gcov'

    temp_dir = f"{sm.temp_dir()}/build{build.id}"
    temp_dir_wsl = wsl_path(f"{sm.temp_dir()}/build{build.id}", build)

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


def c_coverage_html(sm, build):
    temp_dir = f"{sm.temp_dir()}/build{build.id}"
    temp_dir_wsl = wsl_path(f"{sm.temp_dir()}/build{build.id}", build)

    lcov = sm.get('lcov', 'lcov')
    if build.get('wsl') and not lcov.startswith('wsl -e'):
        lcov = 'wsl -e lcov'

    genhtml = sm.get('genhtml', 'genhtml')
    if build.get('wsl') and not genhtml.startswith('wsl -e'):
        genhtml = 'wsl -e genhtml'

    try:
        print(f"{lcov} -t \"{build.get('name', '')}\" "
              f"-o {temp_dir_wsl}/coverage.info -c -d {temp_dir_wsl}")
        res = cmd_command(f"{lcov} -t \"{build.get('name', '')}\" "
                          f"-o {temp_dir_wsl}/coverage.info -c -d {temp_dir_wsl}")
        print(res)
        if res.returncode:
            return None

        res = cmd_command(f"{genhtml} -o {temp_dir_wsl}/report {temp_dir_wsl}/coverage.info")
        print(res)
        if res.returncode:
            return None
        return f"{temp_dir}/report/index.html"
    except FileNotFoundError:
        return None
