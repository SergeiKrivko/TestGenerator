import os

from src.backend.backend_types.build import Build
from src.backend.commands import check_files_mtime, cmd_command, remove_files


class _BuildCAbstract(Build):
    def compile(self, lib=False):
        sm = self._bm.sm
        coverage = self.get('coverage', False)
        compiler = self.program('gcc')

        path = self._project.path()
        temp_dir = self.temp_dir()
        os.makedirs(temp_dir, exist_ok=True)

        c_files = []
        h_dirs = set()
        for key in self.get('files', []):
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

        compiler_keys = self.get('keys', '')
        for c_file, o_file in zip(c_files, o_files):
            if os.path.isfile(o_file) and check_files_mtime(o_file, get_dependencies(c_file)):
                continue
            res = compiler(
                f"{compiler_keys} {'--coverage' if coverage else ''} {h_dirs} {'-fPIC' if lib else ''} "
                f"-c -o {compiler.convert_path(o_file)} {compiler.convert_path(c_file)}", cwd=self._project.path())
            if res.returncode:
                code = False
            errors.append(res.stderr)

        if code:
            if lib:
                app_file = f"{path}/{self.get('lib_file')}"
            else:
                app_file = f"{path}/{self.get('app_file')}"

            if lib and not self.get('dynamic', False):
                res = cmd_command(f"{compiler.vs_args()} ar cr {compiler.convert_path(app_file)} "
                                  f"{' '.join(map(compiler.convert_path, o_files))}", cwd=self._project.path())
                if not res.returncode:
                    res = cmd_command(f"{compiler.vs_args()} ranlib {compiler.convert_path(app_file)}",
                                      cwd=self._project.path())
                    if res.returncode:
                        code = False
                    errors.append(res.stderr)
                else:
                    code = False
                    errors.append(res.stderr)

            else:
                res = compiler(f"{'--coverage' if coverage else ''} -o {compiler.convert_path(app_file)}"
                               f"{' -shared' if lib else ''} {' '.join(map(compiler.convert_path, o_files))} "
                               f"{self.get('linker_keys', '')}",
                               cwd=self._project.path())
                if res.returncode:
                    code = False
                errors.append(res.stderr)

        return code, ''.join(map(str, errors))

    def clear_coverage(self):
        remove_files(self.temp_dir(), ['.gcda', '.gcno', '.gcov', 'coverage.info'])


class BuildCExecutable(_BuildCAbstract):
    def compile(self, *args):
        return super().compile(lib=False)

    def command(self, args=''):
        compiler = self.program('gcc')
        path = compiler.convert_path(os.path.join(self._project.path(), self.get('app_file')))
        return f"{compiler.vs_args()} {path} {args}"

    def coverage(self):
        total_count = 0
        count = 0
        gcov = self.program('gcov')

        temp_dir = self.temp_dir()

        for file in self.get('files', []):
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

    def coverage_html(self):
        temp_dir = self.temp_dir()

        lcov = self.program('lcov')
        genhtml = self.program('genhtml')

        try:
            res = lcov(f"-t \"{self.get('name', '')}\" "
                       f"-o {lcov.convert_path(temp_dir)}/coverage.info -c -d {lcov.convert_path(temp_dir)}",
                       shell=True)
            if res.returncode:
                return None

            res = genhtml(f"-o {lcov.convert_path(temp_dir)}/report {lcov.convert_path(temp_dir)}/coverage.info",
                          shell=True)
            if res.returncode:
                return None
            return f"{temp_dir}/report/index.html"
        except FileNotFoundError:
            return None


class BuildCLibrary(_BuildCAbstract):
    def compile(self, *args):
        return super().compile(lib=True)

