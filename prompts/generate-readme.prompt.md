---
name: generate-readme
description: Introspect the project and generate a complete, accurate README.md using progressive context loading.
skills:
  - using-agent-skills
  - workspace-analysis
  - documentation-and-adrs
agent: documentation-specialist
---

# /generate-readme — Generate README.md

## Goal

Produce a complete, accurate `README.md` by introspecting the project using
progressive context loading — start with the lightest available signal, deepen
only when needed, and never invent facts not grounded in project files.

This prompt is self-contained. Toolkit files (`.ai-sdlc/`) are an
opportunistic cache that speeds up discovery; they are never required. If
they are absent, fall through to direct filesystem introspection.

## Progressive Context Loading Order

Work through each stage in order. Stop loading a stage once its gaps are
resolved. If toolkit files are absent, skip Stage 1 entirely — Stage 2
onwards is fully self-sufficient.

### Stage 1 — Compiled cache (opportunistic, toolkit only)

Skip this stage if `.ai-sdlc/` does not exist.

1. Read `.ai-sdlc/project-profile.yaml`.
2. Read `.ai-sdlc/project-context.md` — use as the project structure source
   if it contains a directory tree; skip Stage 3 structure discovery.
3. Read `.ai-sdlc/knowledge/architecture.md` if present.

### Stage 2 — Manifest files (always run if Stage 1 missed anything)

- `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` / `pom.xml` /
  `build.gradle` — project name, description, version, dependencies, scripts.
- `Makefile` / `justfile` / `taskfile.yml` — available commands.
- `.tool-versions` / `.nvmrc` / `.python-version` — required runtimes.
- `LICENSE` first line — license identifier.

### Stage 3 — Project structure source (progressive; one of three paths)

The **Project Structure** section is always required in the output. Its source
is resolved by trying the following in order — stop at the first hit:

**3a. Existing structured doc (preferred)**
Check in this order for a file that already contains an annotated directory
tree or module layout:
- `.ai-sdlc/project-context.md` (if not fully loaded in Stage 1)
- `.ai-sdlc/knowledge/architecture.md`
- `CONTRIBUTING.md` / `DEVELOPMENT.md`
- The existing `README.md` (Project Structure or Layout section)

If a tree is found, load it and use it as the section source. Validate it
against the actual filesystem (spot-check top-level entries); note any
entries that no longer exist with `<!-- stale: path not found -->`.

**3b. Partial signal (augment)**
If a file was found but only lists top-level dirs without annotations or
source-dir depth, augment it: expand source directories one level deeper
and add missing annotations. Do not restructure what was already there.

**3c. Filesystem generation (fallback — only if 3a and 3b both failed)**
No existing structure doc was found. Generate the tree directly:

1. List the project root (1 level deep). Annotate every entry.
2. For each top-level directory that is clearly source code (e.g., `src/`,
   `lib/`, `app/`, `cmd/`, `pkg/`, primary module dir), list one level deeper.
3. Mark auto-generated / vendored dirs (e.g., `node_modules/`, `dist/`,
   `.git/`, `__pycache__/`, `.venv/`, `vendor/`, `build/`, `coverage/`)
   with a `# generated` annotation and do not expand them.

After resolving structure via whichever path, also run:
- Read `CONTRIBUTING.md` / `DEVELOPMENT.md` / `docs/` index if not yet read —
  for developer setup instructions.
- List `.github/workflows/` filenames only — for CI badges.
- Check for `docker-compose.yml` / `Dockerfile` — for containerised setup.
- List `docs/adr/` if present — to link from the Architecture section.

### Stage 4 — Existing README (always last)

Read the existing `README.md` if present. Preserve any sections with
human-authored content that cannot be derived from code (e.g., project
philosophy, screenshots, demo links, acknowledgements). Flag stale sections
with `<!-- stale: re-verify -->`.

## Instructions

1. If toolkit skills are available, load and follow
   `skills/using-agent-skills/SKILL.md`, then `skills/documentation-and-adrs/SKILL.md`.
   If not, proceed without them — this prompt is fully self-sufficient.
2. Execute the progressive context loading above in order.
3. Write for the first-time reader — assume nothing about prior knowledge.
4. Every fact in the README must be traceable to a file you read. If a fact
   cannot be verified, omit it or mark it `<!-- TODO: verify -->`.
5. Do not invent commands, URLs, or badge slugs. If the repo slug is unknown,
   leave a `<!-- TODO: add repo URL -->` placeholder.

## README Structure

Produce these sections. Omit any section that genuinely does not apply
(e.g., no `## Configuration` if there are no env vars or config files).

```
# <Project Name>

<One-line description — from manifest `description` field or inferred>

<Badges: CI status, license, version — only if verifiable from files>

## Overview
<2–4 sentences: what it does, who it is for, key value proposition>

## Features
<Bullet list grounded in code/docs — not aspirations>

## Project Structure
<Annotated directory tree from Stage 3 — 2 levels for source dirs,
 1 level for everything else. Auto-generated dirs noted but not expanded.
 Example:

  my-project/
  ├── src/
  │   ├── api/          # HTTP handlers
  │   ├── core/         # Business logic
  │   └── db/           # Database layer
  ├── tests/            # Test suite
  ├── docs/             # ADRs and runbooks
  ├── Makefile          # Task runner
  └── docker-compose.yml
>

## Prerequisites
<Runtime versions and required tools — from manifest/tooling files>

## Installation
<Exact commands — from Makefile / package.json scripts / setup files>

## Usage
<Primary usage command(s) with real code block examples>

## Configuration
<Env vars and config files — only if present in the repo>

## Development
<How to run locally, run tests, lint, typecheck — from scripts/Makefile>

## CI / CD
<Badges and brief description — from .github/workflows/ filenames>

## Architecture
<1–2 sentences; link to docs/adr/ or .ai-sdlc/knowledge/architecture.md
 if present; omit section if no architecture docs exist>

## Contributing
<Link to CONTRIBUTING.md if present; omit section if absent>

## License
<Identifier from LICENSE file>
```

## Quality Gates

- No section contains a claim not backed by a file read during context loading.
- The Project Structure tree reflects the actual filesystem — no invented dirs.
- Commands in Installation, Usage, and Development are copy-paste runnable.
- Badge URLs use the correct repo slug; if unknown, a TODO placeholder is used.
- Human-authored sections from an existing README are preserved verbatim with
  a `<!-- preserved: verify before publish -->` comment.

## Output

`README.md` written to the project root. A brief change summary listing
which stages were used and which sections were added, updated, or preserved.
