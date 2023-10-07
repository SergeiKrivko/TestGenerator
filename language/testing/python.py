import os.path

from backend.commands import cmd_command


def python_run(project, build, args=''):
    interpreter = build.get('interpreter')
    if interpreter is None:
        interpreter = project.get('python', 'python')
    return f"{interpreter} {os.path.join(project.path(), build.get('file', 'main.py'))} {args}"


def python_run_coverage(project, sm, build, args=''):
    interpreter = build.get('interpreter')
    if interpreter is None:
        interpreter = project.get('python_coverage', 'coverage')
    key_a = ''
    if os.path.isfile(f"{sm.temp_dir()}/build{build.id}/.coverage"):
        key_a = '-a'
    os.makedirs(f"{sm.temp_dir()}/build{build.id}", exist_ok=True)
    return f"{interpreter} run {key_a} --data-file={sm.temp_dir()}/build{build.id}/.coverage " \
           f"{os.path.join(project.path(), build.get('file', 'main.py'))} {args}"


def python_collect_coverage(sm, build):
    res = cmd_command(f"coverage report --data-file={sm.temp_dir()}/build{build.id}/.coverage", shell=True)
    text = res.stdout
    try:
        for line in text.split('\n'):
            if line.startswith('TOTAL'):
                return int(line.split()[3].rstrip('%'))
    except Exception as ex:
        pass
    return 0


def python_coverage_html(sm, build):
    temp_dir = f"{sm.temp_dir()}/build{build.id}"
    res = cmd_command(f"coverage html --data-file={temp_dir}/.coverage --directory={temp_dir}/htmlcov", shell=True)
    if res.returncode == 0:
        return f"{temp_dir}/htmlcov/index.html"
