import os
import shutil

from backend.backend_types.project import Project
from backend.backend_types.unit_test import UnitTest
from backend.backend_types.unit_tests_module import UnitTestsModule
from backend.backend_types.unit_tests_suite import UnitTestsSuite
from language.languages import languages
from language.utils import get_files


class CheckConverter:
    def __init__(self, data_path: str, project: Project, suites: list[UnitTestsSuite]):
        self._data_path = data_path
        self._project = project

        if not self.check_language():
            return

        self._tests_count = 0
        self._modules = {os.path.basename(path): UnitTestsModule(os.path.basename(path)) for path in get_files(
                project.path(), languages[project.get('language', 'C')].get('files')[0])}
        for suite in suites:
            if os.path.basename(suite.module()) not in self._modules:
                continue
            self._tests_count += len(list(suite.tests()))
            self._modules[os.path.basename(suite.module())].add_suite(suite)

    def check_language(self):
        return self._project.get('language') in ['C']

    def convert(self):
        if os.path.isdir(self._data_path):
            shutil.rmtree(self._data_path)
        if not self.check_language() or not self._tests_count:
            return
        os.makedirs(self._data_path, exist_ok=True)
        suits = []
        for module in self._modules.values():
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
    in_code, run_code, out_code = '', '', ''
    if test.get('in_code') is not None:
        in_code = '\n    ' + '\n    '.join(test['in_code'].split('\n'))
    if test.get('out_code') is not None:
        out_code = '\n\n    ' + '\n    '.join(test['out_code'].split('\n'))
    if test.get('run_code') is not None:
        run_code = '\n\n    ' + '\n    '.join(test['run_code'].split('\n'))
    file.write(f"""START_TEST({test.get('name')})
{{{in_code}{run_code}{out_code}
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
        file.write(f"    tcase_add_test(tc_core, {test.get('name')});\n")
    file.write(f"""    suite_add_tcase(s, tc_core);
    return s;
}}\n""")


def convert_module(path, module: UnitTestsModule):
    file = open(path, 'w', encoding='utf-8')
    file.write(f"#include <check.h>\n")
    file.write(f"#include \"{module.name()[:-2]}.h\"\n\n")

    for suite in module.suits():
        if suite.code().strip():
            file.write(suite.code().strip('\n') + '\n\n\n')

    for suite in module.suits():
        convert_suite(file, suite)

    file.close()
