from src.language.autocomplition.c_lib import words, types
import os


class CodeAutocompletionManager:
    def __init__(self, sm, directory):
        self._sm = sm
        self.dir = directory
        self.text = ''

        self._functions = []
        self._function_definitions = []
        self._types = []
        self._struct_types = []
        self._defines = []

        self._std_libs = dict()
        self.update_libs()
        self._custom_libs = dict()

        self._current_line = 0
        self._current_symbol = 0

    def update_libs(self):
        for name, data in self._get_lib():
            self._std_libs[name] = self._parse_lib(name, data, False)

    def _add_custom_lib(self, lib_name):
        if lib_name not in self._custom_libs:
            self._custom_libs[lib_name] = self._parse_lib_file(lib_name, f"{self.dir}/{lib_name}", True)
        else:
            self._custom_libs[lib_name].set_status(_Lib.ON)

    def _turn_libs_off(self):
        for lib in self._std_libs.values():
            lib.set_status(_Lib.OFF)
        for lib in self._custom_libs.values():
            lib.set_status(_Lib.OFF)

    def full_update(self, text, current_pos):
        self._types.clear()
        self._functions.clear()
        self._struct_types.clear()
        self._defines.clear()
        self._turn_libs_off()
        self._current_line, self._current_symbol = current_pos

        self.text = text
        self._parse_main_file(text)

    def get(self, text: str, current_pos):
        self.text = text
        self._current_line, self._current_symbol = current_pos

        res = []

        line = text.split('\n')[current_pos[0]][:current_pos[1]]
        if line.split():
            line = line.split()[-1]
        line = line.replace('->', '.')
        for func in self._function_definitions:
            if func.start <= self._current_line <= func.stop:
                if len(lst := line.split('.')) == 2:
                    for st in func.struct_variables:
                        if lst[0] == st.name:
                            return st.type.fields, 1

        for el in self._functions:
            res.append(el)
        for el in self._types:
            res.append(el)
        for el in self._defines:
            res.append(el)
        for el in self._struct_types:
            res.append(el)
        for func in self._function_definitions:
            if func.start <= self._current_line <= func.stop:
                for el in func.variables:
                    res.append(el)
                for el in func.struct_variables:
                    res.append(el)
        for lib in self._std_libs.values():
            if lib.status == _Lib.ON:
                for el in lib.types:
                    res.append(el)
                for el in lib.defines:
                    res.append(el)
                for el in lib.functions:
                    res.append(el)
        for lib in self._custom_libs.values():
            if lib.status == _Lib.ON:
                for el in lib.types:
                    res.append(el)
                for el in lib.defines:
                    res.append(el)
                for el in lib.functions:
                    res.append(el)
        for el in words:
            res.append(el)
        for el in types:
            res.append(el)
        return res, 0

    def _parse_include(self, line, custom_lib=None):
        if line.startswith('#include'):
            for lib in self._std_libs.values():
                if line == f"#include <{lib.name}>":
                    lib.set_status(_Lib.ON)
                    if custom_lib:
                        custom_lib.std_libs.append(lib)
                    return True
            else:
                if line.startswith("#include \"") and line.endswith("\""):
                    f = line.split()[1].strip('\"')
                    self._add_custom_lib(f)
                    if custom_lib:
                        custom_lib.custom_libs.append(self._custom_libs[f])
                    return True
        return False

    def _parse_define(self, line):
        if line.startswith('#define') and len(s := line.split()) >= 2:
            return _CDefine(s[1])

    def _parse_typedef(self, line):
        if line.startswith('typedef') and len(s := line.split()) >= 3:
            s = s[2]
            if '[' in s:
                return _CType(s[:s.index('[')].rstrip(';'))
            else:
                return _CType(s.rstrip(';'))

    def _parse_variable(self, line, lib_types=None):
        for var_type in self.get_all_types(lib_types):
            if line.startswith(var_type.strip()) and ' ' in line and line.endswith(";"):
                lst = line[line.index(' ') + 1:-1].split(',')
                for el in lst:
                    el = el.strip().lstrip("*").replace('=', ' ')
                    el = el.replace('[', ' ')
                    if ' ' in el:
                        return _CVariable(el[:el.index(' ')])
                    else:
                        return _CVariable(el)

    def _parse_struct_variable(self, line):
        def get_all_struct_types():
            for t in self._struct_types:
                yield t
            for lib in self._std_libs.values():
                for t in lib.structs:
                    yield t
            for lib in self._custom_libs.values():
                for t in lib.structs:
                    yield t

        for struct_type in get_all_struct_types():
            if (line.startswith(str(struct_type)) and struct_type.typedef or line.startswith(
                    f'struct {struct_type}') and not struct_type.typedef) and ' ' in line and line.endswith(";"):
                line = line.lstrip('struct').strip()
                lst = line[line.index(' ') + 1:-1].split(',')
                for el in lst:
                    el = el.strip().lstrip("*").replace('=', ' ')
                    if ' ' in el:
                        return _CStructVariable(el[:el.index(' ')], struct_type)
                    else:
                        return _CStructVariable(el, struct_type)

    def _is_function_header(self, line):
        for func_type in self.get_all_types():
            if line.startswith(func_type) and '(' in line and line.count('(') == line.count(')') and \
                    (line.endswith(');') or line.endswith(")")):
                header = line.replace(func_type, '', 1)
                return header

    def _parse_main_file(self, text: str):
        current_func = ""
        current_struct = ""
        i = 0
        self._function_definitions.clear()
        for line in text.split(self._sm.line_sep):
            try:
                if current_func:
                    if line.startswith('}'):
                        self._function_definitions[-1].stop = i
                        current_func = ""
                elif current_struct:
                    if line.startswith('}'):
                        current_struct = ""
                    elif r := self._parse_variable(line.strip()):
                        self._struct_types[-1].fields.append(r)
                else:
                    if self._parse_include(line):
                        continue
                    if line.startswith('struct ') or line.startswith('typedef struct '):
                        name = line.lstrip('{').split()[-1].rstrip(';')
                        for st in self._struct_types:
                            if st.name == name:
                                break
                        else:
                            current_struct = name
                            self._struct_types.append(_CStruct(current_struct, [], line.startswith('typedef')))
                    elif r := self._parse_define(line):
                        self._defines.append(r)
                    elif r := self._parse_typedef(line):
                        self._types.append(r)
                    elif header := self._is_function_header(line):
                        self._functions.append(header)
                        if not header.endswith(";"):
                            current_func = header
                            self._function_definitions.append(_CFunction(header, i, i))
            except Exception as ex:
                print(f"{ex.__class__.__name__}: {ex}")
            i += 1
        for func in self._function_definitions:
            self._parse_function(func)

    def _parse_function(self, func):
        params = func.header[func.header.index("(") + 1:func.header.rindex(")")].split(",")
        try:
            for p in params:
                if ' ' in p:
                    func.variables.append(_CVariable(p.split()[1].lstrip("*")))
        except:
            pass

        try:
            for line in self.text.split(self._sm.line_sep)[func.start + 2:func.stop]:
                line = line.strip()
                if r := self._parse_struct_variable(line):
                    func.struct_variables.append(r)
                if r := self._parse_variable(line):
                    func.variables.append(r)
        except Exception as ex:
            print(f"parse_function \"{func.header}\": {ex.__class__.__name__}: {ex}")

    def _parse_lib_file(self, name, path: str, custom_lib: bool):
        with open(path, encoding='utf-8') as file:
            return self._parse_lib(name, file.read(), custom_lib)

    def _parse_lib(self, name, string: str, custom_lib: bool):
        lib_type = _CustomLib if custom_lib else _StdLib
        lib = lib_type(name, _Lib.ON)
        current_struct = ""
        try:
            for line in string.split('\n'):
                line = line.strip()
                if not self._parse_include(line, lib):
                    if current_struct:
                        if line.startswith('}'):
                            current_struct = ""
                        elif r := self._parse_variable(line.strip(), lib.types):
                            lib.structs[-1].fields.append(r)
                    elif line.startswith('struct ') or line.startswith('typedef struct '):
                        name = line.lstrip('{').split()[-1].rstrip(';')
                        for st in self._struct_types:
                            if st.name == name:
                                break
                        else:
                            current_struct = name
                            lib.structs.append(_CStruct(current_struct, [], line.startswith('typedef')))
                    elif r := self._parse_define(line):
                        lib.defines.append(r)
                    elif r := self._parse_typedef(line):
                        lib.types.append(r)
                    else:
                        for func_type in self.get_all_types(lib.types):
                            func_type = func_type.strip()
                            if line.startswith(func_type) and line.count('(') == line.count(')') and line.endswith(
                                    ');'):
                                lib.functions.append(_CFunctionHeader(line.replace(func_type, '', 1)))
        except Exception as ex:
            print(f"parse_header_str \"{string[:10]}...\": {ex.__class__.__name__}: {ex}")
        return lib

    def get_all_types(self, lib_types=None):
        for t in types:
            yield t
        for t in (lib_types if lib_types is not None else self._types):
            yield str(t)

    def _get_lib(self):
        global_libs_dir = f"{self._sm.app_data_dir}/global_libs"
        if os.path.isdir(global_libs_dir):
            for el in os.listdir(global_libs_dir):
                with open(f"{global_libs_dir}/{el}") as f:
                    yield el, f.read()


