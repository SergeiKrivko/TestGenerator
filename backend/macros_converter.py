import os
from json import loads, JSONDecodeError

from PyQt6.QtCore import QThread, pyqtSignal, QObject

from backend.backend_types.func_test import FuncTest
from backend.backend_types.project import Project
from backend.commands import inflect
from other.binary_redactor.convert_binary import convert as convert_binary


class MacrosConverter(QThread):
    def __init__(self, project: Project, tests: dict[str: list[FuncTest]], sm):
        super(MacrosConverter, self).__init__()

        self.src_dir = f"{project.data_path()}/func_tests"
        self.dst_dir = project.path()
        self.project = project
        self.tests = tests
        self.sm = sm
        os.makedirs(os.path.split(project.readme_path())[0], exist_ok=True)
        self.readme = open(project.readme_path(), 'w', encoding='utf-8')
        self._file = None
        self.closed = False

        self.line_sep = sm.line_sep
        self.data_path = project.data_path()

    @staticmethod
    def convert_txt(text, path, line_sep):
        os.makedirs(os.path.split(path)[0], exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline=line_sep) as f:
            f.write(text)

    @staticmethod
    def convert_bin(text, path):
        os.makedirs(os.path.split(path)[0], exist_ok=True)
        try:
            convert_binary(text, path)
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")

    @staticmethod
    def convert_args(text, path, test_type, index, in_files, out_files, data_path, line_sep='\n'):
        text = text.split()
        for i in range(len(text)):
            if text[i] == '#fin':
                text[i] = '#fin1'
            if text[i].startswith('#fin') and (n := text[i].lstrip('#fin')).isdigit():
                text[i] = in_files.get(int(n), '#fin').replace('\\', '/')
            if text[i] == '#fout':
                text[i] = '#fout1'
            if text[i].startswith('#fout') and (n := text[i].lstrip('#fout')).isdigit():
                if int(n) in out_files:
                    text[i] = f"{data_path}/temp_{int(n)}{out_files[int(n)][-4:]}".replace('\\', '/')
                else:
                    text[i] = f"{data_path}/temp_{int(n)}".replace('\\', '/')
        if path:
            os.makedirs(os.path.split(path)[0], exist_ok=True)
            with open(path, 'w', encoding='utf-8', newline=line_sep) as f:
                f.write(' '.join(text))
        else:
            return ' '.join(text)

    def add_file(self, path: str):
        path = os.path.relpath(path, self.dst_dir)
        self._file.write(path + '\n')

    def convert_tests(self, tests_type='pos'):
        if not os.path.isdir(f"{self.src_dir}/{tests_type}"):
            return

        for index, test in enumerate(self.tests[tests_type]):
            if self.closed:
                return

            self.readme.write(f"- {index + 1:0>2} - {test.get('desc', '-')}\n")
            self.convert_txt(test.get('in', ''),
                             self.project.test_in_path(tests_type, index),
                             self.line_sep)
            self.add_file(self.project.test_in_path(tests_type, index))
            self.convert_txt(test.get('out', ''),
                             self.project.test_out_path(tests_type, index),
                             self.line_sep)
            self.add_file(self.project.test_out_path(tests_type, index))

            in_files = dict()
            out_files = dict()

            for i, el in enumerate(test.get('in_files', [])):
                if el.get('type', 'txt') == 'txt':
                    self.convert_txt(el['text'],
                                     s := self.project.test_in_file_path(tests_type, index, i, False),
                                     self.line_sep)
                    self.add_file(s)
                    in_files[i + 1] = os.path.relpath(s, self.dst_dir)
                    if 'check' in el:
                        self.convert_txt(el['check'],
                                         s := self.project.test_check_file_path(tests_type, index, i, False),
                                         self.line_sep)
                        self.add_file(s)
                else:
                    self.convert_bin(el['text'],
                                     s := self.project.test_in_file_path(tests_type, index, i, True))
                    in_files[i + 1] = os.path.relpath(s, self.dst_dir)
                    self.add_file(s)
                    if 'check' in el:
                        self.convert_bin(el['check'],
                                         s := self.project.test_check_file_path(tests_type, index, i, True))
                        self.add_file(s)

            for i, el in enumerate(test.get('out_files', [])):
                if el.get('type', 'txt') == 'txt':
                    self.convert_txt(el['text'],
                                     s := self.project.test_out_file_path(tests_type, index, i, False),
                                     self.line_sep)
                    self.add_file(s)
                    out_files[i + 1] = os.path.relpath(s, self.dst_dir)
                else:
                    self.convert_bin(el['text'],
                                     s := self.project.test_out_file_path(tests_type, index, i, True))
                    out_files[i + 1] = os.path.relpath(s, self.dst_dir)
                    self.add_file(s)

            if test.get('args', ''):
                self.convert_args(test.get('args', ''),
                                  self.project.test_args_path(tests_type, index),
                                  tests_type, index, in_files, out_files, self.project.get('temp_files_dir', '.'),
                                  self.line_sep)
                self.add_file(self.project.test_args_path(tests_type, index))

    def close(self):
        self.closed = True

    def run(self):
        try:
            self._file = open(f"{self.data_path}/files.txt", encoding='utf-8')
            for line in self._file:
                try:
                    os.remove(path := f"{self.dst_dir}/{line.strip()}")
                    os.removedirs(os.path.split(path)[0])
                except FileNotFoundError:
                    pass
                except PermissionError:
                    pass
                except OSError:
                    pass
            self._file.close()
        except FileNotFoundError:
            pass
        self._file = open(f"{self.data_path}/files.txt", 'w', encoding='utf-8')
        self.finished.connect(self._file.close)

        self.readme.write(f"# Тесты для {inflect(self.project.name(), 'gent')}:\n")

        self.readme.write("\n## Позитивные тесты:\n")
        self.convert_tests('pos')

        self.readme.write("\n## Негативные тесты:\n")
        self.convert_tests('neg')
        self.readme.close()
