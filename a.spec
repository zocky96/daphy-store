from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\kivygui\\new'],
             binaries=[],
             datas=[],
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

a.datas += [('Code\a.kv', 'C:\\kivygui\\new\\libs\\uix\\kv\\a.kv', 'DATA'),('Code\b.kv', 'C:\\kivygui\\new\\libs\\uix\\kv\\b.kv', 'DATA'),('Code\c.kv', 'C:\\kivygui\\new\\libs\\uix\\kv\\c.kv', 'DATA'),('Code\d.kv', 'C:\\kivygui\\new\\libs\\uix\\kv\\d.kv', 'DATA'),('Code\e.kv', 'C:\\kivygui\\new\\libs\\uix\\kv\\e.kv', 'DATA'),('Code\f.kv', 'C:\\kivygui\\new\\libs\\uix\\kv\\f.kv', 'DATA'),('Code\g.kv', 'C:\\kivygui\\new\\libs\\uix\\kv\\g.kv', 'DATA'),('Code\h.kv', 'C:\\kivygui\\new\\libs\\uix\\kv\\h.kv', 'DATA'),('Code\i.kv', 'C:\\kivygui\\new\\libs\\uix\\kv\\i.kv', 'DATA'),('Code\j.kv', 'C:\\kivygui\\new\\libs\\uix\\kv\\j.kv', 'DATA')]


exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='daphy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, Tree('C:\\kivygui\\new\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='daphy')
