import os

from src.backend.backend_types.build import Build
from src.backend.backend_types.program import PROGRAMS


class BuildBash(Build):
    def command(self, args=''):
        interpreter = self.program('bash')
        path = interpreter.convert_path(os.path.join(self._project.path(), self.get('file', 'main.sh')))
        return f"{interpreter.path} {path} {args}"


class BuildCommand(Build):
    def command(self, args=''):
        return f"{self.get('command', 'echo')} {args}"


def bash_fast_run(path, bm):
    interpreter = PROGRAMS['bash'].get(bm.sm)
    return f"{interpreter.command()} \"{interpreter.convert_path(path)}\""


def batch_fast_run(path, bm):
    if os.path.isabs(path):
        return path
    return f".\\{path}"
