import os
import re
import time

from PyQt5.QtCore import QThread


class PythonObject:
    def __init__(self, name, _class):
        super().__init__()
        self._class = _class
        self.name = name

    def type(self):
        return self._class

    def fields(self):
        return self._class.fields


class PythonType(PythonObject):
    def __init__(self, name, fields):
        super().__init__(name, None)
        self.fields = fields

    def get_all(self, line=-1):
        for el in self.fields:
            yield el

    def get_fields(self):
        for el in self.fields:
            yield el

    def get(self, key, default=None):
        return self.fields.get(key, default)

    def __repr__(self):
        return f"PythonType({self.name})"


MAX_IMPORT_RECURSION = 12
FUNCTION = PythonType('function', dict())
UNKNOWN_CLASS = PythonType('unknown', dict())


class PythonFunction(PythonObject):
    def __init__(self, module, name, header, start):
        super().__init__(name, FUNCTION)
        self.module = module
        self.header = header
        self.start = start
        self.stop = start
        self.lines = []

        self.params = []
        self.variables = dict()

        self.main_indent = 0

    def add_line(self, i, indent, line):
        if self.main_indent == 0:
            self.main_indent = indent
        self.lines.append((i, indent - self.main_indent, line))
        self.stop = max(self.stop, i)

    def add_param(self, param):
        self.params.append(param)

    def parse_header(self):
        if '#' in self.header:
            self.header = self.header[:self.header.index('#')]
        if self.header[-1] == ':':
            self.header.pop()
        if self.header[-1] == ')':
            self.header.pop()
        if self.header[0] == '(':
            self.header.pop(0)

        param = []
        scip = False
        for el in self.header:
            if el == ',':
                self.add_param(''.join(param))
                param.clear()
                scip = False
            elif el == '=':
                scip = True
            elif not scip:
                param.append(el)
        self.add_param(''.join(param))

    def parse(self):
        for i, indent, line in self.lines:
            if len(line) > 2 and line[1] == '=':
                self.variables[line[0]] = self.module.get_object_type(line[2:])

    def get(self, name):
        return self.variables.get(name)

    def get_all(self, line=-1):
        return *self.variables.keys(), *self.params

    def __repr__(self):
        return f"PythonFunction({self.name})"


class PythonClass(PythonObject):
    def __init__(self, module, name, parent, start):
        super().__init__(name, FUNCTION)
        self.module = module
        self.parent = parent
        self.start = start
        self.stop = start
        self.lines = []

        self.fields = dict()
        self.methods = dict()

        self.main_indent = 0

    def parse_fields(self):
        current_function = None
        for i, indent, line in self.lines:
            if not current_function or indent == 0:
                if indent == 0 and line[0] == 'def' and len(line) > 2:
                    current_function = PythonFunction(self.module, line[1], line[2:], i)
                    self.methods[line[1]] = current_function
                elif len(line) > 2 and line[1] == '=':
                    self.fields[line[0]] = self.module.get_object_type(line[2:])
                elif len(line) > 4 and line[0] == 'self' and line[1] == '.' and line[3] == '=':
                    self.fields[line[2]] = self.module.get_object_type(line[4:])
            else:
                current_function.add_line(i, indent, line)
                if len(line) > 4 and line[0] == 'self' and line[1] == '.' and line[3] == '=':
                    self.fields[line[2]] = self.module.get_object_type(line[4:])

        for func in self.methods.values():
            func.parse_header()
            func.parse()

    def add_line(self, i, indent, line):
        if self.main_indent == 0:
            self.main_indent = indent
        self.lines.append((i, indent - self.main_indent, line))
        self.stop = max(self.stop, i)

    def get_all(self, line=-1):
        yield 'self'
        for method in self.methods.values():
            if method.start <= line <= method.stop + 1:
                for el in method.get_all(line):
                    yield el
                break

    def get_fields(self):
        for el in self.fields:
            yield el
        for el in self.methods:
            yield el
        for el in self.parent.get_fields():
            yield el

    def get(self, key, default=None):
        if key == 'self':
            return self
        return self.methods.get(key, self.fields.get(key, self.parent.get(key, default)))

    def __repr__(self):
        return f"PythonClass({self.name})"


