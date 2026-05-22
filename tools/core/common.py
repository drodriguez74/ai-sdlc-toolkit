"""Shared helpers for toolkit Python tools.

This module is intentionally stdlib-only.
"""
from __future__ import annotations
import json
import pathlib
import re
import sys
from typing import Iterable

MANAGED_BLOCK_PATTERN = re.compile(
    r"<!-- AI-SDLC-TOOLKIT:BEGIN[^>]*-->.*?<!-- AI-SDLC-TOOLKIT:END -->",
    re.DOTALL,
)


def parse_frontmatter(text: str) -> dict | None:
    """Parse minimal YAML-like frontmatter from a Markdown document.

    Returns a dict of top-level scalar/string values, or None when no
    frontmatter is found. List values (using `-` bullets) are parsed as
    lists of strings. This is intentionally simple and does not handle
    nested structures.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    body = text[4:end].strip("\n")
    result: dict = {}
    current_key: str | None = None
    current_list: list[str] | None = None
    for line in body.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list is not None:
            current_list.append(line[4:].strip())
            continue
        if line.startswith("- ") and current_list is not None:
            current_list.append(line[2:].strip())
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "":
            current_list = []
            result[key] = current_list
            current_key = key
        else:
            current_list = None
            current_key = key
            # strip surrounding quotes
            if value and value[0] in "\"'":
                value = value.strip(value[0])
            result[key] = value
    return result


def find_files(root: pathlib.Path, *patterns: str) -> Iterable[pathlib.Path]:
    """Yield matching files under root, skipping common ignored directories."""
    skip = {".git", "node_modules", "__pycache__", ".venv", "dist", "build"}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip for part in path.parts):
            continue
        for pat in patterns:
            if path.match(pat):
                yield path
                break


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text())
