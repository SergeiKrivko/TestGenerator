import os

from language.build.make_command import MakeCommand
from language.utils import get_files


def c_compile(path, cm, sm, coverage=False):
    old_dir = os.getcwd()
    os.chdir(path)
    if os.name == 'nt' and sm.get_smart("C_wsl", False):
        compiler = "wsl -e gcc"
        env = None
    else:
        compiler = sm.get_smart('gcc', 'gcc')
        env = {'PATH': f"{os.path.split(compiler)[0]};{os.getenv('PATH')}"}
    compiler_keys = sm.get_smart('c_compiler_keys', '')
    command = f"{compiler} {compiler_keys} -c {'--coverage' if coverage else ''} " \
              f"{' '.join(get_files(path, '.c'))} " \
              f"-g {'-lm' if sm.get_smart('-lm', False) else ''}"
    compile_res = cm.cmd_command(command, shell=True, env=env)
    if not compile_res.returncode:
        command = f"{compiler} {compiler_keys} {'--coverage' if coverage else ''} -o app.exe " \
                  f"{' '.join(get_files(path, '.o'))} " \
                  f"{'-lm' if sm.get_smart('-lm', False) else ''}"
        compile_res = cm.cmd_command(command, shell=True, env=env)

        if not compile_res.returncode:
            for file in os.listdir(path):
                if file.endswith('.o'):
                    os.remove(f"{path}/{file}")
            os.chdir(old_dir)
            return True, ''

    for file in os.listdir(path):
        if file.endswith('.o'):
            os.remove(f"{path}/{file}")
    os.chdir(old_dir)
    return False, compile_res.stderr


def c_run(path, sm, args='', coverage=False):
    if os.name == 'nt' and sm.get_smart("C_wsl", False):
        return f"wsl -e ./app.exe {args}"
    if os.path.isfile(path):
        if path.endswith('.c') or path.endswith('.h'):
            return f"{os.path.join(os.path.split(path)[0], 'app.exe')} {args}"
        return f"{path} {args}"
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

    for file in get_files(path, '.c'):
        if os.name == 'nt' and sm.get_smart("C_wsl", False):
            res = cm.cmd_command(f"wsl -e gcov {file}", shell=True)
        else:
            res = cm.cmd_command(f"{sm.get_smart('gcov', 'gcov')} {file}", shell=True)

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
    for key, item in data['files'].items():
        if item:
            c_files.append(key)
    o_files = [el[:-2] + '.o' for el in c_files]

    if os.name == 'nt' and sm.get_smart("C_wsl", False):
        compiler = "wsl -e gcc"
    else:
        compiler = sm.get_smart('gcc', 'gcc')
    compiler_keys = sm.get_smart('c_compiler_keys', '')

    res = [MakeCommand(data['name'], o_files, f"{compiler} --coverage -g {' '.join(o_files)} -o {data['name']} "
                                              f"{data['keys']}")]
    for c_file, o_file in zip(c_files, o_files):
        res.append(MakeCommand(o_file, c_file, f"{compiler} {compiler_keys} --coverage -g -c {c_file} -o {o_file}"))
    return res