class PythonModule(PythonObject):
    def __init__(self, name, text, libs, builtins: dict, modules: dict = None, recursion=0, main=False):
        super().__init__(name, None)
        self.libs = libs
        self.main = main
        self.imported_modules = modules if modules is not None else dict()
        self.builtins = builtins
        self.text = text
        self.recursion = recursion
        self.variables = dict()
        self.imported_variables = dict()
        self.functions = dict()
        self.classes = dict()
        self.modules = dict()

        self.re = re.compile(r"[*]\/|\/[*]|\s+|\w+|\W")
        self.terminate = False
        self.current_module = None

        if not main:
            self.parse_file()

    def _get_lines(self, file=None):
        scip = False
        if file is None:
            for i, line in enumerate(self.text.split('\n')):
                if not line.strip():
                    continue
                if scip:
                    if line.count('"""') % 2 or line.count("'''") % 2:
                        scip = False
                        continue
                if line.count('"""') % 2 or line.count("'''") % 2:
                    scip = True
                    continue
                indent = len(line) - len(line.lstrip())
                split_line = self.re.findall(line.rstrip('\n'))
                res = []
                quote = ""
                string = []
                for j, el in enumerate(split_line):
                    if el.strip():
                        if quote:
                            string.append(el)
                            if el == quote:
                                res.append(''.join(string))
                                string.clear()
                        elif el in ["'", "\"", "'''", "\"\"\""]:
                            quote = el
                            string.append(el)
                        elif el in ['f', 'r', 'b'] and len(split_line) > i + 1 and \
                                split_line[i + 1] in ["'", "\"", "'''", "\"\"\""]:
                            string.append(el)
                        else:
                            res.append(el)
                yield i, indent, res

    def get_object_type(self, line):
        if line[0][0].isdigit():
            if len(line) > 1 and line[1] in ('.', 'e', 'E'):
                return self.get_builtin('float', UNKNOWN_CLASS)
            return self.get_builtin('int', UNKNOWN_CLASS)
        if line[0] in ('True', 'False'):
            return self.get_builtin('bool', UNKNOWN_CLASS)
        if line[0][0] in ['\'', '"']:
            return self.get_builtin('str', UNKNOWN_CLASS)
        if len(line) >= 3:
            if line[0] == '(' and line[2] == ',':
                return self.get_builtin('tuple', UNKNOWN_CLASS)
            if line[0] == '[':
                return self.get_builtin('list', UNKNOWN_CLASS)
            if line[0] == '{' and line[2] == ':':
                return self.get_builtin('dict', UNKNOWN_CLASS)
        return self.get(line[0], UNKNOWN_CLASS)

    def _parse_variable(self, line):
        if line[1] != '=':
            return
        return self.get_object_type(line[2:])

    def parse_file(self):
        if self.main:
            self.variables = self.builtins.copy()
        else:
            self.variables.clear()
        self.functions.clear()
        self.classes.clear()
        new_modules = []
        current_function = None
        function_indent = 0
        for i, indent, line in self._get_lines():
            if self.terminate:
                return
            if not current_function or indent <= function_indent:
                current_function = None
                if len(line) > 2 and line[1] == '=':
                    self.variables[line[0]] = self._parse_variable(line)
                elif len(line) > 3 and line[0] == 'def':
                    current_function = PythonFunction(self, line[1], line[2:], i)
                    function_indent = indent
                    self.functions[line[1]] = current_function
                elif len(line) >= 3 and line[0] == 'class':
                    if len(line) >= 5 and line[3].isidentifier():
                        parent = self.get(line[3], UNKNOWN_CLASS)
                        if not isinstance(parent, PythonClass):
                            parent = UNKNOWN_CLASS
                    else:
                        parent = UNKNOWN_CLASS
                    current_function = PythonClass(self, line[1], parent, i)
                    function_indent = indent
                    self.classes[line[1]] = current_function
                elif indent == 0 and line[0] == 'import' and self.recursion < MAX_IMPORT_RECURSION:
                    lst = []
                    name = ''
                    for j in range(1, len(line)):
                        if line[j] == 'as':
                            if len(line) > j + 1:
                                name = line[j + 1]
                            break
                        elif line[j].isidentifier():
                            lst.append(line[j])
                            name = line[j]
                    new_modules.append(name)
                    if lst and name not in self.modules:
                        for directory in self.libs:
                            for path in [f"{directory}/{'/'.join(lst)}.py",
                                         f"{directory}/{'/'.join(lst)}/__init__.py"]:
                                if path in self.imported_modules:
                                    self.modules[name] = self.imported_modules[path]
                                    break
                                elif os.path.isfile(path):
                                    with open(path, encoding='utf-8') as f:
                                        self.current_module = PythonModule(name, f.read(), self.libs, self.builtins,
                                                                           self.imported_modules, self.recursion + 1)
                                        self.modules[name] = self.current_module
                                        self.imported_modules[path] = self.modules[name]
                                    break

                elif indent == 0 and line[0] == 'from' and self.recursion < MAX_IMPORT_RECURSION:
                    path_list = []
                    names = []
                    flag = False
                    for j in range(1, len(line)):
                        if line[j] == 'import':
                            flag = True
                        elif line[j].isidentifier():
                            if flag:
                                names.append(line[j])
                            else:
                                path_list.append(line[j])
                    if path_list:
                        for directory in self.libs:
                            for path in [f"{directory}/{'/'.join(path_list)}.py",
                                         f"{directory}/{'/'.join(path_list)}.pyi",
                                         f"{directory}/{'/'.join(path_list)}/__init__.py"]:
                                if os.path.isfile(path):
                                    with open(path, encoding='utf-8') as f:
                                        module = self.imported_modules.get(path, None)
                                        for el in names:
                                            if el in self.imported_variables:
                                                self.variables[el] = self.imported_variables[el]
                                            else:
                                                if module is None:
                                                    self.current_module = PythonModule('', f.read(), self.libs, self.builtins,
                                                                          self.imported_modules, self.recursion + 1)
                                                    module = self.current_module
                                                self.variables[el] = module.get(el, UNKNOWN_CLASS)
                                                self.imported_variables[el] = self.variables[el]
            else:
                current_function.add_line(i, indent, line)

        for module in list(self.modules.keys()):
            if module not in new_modules:
                self.modules.pop(module)

        for var in list(self.imported_variables.keys()):
            if var not in self.variables:
                self.imported_variables.pop(var)

        if self.main:
            for func in self.functions.values():
                if self.terminate:
                    return
                func.parse_header()
                func.parse()

        for func in self.classes.values():
            if self.terminate:
                return
            func.parse_fields()

    def stop(self):
        self.terminate = True
        if self.current_module:
            self.current_module.stop()

    def get(self, key, default=None):
        return self.functions.get(key, self.classes.get(key, self.variables.get(
            key, self.modules.get(key, self.builtins.get(key, default)))))

    def get_builtin(self, key, default=None):
        return self.builtins.get(key, self.get(key, default))

    def get_all(self, line):
        for el in self.variables:
            yield el
        for el in self.functions:
            yield el
        for el in self.classes:
            yield el
        for el in self.modules:
            yield el


