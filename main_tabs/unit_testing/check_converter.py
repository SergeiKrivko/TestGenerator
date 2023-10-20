import os
import shutil

from backend.backend_types.unit_test import UnitTest
from backend.backend_types.unit_tests_module import UnitTestsModule
from backend.backend_types.unit_tests_suite import UnitTestsSuite


class CheckConverter:
    def __init__(self, data_path: str, modules: list[UnitTestsModule]):
        self._data_path = data_path

        self._modules = modules

    def _check_tests_count(self):
        for module in self._modules:
            for suite in module.suits():
                for test in suite.tests():
                    return True
        return False

    def convert(self):
        if os.path.isdir(self._data_path):
            shutil.rmtree(self._data_path)
        if not self._check_tests_count():
            return
        os.makedirs(self._data_path, exist_ok=True)
        suits = []
        for module in self._modules:
            if module.has_suits():
                for el in module.suits():
                    suits.append(el.name())
                convert_module(f"{self._data_path}/check_{module.name()}", module)
        self._write_main(suits)

    def _write_main(self, suits):
        with open(f"{self._data_path}/check_main.c", 'w', encoding='utf-8') as file:
            file.write(f"#include <check.h>\n#include <stdlib.h>\n\n")
            for el in suits:
                file.write(f"Suite *{el}_suite(void);\n")
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
    return n_failed;
}}
""")


def convert_test(file, test: UnitTest):
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


def convert_suite(file, suite: UnitTestsSuite):
    file.write('\n\n')
    for test in suite.tests():
        convert_test(file, test)

    file.write(f"""Suite *{suite.name()}_suite(void)
{{
    Suite *s;
    TCase *tc_core;
    s = suite_create("{suite.name()}");
    tc_core = tcase_create("core");
""")
    for test in suite.tests():
        file.write(f"    tcase_add_test(tc_core, {test['name']});\n")
    file.write(f"""    suite_add_tcase(s, tc_core);
    return s;
}}\n\n""")


def convert_module(path, module: UnitTestsModule):
    file = open(path, 'w', encoding='utf-8')
    file.write(f"#include <check.h>\n")
    file.write(f"#include \"{module.name()[:-2]}.h\"\n\n")

    for suite in module.suits():
        file.write(suite.code() + '\n\n')

    for suite in module.suits():
        convert_suite(file, suite)

    file.close()
