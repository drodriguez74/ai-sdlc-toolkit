#!/usr/bin/env python3
"""List changed files between two refs as JSON."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="main")
    parser.add_argument("--head", default="HEAD")
    args = parser.parse_args()
    result = subprocess.run(
        ["git", "diff", "--name-status", f"{args.base}...{args.head}"],
        check=False, capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        return result.returncode
    files = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            files.append({"status": parts[0], "path": parts[-1]})
    print(json.dumps(files, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
