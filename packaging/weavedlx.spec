# PyInstaller Spec File for yt-dlp GUI Backend
# Usage: pyinstaller weavedlx.spec

import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# 隠しモジュール
hiddenimports = [
    'fastapi',
    'uvicorn',
    'sqlalchemy',
    'croniter',
    'pydantic',
    'dotenv',
]

# データファイル
datas = [
    # SQLAlchemy dialect
    (os.path.join('lib', 'python', 'site-packages', 'sqlalchemy'), 'sqlalchemy'),
    # プロジェクト設定ファイル
    ('backend', 'backend'),
]

a = Analysis(
    ['backend/app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
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
    name='weavedlx-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='weavedlx-backend',
)
