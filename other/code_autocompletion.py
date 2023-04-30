from other.lib import words, types


class CodeAutocompletionManager:
    def __init__(self, sm, directory):
        self.sm = sm
        self.dir = directory
        self.text = ''
        self.std_libs = dict()
        for name, data in self.get_lib():
            self.std_libs[name] = self.parse_header_str(name, data)
        self.custom_libs = dict()

    def add_custom_lib(self, lib_name):
        if lib_name not in self.custom_libs:
            self.custom_libs[lib_name] = self.parse_header_file(lib_name, f"{self.dir}/{lib_name}")
        else:
            self.custom_libs[lib_name].set_status(Lib.ON)

    def turn_libs_off(self):
        for lib in self.std_libs.values():
            lib.set_status(Lib.OFF)
        for lib in self.custom_libs.values():
            lib.set_status(Lib.OFF)

    def get(self, text: str, current_line):
        self.text = text
        self.turn_libs_off()
        for el in self.parse_main_file(text, current_line):
            yield el
        for lib in self.std_libs.values():
            if lib.status == Lib.ON:
                for el in lib.data:
                    yield el
        for lib in self.custom_libs.values():
            if lib.status == Lib.ON:
                for el in lib.data:
                    yield el
        for el in words:
            yield el
        for el in types:
            yield el

    def parse_main_file(self, text: str, current_line):
        current_func = ""
        i = 0
        functions = []
        for line in text.split(self.sm.get('line_sep', '\n')):
            try:
                if not current_func:
                    if line.startswith('#include'):
                        for lib in self.std_libs.values():
                            if line == f"#include <{lib.name}>":
                                lib.set_status(Lib.ON)
                        else:
                            if line.startswith("#include \"") and line.endswith("\""):
                                f = line.split()[1].strip('\"')
                                self.add_custom_lib(f)
                                continue
                    if line.startswith('#define') and len(s := line.split()) >= 2:
                        yield s[1]
                    elif line.startswith('typedef') and len(s := line.split()) >= 3:
                        s = s[2]
                        if '[' in s:
                            yield s[:s.index('[')]
                        else:
                            yield s
                    else:
                        for func_type in types:
                            if line.startswith(func_type) and '(' in line and line.count('(') == line.count(')') and \
                                    (line.endswith(');') or line.endswith(")")):
                                header = line.replace(func_type, '', 1)
                                yield header
                                if not header.endswith(";"):
                                    current_func = header
                                    functions.append(CFunction(header, i, i))
                elif line.startswith('}'):
                    functions[-1].stop = i
                    current_func = ""
            except Exception as ex:
                print(f"{ex.__class__.__name__}: {ex}")
            i += 1
        for func in functions:
            if func.start < current_line < func.stop:
                for el in self.parse_function(func):
                    yield el
                break

    def parse_function(self, func):
        params = func.header[func.header.index("(") + 1:func.header.rindex(")")].split(",")
        try:
            for p in params:
                if ' ' in p:
                    yield p.split()[1].lstrip("*")
        except:
            pass

        try:
            for line in self.text.split(self.sm.get('line_sep', '\n'))[func.start + 2:func.stop]:
                line = line.strip()
                for var_type in types:
                    if line.startswith(var_type.strip()) and ' ' in line and line.endswith(";"):
                        lst = line[line.index(' ') + 1:-1].split(',')
                        for el in lst:
                            el = el.strip().lstrip("*").replace('=', ' ')
                            el = el.replace('[', ' ')
                            if ' ' in el:
                                yield el[:el.index(' ')]
                            else:
                                yield el
        except:
            pass

    def parse_header_file(self, name, path):
        lib = Lib(name, [], Lib.ON, [], [])
        try:
            with open(path, encoding='utf-8') as header_file:
                for line in header_file:
                    res, std_lib, custom_lib = self.parse_header(line)
                    if res:
                        lib.data.append(res)
                    if std_lib:
                        lib.std_libs.append(std_lib)
                    if custom_lib:
                        lib.custom_libs.append(custom_lib)
        except Exception as ex:
            print(f"parse_header_file \"{path}\": {ex.__class__.__name__}: {ex}")
        return lib

    def parse_header_str(self, name, string: str):
        lib = Lib(name, [], Lib.ON, [], [])
        try:
            for line in string.split('\n'):
                res, std_lib, custom_lib = self.parse_header(line)
                if res:
                    lib.data.append(res)
                if std_lib:
                    lib.std_libs.append(std_lib)
                if custom_lib:
                    lib.custom_libs.append(custom_lib)
        except Exception as ex:
            print(f"parse_header_str \"{string[:10]}...\": {ex.__class__.__name__}: {ex}")
        return lib

    def parse_header(self, line):
        line = line.strip()
        for lib in self.std_libs.values():
            if line == f"#include <{lib.name}>":
                lib.set_status(Lib.ON)
                return None, self.std_libs[lib.name], None
        else:
            if line.startswith("#include \"") and line.endswith("\""):
                f = line.split()[1].strip('\"')
                self.add_custom_lib(f)
                return None, None, self.custom_libs[f]
            if line.startswith('#define') and len(s := line.split()) == 3:
                return s[1], None, None
            elif line.startswith('typedef') and len(s := line.split()) >= 3:
                s = s[2]
                if '[' in s:
                    return s[:s.index('[')], None, None
                else:
                    return s, None, None
            else:
                for func_type in types:
                    func_type = func_type.strip()
                    if line.startswith(func_type) and line.count('(') == line.count(')') and line.endswith(');'):
                        return line.replace(func_type, '', 1), None, None
        return None, None, None

    def get_lib(self):
        # for lib in os.listdir("lib"):
        #     if lib not in ("words", "types") and lib.endswith(".txt"):
        #         yield lib.replace(".txt", ".h")
        lib_list = self.sm.get_general('lib')
        if isinstance(lib_list, str):
            for lib_info in lib_list.split(';'):
                lib_name, _ = lib_info.split(':')
                lib_data = self.sm.get_general(lib_name)
                if lib_data:
                    yield lib_name, lib_data


class Lib:
    ON = 0
    OFF = 1

    def __init__(self, name, data, status, std_libs, custom_libs):
        self.name = name
        self.data = data
        self.std_libs = std_libs
        self.custom_libs = custom_libs
        self.status = status

    def set_status(self, status):
        self.status = status
        if status == Lib.ON:
            for lib in self.std_libs:
                lib.set_status(Lib.ON)
            for lib in self.custom_libs:
                lib.set_status(Lib.ON)

    def __str__(self):
        return self.name


class CFunction:
    def __init__(self, header, start, stop):
        self.header = header
        self.start = start
        self.stop = stop
