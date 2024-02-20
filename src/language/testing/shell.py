import os

from src.backend.backend_types.program import PROGRAMS


def bash_run(project, sm, build, args=''):
    interpreter = PROGRAMS['bash'].get(sm, build)
    return f"{interpreter.path} " \
           f"{interpreter.convert_path(os.path.join(project.path(), build.get('file', 'main.sh')))} {args}"


def batch_run(path, sm, args='', coverage=False):
    return f"\"{path}\" {args}"
