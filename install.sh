#!/usr/bin/env bash
# install.sh — Install the AI SDLC Toolkit globally under ~/.copilot/ai-sdlc-toolkit.
# Idempotent: safe to re-run. Does not overwrite user content outside managed blocks.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLKIT_HOME="${TOOLKIT_HOME:-${HOME}/.copilot/ai-sdlc-toolkit}"
COPILOT_HOME="${HOME}/.copilot"
VERSION_FILE="${SCRIPT_DIR}/VERSION"
VERSION="$(cat "${VERSION_FILE}" 2>/dev/null || echo 'unknown')"

echo "==> Installing AI SDLC Toolkit v${VERSION} -> ${TOOLKIT_HOME}"

mkdir -p "${TOOLKIT_HOME}" "${COPILOT_HOME}/.github"

# Copy all toolkit files (preserve structure, follow symlinks would be wrong here).
# Exclude .git and any local user state.
copy_files() {
  rsync -a \
    --exclude='.git/' \
    --exclude='node_modules/' \
    --exclude='.DS_Store' \
    "${SCRIPT_DIR}/" "${TOOLKIT_HOME}/"
}

if command -v rsync >/dev/null 2>&1; then
  copy_files
else
  # POSIX fallback: cp -R then prune.
  cp -R "${SCRIPT_DIR}/." "${TOOLKIT_HOME}/"
  rm -rf "${TOOLKIT_HOME}/.git" 2>/dev/null || true
fi

# Resolve manifest template.
if [ -f "${TOOLKIT_HOME}/manifest.json.tpl" ]; then
  sed "s|__TOOLKIT_HOME__|${TOOLKIT_HOME}|g" "${TOOLKIT_HOME}/manifest.json.tpl" \
    > "${TOOLKIT_HOME}/manifest.json"
fi

# Make scripts executable.
chmod +x "${TOOLKIT_HOME}"/*.sh 2>/dev/null || true
find "${TOOLKIT_HOME}/tools" -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
find "${TOOLKIT_HOME}/tools" -type f -name "*.py" -exec chmod +x {} \; 2>/dev/null || true

# Awareness files at ~/.copilot/.
write_managed_block() {
  local target="$1" body="$2"
  local begin="<!-- AI-SDLC-TOOLKIT:BEGIN version=\"${VERSION}\" -->"
  local end="<!-- AI-SDLC-TOOLKIT:END -->"
  if [ ! -f "${target}" ]; then
    printf '%s\n%s\n%s\n' "${begin}" "${body}" "${end}" > "${target}"
    return
  fi
  if grep -q 'AI-SDLC-TOOLKIT:BEGIN' "${target}"; then
    # Replace existing block in-place.
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

AGENTS_BODY="# AI SDLC Toolkit Agent Guidance

The toolkit is installed at ${TOOLKIT_HOME}.

For project work, link a repo with:
  ${TOOLKIT_HOME}/link-to-project.sh /path/to/repo

Then start every task by checking:
1. .ai-sdlc/project-profile.yaml
2. .ai-sdlc/project-context.md
3. .github/skills/using-agent-skills/SKILL.md
4. The task-specific skill under .github/skills/
5. The relevant persona under .github/agents/

Do not mutate ${TOOLKIT_HOME} from a project task. Use override folders."

write_managed_block "${COPILOT_HOME}/AGENTS.md"  "${AGENTS_BODY}"
write_managed_block "${COPILOT_HOME}/CLAUDE.md"  "${AGENTS_BODY}"
write_managed_block "${COPILOT_HOME}/GEMINI.md"  "${AGENTS_BODY}"
write_managed_block "${COPILOT_HOME}/CODEX.md"   "${AGENTS_BODY}"

COPILOT_BODY="# AI SDLC Toolkit

Global toolkit installed at ${TOOLKIT_HOME}.

Discovery paths (when linked to a project):
- Agents: .github/agents/
- Skills: .github/skills/
- Prompts: .github/prompts/
- Instructions: .github/instructions/

Run ${TOOLKIT_HOME}/link-to-project.sh /path/to/repo to wire a repo."

write_managed_block "${COPILOT_HOME}/.github/copilot-instructions.md" "${COPILOT_BODY}"

# Run doctor.
if [ -x "${TOOLKIT_HOME}/doctor.sh" ]; then
  "${TOOLKIT_HOME}/doctor.sh" || {
    echo "WARNING: doctor.sh reported failures. Review output above."
    exit 1
  }
fi

echo "==> Install complete."
echo "    Toolkit:   ${TOOLKIT_HOME}"
echo "    Link a project:  ${TOOLKIT_HOME}/link-to-project.sh /path/to/repo"
