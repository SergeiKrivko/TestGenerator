import json
import os.path
import shutil

from backend.commands import read_json, read_file

from language.testing.c import *
from language.testing.cpp import *
from language.testing.python import *
from language.testing.shell import bash_run
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
        # self.clear(bm.sm)
        match self.get('type'):
            case 'C':
                return c_compile(project, self, bm.sm)
            case 'C-lib':
                return c_compile(project, self, bm.sm, lib=True)
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

    def run_preproc(self, project, bm):
        res, errors = True, ''
        for el in self.get('preproc', []):
            match el['type']:
                case 0:
                    build = bm.get_build(el['data'])
                    res, errors = build.execute(project, bm)
            if not res:
                break
        return res, errors

    def run_postproc(self, project, bm):
        res, errors = True, ''
        for el in self.get('postproc', []):
            match el['type']:
                case 0:
                    build = bm.get_build(el['data'])
                    res, errors = build.execute(project, bm)
            if not res:
                break
        return res, errors

    def run(self, project, sm, args=''):
        match self.get('type'):
            case 'C':
                return c_run(project, sm, self, args)
            case 'C++':
                return cpp_run(project, sm, self, args)
            case 'python':
                return python_run(project, sm, self, args)
            case 'python_coverage':
                return python_run_coverage(project, sm, self, args)
            case 'bash':
                return bash_run(project, sm, self, args)
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
            case 'C++':
                return c_collect_coverage(sm, self)
            case 'python_coverage':
                return python_collect_coverage(sm, self)
            case _:
                return None

    def coverage_html(self, project, sm):
        match self.get('type', 'C'):
            case 'C':
                return c_coverage_html(sm, self)
            case 'C++':
                return c_coverage_html(sm, self)
            case 'python_coverage':
                return python_coverage_html(sm, self)
            case _:
                return None

    def execute(self, project, bm):
        res, errors = self.run_preproc(project, bm)
        if not res:
            return res, errors

        res, errors = self.compile(project, bm)
        if not res:
            return res, errors

        if command := self.run(project, bm.sm):
            run_res = cmd_command(command)
            res = not run_res.returncode
            errors = run_res.stdout + run_res.stderr
        if not res:
            return res, errors
        res, errors = self.run_postproc(project, bm)

        return res, errors
