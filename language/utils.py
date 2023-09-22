import os


def get_files(path: str, extension: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)
