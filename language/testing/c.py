import os


def c_compile(path, cm, sm, coverage=False):
    old_dir = os.getcwd()
    os.chdir(path)
    compiler = sm.get_smart('gcc', 'gcc')
    compiler_keys = sm.get_smart('c_compiler_keys', '')
    env = {'PATH': f"{os.path.split(compiler)[0]};{os.getenv('PATH')}"}
    command = f"{compiler} {compiler_keys} -c {'--coverage' if coverage else ''} " \
              f"{' '.join(filter(lambda path: path.endswith('.c'), os.listdir(path)))} " \
              f"-g {'-lm' if sm.get_smart('-lm', False) else ''}"
    compile_res = cm.cmd_command(command, shell=True, env=env)
    if not compile_res.returncode:
        command = f"{compiler} {compiler_keys} {'--coverage' if coverage else ''} -o {path}/app.exe " \
                  f"{' '.join(filter(lambda path: path.endswith('.c'), os.listdir(path)))} " \
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
    if os.path.isfile(path):
        if path.endswith('.c') or path.endswith('.h'):
            return f"{os.path.split(path)[0]}/app.exe {args}"
        return f"{path} {args}"
    return f"{path}/app.exe {args}"


def c_clear_coverage_files(path):
    for file in os.listdir(path):
        if '.gcda' in file or '.gcno' in file or 'temp.txt' in file or '.gcov' in file:
            os.remove(f"{path}/{file}")


def c_collect_coverage(path, sm, cm):
    total_count = 0
    count = 0

    for file in os.listdir(path):
        if file.endswith('.c'):
            res = cm.cmd_command(f"{sm.get_smart('gcov', 'gcov')} {path}/{file}", shell=True)
            for line in res.stdout.split('\n'):
                if "Lines executed:" in line:
                    p, _, c = line.split(":")[1].split()
                    total_count += int(c)
                    count += round(float(p[:-1]) / 100 * int(c))
                    break

    if total_count == 0:
        return 0
    return count / total_count * 100
