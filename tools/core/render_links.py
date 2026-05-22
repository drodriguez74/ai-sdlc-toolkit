#!/usr/bin/env python3
"""Helper for symlink/copy operations.

The actual link farm logic lives inline in refresh-project-links.sh (it's
simpler that way for a script-driven flow). This file exists for the rare case
where another script needs to reuse the helper.
"""
from __future__ import annotations
import argparse
import os
import pathlib
import shutil
import sys


def install(source: pathlib.Path, dest: pathlib.Path, mode: str = "symlink") -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        if dest.is_symlink() or dest.is_file():
            dest.unlink()
        else:
            shutil.rmtree(dest)
    if mode == "symlink":
        try:
            os.symlink(source, dest)
            return "symlink"
        except OSError:
            pass
    if source.is_dir():
        shutil.copytree(source, dest)
    else:
        shutil.copy2(source, dest)
    return "copy"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("dest")
    parser.add_argument("--mode", default="symlink", choices=["symlink", "copy"])
    args = parser.parse_args()
    result = install(pathlib.Path(args.source), pathlib.Path(args.dest), args.mode)
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
