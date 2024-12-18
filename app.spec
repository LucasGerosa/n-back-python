# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

#pyinstaller app.spec --distpath C:\Users\Lucas\Downloads\nback -y.

vlc_libs = collect_dynamic_libs('vlc')

# Manually add VLC plugins folder
vlc_plugins = [
    (os.path.join('C:/Program Files/VideoLAN/VLC/plugins'), 'plugins')
]

a = Analysis(
    ['source\\app.py'],
    pathex=['source'],
    #binaries=[('ffmpeg/bin/ffmpeg.exe', 'ffmpeg/bin/'), ('ffmpeg/bin/ffprobe.exe', 'ffmpeg/bin/')],
    binaries=vlc_libs + vlc_plugins,
    datas=[
        ('input/piano/*.mp3', 'input/piano/'), 
        #('input/guitar/*.mp3', 'input/guitar/'), 
        ('settings.ini', '.'),  # Add the settings.ini file to the root of the output directory
    ],
    hiddenimports=['simpleaudio'],
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
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon= r"C:\Users\Lucas\GitHub\n-back-python\build\n-back_logo.ico",
    contents_directory=''
)

import os
import glob

translations_path = 'translations'
for root, dirs, files in os.walk(translations_path):
    for file in files:
        src = os.path.join(root, file)
        dst = os.path.join(translations_path, os.path.relpath(src, translations_path))
        a.datas.append((src, dst, 'DATA'))

# Add static folder and its contents
static_path = 'static'
for root, dirs, files in os.walk(static_path):
    for file in files:
        src = os.path.join(root, file)
        dst = os.path.join(static_path, os.path.relpath(src, static_path))
        a.datas.append((src, dst, 'DATA'))


coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
