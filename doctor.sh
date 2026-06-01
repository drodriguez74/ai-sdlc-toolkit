#!/usr/bin/env bash
# doctor.sh — Validate toolkit structure, frontmatter, and detect secret-like strings.
# Windows: run inside Git Bash / MSYS2 / WSL.
set -uo pipefail

# Windows Git Bash / MSYS2 may not set HOME; fall back to USERPROFILE.
: "${HOME:=${USERPROFILE:-$(cd ~ && pwd)}}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ALLOWLIST="${SCRIPT_DIR}/.doctor-allowlist"
PROJECT_REPO=""

while [ $# -gt 0 ]; do
  case "$1" in
    --allowlist) ALLOWLIST="$2"; shift 2 ;;
    *)           PROJECT_REPO="$1"; shift ;;
  esac
done

PASS=0
FAIL=0

ok()   { echo "  [PASS] $1"; PASS=$((PASS+1)); }
bad()  { echo "  [FAIL] $1"; FAIL=$((FAIL+1)); }
info() { echo "  [INFO] $1"; }

echo "==> Validating toolkit at ${SCRIPT_DIR}"

# 1. Required directories.
for d in agents skills prompts commands tools references schemas harness; do
  if [ -d "${SCRIPT_DIR}/${d}" ]; then
    ok "dir ${d}"
  else
    bad "missing dir ${d}"
  fi
done

# 2. Required root files.
for f in VERSION manifest.json.tpl README.md \
         install.sh upgrade.sh doctor.sh \
         link-to-project.sh refresh-project-links.sh tune-project.sh; do
  if [ -f "${SCRIPT_DIR}/${f}" ]; then
    ok "file ${f}"
  else
    bad "missing file ${f}"
  fi
done

# 3. Script executability.
for f in install.sh upgrade.sh doctor.sh link-to-project.sh \
         refresh-project-links.sh tune-project.sh; do
  if [ -f "${SCRIPT_DIR}/${f}" ]; then
    if [ -x "${SCRIPT_DIR}/${f}" ]; then
      ok "exec ${f}"
    else
      bad "not executable: ${f}"
    fi
  fi
done

# 4. Frontmatter validation via Python helper.
if [ -x "${SCRIPT_DIR}/tools/core/validate_frontmatter.py" ]; then
  if python3 "${SCRIPT_DIR}/tools/core/validate_frontmatter.py" "${SCRIPT_DIR}"; then
    ok "frontmatter (agents, skills, prompts)"
  else
    bad "frontmatter validation failed"
  fi
else
  info "skip frontmatter validation (tools/core/validate_frontmatter.py missing)"
fi

# 5. Manifest schema validation.
if [ -x "${SCRIPT_DIR}/tools/core/validate_manifest.py" ]; then
  if python3 "${SCRIPT_DIR}/tools/core/validate_manifest.py" "${SCRIPT_DIR}"; then
    ok "manifest schema"
  else
    bad "manifest schema validation failed"
  fi
else
  info "skip manifest validation (helper missing)"
fi

# 6. Secret-pattern scan.
echo "==> Scanning for secret-like patterns"
if python3 - "${SCRIPT_DIR}" "${ALLOWLIST}" <<'PY'
import os, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
allow_path = pathlib.Path(sys.argv[2])
patterns = [
    re.compile(r'-----BEGIN [^\n]*PRIVATE KEY-----'),
    re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
]
allow = []
if allow_path.exists():
    for line in allow_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            allow.append(re.compile(line))

def allowed(token: str) -> bool:
    return any(a.search(token) for a in allow)

skip_dirs = {'.git', 'node_modules', '__pycache__'}
hits = 0
for path in root.rglob('*'):
    if not path.is_file():
        continue
    if any(part in skip_dirs for part in path.parts):
        continue
    try:
        text = path.read_text(errors='ignore')
    except Exception:
        continue
    for i, line in enumerate(text.splitlines(), 1):
        for pat in patterns:
            m = pat.search(line)
            if m and not allowed(m.group(0)):
                print(f"  [FAIL] secret-like match in {path.relative_to(root)}:{i}: {m.group(0)[:40]}...")
                hits += 1
if hits == 0:
    print("  [PASS] no secret-like patterns")
sys.exit(1 if hits else 0)
PY
then
  PASS=$((PASS+1))
else
  FAIL=$((FAIL+1))
fi

# 7. Project-level checks if a repo path was given.
if [ -n "${PROJECT_REPO}" ]; then
  echo "==> Validating linked project at ${PROJECT_REPO}"
  if [ -d "${PROJECT_REPO}/.github" ]; then
    BROKEN="$(find "${PROJECT_REPO}/.github" -type l ! -exec test -e {} \; -print 2>/dev/null | wc -l | tr -d ' ')"
    if [ "${BROKEN}" -eq 0 ]; then
      ok "no broken symlinks in ${PROJECT_REPO}/.github"
    else
      bad "${BROKEN} broken symlink(s) in ${PROJECT_REPO}/.github"
    fi
  else
    bad "${PROJECT_REPO}/.github does not exist"
  fi
fi

echo "==> doctor: ${PASS} pass, ${FAIL} fail"
[ "${FAIL}" -eq 0 ]
