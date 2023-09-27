import os


def get_files(path: str, extensions: str | list[str]):
    if isinstance(extensions, str):
        extensions = [extensions]
    for root, dirs, files in os.walk(path):
        for file in files:
            for ex in extensions:
                if file.endswith(ex):
                    yield os.path.join(root, file)
