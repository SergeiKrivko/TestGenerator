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
        self.dict[key] = process
        process.finished.connect(lambda: self.process_finished(key))

    def process_finished(self, key):
        self.dict.pop(key)
        if len(self.dict) == 0:
            self.all_finished.emit()


background_process_manager = BackgroundProcessManager()


class MacrosConverter(QThread):
    def __init__(self, src_dir, dst_dir, dst_format, sm, readme=None):
        super(MacrosConverter, self).__init__()

        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.dst_format = dst_format
        self.readme = readme
        self.closed = False

        self.line_sep = sm.get_general('line_sep', '\n')
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

    def convert_args(self, text, path, test_type, index, in_files, out_files):
        text = text.split()
        for i in range(len(text)):
            if text[i].startswith('#fin') and (n := text[i].lstrip('#fin').isdigit()):
                text[i] = in_files.get(int(n), '#fin')
            if text[i].startswith('#fout') and (n := text[i].lstrip('#fout').isdigit()):
                if int(n) in out_files:
                    text[i] = os.path.split(out_files[int(n)])[0] + f'/temp_{int(n)}{out_files[int(n)][-4:]}'
        with open(path, 'w', encoding='utf-8', newline=self.line_sep) as f:
            f.write(' '.join(text))

    def convert_tests(self, tests_type='pos'):
        if not os.path.isdir(f"{self.src_dir}/{tests_type}"):
            return
        for file in os.listdir(f"{self.src_dir}/{tests_type}"):
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

            self.readme.write(f"- {index:0>2} - {data.get('desc', '-')}\n")
            self.convert_txt(data.get('in', ''),
                             f"{self.dst_dir}/{self.dst_format.get(f'{tests_type}_in').format(index + 1)}",
                             self.line_sep)
            self.convert_txt(data.get('out', ''),
                             f"{self.dst_dir}/{self.dst_format.get(f'{tests_type}_out').format(index + 1)}",
                             self.line_sep)

            in_files = dict()
            out_files = dict()
            check_files = dict()

            for i, el in enumerate(data.get('in_files', [])):
                if el.get('type', 'txt') == 'txt':
                    self.convert_txt(el['text'], self.dst_dir + '/' + (s := self.dst_format.get(
                        f'{tests_type}_in_files').format(index + 1, i + 1) + '.txt'), self.line_sep)
                    in_files[i + 1] = s
                else:
                    self.convert_bin(el['text'], self.dst_dir + '/' + (s := self.dst_format.get(
                        f'{tests_type}_in_files').format(index + 1, i + 1) + '.bin'))
                    in_files[i + 1] = s

            for i, el in enumerate(data.get('out_files', [])):
                if el.get('type', 'txt') == 'txt':
                    self.convert_txt(el['text'], self.dst_dir + '/' + (s := self.dst_format.get(
                        f'{tests_type}_out_files').format(index + 1, i + 1) + '.txt'),
                                     self.line_sep)
                    out_files[i + 1] = s
                else:
                    self.convert_bin(el['text'], self.dst_dir + '/' + (s := self.dst_format.get(
                        f'{tests_type}_out_files').format(index + 1, i + 1) + '.bin'))
                    out_files[i + 1] = s

            for i, el in data.get('check_files', dict()).items():
                if el.get('type', 'txt') == 'txt':
                    self.convert_txt(el['text'], self.dst_dir + '/' + (s := self.dst_format.get(
                        f'{tests_type}_check_files').format(index + 1, i) + '.txt'), self.line_sep)
                    check_files[i] = s
                else:
                    self.convert_bin(el['text'], self.dst_dir + '/' + (s := self.dst_format.get(
                        f'{tests_type}_check_files').format(index + 1, i) + '.bin'))
                    check_files[i] = s

            if data.get('args', ''):
                self.convert_args(data.get('args', ''),
                                  f"{self.dst_dir}/{self.dst_format.get(f'{tests_type}_args').format(index + 1)}",
                                  tests_type, index, in_files, out_files)

    def close(self):
        self.closed = True

    def run(self):
        for el in ['pos_in', 'pos_out', 'pos_args', 'neg_in', 'neg_out', 'neg_args']:
            shutil.rmtree(d := os.path.split(f"{self.dst_dir}/{self.dst_format.get(el).format(0)}")[0],
                          ignore_errors=True)
            os.makedirs(d, exist_ok=True)
        for el in ['pos_in_files', 'pos_out_files', 'pos_check_files',
                   'neg_in_files', 'neg_out_files', 'neg_check_files']:
            shutil.rmtree(d := os.path.split(f"{self.dst_dir}/{self.dst_format.get(el).format(0, 0)}")[0],
                          ignore_errors=True)
            os.makedirs(d, exist_ok=True)

        self.readme.write("\n## Позитивные тесты:\n")
        self.convert_tests('pos')

        self.readme.write("\n## Негативные тесты:\n")
        self.convert_tests('neg')
        self.readme.close()
