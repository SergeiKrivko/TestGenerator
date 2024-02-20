import json
import os.path
import shutil
from uuid import UUID

from src.backend.commands import read_json, read_file

from src.language.testing.c import *
from src.language.testing.cpp import *
from src.language.testing.python import *
from src.language.testing.shell import bash_run
from src.other.report.markdown_parser import MarkdownParser


class Build:
    def __init__(self, id: UUID, path=None):
        self._data = dict() if path is None else read_json(path)
        self._id = id
        self._path = path

    @property
    def type(self):
        return self.get('type')

    @property
    def id(self):
        return self._id

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

    def temp_dir(self, sm):
        return f"{sm.temp_dir()}/build-{self.id}"

    def clear(self, sm):
        temp_dir = self.temp_dir(sm)
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)

    def compile(self, project, bm):
        # self.clear(bm.sm)
        match self.get('type'):
            case 'C':
                return c_compile(project, self, bm._sm)
            case 'C-lib':
                return c_compile(project, self, bm._sm, lib=True)
            case 'C++':
                return cpp_compile(project, self, bm._sm)
            case 'report':
                try:
                    path = self.get('cwd', '') if os.path.isabs(self.get('cwd', '')) else \
                        f"{project.path()}/{self.get('cwd', '')}"
                    file = f"{path}/{self.get('file', '')}"
                    if self.get('output', '').endswith('.pdf'):
                        out_file = f"{bm._sm.temp_dir()}/out.docx"
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
                    build = bm.builds.get(el['data'])
                    res, errors = build.execute(project, bm)
            if not res:
                break
        return res, errors

    def run_postproc(self, project, bm):
        res, errors = True, ''
        for el in self.get('postproc', []):
            match el['type']:
                case 0:
                    build = bm.builds.get(el['data'])
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
        if not self.get('coverage'):
            return None
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
        if not self.get('coverage'):
            return None
        match self.get('type', 'C'):
            case 'C':
                return c_coverage_html(sm, self)
            case 'C++':
                return c_coverage_html(sm, self)
            case 'python_coverage':
                return python_coverage_html(sm, self)
            case _:
                return None

    def clear_coverage(self, sm):
        match self.get('type', 'C'):
            case 'C':
                remove_files(self.temp_dir(sm), ['.gcda', '.gcov', 'coverage.info'])

    def execute(self, project, bm):
        res, errors = self.run_preproc(project, bm)
        if not res:
            return res, errors

        res, errors = self.compile(project, bm)
        if not res:
            return res, errors

        if command := self.run(project, bm._sm):
            run_res = cmd_command(command)
            res = not run_res.returncode
            errors = run_res.stdout + run_res.stderr
        if not res:
            return res, errors
        res, errors = self.run_postproc(project, bm)

        return res, errors
