#!/usr/bin/env bash
# tune-project.sh — Two-phase project tuning.
#   Phase 1 (Analysis): detect workspace characteristics, write project-profile.yaml
#                       and project-context.md. Fully scriptable.
#   Phase 2 (Prompt assembly): write tune-prompt.md for the user's AI CLI to read.
#
# This script does NOT call any external AI API. It is designed to run inside an
# AI CLI session (Claude Code, GitHub Copilot, Gemini CLI, etc.) so that the AI
# harness already active reads tune-prompt.md and generates override files.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLKIT_HOME="${TOOLKIT_HOME:-${SCRIPT_DIR}}"
TARGET="${1:-$(pwd)}"
TARGET="$(cd "${TARGET}" && pwd)"

case "${1:-}" in
  -h|--help)
    cat <<EOF
Usage: tune-project.sh [TARGET_REPO]

Runs in two phases:
  Phase 1 — Analysis: writes .ai-sdlc/project-profile.yaml and project-context.md.
  Phase 2 — Prompt assembly: writes .ai-sdlc/tune-prompt.md.

After this script exits, open .ai-sdlc/tune-prompt.md in your running AI CLI to
generate project-specific overrides. The script never calls an external AI API.
EOF
    exit 0
    ;;
esac

mkdir -p "${TARGET}/.ai-sdlc"

echo "==> Phase 1: Analyzing workspace at ${TARGET}"
python3 "${TOOLKIT_HOME}/tools/core/detect_workspace.py" "${TARGET}"

echo "==> Phase 2: Assembling tune-prompt.md"
python3 "${TOOLKIT_HOME}/tools/core/tune_assets.py" \
  --toolkit-home "${TOOLKIT_HOME}" --target "${TARGET}"

cat <<EOF

==> Analysis complete.
    Profile:  ${TARGET}/.ai-sdlc/project-profile.yaml
    Context:  ${TARGET}/.ai-sdlc/project-context.md
    Prompt:   ${TARGET}/.ai-sdlc/tune-prompt.md

Open .ai-sdlc/tune-prompt.md in your AI session to generate project-specific
overrides into .github/*-overrides/. Then run:
  ${TOOLKIT_HOME}/refresh-project-links.sh ${TARGET}
to activate them.
EOF
