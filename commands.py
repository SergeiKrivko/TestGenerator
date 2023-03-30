import os

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

        os.system(f"{self.settings['compiler']} -c {self.path}/?*.c {'--coverage' if coverage else ''} -g "
                  f"2> {self.path}/temp.txt")
        errors = CommandManager.read_file(f"{self.path}/temp.txt")
        if errors:
            QMessageBox.warning(None, "Ошибка компиляции", errors)
            if os.path.isfile(f"{self.path}/temp.txt"):
                os.remove(f"{self.path}/temp.txt")
            os.chdir(old_dir)
            return False

        os.system(f"{self.settings['compiler']} {'--coverage' if coverage else ''} -o {self.path}/app.exe "
                  f"{self.path}/?*.o {' -lm' if self.settings['-lm'] else ''} 2> {self.path}/temp.txt")

        errors = CommandManager.read_file(f"{self.path}/temp.txt")
        if errors:
            QMessageBox.warning(None, "Ошибка компиляции", errors)
            if os.path.isfile(f"{self.path}/temp.txt"):
                os.remove(f"{self.path}/temp.txt")
            os.chdir(old_dir)
            return False

        for file in os.listdir(self.path):
            if ".o" in file:
                os.remove(f"{self.path}/{file}")

        os.chdir(old_dir)
        return True

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

        return count / total_count * 100

    def clear_coverage_files(self):
        for file in os.listdir(self.path):
            if '.gcda' in file or '.gcno' in file or 'temp.txt' in file or '.gcov' in file:
                os.remove(f"{self.path}/{file}")

    @staticmethod
    def read_file(path):
        file = open(path, encoding='utf-8')
        res = file.read()
        file.close()
        return res
