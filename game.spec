# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import os, pymunk
pymunk_dir = os.path.dirname(pymunk.__file__)
chimpunk_libs = [
    ('chipmunk.dll', os.path.join(pymunk_dir, 'chipmunk.dll'), 'DATA'),
]

a = Analysis(['game.py'],
             pathex=['F:\\Python Projects\\NamelessDungeonCrawler'],
             binaries=[],
             datas=[('resources', 'resources')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='game',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='game')
