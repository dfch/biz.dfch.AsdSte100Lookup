# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

import biz.dfch.asdste100vocab as vocab

a = Analysis(
    ["src/main.py"],
    pathex=["./src", "./src/biz"],
    binaries=[],
    datas=[
        ("./src/logging.conf", "./src/"),
        ("./pyproject.toml", "."),
        (
            "./src/biz/dfch/asdste100lookup/data/",
            "./biz/dfch/asdste100lookup/data/",
        ),
        (
            os.path.join(Path(vocab.__file__).parent, "data"),
            "biz/dfch/asdste100vocab/data",
        ),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="AsdSte100Lookup",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
