import json
import sys

from src.backend.commands import cmd_command, wsl_path, path_from_wsl_path


class _ProgramValidator:
    def __init__(self, key='--version',
                 prefix: str | list[str] | tuple[str] = '',
                 postfix: str | list[str] | tuple[str] = ''):
        self.key = key
        self.prefix = (prefix,) if isinstance(prefix, str) else prefix
        self.postfix = (postfix,) if isinstance(postfix, str) else postfix


class Program:
    WSL = 1

    def __init__(self, name, win=None, linux=None, mac=None, validator: _ProgramValidator = None):
        self.name = name
        self.win_name = win if win else self.name + '.exe'
        self.linux_name = linux if linux else self.name
        self.mac_name = mac if mac else self.linux_name
        self._existing = dict()
        self._validator = validator

    def win_basic(self):
        return ProgramInstance(self, self.win_name)

    def linux_basic(self):
        return ProgramInstance(self, self.linux_name)

    def existing(self):
        return self._existing.values()

    def set_existing(self, programs: list['ProgramInstance']):
        for program in programs:
            self.add_existing(program, check=False)

    def add_existing(self, program: 'ProgramInstance', check=True):
        valid = True
        if check and isinstance(self._validator, _ProgramValidator):
            valid = False
            try:
                res = program(self._validator.key, timeout=5)
                if res.returncode != 0:
                    raise ValueError
            except Exception as ex:
                pass
            else:
                for el in self._validator.prefix:
                    if res.stdout.startswith(el):
                        for el2 in self._validator.postfix:
                            if res.stdout.endswith(el2):
                                valid = True
                                break
                        break
        if valid:
            self._existing[(program.path, program.virtual_system)] = program
        program.valid = valid
        return valid

    def key(self):
        return f"program_{self.name}"

    def get(self, sm, build=None):
        res = None
        if build:
            res = build.get(self.key(), None)
        if res is None:
            res = sm.get(self.key(), None)
        if res is None:
            res = sm.get_general(self.key(), None)
        if res is None:
            return self.basic()
        return ProgramInstance.from_json(res)

    def basic(self):
        match sys.platform:
            case 'win32':
                return self.win_basic()
            case 'linux':
                return self.linux_basic()
            case _:
                return self.linux_basic()

    @staticmethod
    def program(name, path, vs=0):
        return ProgramInstance(PROGRAMS[name], path, vs)


class ProgramInstance:
    def __init__(self, program, path, virtual_system=0):
        self.program = program
        self.path = path
        self.virtual_system = virtual_system
        self.valid = True

    def vs_args(self):
        vs_args = []
        match self.virtual_system:
            case Program.WSL:
                vs_args = ['wsl', '-e']
        return ' '.join(vs_args)

    def command(self):
        return self.vs_args() + ' ' + self.path

    def __call__(self, args, **kwargs):
        vs_args = []
        match self.virtual_system:
            case Program.WSL:
                vs_args = ['wsl', '-e']

        if isinstance(args, str):
            args = ' '.join(vs_args) + ' ' + self.path + ' ' + args
        else:
            args = vs_args + [self.path] + list(args)
        if 'shell' not in kwargs:
            kwargs['shell'] = True
        return cmd_command(args, **kwargs)

    def name(self):
        match self.virtual_system:
            case Program.WSL:
                return f"(WSL) {self.path}"
            case _:
                return self.path

    def convert_path(self, path):
        match self.virtual_system:
            case Program.WSL:
                return wsl_path(path)
            case _:
                return path

    def recover_path(self, path):
        match self.virtual_system:
            case Program.WSL:
                return path_from_wsl_path(path)
            case _:
                return path

    def to_json(self):
        return json.dumps({
            'program': self.program.name,
            'path': self.path,
            'virtual_system': self.virtual_system,
        })

    @staticmethod
    def from_json(data):
        if isinstance(data, str):
            data = json.loads(data)
        return ProgramInstance(PROGRAMS[data['program']], data['path'], data['virtual_system'])


PROGRAMS = {
    'gcc': Program('gcc', validator=_ProgramValidator(prefix='gcc')),
    'g++': Program('g++', validator=_ProgramValidator(prefix='g++')),
    'gcov': Program('gcov', validator=_ProgramValidator(prefix='gcov')),
    'lcov': Program('lcov', validator=_ProgramValidator(prefix='lcov: LCOV version')),
    'genhtml': Program('genhtml', validator=_ProgramValidator(prefix='genhtml: LCOV version')),
    'python': Program('python', linux='python3', validator=_ProgramValidator(prefix=['python', 'Python'])),
    'python_coverage': Program('python_coverage', win='coverage.exe', linux='coverage',
                               validator=_ProgramValidator(prefix='Coverage.py, version')),
    'bash': Program('bash', validator=_ProgramValidator(prefix='GNU bash, version')),
}