class _Lib:
    ON = 0
    OFF = 1

    def __init__(self, name, status):
        self.name = name
        self.functions = []
        self.std_libs = []
        self.custom_libs = []
        self.types = []
        self.defines = []
        self.structs = []
        self.status = status

    def set_status(self, status):
        self.status = status
        if status == _Lib.ON:
            for lib in self.std_libs:
                lib.set_status(_Lib.ON)
            for lib in self.custom_libs:
                lib.set_status(_Lib.ON)

    def __str__(self):
        return self.name


class _StdLib(_Lib):
    def __init__(self, name, status):
        super(_StdLib, self).__init__(name, status)


class _CustomLib(_Lib):
    def __init__(self, name, status):
        super(_CustomLib, self).__init__(name, status)


class _CFunctionHeader:
    def __init__(self, header: str):
        self.header = header

    def __str__(self):
        return self.header


class _CFunction:
    def __init__(self, header: str, start: int, stop: int):
        self.header = header
        self.start = start
        self.stop = stop
        self.variables = []
        self.struct_variables = []

    def __str__(self):
        return self.header


class _CVariable:
    def __init__(self, name: str, var_type: str = ''):
        self.name = name
        self.type = var_type

    def __str__(self):
        return self.name


class _CType:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class _CStruct:
    def __init__(self, name: str, fields: list | tuple, typedef: bool):
        self.name = name
        self.fields = fields
        self.typedef = typedef

    def __str__(self):
        return self.name


class _CStructVariable:
    def __init__(self, name: str, struct_type: _CStruct):
        self.name = name
        self.type = struct_type

    def __str__(self):
        return self.name


class _CDefine:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

