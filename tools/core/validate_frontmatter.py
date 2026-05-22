#!/usr/bin/env python3
"""Validate frontmatter in agents/, skills/, and prompts/."""
from __future__ import annotations
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import parse_frontmatter  # noqa: E402


def check_file(path: pathlib.Path, required: list[str]) -> list[str]:
    errs: list[str] = []
    try:
        text = path.read_text()
    except Exception as exc:
        return [f"{path}: read error: {exc}"]
    fm = parse_frontmatter(text)
    if fm is None:
        return [f"{path}: missing or invalid frontmatter"]
    for key in required:
        if key not in fm or not fm[key]:
            errs.append(f"{path}: missing frontmatter field: {key}")
    return errs


def main(root_arg: str) -> int:
    root = pathlib.Path(root_arg)
    errors: list[str] = []

    for agent in (root / "agents").glob("*.md"):
        errors.extend(check_file(agent, ["name", "description"]))

    for skill in (root / "skills").glob("*/SKILL.md"):
        errors.extend(check_file(skill, ["name", "description"]))

    for prompt in (root / "prompts").glob("*.prompt.md"):
        errors.extend(check_file(prompt, ["name", "description"]))

    if errors:
        for e in errors:
            print(f"  [FAIL] {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
