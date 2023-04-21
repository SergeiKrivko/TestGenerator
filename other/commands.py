import os
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal


class CommandManager:
    def __init__(self, settings):
        self.settings = settings
        self.path = ''

    @staticmethod
    def cmd_command(args, **kwargs):
        if os.name == 'nt':
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            return subprocess.run(args, capture_output=True, text=True, startupinfo=si, **kwargs)
        else:
            return subprocess.run(args, capture_output=True, text=True, **kwargs)

    def update_path(self):
        if self.settings['var'] == -1:
            self.path = self.settings['path'] + f"/lab_{self.settings['lab']:0>2}_" \
                                                f"{self.settings['task']:0>2}"
        else:
            self.path = self.settings['path'] + f"/lab_{self.settings['lab']:0>2}_" \
                                                f"{self.settings['task']:0>2}_" \
                                                f"{self.settings['var']:0>2}"

    def compile2(self, coverage=False):
        self.update_path()
        old_dir = os.getcwd()
        os.chdir(self.path)

        compile_res = self.cmd_command(self.settings['compiler'].split() + ["-c"] +
                                       (['--coverage'] if coverage else []) +
                                       list(filter(lambda path: path.endswith('.c'), os.listdir(self.path))) + ["-g"] +
                                       (['-lm'] if self.settings['-lm'] else []))
        if compile_res.returncode:
            os.chdir(old_dir)
            return False, compile_res.stderr

        compile_res = self.cmd_command(self.settings['compiler'].split() +
                                       (['--coverage'] if coverage else []) + ['-o'] +
                                       [f"{self.path}/app.exe"] +
                                       list(filter(lambda path: path.endswith('.o'), os.listdir(self.path))) +
                                       (['-lm'] if self.settings['-lm'] else []))

        if compile_res.returncode:
            os.chdir(old_dir)
            return False, compile_res.stderr

        for file in os.listdir(self.path):
            if file.endswith('.o'):
                os.remove(f"{self.path}/{file}")

        os.chdir(old_dir)
        return True, ''

    def collect_coverage(self):
        total_count = 0
        count = 0

        self.update_path()
        for file in os.listdir(self.path):
            if '.c' in file:
                res = self.cmd_command(["gcov", f"{self.path}/{file}"])
                for line in res.stdout.split('\n'):
                    if "Lines executed:" in line:
                        p, _, c = line.split(":")[1].split()
                        total_count += int(c)
                        count += round(float(p[:-1]) / 100 * int(c))
                        break

        self.clear_coverage_files()

        if total_count == 0:
            return 0
        return count / total_count * 100

    def clear_coverage_files(self):
        for file in os.listdir(self.path):
            if '.gcda' in file or '.gcno' in file or 'temp.txt' in file or '.gcov' in file:
                os.remove(f"{self.path}/{file}")

    def testing(self, pos_comparator, neg_comparator, memory_testing, coverage):
        self.update_path()
        self.looper = Looper(self.compile2, self.path, pos_comparator, neg_comparator, memory_testing, coverage)
        self.looper.start()

    def test_count(self):
        count = 0
        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt"):
            count += 1
        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt"):
            count += 1
        return count

    @staticmethod
    def read_file(path):
        try:
            file = open(path, encoding='utf-8')
            res = file.read()
            file.close()
            return res
        except Exception:
            return ''

    def list_of_tasks(self):
        res = []
        for file in os.listdir(self.settings['path']):
            if file.startswith(f"lab_{self.settings['lab']:0>2}_"):
                try:
                    res.append(int(file[7:9]))
                except Exception:
                    pass
        res.sort()
        return res

    def parce_todo_md(self):
        res = []
        try:
            file = open(f"{self.settings['path']}/TODO/lab_{self.settings['lab']:0>2}.md")
            task = -1
            for line in file:
                if line.startswith('## Общее'):
                    task = 0
                elif line.startswith('## Задание'):
                    task = int(line.split()[2])
                elif line.startswith('- '):
                    res.append((task, line[1:].strip()))
                res.sort()
        except Exception:
            pass
        return res

    def parse_todo_in_code(self, current_task=False):
        res = []
        for folder in (
                os.listdir(self.settings['path']) if not current_task else
                (f"lab_{self.settings['lab']:0>2}_"
                 f"{self.settings['task']:0>2}_{self.settings['var']:0>2}",)):

            if os.path.isdir(f"{self.settings['path']}/{folder}"):
                for file in os.listdir(f"{self.settings['path']}/{folder}"):
                    if file.endswith(".c") or file.endswith(".h"):
                        i = 1
                        for line in (f := open(f"{self.settings['path']}/{folder}/{file}", encoding='utf-8')):
                            if "// TODO:" in line:
                                res.append((f"{folder}/{file}", i, line[line.index("// TODO:") + 8:].strip()))
                            i += 1
                        f.close()
        return res


class Looper(QThread):
    test_complete = pyqtSignal(bool, str, int, bool, str)
    test_crush = pyqtSignal(str, int, str)
    end_testing = pyqtSignal()
    testing_terminate = pyqtSignal(str)

    def __init__(self, compiler, path, pos_comparator, neg_comparator, memory_testing=False, coverage=False):
        super(Looper, self).__init__()
        self.compiler = compiler
        self.memory_testing = memory_testing
        self.path = path
        self.pos_comparator = pos_comparator
        self.neg_comparator = neg_comparator
        self.coverage = coverage

    def run(self):
        code, errors = self.compiler(coverage=self.coverage)
        if not code:
            self.testing_terminate.emit(errors)
            return

        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt"):
            res = CommandManager.cmd_command(f"{self.path}/app.exe", input=CommandManager.read_file(
                f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt"))
            if res.stderr:
                self.test_crush.emit(res.stdout, res.returncode, res.stderr)
                i += 1
                continue
            comparator_res = self.pos_comparator(
                CommandManager.read_file(f"{self.path}/func_tests/data/pos_{i:0>2}_out.txt"), res.stdout)

            if self.memory_testing:
                os.system(f"valgrind -q ./app.exe < "
                          f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt > temp_null.txt 2> temp.txt")
                valgrind_out = CommandManager.read_file(f"{self.path}/temp.txt")
            else:
                valgrind_out = ""

            self.test_complete.emit(not res.returncode and comparator_res,
                                    res.stdout, res.returncode, not valgrind_out, valgrind_out)
            i += 1

        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt"):
            res = CommandManager.cmd_command(f"{self.path}/app.exe", input=CommandManager.read_file(
                f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt"))
            if res.stderr:
                self.test_crush.emit(res.stdout, res.returncode, res.stderr)
                i += 1
                continue
            comparator_res = self.neg_comparator(
                CommandManager.read_file(f"{self.path}/func_tests/data/neg_{i:0>2}_out.txt"), res.stdout)

            if self.memory_testing:
                os.system(f"valgrind -q ./app.exe < "
                          f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt > temp_null.txt 2> temp.txt")
                valgrind_out = CommandManager.read_file(f"{self.path}/temp.txt")
            else:
                valgrind_out = ""

            self.test_complete.emit(res.returncode and comparator_res,
                                    res.stdout, res.returncode, not valgrind_out, valgrind_out)
            i += 1

        if os.path.isfile("temp_null.txt"):
            os.remove("temp_null.txt")
        if os.path.isfile("temp_errors.txt"):
            os.remove("temp_errors.txt")

        self.end_testing.emit()

    def terminate(self) -> None:
        for file in os.listdir(self.path):
            if '.gcda' in file or '.gcno' in file or 'temp.txt' in file or '.gcov' in file:
                os.remove(f"{self.path}/{file}")
        super(Looper, self).terminate()
