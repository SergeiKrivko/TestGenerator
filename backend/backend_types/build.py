import json
import os.path
import shutil

from backend.commands import read_json, read_file

from language.testing.c import *
from language.testing.cpp import *
from language.testing.python import *
from other.report.markdown_parser import MarkdownParser


class Build:
    def __init__(self, id, path=None):
        self._data = dict() if path is None else read_json(path)
        self.id = id
        self._path = path

    def get(self, key, default=None):
        return self._data.get(key, default)

    def store(self):
        os.makedirs(os.path.split(self._path)[0], exist_ok=True)
        with open(self._path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._data))

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value
        self.store()

    def pop(self, key):
        self._data.pop(key)

    def clear(self, sm):
        temp_dir = f"{sm.temp_dir()}/build{self.id}"
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)

    def compile(self, project, bm):
        self.clear(bm.sm)
        match self.get('type'):
            case 'C':
                return c_compile(project, self, bm.sm)
            case 'C++':
                return cpp_compile(project, self, bm.sm)
            case 'report':
                try:
                    path = self.get('cwd', '') if os.path.isabs(self.get('cwd', '')) else \
                        f"{project.path()}/{self.get('cwd', '')}"
                    file = f"{path}/{self.get('file', '')}"
                    if self.get('output', '').endswith('.pdf'):
                        out_file = f"{bm.sm.temp_dir()}/out.docx"
                        pdf_file = f"{path}/{self.get('output', '')}"
                    else:
                        out_file = f"{path}/{self.get('output', '')}"
                        pdf_file = ''
                    converter = MarkdownParser(bm, read_file(file, ''), out_file, pdf_file)
                    converter.convert()
                except Exception as ex:
                    return False, f"{ex.__class__.__name__}: {ex}"
                return True, ''
            case _:
                return True, ''

    def run_preproc(self):
        pass

    def run(self, project, sm, args=''):
        match self.get('type'):
            case 'C':
                return c_run(project, self, args)
            case 'C++':
                return cpp_run(project, self, args)
            case 'python':
                return python_run(project, self, args)
            case 'python_coverage':
                return python_run_coverage(project, sm, self, args)
            case 'bash':
                return f"{sm.get_general('bash', 'usr/bin/bash')} " \
                       f"\"{os.path.join(project.path(), self.get('file'))}\" {args}"
            case 'script':
                return f"{os.path.join(project.path(), self.get('file'))} {args}"
            case 'command':
                return self.get('command')
            case _:
                return ""

    def collect_coverage(self, project, sm):
        match self.get('type', 'C'):
            case 'C':
                return c_collect_coverage(sm, self)
            case 'python_coverage':
                return python_collect_coverage(sm, self)
            case _:
                return None

    def coverage_html(self, project, sm):
        match self.get('type', 'C'):
            case 'C':
                return c_coverage_html(sm, self)
            case 'python_coverage':
                return python_coverage_html(sm, self)
            case _:
                return None

    def run_postproc(self):
        pass
