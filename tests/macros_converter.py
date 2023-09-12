import os
import shutil
from json import loads, JSONDecodeError

from PyQt5.QtCore import QThread, pyqtSignal, QObject

from tests.convert_binary import convert as convert_binary


class BackgroundProcessManager(QObject):
    all_finished = pyqtSignal()

    def __init__(self):
        super(BackgroundProcessManager, self).__init__()
        self.dict = dict()

    def add_process(self, key, process):
        if key in self.dict:
            self.dict[key].terminate()
        self.dict[key] = process
        process.finished.connect(lambda: self.process_finished(key))

    def process_finished(self, key):
        if key in self.dict:
            self.dict.pop(key)
        if len(self.dict) == 0:
            self.all_finished.emit()


background_process_manager = BackgroundProcessManager()


class MacrosConverter(QThread):
    def __init__(self, src_dir, dst_dir, project, sm, readme=None):
        super(MacrosConverter, self).__init__()

        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.project = project
        self.sm = sm
        self.readme = readme
        self._file = None
        self.closed = False

        self.line_sep = sm.line_sep
        self.lab_path = sm.lab_path()
        self.data_path = sm.data_lab_path()
        self.lab = self.sm.get('lab'), self.sm.get('task'), self.sm.get('var')
        background_process_manager.add_process(src_dir, self)

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

        for file in sorted(os.listdir(f"{self.src_dir}/{tests_type}"), key=lambda s: int(s.rstrip('.json'))):
            if self.closed:
                return
            if not file.rstrip('.json').isdigit():
                continue
            index = int(file.rstrip('.json'))
            with open(f"{self.src_dir}/{tests_type}/{file}", encoding='utf-8') as f:
                try:
                    data = loads(f.read())
                    data = data if isinstance(data, dict) else dict()
                except JSONDecodeError:
                    data = dict()

            self.readme.write(f"- {index + 1:0>2} - {data.get('desc', '-')}\n")
            self.convert_txt(data.get('in', ''),
                             self.sm.test_in_path(tests_type, index, lab=self.lab, project=self.project),
                             self.line_sep)
            self.add_file(self.sm.test_in_path(tests_type, index, lab=self.lab, project=self.project))
            self.convert_txt(data.get('out', ''),
                             self.sm.test_out_path(tests_type, index, lab=self.lab, project=self.project),
                             self.line_sep)
            self.add_file(self.sm.test_out_path(tests_type, index, lab=self.lab, project=self.project))

            in_files = dict()
            out_files = dict()

            for i, el in enumerate(data.get('in_files', [])):
                if el.get('type', 'txt') == 'txt':
                    self.convert_txt(el['text'],
                                     s := self.sm.test_in_file_path(tests_type, index, i, False, lab=self.lab,
                                                                    project=self.project),
                                     self.line_sep)
                    self.add_file(s)
                    in_files[i + 1] = os.path.relpath(s, self.dst_dir)
                    if 'check' in el:
                        self.convert_txt(el['check'],
                                         s := self.sm.test_check_file_path(tests_type, index, i, False, lab=self.lab,
                                                                           project=self.project),
                                         self.line_sep)
                        self.add_file(s)
                else:
                    self.convert_bin(el['text'],
                                     s := self.sm.test_in_file_path(tests_type, index, i, True, lab=self.lab,
                                                                    project=self.project))
                    in_files[i + 1] = os.path.relpath(s, self.dst_dir)
                    self.add_file(s)
                    if 'check' in el:
                        self.convert_bin(el['check'],
                                         s := self.sm.test_check_file_path(tests_type, index, i, True, lab=self.lab,
                                                                           project=self.project))
                        self.add_file(s)

            for i, el in enumerate(data.get('out_files', [])):
                if el.get('type', 'txt') == 'txt':
                    self.convert_txt(el['text'],
                                     s := self.sm.test_out_file_path(tests_type, index, i, False, lab=self.lab,
                                                                     project=self.project),
                                     self.line_sep)
                    self.add_file(s)
                    out_files[i + 1] = os.path.relpath(s, self.dst_dir)
                else:
                    self.convert_bin(el['text'],
                                     s := self.sm.test_out_file_path(tests_type, index, i, True, lab=self.lab,
                                                                     project=self.project))
                    out_files[i + 1] = os.path.relpath(s, self.dst_dir)
                    self.add_file(s)

            if data.get('args', ''):
                self.convert_args(data.get('args', ''),
                                  self.sm.test_args_path(tests_type, index, lab=self.lab, project=self.project),
                                  tests_type, index, in_files, out_files, '.', self.line_sep)
                self.add_file(self.sm.test_args_path(tests_type, index, lab=self.lab, project=self.project))

    def close(self):
        self.closed = True

    def run(self):
        # for test_type in ['pos', 'neg']:
        #     for d in [self.sm.test_in_path(test_type, 0), self.sm.test_out_path(test_type, 0),
        #               self.sm.test_args_path(test_type, 0), self.sm.test_in_file_path(test_type, 0, 1, False),
        #               self.sm.test_out_file_path(test_type, 0, 1, False),
        #               self.sm.test_check_file_path(test_type, 0, 1, False)]:
        #         try:
        #             shutil.rmtree(d := os.path.split(d)[0])
        #             os.makedirs(d, exist_ok=True)
        #         except Exception:
        #             pass

        self.readme.write("\n## Позитивные тесты:\n")
        self.convert_tests('pos')

        self.readme.write("\n## Негативные тесты:\n")
        self.convert_tests('neg')
        self.readme.close()
