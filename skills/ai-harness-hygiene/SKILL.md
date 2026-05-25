---
name: ai-harness-hygiene
description: Audit AI harness files (AGENTS.md, CLAUDE.md, copilot-instructions.md, GEMINI.md, README.md) for context bloat, context rot, register violations, contradictions, and missing baselines. Use before onboarding an AI agent to a repo and after significant structural changes.
---

# AI Harness Hygiene

## Overview

AI harness files are the first thing an agent reads. Bloated, stale, or
contradictory files waste tokens, mislead the agent, and produce inconsistent
behaviour across tools. This skill defines what good looks like and how to
detect violations.

## When To Use

- Before onboarding a new AI agent to a repo.
- After significant structural changes (major refactor, rename, stack change).
- When agent behaviour has become inconsistent or surprising across tools.
- As a periodic health check (e.g., after every major release).

## Harness File Roles

Understand the role of each file before auditing. A violation is often a file
doing another file's job.

| File | Audience | Auto-loaded by | Register |
|---|---|---|---|
| `README.md` | Humans | Nobody (AI tools don't auto-load it) | Narrative, explanatory |
| `AGENTS.md` | All AI agents | OpenAI Codex natively; others on request | Imperative, tool-agnostic |
| `.github/copilot-instructions.md` | GitHub Copilot | Copilot (every session) | Directive, Copilot-specific |
| `CLAUDE.md` | Claude Code | Claude Code (every session) | Directive, Claude-specific |
| `GEMINI.md` | Gemini Code Assist | Gemini (every session) | Directive, Gemini-specific |

**Baseline rule:** `AGENTS.md` is the canonical source of truth for all AI
agents. Tool-specific files extend or override it — they should never
duplicate it.

## Workflow

### 1. Inventory

List all harness files present in the repo:
- Project root: `README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
- `.github/`: `copilot-instructions.md`
- Any other `*.md` files in root that appear to be agent instructions

Record which files are present and which are absent.

### 2. Check for missing baseline

If tool-specific files (`CLAUDE.md`, `copilot-instructions.md`, `GEMINI.md`)
exist but `AGENTS.md` does not: **MISSING-BASELINE**. Each tool file is
carrying the full context load that should live in one shared document.

### 3. Check for context bloat (duplication)

For every pair of harness files, compare their sections:
- If two or more files contain substantially the same content (commands,
  directory layout, conventions, stack description), that content belongs in
  `AGENTS.md` only. Tool-specific files should reference or extend it, not
  repeat it.
- Flag sections that are >70% identical across files as **BLOAT**.

### 4. Check for context rot (staleness)

For every factual claim in a harness file, verify it against the current
repo state:

- **Commands**: run or dry-run each listed command; flag any that fail or
  reference scripts/targets that no longer exist as **ROT-COMMAND**.
- **File paths**: check that every path mentioned exists; flag missing paths
  as **ROT-PATH**.
- **Directory structure**: compare any layout or tree in harness files
  against `ls` output; flag dirs that no longer exist or new top-level dirs
  that are unmentioned as **ROT-STRUCTURE**.
- **Stack/dependencies**: compare listed frameworks, languages, and tools
  against current manifest files (`package.json`, `pyproject.toml`,
  `go.mod`, etc.); flag mismatches as **ROT-STACK**.

### 5. Check for register violations

Audit each file against its expected register:

- `README.md` contains imperative agent directives ("Do not modify X",
  "Always run Y before pushing") → **REGISTER-README**: move to `AGENTS.md`.
- `AGENTS.md` is written narratively (explaining context, telling a story)
  rather than imperatively → **REGISTER-AGENTS**: rewrite as directives.
- Tool-specific file contains universal, tool-agnostic instructions that
  apply to all agents equally → **REGISTER-TOOL**: move to `AGENTS.md`.

### 6. Check for contradictions

Compare instructions across files for conflicts:
- Same command referenced differently (e.g., `npm test` vs `make test`).
- Conflicting naming conventions, branch rules, or code style instructions.
- One file permitting what another prohibits.

Flag each conflict as **CONFLICT** with both file:line references.

### 7. Check for missing required sections

`AGENTS.md` (if present) should have at minimum:
- Repository layout
- Stack
- Build & test commands
- Key conventions
- What not to touch

Flag any missing required section as **INCOMPLETE**.

## Severity Levels

| Severity | Meaning |
|---|---|
| **CRITICAL** | Contradictions or rot that will cause an agent to take a wrong action |
| **HIGH** | Missing baseline; significant bloat inflating token usage every session |
| **MEDIUM** | Register violations; moderate duplication |
| **LOW** | Minor staleness; cosmetic or trivial duplication |

## Evidence And Verification

- Every finding cites the specific file and line range.
- Rot findings include the actual repo state that contradicts the claim.
- Bloat findings quote the duplicated content from both files.
- Register findings quote the offending passage.

## Common Rationalizations

- "Each tool needs its own copy" — no, each tool needs only its delta.
- "It doesn't hurt to repeat it" — it costs tokens every session, forever.
- "We'll update the docs later" — rot compounds; update now or delete now.

## Red Flags

- `CLAUDE.md` longer than `AGENTS.md` — the tool-specific file has become
  the de-facto baseline, which means Copilot and Gemini are flying blind.
- Harness files that describe a directory or command not present in the repo.
- README with a "For AI agents" section.
- No `AGENTS.md` but three tool-specific files all carrying the same layout.

## Output Contract

A prioritised findings list, severity-tagged, with file:line references,
the exact violation quoted, and a concrete fix for each. Followed by a
**PASS / NEEDS-WORK** signal and a one-line summary of the highest-severity
issue found.
