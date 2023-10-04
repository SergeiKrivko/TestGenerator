import json
import os
import shutil


class Project:
    TEST_GENERATOR_DIR = ".TestGenerator"
    SETTINGS_FILE = "TestGeneratorSettings.json"

    def __init__(self, path, sm, parent=None, makedirs=False, load=False):
        self._path = os.path.abspath(path)
        sm.all_projects[self._path] = self

        if makedirs:
            os.makedirs(os.path.join(self._path, Project.TEST_GENERATOR_DIR))
        elif not os.path.isdir(os.path.join(self._path, Project.TEST_GENERATOR_DIR)):
            raise FileNotFoundError

        self._sm = sm
        self._data = dict()
        self._parent = parent
        self._children = dict()

        if load:
            self.load_settings()
            self.load_projects()

        self.load_settings()

    def name(self):
        if 'name' in self._data:
            return self['name']
        return os.path.basename(self._path)

    def path(self):
        return self._path

    def set_path(self, path):
        self._path = path

    def data_path(self):
        return os.path.join(self._path, Project.TEST_GENERATOR_DIR)

    def children(self) -> dict[str: 'Project']:
        return self._children

    def load_projects(self):
        if self._parent is None:
            self._search_parent()
        self._search_children(self._path)

    def _search_parent(self):
        path = self._path
        while True:
            path, name = os.path.split(path)
            if not name:
                break
            if os.path.isdir(os.path.join(path, Project.TEST_GENERATOR_DIR)):
                if path in self._sm.all_projects:
                    self._parent = self._sm.all_projects[path]
                else:
                    self._parent = Project(path, self._sm, load=True)
                break

    def _search_children(self, path):
        for el in os.listdir(path):
            pp = os.path.join(path, el)
            if os.path.isdir(pp):
                if os.path.isdir(os.path.join(pp, Project.TEST_GENERATOR_DIR)):
                    if pp in self._sm.all_projects:
                        self._children[pp] = self._sm.all_projects[pp]
                    else:
                        self._children[pp] = Project(pp, self._sm, self, load=True)
                else:
                    self._search_children(pp)

    def load_settings(self):
        try:
            with open(os.path.join(self.data_path(), Project.SETTINGS_FILE), encoding='utf-8') as f:
                self._data = json.loads(f.read())
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass

    def save_settings(self):
        os.makedirs(self._path, exist_ok=True)
        with open(os.path.join(self.data_path(), Project.SETTINGS_FILE), 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._data, indent=2))

    def __getitem__(self, item):
        if item in self._data or self._parent is None:
            return self._data[item]
        return self._parent[item]

    def has_item(self, key):
        return key in self._data

    def __setitem__(self, key, value):
        self._data[key] = value

    def get(self, key, default=None):
        if key in self._data or self._parent is None:
            return self._data.get(key, default)
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value

    def pop(self, key):
        if key in self._data:
            self._data.pop(key)

    def get_child(self, name):
        return self._children[name]

    def add_child(self, path):
        if not os.path.isabs(path):
            path = os.path.join(self._path, path)
        self._children[path] = Project(path, self._sm, parent=self, makedirs=True)

    def test_in_path(self, test_type, number):
        if not self.get('func_tests_in_project', True):
            return f"{self.data_path()}/func_tests_data/{test_type}_{number}_in.txt"
        return os.path.join(self._path, self.get(
            'stdin_pattern', "func_tests/data/{test_type}_{number:0>2}_in.txt").format(
            test_type=test_type, number=number + 1))

    def test_out_path(self, test_type, number):
        if not self.get('func_tests_in_project', True):
            return f"{self.data_path()}/func_tests_data/{test_type}_{number}_out.txt"
        return os.path.join(self._path, self.get(
            'stdout_pattern', "func_tests/data/{test_type}_{number:0>2}_out.txt").format(
            test_type=test_type, number=number + 1))

    def test_args_path(self, test_type, number):
        if not self.get('func_tests_in_project', True):
            return f"{self.data_path()}/func_tests_data/{test_type}_{number}_args.txt"
        return os.path.join(self._path, self.get(
            'args_pattern', "func_tests/data/{test_type}_{number:0>2}_args.txt").format(
            test_type=test_type, number=number + 1))

    def test_in_file_path(self, test_type, number, file_number=1, binary=False):
        if not self.get('func_tests_in_project', True):
            return f"{self._sm.app_data_dir}/temp_files/{test_type}_{number}_fin{file_number}." \
                   f"{'bin' if binary else 'txt'}"
        return os.path.join(self._path, self.get(
            'fin_pattern', "func_tests/data_files/{test_type}_{number:0>2}_in{index}.{extension}").format(
            test_type=test_type, number=number + 1, index=file_number + 1, extension=('bin' if binary else 'txt')))

    def test_out_file_path(self, test_type, number, file_number=1, binary=False):
        if not self.get('func_tests_in_project', True):
            return f"{self._sm.app_data_dir}/temp_files/{test_type}_{number}_fout{file_number}." \
                   f"{'bin' if binary else 'txt'}"
        return os.path.join(self._path, self.get(
            'fout_pattern', "func_tests/data_files/{test_type}_{number:0>2}_out{index}.{extension}").format(
            test_type=test_type, number=number + 1, index=file_number + 1, extension=('bin' if binary else 'txt')))

    def test_check_file_path(self, test_type, number, file_number=1, binary=False):
        if not self.get('func_tests_in_project', True):
            return f"{self._sm.app_data_dir}/temp_files/{test_type}_{number}_fcheck{file_number}." \
                   f"{'bin' if binary else 'txt'}"
        return os.path.join(self._path, self.get(
            'fcheck_pattern', "func_tests/data_files/{test_type}_{number:0>2}_check{index}.{extension}").format(
            test_type=test_type, number=number + 1, index=file_number + 1, extension=('bin' if binary else 'txt')))

    def readme_path(self):
        if not self.get('func_tests_in_project', True):
            return f"{self.data_path()}/func_tests_readme.md"
        return os.path.join(self._path, self.get('readme_pattern', "func_tests/readme.md"))

    def create_gitignore(self):
        os.makedirs(self.data_path(), exist_ok=True)
        with open(os.path.join(self.data_path(), ".gitignore"), 'w', encoding='utf-8') as f:
            f.write('# Created by TestGenerator\n*\n')

    def delete(self, dir=False):
        if dir:
            shutil.rmtree(self.path())
        else:
            shutil.rmtree(self.data_path())
