import os

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox


class CommandManager:
    def __init__(self, settings):
        self.settings = settings
        self.path = ''

    def update_path(self):
        if self.settings['var'] == -1:
            self.path = self.settings['path'] + f"/lab_{self.settings['lab']:0>2}_" \
                                                f"{self.settings['task']:0>2}"
        else:
            self.path = self.settings['path'] + f"/lab_{self.settings['lab']:0>2}_" \
                                                f"{self.settings['task']:0>2}_" \
                                                f"{self.settings['var']:0>2}"

    def compile(self):
        os.system(f"{self.settings['compiler']} {self.path}/main.c -o {self.path}/app.exe"
                  f"{' -lm' if self.settings['-lm'] else ''} 2> {self.path}/temp.txt")
        errors = CommandManager.read_file(f"{self.path}/temp.txt")
        if errors:
            QMessageBox.warning(None, "Ошибка компиляции", errors)
            if os.path.isfile(f"{self.path}/temp.txt"):
                os.remove(f"{self.path}/temp.txt")
            return

    def compile2(self, coverage=False):
        self.update_path()
        old_dir = os.getcwd()
        os.chdir(self.path)

        code = os.system(f"{self.settings['compiler']} -c {self.path}/?*.c {'--coverage' if coverage else ''} -g "
                         f"2> {self.path}/temp.txt")
        errors = CommandManager.read_file(f"{self.path}/temp.txt")
        if code:
            if os.path.isfile(f"{self.path}/temp.txt"):
                os.remove(f"{self.path}/temp.txt")
            os.chdir(old_dir)
            return False, errors

        code = os.system(f"{self.settings['compiler']} {'--coverage' if coverage else ''} -o {self.path}/app.exe "
                         f"{self.path}/?*.o {' -lm' if self.settings['-lm'] else ''} 2> {self.path}/temp.txt")

        errors = CommandManager.read_file(f"{self.path}/temp.txt")
        if code:
            if os.path.isfile(f"{self.path}/temp.txt"):
                os.remove(f"{self.path}/temp.txt")
            os.chdir(old_dir)
            return False, errors

        for file in os.listdir(self.path):
            if ".o" in file:
                os.remove(f"{self.path}/{file}")

        os.chdir(old_dir)
        return True, ''

    def collect_coverage(self):
        total_count = 0
        count = 0

        self.update_path()
        for file in os.listdir(self.path):
            if '.c' in file:
                os.system(f"gcov {self.path}/{file} > {self.path}/temp.txt")
                for line in (f := open(f"{self.path}/temp.txt")):
                    if "Lines executed:" in line:
                        p, _, c = line.split(":")[1].split()
                        total_count += int(c)
                        count += round(float(p[:-1]) / 100 * int(c))
                        break
                f.close()

        self.clear_coverage_files()

        if total_count == 0:
            return 0
        return count / total_count * 100

    def clear_coverage_files(self):
        for file in os.listdir(self.path):
            if '.gcda' in file or '.gcno' in file or 'temp.txt' in file or '.gcov' in file:
                os.remove(f"{self.path}/{file}")

    def testing(self, pos_comparator, neg_comparator):
        self.update_path()
        self.looper = Looper(self.compile2, self.path, pos_comparator, neg_comparator)
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


class Looper(QThread):
    test_complete = pyqtSignal(bool, str, int)
    end_testing = pyqtSignal()
    testing_terminate = pyqtSignal(str)

    def __init__(self, compiler, path, pos_comparator, neg_comparator):
        super(Looper, self).__init__()
        self.compiler = compiler
        self.path = path
        self.pos_comparator = pos_comparator
        self.neg_comparator = neg_comparator

    def run(self):
        code, errors = self.compiler(coverage=True)
        if not code:
            self.testing_terminate.emit(errors)
            return

        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/pos_{i:0>2}_in.txt"):
            exit_code = os.system(f"{self.path}/app.exe < {self.path}/func_tests/data/pos_{i:0>2}_in.txt > "
                                  f"{self.path}/temp.txt")
            if exit_code % 256 == 0:
                exit_code //= 256
            self.test_complete.emit(self.pos_comparator(f"{self.path}/func_tests/data/pos_{i:0>2}_out.txt",
                                                        f"{self.path}/temp.txt"),
                                    CommandManager.read_file(f"{self.path}/temp.txt"), exit_code)
            i += 1

        i = 1
        while os.path.isfile(f"{self.path}/func_tests/data/neg_{i:0>2}_in.txt"):
            exit_code = os.system(f"{self.path}/app.exe < {self.path}/func_tests/data/neg_{i:0>2}_in.txt > "
                                  f"{self.path}/temp.txt")
            if exit_code % 256 == 0:
                exit_code //= 256
            self.test_complete.emit(self.neg_comparator(f"{self.path}/func_tests/data/neg_{i:0>2}_out.txt",
                                                        f"{self.path}/temp.txt"),
                                    CommandManager.read_file(f"{self.path}/temp.txt"), exit_code)
            i += 1

        self.end_testing.emit()

    def terminate(self) -> None:
        for file in os.listdir(self.path):
            if '.gcda' in file or '.gcno' in file or 'temp.txt' in file or '.gcov' in file:
                os.remove(f"{self.path}/{file}")
        super(Looper, self).terminate()
