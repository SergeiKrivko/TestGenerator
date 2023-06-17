import os


def c_compile(path, cm, sm, coverage=False):
    old_dir = os.getcwd()
    os.chdir(path)
    compiler = sm.get_smart('compiler', 'gcc')
    compile_res = cm.cmd_command(f"{compiler} -c {'--coverage' if coverage else ''} "
                                 f"{' '.join(filter(lambda path: path.endswith('.c'), os.listdir(path)))} "
                                 f"-g {'-lm' if sm.get_smart('-lm', False) else ''}", shell=True)
    if not compile_res.returncode:
        compile_res = cm.cmd_command(f"{compiler} {'--coverage' if coverage else ''} -o {path}/app.exe "
                                     f"{' '.join(filter(lambda path: path.endswith('.c'), os.listdir(path)))} "
                                     f"{'-lm' if sm.get_smart('-lm', False) else ''}", shell=True)

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


def c_run(path, sm, cm, args, in_data):
    if os.path.isfile(path):
        return cm.cmd_command(f"{path} {args}", input=in_data, shell=True, timeout=sm.get_smart('time_limit', 3))
    return cm.cmd_command(f"{path}/app.exe {args}", input=in_data, shell=True, timeout=sm.get_smart('time_limit', 3))


def c_clear_coverage_files(path):
    for file in os.listdir(path):
        if '.gcda' in file or '.gcno' in file or 'temp.txt' in file or '.gcov' in file:
            os.remove(f"{path}/{file}")


def c_collect_coverage(path, sm, cm):
    total_count = 0
    count = 0

    for file in os.listdir(path):
        if file.endswith('.c'):
            res = cm.cmd_command(f"gcov {path}/{file}", shell=True)
            for line in res.stdout.split('\n'):
                if "Lines executed:" in line:
                    p, _, c = line.split(":")[1].split()
                    total_count += int(c)
                    count += round(float(p[:-1]) / 100 * int(c))
                    break

    c_clear_coverage_files(path)

    if total_count == 0:
        return 0
    return count / total_count * 100
