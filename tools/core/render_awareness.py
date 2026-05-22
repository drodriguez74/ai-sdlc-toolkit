#!/usr/bin/env python3
"""Render or refresh managed blocks in awareness files."""
from __future__ import annotations
import argparse
import pathlib
import re
import sys

BEGIN_RE = re.compile(r'<!-- AI-SDLC-TOOLKIT:BEGIN[^>]*-->')
END_RE = re.compile(r'<!-- AI-SDLC-TOOLKIT:END -->')
BLOCK_RE = re.compile(
    r'<!-- AI-SDLC-TOOLKIT:BEGIN[^>]*-->.*?<!-- AI-SDLC-TOOLKIT:END -->',
    re.DOTALL,
)


def render(target: pathlib.Path, version: str, body: str) -> None:
    begin = f'<!-- AI-SDLC-TOOLKIT:BEGIN version="{version}" -->'
    end = '<!-- AI-SDLC-TOOLKIT:END -->'
    block = f'{begin}\n{body}\n{end}'
    if not target.exists():
        target.write_text(block + '\n')
        return
    content = target.read_text()
    if BLOCK_RE.search(content):
        target.write_text(BLOCK_RE.sub(block, content))
    else:
        if not content.endswith('\n'):
            content += '\n'
        target.write_text(content + '\n' + block + '\n')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('--version', required=True)
    parser.add_argument('--body-file', required=True)
    args = parser.parse_args()
    body = pathlib.Path(args.body_file).read_text()
    render(pathlib.Path(args.target), args.version, body)
    return 0


if __name__ == '__main__':
    sys.exit(main())
