---
name: generate-agents-md
description: Introspect the project and generate an AGENTS.md that orients AI agents to the codebase using progressive context loading.
skills:
  - using-agent-skills
  - workspace-analysis
  - documentation-and-adrs
agent: documentation-specialist
---

# /generate-agents-md — Generate AGENTS.md

## Goal

Produce an `AGENTS.md` at the project root that gives AI coding agents
accurate, actionable orientation to this codebase. Use progressive context
loading — start with the lightest signal, deepen only when needed, and ground
every claim in files you actually read.

This prompt is self-contained. Toolkit files (`.ai-sdlc/`) are an
opportunistic cache that speeds up discovery; they are never required. If
they are absent, fall through to direct filesystem introspection.

## What Is AGENTS.md

`AGENTS.md` is the AI-agent equivalent of an onboarding doc. Tools like
Claude Code, Codex, and Cursor read it to understand how to work safely in a
repo. It must be factual, opinionated, and direct — written for an agent that
will act on the instructions immediately.

## Progressive Context Loading Order

Work through each stage in order. Stop loading a stage once its gaps are
resolved. If toolkit files are absent, skip Stage 1 entirely — Stages 2–4
are fully self-sufficient.

### Stage 1 — Compiled cache (opportunistic, toolkit only)

Skip this stage if `.ai-sdlc/` does not exist.

1. Read `.ai-sdlc/project-profile.yaml`.
2. Read `.ai-sdlc/project-context.md` — use as the repository layout source
   if it contains a directory tree; skip Stage 3 structure discovery.
3. Read `.ai-sdlc/knowledge/architecture.md` if present.

### Stage 2 — Manifest and tooling files (always run if Stage 1 missed anything)

- `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` / `pom.xml` /
  `build.gradle` — stack, test command, lint command, build command.
- `Makefile` / `justfile` / `taskfile.yml` — canonical task runner commands.
- `.tool-versions` / `.nvmrc` / `.python-version` — required runtimes.
- `CLAUDE.md` / `.cursorrules` / `.github/copilot-instructions.md` — existing
  AI guidance to merge (do not duplicate).

### Stage 3 — Repository layout source (progressive; one of three paths)

The **Repository Layout** section is always required in the output. Its source
is resolved by trying the following in order — stop at the first hit:

**3a. Existing structured doc (preferred)**
Check in this order for a file that already contains an annotated directory
tree or module layout:
- `.ai-sdlc/project-context.md` (if not fully loaded in Stage 1)
- `.ai-sdlc/knowledge/architecture.md`
- `AGENTS.md` (existing, loaded in Stage 5 — peek ahead for a layout section)
- `CONTRIBUTING.md` / `DEVELOPMENT.md`

If a tree is found, load it and use it as the section source. Validate it
against the actual filesystem (spot-check top-level entries); mark stale
entries with `<!-- stale: path not found -->`.

**3b. Partial signal (augment)**
If a file was found but only lists top-level dirs without annotations or
source-dir depth, augment it: expand source directories one level deeper,
add `# generated — do not edit` annotations on generated dirs, and add
test-dir annotations with the detected framework. Do not restructure what
was already there.

**3c. Filesystem generation (fallback — only if 3a and 3b both failed)**
No existing layout doc was found. Generate the tree directly:

1. List the project root (1 level deep). Annotate every entry.
2. For each top-level directory that is clearly source code (e.g., `src/`,
   `lib/`, `app/`, `cmd/`, `pkg/`, primary module dir), list one level deeper.
3. Mark auto-generated / vendored dirs (e.g., `node_modules/`, `dist/`,
   `.git/`, `__pycache__/`, `.venv/`, `vendor/`, `build/`, `coverage/`)
   with `# generated — do not edit`; agents must never modify them.

After resolving layout via whichever path, also run:
- List test directories (`tests/`, `__tests__/`, `spec/`, `test/`) and note
  the framework detected from the manifest.
- Check `.github/workflows/` filenames — for CI commands agents should run
  before pushing.
