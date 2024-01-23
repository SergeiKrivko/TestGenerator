import os
import shutil

import config

with open(r"data/setup.iss", encoding='utf-8') as f:
    text = f.read()

    index = text.index('#define MyAppVersion ') + len('#define MyAppVersion ')
    text = text[:index] + f'"{config.APP_VERSION}"' + text[index:][text[index:].index('\n'):]

with open(r"data/setup.iss", 'w', encoding='utf-8') as f:
    f.write(text)

if os.path.isdir(r"..\dist\TestGenerator\PyQt6\Qt5"):
    shutil.rmtree(r"..\dist\TestGenerator\PyQt6\Qt5")
    for el in os.listdir(r"..\venv\Lib\site-packages\PyQt6\Qt6"):
        if el == 'bin':
            continue
        shutil.copytree(fr"..\venv\Lib\site-packages\PyQt6\Qt6\{el}",
                        fr"..\dist\TestGenerator\PyQt6\Qt6\{el}")
