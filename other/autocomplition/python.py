

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
        for name, data in self._get_lib():
            self._std_libs[name] = self._parse_lib(name, data, False)
        self._custom_libs = dict()

        self._current_line = 0
        self._current_symbol = 0

    def parse_main_file(self):
        pass

