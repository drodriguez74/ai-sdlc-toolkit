#!/usr/bin/env python3
"""Validate manifest.json (rendered) against the manifest schema, minimally."""
from __future__ import annotations
import json
import pathlib
import sys


def main(root_arg: str) -> int:
    root = pathlib.Path(root_arg)
    manifest_path = root / "manifest.json"
    if not manifest_path.exists():
        # Template is fine; rendered manifest is created by install.sh.
        tpl = root / "manifest.json.tpl"
        if tpl.exists():
            try:
                json.loads(tpl.read_text().replace("__TOOLKIT_HOME__", "/tmp/tk"))
                return 0
            except Exception as exc:
                print(f"  [FAIL] manifest.json.tpl invalid JSON after substitution: {exc}")
                return 1
        print("  [FAIL] no manifest.json or manifest.json.tpl found")
        return 1
    try:
        data = json.loads(manifest_path.read_text())
    except Exception as exc:
        print(f"  [FAIL] manifest.json is not valid JSON: {exc}")
        return 1

    required = ["name", "version", "install_root", "agents_dir", "skills_dir",
                "prompts_dir", "linking"]
    missing = [k for k in required if k not in data]
    if missing:
        print(f"  [FAIL] manifest.json missing fields: {missing}")
        return 1

    linking = data.get("linking", {})
    for k in ["default_mode", "project_paths", "override_paths"]:
        if k not in linking:
            print(f"  [FAIL] manifest.json linking missing: {k}")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
