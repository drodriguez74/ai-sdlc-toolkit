#!/usr/bin/env python3
"""Print git diff between two refs (default: HEAD vs main)."""
from __future__ import annotations
import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="main")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--name-only", action="store_true")
    args = parser.parse_args()
    cmd = ["git", "diff", f"{args.base}...{args.head}"]
    if args.name_only:
        cmd.append("--name-only")
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        print("ERROR: git not installed", file=sys.stderr)
        return 1
    sys.stdout.write(result.stdout)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
