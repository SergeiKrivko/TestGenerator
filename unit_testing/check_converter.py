import os.path

from unit_testing.unit_test import UnitTest


class CheckConverter:
    def __init__(self, data_path: str):
        self._data_path = data_path

        self._modules = dict()
        self._headers = []

    def add_module(self, name):
        m = _Module(name, self._data_path)
        self._modules[name] = m
        return m

    def convert(self):
        modules = []
        suits = []
        for key, item in self._modules.items():
            if item.suits():
                modules.append(key)
                suits.extend(item.suits())
                item.convert(self._headers)
        self._write_main(modules, suits)

    def _write_main(self, modules, suits):
        with open(f"{self._data_path}/check_main.c", 'w', encoding='utf-8') as file:
            file.write(f"#include <check.h>\n#include <stdlib.h>\n")
            for el in self._headers:
                file.write(el)
            file.write("\ntypedef Suite *(*suite_array_t)(void);\n\n")
            file.write(f"""int main(void)
{{
    int n_failed = 0;
    SRunner *sr = srunner_create(NULL);
    suite_array_t suite_arr[] = {{{'_suite, '.join(suits)}_suite}};
    int n_suites = {len(suits)};
    for (int i = 0; i < n_suites; i++)
        srunner_add_suite(sr, suite_arr[i]());
    srunner_run_all(sr, CK_VERBOSE);
    n_failed = srunner_ntests_failed(sr);
    srunner_free(sr);
    return (n_failed == 0) ? EXIT_SUCCESS : EXIT_FAILURE;
}}
""")


class _Module:
    def __init__(self, name, path):
        self._name = name
        self._path = f"{path}/check_{self._name}"
        self._path_h = f"{path}/check_{self._name[:-2]}.h"
        self._suits = dict()

    def add_suite(self, name):
        s = _Suite(name)
        self._suits[name] = s
        return s

    def convert(self, headers):
        with open(self._path, 'w', encoding='utf-8') as file:
            file.write(f"#include <check.h>\n")
            file.write(f"#include \"{self._name[:-2]}.h\"\n\n")
            for item in self._suits.values():
                item.convert(file, headers)

    def suits(self):
        return list(self._suits.keys())


class _Suite:
    def __init__(self, name: str):
        self._name = name
        self._tests = []

    def _convert_test(self, file, index):
        test: UnitTest = self._tests[index]
        in_code = '\n    '.join(test['in_code'].split('\n'))
        run_code = '\n    '.join(test['run_code'].split('\n'))
        out_code = '\n    '.join(test['out_code'].split('\n'))
        file.write(f"""START_TEST({test['name']})
{{
    {in_code}
    {run_code}
    {out_code}
}}
END_TEST\n\n""")

    def convert(self, file, headers):
        for i in range(len(self._tests)):
            self._convert_test(file, i)

        headers.append(f"Suite *{self._name}_suite(void);\n")

        file.write(f"""Suite *{self._name}_suite(void)
{{
    Suite *s;
    TCase *tc_core;
    s = suite_create("{self._name}");
    tc_core = tcase_create("core");
""")
        for test in self._tests:
            file.write(f"    tcase_add_test(tc_core, {test['name']});\n")
        file.write(f"""    suite_add_tcase(s, tc_core);
    return s;
}}\n\n""")

    def add_test(self, test: UnitTest):
        self._tests.append(test)
