import json
import os
import shutil

from src.backend.commands import read_json
from src.config import APP_VERSION


class Project:
    TEST_GENERATOR_DIR = ".TestGenerator"
    SETTINGS_FILE = "TestGeneratorSettings.json"
    DATA_FILE = "TestGeneratorData.json"

    def __init__(self, path, sm, parent=None, makedirs=False, appdata=None):
        self._path = os.path.abspath(path)

        self._sm = sm
        self._data = dict()
        self._settings = dict()
        self._parent = parent
        self._children = dict()
        self._deliting = False
        self._appdata = None if appdata is None else f'{sm.app_data_dir}/{appdata}'

        if makedirs:
            os.makedirs(self.data_path(), exist_ok=True)
            self.create_gitignore()
        elif not os.path.isdir(self.data_path()):
            raise FileNotFoundError

        self.load_settings()
        self['version'] = APP_VERSION

    def name(self):
        if 'name' in self._data and self._data['name'].strip():
            return self._data['name']
        return os.path.basename(self._path)

    def path(self):
        return self._path

    def set_path(self, path):
        self._path = path

    def data_path(self):
        return os.path.join(self._appdata or self._path, Project.TEST_GENERATOR_DIR)

    def children(self) -> dict[str: 'Project']:
        return self._children

    def load_settings(self):
        try:
            self._settings = read_json(os.path.join(self.data_path(), Project.SETTINGS_FILE))
            self._data = read_json(os.path.join(self.data_path(), Project.DATA_FILE))
            self.load_settings_old()
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass

    def load_settings_old(self):
        for key in ['version', 'pos_func_tests', 'neg_func_tests', 'unit_tests']:
            if key in self._settings:
                self._data[key] = self._settings[key]
                self._settings.pop(key)

    def save_settings(self):
        if self._deliting:
            return
        os.makedirs(self.data_path(), exist_ok=True)
        with open(os.path.join(self.data_path(), Project.SETTINGS_FILE), 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._settings, indent=2))
        with open(os.path.join(self.data_path(), Project.DATA_FILE), 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._data, indent=2))

    def __getitem__(self, item):
        if item in self._settings or self._parent is None:
            return self._settings[item]
        return self._parent[item]

    def has_item(self, key):
        return key in self._settings

    def __setitem__(self, key, value):
        self._settings[key] = value
        self.save_settings()

    def get(self, key, default=None):
        if key in self._settings or self._parent is None:
            return self._settings.get(key, default)
        return self._settings.get(key, default)

    def get_data(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        if 'POS' in key or 'NEG' in key:
            raise KeyError
        self._settings[key] = value
        self.save_settings()

    def set_data(self, key, value):
        self._data[key] = value
        self.save_settings()

    def pop(self, key):
        if key in self._settings:
            self._settings.pop(key)
        self.save_settings()

    def pop_data(self, key):
        if key in self._data:
            self._data.pop(key)
        self.save_settings()

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

    def test_temp_file_path(self, file_number=1, binary=False):
        if not self.get('func_tests_in_project', True):
            return f"{self._sm.app_data_dir}/temp_files/temp_{file_number}." \
                   f"{'bin' if binary else 'txt'}"
        return f"{self.temp_dir()}/temp_{file_number}.{'bin' if binary else 'txt'}"

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

    def unit_tests_path(self):
        return os.path.join(self._path, self.get('unit_tests_dir', "unit_tests"))

    def temp_dir(self):
        return os.path.join(self._path, self.get('temp_files_dir', "temp"))

    def create_gitignore(self):
        os.makedirs(self.data_path(), exist_ok=True)
        with open(os.path.join(self.data_path(), ".gitignore"), 'w', encoding='utf-8') as f:
            f.write(f'# Created by TestGenerator\n*\n{Project.SETTINGS_FILE}\n')

    def delete(self, dir=False):
        self._deliting = True
        if isinstance(self._parent, Project):
            self._parent.children().pop(self.path())
        if dir:
            shutil.rmtree(self.path())
        else:
            shutil.rmtree(self.data_path())