class CodeAutocompletionManager(QThread):
    def __init__(self, sm, directory):
        super().__init__()
        self._sm = sm
        self.dir = directory

        self._variables = dict()
        self._functions = dict()
        self._classes = dict()

        self._std_libs = dict()
        # for name, data in self._get_lib():
        #     self._std_libs[name] = self._parse_lib(name, data, False)
        self._custom_libs = dict()

        self._current_line = 0
        self._current_symbol = 0

        self.re = re.compile(r"[*]\/|\/[*]|\s+|\w+|\W")
        self.keywords = ('def', 'class', 'if', 'elif', 'else', 'while', 'for', 'in', 'is', 'try', 'except', 'finally',
                         'None', 'True', 'False', 'pass', 'and', 'or', 'not', 'lambda', 'import', 'from', 'as',
                         'return', 'yield', 'global', 'nonlocal', 'del', 'with', 'raise')
        lib_path1 = f"{os.path.split(self._sm.get('python', ''))[0]}/Lib"
        lib_path2 = f"{lib_path1}/site-packages"
        lib_path3 = f"{os.path.split(os.path.split(self._sm.get('python', ''))[0])[0]}/Lib"
        lib_path4 = f"{lib_path3}/site-packages"
        if os.path.isfile(f"{self._sm.app_data_dir}/global_libs/builtins.py"):
            with open(f"{self._sm.app_data_dir}/global_libs/builtins.py", encoding='utf-8') as f:
                self.builtins = PythonModule('__builtins__', f.read(), [], dict())
        else:
            self.builtins = PythonModule('__builtins__', '', [], dict())

        builtins = dict()
        for el in self.builtins.get_all(-1):
            builtins[el] = self.builtins.get(el)

        self.main = PythonModule('__main__', '', [self.dir, lib_path1, lib_path2, lib_path3, lib_path4,
                                                  f"{self._sm.app_data_dir}/global_libs",
                                                  f"{self._sm.app_data_dir}/custom_libs"], builtins, main=True)
        self.parsed = False

    def run(self):
        self.parsed = True
        time.sleep(0.01)
        self.main.parse_file()

    def terminate(self):
        if not self.isFinished():
            self.stop()
            super().terminate()

    def update_libs(self):
        pass

    def stop(self):
        self.main.stop()

    def full_update(self, text, current_pos):
        self.main.text = text
        self._current_line, self._current_symbol = current_pos
        if not self.parsed:
            self.start()
            return
        if not self.isFinished():
            return
        self.main.parse_file()

    def parse_current_line(self, line):
        line = self.re.findall(line)
        if len(line) == 0:
            return

        if line[-1] != '.':
            line.pop()
        lst = []
        for i in range(-1, -len(line) - 1, -2):
            if line[i] != '.':
                break
            if line[i - 1].isidentifier():
                lst.insert(0, line[i - 1])
        if len(lst) == 0:
            return None

        for objects_list in [self.main.functions, self.main.classes]:
            for func in objects_list.values():
                if func.start <= self._current_line <= func.stop + 1 and (obj := func.get(lst[0])):
                    for i in range(1, len(lst)):
                        obj = obj.get(lst[i])
                        if obj is None:
                            return []
                    if isinstance(obj, PythonClass):
                        return obj.get_fields()
                    return []
        else:
            if obj := self.main.get(lst[0]):
                for i in range(1, len(lst)):
                    obj = obj.get(lst[i])
                    if obj is None:
                        return []
                if isinstance(obj, PythonClass):
                    return obj.get_fields()
                if isinstance(obj, PythonModule):
                    return obj.get_all(-1)
        return

    def get(self, text: str, current_pos):
        if not self.parsed:
            self.start()
            return [], 0
        if not self.isFinished():
            return [], 0
        self._current_line, self._current_symbol = current_pos
        lst = []
        if (res := self.parse_current_line(text.split('\n')[self._current_line][:self._current_symbol])) is not None:
            return res, 1
        for func in self.main.functions.values():
            if func.start <= self._current_line <= func.stop + 1:
                lst = list(func.get_all(self._current_line))
        else:
            for cls in self.main.classes.values():
                if cls.start <= self._current_line <= cls.stop + 1:
                    lst = list(cls.get_all(self._current_line))
        return [*self.builtins.get_all(self._current_line), *self.main.get_all(self._current_line), *self.keywords,
                *lst], 0