- Read `CONTRIBUTING.md` if not yet read — for contribution rules to surface.
- Check `docker-compose.yml` / `Dockerfile` — for local environment setup.
- List `docs/adr/` if present — to tell agents where decisions live.

### Stage 4 — AI SDLC Toolkit integration (opportunistic)

Skip if `.ai-sdlc/` does not exist. If present:

- List `agents/*.md` filenames — surface available agent personas.
- List `skills/*/SKILL.md` filenames — surface available skills.
- List `prompts/*.prompt.md` filenames — surface available slash commands.

### Stage 5 — Existing AGENTS.md (always last)

Read the existing `AGENTS.md` if present. Preserve human-authored sections
that cannot be derived from code. Flag stale content with
`<!-- stale: re-verify -->`.

## Instructions

1. If toolkit skills are available, load and follow
   `skills/using-agent-skills/SKILL.md`, then `skills/documentation-and-adrs/SKILL.md`.
   If not, proceed without them — this prompt is fully self-sufficient.
2. Execute the progressive context loading above in order.
3. Write in second-person imperative addressed to the AI agent: "Run X",
   "Do not modify Y", "Always check Z before acting."
4. Every fact must be traceable to a file you read. Omit or flag with
   `<!-- TODO: verify -->` anything you cannot verify.
5. Merge (do not duplicate) any instructions already in `CLAUDE.md`,
   `.cursorrules`, or `.github/copilot-instructions.md`.

## AGENTS.md Structure

Produce these sections. Omit any section that genuinely does not apply.

```
# AGENTS.md — <Project Name>

<One-sentence project description>

## Repository Layout
<Annotated directory tree from Stage 3 — 2 levels for source dirs,
 1 level for everything else. Auto-generated dirs marked do-not-edit.
 Example:

  my-project/
  ├── src/
  │   ├── api/          # HTTP handlers — entry point for new routes
  │   ├── core/         # Business logic — no framework imports
  │   └── db/           # Database layer — migrations in db/migrations/
  ├── tests/            # Pytest suite — mirrors src/ structure
  ├── docs/adr/         # Architecture decision records
  ├── Makefile          # Use `make help` for available targets
  ├── dist/             # generated — do not edit
  └── node_modules/     # generated — do not edit
>

## Stack
<Language(s), frameworks, runtimes, key libraries — from manifest>

## Environment Setup
<Exact commands to bootstrap a dev environment — verified from files>

## Build & Test
<Canonical commands: build, test, lint, typecheck — from scripts/Makefile>

## Key Conventions
<Patterns agents must follow: naming, file placement, module boundaries,
 import rules — inferred from the existing code structure>

## What Not To Touch
<Files and dirs that are auto-generated, vendored, or human-only —
 derived from Stage 3 introspection>

## Testing Rules
<Where tests live, how to run them, naming conventions, coverage
 requirements — from test dir structure and manifest scripts>

## CI
<What CI checks run and the exact commands to run them locally before
 pushing — from .github/workflows/ filenames and Makefile>

## Architecture Notes
<High-level call flow or data flow — 3–5 sentences max; link to
 docs/adr/ or .ai-sdlc/knowledge/architecture.md if present>

## AI SDLC Toolkit (if present)
<Available agents, skills, and slash commands — from Stage 4 discovery>

## Sensitive Areas
<Files/subsystems requiring extra caution: auth, payments, migrations,
 secrets, generated code — flag explicitly with "tread carefully">
```

## Quality Gates

- Every command listed is runnable from the project root.
- The Repository Layout tree reflects the actual filesystem — no invented dirs.
- Auto-generated dirs are annotated `# generated — do not edit` in the tree.
- No section is based on assumption — only files read during context loading.
- Instructions to the agent are specific enough to act on without follow-up.
- If `CLAUDE.md` / `.cursorrules` existed, their content is merged, not repeated.
- Sensitive or security-critical areas are explicitly flagged.

## Output

`AGENTS.md` written to the project root. A brief summary listing which
context stages were used and any gaps that required human input.
