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

    def compile2(self):
        self.update_path()
        old_dir = os.getcwd()
        os.chdir(self.path)

        os.system(f"{self.settings['compiler']} -c {self.path}/?*.c --coverage -g 2> {self.path}/temp.txt")
        errors = CommandManager.read_file(f"{self.path}/temp.txt")
        if errors:
            QMessageBox.warning(None, "Ошибка компиляции", errors)
            if os.path.isfile(f"{self.path}/temp.txt"):
                os.remove(f"{self.path}/temp.txt")
            os.chdir(old_dir)
            return False

        os.system(f"{self.settings['compiler']} --coverage -o {self.path}/app.exe {self.path}/?*.o"
                  f"{' -lm' if self.settings['-lm'] else ''} 2> {self.path}/temp.txt")

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

        for file in os.listdir(self.path):
            if '.gcda' in file or '.gcno' in file or 'temp.txt' in file:
                os.remove(f"{self.path}/{file}")

        return count / total_count * 100

    @staticmethod
    def read_file(path):
        file = open(path, encoding='utf-8')
        res = file.read()
        file.close()
        return res
