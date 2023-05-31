import os
import shutil
from json import loads, JSONDecodeError

from PyQt5.QtCore import QThread


class MacrosConverter(QThread):
    def __init__(self, src_dir, dst_dir, dst_format, sm, readme):
        super(MacrosConverter, self).__init__()

        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.dst_format = dst_format
        self.readme = readme

        self.line_sep = sm.get_general('line_sep', '\n')

    def convert_txt(self, text, path):
        os.makedirs(os.path.split(path)[0], exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline=self.line_sep) as f:
            f.write(text)

    def convert_tests(self, tests_type='pos'):
        if not os.path.isdir(f"{self.src_dir}/{tests_type}"):
            return
        for file in os.listdir(f"{self.src_dir}/{tests_type}"):
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
                             f"{self.dst_dir}/{self.dst_format.get(f'{tests_type}_in').format(index + 1)}")
            self.convert_txt(data.get('out', ''),
                             f"{self.dst_dir}/{self.dst_format.get(f'{tests_type}_out').format(index + 1)}")
            if data.get('args', ''):
                self.convert_txt(data.get('args', ''),
                                 f"{self.dst_dir}/{self.dst_format.get(f'{tests_type}_args').format(index + 1)}")

    def run(self):
        for el in ['pos_in', 'pos_out', 'pos_args', 'neg_in', 'neg_out', 'neg_args']:
            shutil.rmtree(d := os.path.split(f"{self.dst_dir}/{self.dst_format.get(el).format(0)}")[0],
                          ignore_errors=True)
            os.makedirs(d, exist_ok=True)

        self.readme.write("\n## Позитивные тесты:\n")
        self.convert_tests('pos')

        self.readme.write("\n## Негативные тесты:\n")
        self.convert_tests('neg')
        self.readme.close()
