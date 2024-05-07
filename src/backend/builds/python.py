import os

from src.backend.backend_types.build import Build
from src.backend.backend_types.program import PROGRAMS


class BuildPython(Build):
    def command(self, args=''):
        interpreter = self.program('python')
        path = interpreter.convert_path(os.path.join(self._project.path(), self.get('file', 'main.py')))
        if self.get('coverage'):
            key_a = ''
            if os.path.isfile(f"{self.temp_dir()}/.coverage"):
                key_a = '-a'
            os.makedirs(f"{self.temp_dir()}", exist_ok=True)
            return f"{interpreter.path} -m coverage run {key_a} --data-file={self.temp_dir()}/.coverage {path} {args}"
        return f"{interpreter.path} {path} {args}"

    def coverage(self):
        interpreter = self.program('python')
        res = interpreter(f"-m coverage report --data-file={self.temp_dir()}/.coverage", shell=True)
        text = res.stdout
        try:
            for line in text.split('\n'):
                if line.startswith('TOTAL'):
                    return int(line.split()[3].rstrip('%'))
        except Exception as ex:
            pass
        return 0

    def coverage_html(self):
        interpreter = self.program('python')
        res = interpreter(f"-m coverage html --data-file={self.temp_dir()}/.coverage --directory={self.temp_dir()}/htmlcov",
                          shell=True)
        if res.returncode == 0:
            return f"{self.temp_dir()}/htmlcov/index.html"


def python_fast_run(path, project, bm):
    interpreter = PROGRAMS['python'].get(bm.sm)
    return f"{interpreter} \"{path}\"", ''
