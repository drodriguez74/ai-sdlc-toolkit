#!/usr/bin/env bash
# link-to-project.sh — Wire a target repo to the AI SDLC Toolkit.
# Creates .ai-sdlc, .github structure, override folders, and awareness files.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLKIT_HOME="${TOOLKIT_HOME:-${SCRIPT_DIR}}"
TARGET="${1:-$(pwd)}"
TARGET="$(cd "${TARGET}" && pwd)"
VERSION="$(cat "${TOOLKIT_HOME}/VERSION" 2>/dev/null || echo unknown)"

echo "==> Linking ${TARGET} -> toolkit ${TOOLKIT_HOME}"

mkdir -p \
  "${TARGET}/.ai-sdlc" \
  "${TARGET}/.github" \
  "${TARGET}/.github/agents-overrides" \
  "${TARGET}/.github/skills-overrides" \
  "${TARGET}/.github/prompts-overrides" \
  "${TARGET}/.github/instructions-overrides" \
  "${TARGET}/.claude/commands" \
  "${TARGET}/.gemini/commands"

# Keep override folders even when empty.
for d in agents-overrides skills-overrides prompts-overrides instructions-overrides; do
  [ -f "${TARGET}/.github/${d}/.gitkeep" ] || touch "${TARGET}/.github/${d}/.gitkeep"
done

write_managed_block() {
  local target="$1" body="$2"
  local begin="<!-- AI-SDLC-TOOLKIT:BEGIN version=\"${VERSION}\" -->"
  local end="<!-- AI-SDLC-TOOLKIT:END -->"
  if [ ! -f "${target}" ]; then
    printf '%s\n%s\n%s\n' "${begin}" "${body}" "${end}" > "${target}"
    return
  fi
  if grep -q 'AI-SDLC-TOOLKIT:BEGIN' "${target}"; then
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

# Awareness file bodies.
read -r -d '' AGENTS_BODY <<EOF || true
# AI SDLC Toolkit Agent Guidance

This repo is linked to the AI SDLC Toolkit at ${TOOLKIT_HOME}.

Start every task by checking:
1. .ai-sdlc/project-profile.yaml
2. .ai-sdlc/project-context.md
3. .github/skills/using-agent-skills/SKILL.md
4. The task-specific skill under .github/skills/
5. The relevant persona under .github/agents/

Load only what you need for the task. Do not load all agents and skills at once.

Project overrides under .github/*-overrides/ take precedence over global defaults.
Never edit files under ${TOOLKIT_HOME} from a project task.
EOF

read -r -d '' COPILOT_BODY <<EOF || true
# AI SDLC Toolkit

This repository is linked to the global AI SDLC Toolkit.

Toolkit root: ${TOOLKIT_HOME}

## What Copilot Reads Automatically

- Global instructions: .github/copilot-instructions.md
- Slash commands (/spec, /plan, /build, ...): .github/prompts/
- Scoped instructions: .github/instructions/
- Project profile: .ai-sdlc/project-profile.yaml
- Project context: .ai-sdlc/project-context.md

## Agent and Skill Files

Agent personas (.github/agents/) and skill playbooks (.github/skills/) are
available but must be attached manually as context:
  #file:.github/agents/tech-lead.md
  #file:.github/skills/backend-engineering/SKILL.md

Note: @agent-name mentions are NOT supported — Copilot @ participants are
VS Code extensions, not file-based definitions.

## Rules

1. Follow the relevant skill before acting (attach as #file context).
2. Use the relevant agent persona for perspective (attach as #file context).
3. Project overrides under .github/*-overrides/ beat global defaults.
4. Do not edit global toolkit files from a project task.
EOF

write_managed_block "${TARGET}/AGENTS.md" "${AGENTS_BODY}"
write_managed_block "${TARGET}/CLAUDE.md" "${AGENTS_BODY}"
write_managed_block "${TARGET}/GEMINI.md" "${AGENTS_BODY}"
write_managed_block "${TARGET}/CODEX.md"  "${AGENTS_BODY}"
write_managed_block "${TARGET}/.github/copilot-instructions.md" "${COPILOT_BODY}"

# Build link farms.
"${TOOLKIT_HOME}/refresh-project-links.sh" "${TARGET}"

# Run project-level doctor.
"${TOOLKIT_HOME}/doctor.sh" "${TARGET}" || {
  echo "WARNING: project doctor reported issues."
}

echo "==> Link complete."
echo "    Next: run ${TOOLKIT_HOME}/tune-project.sh ${TARGET} from inside your AI CLI."
