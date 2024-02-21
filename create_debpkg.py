import os
import shutil
import sys

from src import config

SRC_PATH = f'dist/{config.APP_NAME}' if len(sys.argv) < 2 else sys.argv[1]
DST_APP_PATH = f'dist/debpkg/opt/{config.ORGANISATION_NAME}/{config.APP_NAME}'

shutil.copytree(SRC_PATH, DST_APP_PATH)

os.makedirs('dist/debpkg/usr/share/applications', exist_ok=True)
with open(f'dist/debpkg/usr/share/applications/{config.APP_NAME}.desktop', 'w', encoding='utf-8') as f:
    f.write(f"""[Desktop Entry]
Version={config.APP_VERSION}
Name={config.APP_NAME}
Exec=/opt/{config.ORGANISATION_NAME}/{config.APP_NAME}/{config.APP_NAME}
StartupNotify=true
Terminal=false
Icon=/opt/{config.ORGANISATION_NAME}/{config.APP_NAME}/_internal/icon.png
Type=Application
Categories=Network;WebBrowser;
""")
