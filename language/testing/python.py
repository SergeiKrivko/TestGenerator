import os.path


def python_compile(path, sm, cm, coverage):
    return True, ''


def python_run(path, sm, cm, args='', in_data=''):
    if os.path.isfile(path):
        return cm.cmd_command(f"{sm['python']} {path} {args}", input=in_data, shell=True,
                              timeout=float(sm.get_smart('time_limit', 3)))
    return cm.cmd_command(f"{sm['python']} {path}/main.py {args}", input=in_data, shell=True,
                          timeout=float(sm.get_smart('time_limit', 3)))


def python_collect_coverage(path, sm, cm):
    old_dir = os.getcwd()
    os.chdir(path)
    res = cm.cmd_command(f"coverage report", shell=True)
    text = res.stdout
    try:
        for line in text.split('\n'):
            if line.startswith('TOTAL'):
                os.chdir(old_dir)
                return int(line.split()[3].rstrip('%'))
    except Exception as ex:
        raise ex
        pass
    os.chdir(old_dir)
    return 0


def python_clear_coverage_files(path):
    if os.path.isfile(f"{path}/.coverage"):
        os.remove(f"{path}/.coverage")
