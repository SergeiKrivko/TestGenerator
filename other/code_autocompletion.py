from other.lib import words, types


class CodeAutocompletionManager:
    def __init__(self, sm, directory):
        self._sm = sm
        self.dir = directory
        self.text = ''
        self._std_libs = dict()
        for name, data in self._get_lib():
            self._std_libs[name] = self._parse_header_str(name, data, False)
        self._custom_libs = dict()

    def _add_custom_lib(self, lib_name):
        if lib_name not in self._custom_libs:
            self._custom_libs[lib_name] = self._parse_header_file(lib_name, f"{self.dir}/{lib_name}", True)
        else:
            self._custom_libs[lib_name].set_status(_Lib.ON)

    def _turn_libs_off(self):
        for lib in self._std_libs.values():
            lib.set_status(_Lib.OFF)
        for lib in self._custom_libs.values():
            lib.set_status(_Lib.OFF)

    def get(self, text: str, current_line):
        self.text = text
        self._turn_libs_off()
        for el in self._parse_main_file(text, current_line):
            yield str(el)
        for lib in self._std_libs.values():
            if lib.status == _Lib.ON:
                for el in lib.types:
                    yield str(el)
                for el in lib.defines:
                    yield str(el)
                for el in lib.functions:
                    yield str(el)
        for lib in self._custom_libs.values():
            if lib.status == _Lib.ON:
                for el in lib.types:
                    yield str(el)
                for el in lib.defines:
                    yield str(el)
                for el in lib.functions:
                    yield str(el)
        for el in words:
            yield str(el)
        for el in types:
            yield str(el)

    def _parse_include(self, line):
        if line.startswith('#include'):
            for lib in self._std_libs.values():
                if line == f"#include <{lib.name}>":
                    lib.set_status(_Lib.ON)
                    return True
            else:
                if line.startswith("#include \"") and line.endswith("\""):
                    f = line.split()[1].strip('\"')
                    self._add_custom_lib(f)
                    return True
        return False

    def _parse_define(self, line):
        if line.startswith('#define') and len(s := line.split()) >= 2:
            return _CDefine(s[1])

    def _parse_typedef(self, line):
        if line.startswith('typedef') and len(s := line.split()) >= 3:
            s = s[2]
            if '[' in s:
                return _CType(s[:s.index('[')])
            else:
                return _CType(s)

    def _parse_variable(self, line):
        for var_type in types:
            if line.startswith(var_type.strip()) and ' ' in line and line.endswith(";"):
                lst = line[line.index(' ') + 1:-1].split(',')
                for el in lst:
                    el = el.strip().lstrip("*").replace('=', ' ')
                    el = el.replace('[', ' ')
                    if ' ' in el:
                        return _CVariable(el[:el.index(' ')])
                    else:
                        return _CVariable(el)

    def _is_function_header(self, line):
        for func_type in types:
            if line.startswith(func_type) and '(' in line and line.count('(') == line.count(')') and \
                    (line.endswith(');') or line.endswith(")")):
                header = line.replace(func_type, '', 1)
                return header

    def _parse_main_file(self, text: str, current_line):
        current_func = ""
        i = 0
        functions = []
        for line in text.split(self._sm.get('line_sep', '\n')):
            try:
                if not current_func:
                    if self._parse_include(line):
                        continue
                    if r := self._parse_define(line):
                        yield r
                    if r := self._parse_typedef(line):
                        yield r
                    elif header := self._is_function_header(line):
                        yield _CFunctionHeader(header)
                        if not header.endswith(";"):
                            current_func = header
                            functions.append(_CFunction(header, i, i))
                elif line.startswith('}'):
                    functions[-1].stop = i
                    current_func = ""
            except Exception as ex:
                print(f"{ex.__class__.__name__}: {ex}")
            i += 1
        for func in functions:
            if func.start < current_line < func.stop:
                for el in self._parse_function(func):
                    yield el
                break

    def _parse_function(self, func):
        params = func.header[func.header.index("(") + 1:func.header.rindex(")")].split(",")
        try:
            for p in params:
                if ' ' in p:
                    yield _CVariable(p.split()[1].lstrip("*"))
        except:
            pass

        try:
            for line in self.text.split(self._sm.get('line_sep', '\n'))[func.start + 2:func.stop]:
                line = line.strip()
                if r := self._parse_variable(line):
                    yield r
        except:
            pass

    def _parse_header_file(self, name, path: str, custom_lib: bool):
        lib_type = _CustomLib if custom_lib else _StdLib
        lib = lib_type(name, _Lib.ON)
        try:
            with open(path, encoding='utf-8') as header_file:
                for line in header_file:
                    res = self._parse_header(line)
                    if isinstance(res, _CFunctionHeader):
                        lib.functions.append(res)
                    if isinstance(res, _StdLib):
                        lib.std_libs.append(res)
                    if isinstance(res, _CustomLib):
                        lib.custom_libs.append(res)
                    if isinstance(res, _CDefine):
                        lib.defines.append(res)
                    if isinstance(res, _CType):
                        lib.types.append(res)
        except Exception as ex:
            print(f"parse_header_file \"{path}\": {ex.__class__.__name__}: {ex}")
        return lib

    def _parse_header_str(self, name, string: str, custom_lib: bool):
        lib_type = _CustomLib if custom_lib else _StdLib
        lib = lib_type(name, _Lib.ON)
        try:
            for line in string.split('\n'):
                res = self._parse_header(line)
                if isinstance(res, _CFunctionHeader):
                    lib.functions.append(res)
                if isinstance(res, _StdLib):
                    lib.std_libs.append(res)
                if isinstance(res, _CustomLib):
                    lib.custom_libs.append(res)
                if isinstance(res, _CDefine):
                    lib.defines.append(res)
                if isinstance(res, _CType):
                    lib.types.append(res)
        except Exception as ex:
            print(f"parse_header_str \"{string[:10]}...\": {ex.__class__.__name__}: {ex}")
        return lib

    def _parse_header(self, line):
        line = line.strip()
        if not self._parse_include(line):
            if r := self._parse_define(line):
                return r
            if r := self._parse_typedef(line):
                return r
            else:
                for func_type in types:
                    func_type = func_type.strip()
                    if line.startswith(func_type) and line.count('(') == line.count(')') and line.endswith(');'):
                        return _CFunctionHeader(line.replace(func_type, '', 1))

    def _get_lib(self):
        lib_list = self._sm.get_general('lib')
        if isinstance(lib_list, str):
            for lib_info in lib_list.split(';'):
                lib_name, _ = lib_info.split(':')
                lib_data = self._sm.get_general(lib_name)
                if lib_data:
                    yield lib_name, lib_data


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

