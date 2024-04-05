# -*- mode: python ; coding: utf-8 -*-

import sys

# Define platform-specific data tuples
if sys.platform.startswith('win'):
    tkdnd_path = 'E:/Project/PyCharm/FlacToWavConverter/venv/Lib/site-packages/tkdnd/tkdnd/win64/'
    datas = [(tkdnd_path, 'tkdnd')]
elif sys.platform.startswith('darwin'):
    tkdnd_path = 'E:/Project/PyCharm/FlacToWavConverter/venv/Lib/site-packages/tkdnd/tkdnd/osx64/'
    datas = [(tkdnd_path, 'tkdnd')]
elif sys.platform.startswith('linux'):
    tkdnd_path = 'E:/Project/PyCharm/FlacToWavConverter/venv/Lib/site-packages/tkdnd/tkdnd/linux64/'
    datas = [(tkdnd_path, 'tkdnd')]
else:
    datas = []

a = Analysis(
    ['main.py'],
    pathex=['E:\Project\PyCharm\FlacToWavConverter\venv\Lib\site-packages\pydub'],
    binaries=[],
    datas=datas,
    hiddenimports=['pydub'],  # Add 'pydub' here
    hookspath=[],
    hooksconfig={},
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
