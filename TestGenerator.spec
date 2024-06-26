# -*- mode: python ; coding: utf-8 -*-


import os
import sys

block_cipher = None
lib_path = r"venv\Lib\site-packages" if sys.platform == 'win32' else "venv/lib/python3.11/site-packages"

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[(os.path.abspath(f"{lib_path}/PyQtUIkit/fonts"), "PyQtUIkit/fonts"),
           (os.path.abspath("assets"), "assets"),
           (f"{lib_path}/pymorphy3_dicts_ru/data", r"pymorphy3_dicts_ru/data"), ],
    hiddenimports=['StdioBridge.client'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TestGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/icon.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TestGenerator',
)

app = BUNDLE(
    coll,
    name='TestGenerator.app',
    icon='assets/icon-mac.icns',
    bundle_identifier=None,
    info_plist={
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeExtension': [ext],
                'CFBundleTypeIconFile': 'icon-mac.icns',
                'CFBundleTypeRole': 'Editor'
            } for ext in {'py', 'c', 'cpp', 'h', 'txt', 'json', 'html', 'css', 'js', 'ts', 'cs', 'java', 'asm', 'xml',
                          'yaml', 'yml', 'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'md', 't2b', 'svg', 'sh', 'cmd',
                          'bat', 'ps1', 'hpp'}
        ]
    })
