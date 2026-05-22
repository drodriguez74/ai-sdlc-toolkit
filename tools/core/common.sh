#!/usr/bin/env bash
# common.sh — shared helpers for toolkit scripts.
# Source this file; do not execute directly.

resolve_toolkit_home() {
  # Echoes the resolved toolkit home directory.
  local dir
  dir="${TOOLKIT_HOME:-}"
  if [ -z "${dir}" ]; then
    # Fall back to the directory of the calling script's grandparent (tools/core -> root).
    dir="$(cd "$(dirname "${BASH_SOURCE[1]}")/.." && pwd)"
  fi
  printf '%s' "${dir}"
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "ERROR: required command not found: $1" >&2
    return 1
  }
}

write_managed_block() {
  # write_managed_block <file> <begin_marker> <end_marker> <body>
  local target="$1" begin="$2" end="$3" body="$4"
  if [ ! -f "${target}" ]; then
    printf '%s\n%s\n%s\n' "${begin}" "${body}" "${end}" > "${target}"
    return
  fi
  if grep -q "${begin%% *}" "${target}"; then
    python3 - "$target" "$begin" "$end" "$body" <<'PY'
import re, sys, pathlib
target, begin, end, body = sys.argv[1:5]
p = pathlib.Path(target)
content = p.read_text()
pattern = re.compile(r'<!-- AI-SDLC-TOOLKIT:BEGIN[^>]*-->.*?<!-- AI-SDLC-TOOLKIT:END -->', re.DOTALL)
new_block = f"{begin}\n{body}\n{end}"
p.write_text(pattern.sub(new_block, content))
PY
  else
    printf '\n%s\n%s\n%s\n' "${begin}" "${body}" "${end}" >> "${target}"
  fi
}
