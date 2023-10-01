import json
import os


class Build:
    def __init__(self, path):
        self.path = path

        self.name = '-'
        self.language = 'C'
        self.keys = ''
        self.linker_keys = ''
        self.files = set()

        self.load()

    def set_name(self, name):
        self.name = name

    def set_language(self, language):
        self.language = language

    def set_keys(self, keys):
        self.keys = keys

    def set_lkeys(self, keys):
        self.linker_keys = keys

    def set_file_status(self, file, status):
        if status:
            self.files.add(file)
        else:
            self.files.remove(file)

    def load(self):
        try:
            with open(self.path, encoding='utf-8') as f:
                data = json.loads(f.read())
                if not isinstance(data, dict):
                    data = dict()
        except FileNotFoundError:
            data = dict()
        except json.JSONDecodeError:
            data = dict()

        self.set_name(data.get('name', ''))
        self.language = data.get('language', 'C')
        self.files = set(data.get('files', []))
        self.keys = data.get('keys', '')
        self.linker_keys = data.get('linker_keys', '')

    def store(self):
        data = {
            'name': self.name,
            'language': self.language,
            'files': list(self.files),
            'keys': self.keys,
            'linker_keys': self.keys
        }
        os.makedirs(os.path.split(self.path)[0], exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data))
