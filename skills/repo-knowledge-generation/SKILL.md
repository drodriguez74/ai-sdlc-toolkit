---
name: repo-knowledge-generation
description: Analyze a codebase and generate a structured knowledge base under .ai-sdlc/knowledge/. Use after workspace-analysis when onboarding to a new repo or when documentation is absent or stale.
---

# Repo Knowledge Generation

## Overview

Code is self-describing, but only to someone who already understands it.
This skill extracts architecture, patterns, domain terms, and key decisions
from the codebase and writes them as durable, human-readable documents.
The output is the knowledge base that future tasks — and future contributors — load instead of re-deriving from scratch.

## When To Use

- Onboarding to an unfamiliar repo for the first time.
- Documentation is absent, stale, or scattered.
- Before a large refactor or architecture change that requires a baseline.
- When `workspace-analysis` has run but no narrative knowledge exists.

Do not run on repos you own and already have current docs for — prefer
`documentation-and-adrs` for incremental doc updates instead.

## Workflow

1. **Ensure a project profile exists.** If `.ai-sdlc/project-profile.yaml` is
   missing or older than 7 days, run the `workspace-analysis` skill first.

2. **Read the project profile and context.**
   Load `.ai-sdlc/project-profile.yaml` and `.ai-sdlc/project-context.md`.
   These are the authoritative detected-facts baseline.

3. **Map the component structure.**
   Walk entry points, top-level modules, and package boundaries. Identify
   the major components and how they relate (dependency edges, call graph,
   event flow). Focus on structure, not line-by-line logic.

4. **Trace data flow.**
   Follow data from ingestion (API, queue, file) through transformation to
   persistence or output. Note where data crosses component or service
   boundaries.

5. **Extract coding patterns and conventions.**
   Identify: naming conventions, error-handling idioms, logging patterns,
   test structure, folder layout rules, and any documented or implied style
   decisions. Sample 3–5 representative files per layer.

6. **Detect architectural decisions.**
   Look for: framework and library choices, patterns adopted (e.g. repository
   pattern, CQRS, saga), security approaches, infra choices. Note where the
   decision is visible in code but undocumented — flag these as candidate ADRs.

7. **Identify external integrations.**
   Enumerate third-party services, APIs, queues, and data stores the codebase
   depends on. Source from: imports, env var references, config files, adapter
   definitions.

8. **Build a domain glossary.**
   Extract recurring domain terms from class names, function names, comments,
   and config keys. Define each term in one sentence using the codebase's own
   language, not generic descriptions.

9. **Write knowledge documents** to `.ai-sdlc/knowledge/`:

   | File | Contents |
   |------|----------|
   | `architecture.md` | System overview, component map, data flow diagram (text or Mermaid) |
   | `patterns.md` | Coding conventions, idioms, structural rules found in the repo |
   | `decisions.md` | Detected architectural decisions; flag undocumented ones as candidate ADRs |
   | `integrations.md` | External dependencies, APIs, queues, data stores with config pointers |
   | `glossary.md` | Domain terms and definitions sourced from the codebase |

10. **Update `.ai-sdlc/project-context.md`** with a `## Knowledge Base` section
    linking to the files above.

11. **Report gaps.** List any areas where the code alone was insufficient to
    determine intent — these require human input.

## Evidence And Verification

- Every claim in the knowledge docs is traceable to a specific file or config.
- No "likely" or "probably" without a gap flag.
- `decisions.md` distinguishes confirmed decisions from candidate ADRs.
- Glossary terms are sourced from actual identifiers or comments, not invented.

## Common Rationalizations

- "I can just read the code" — you can, every time; the knowledge base means you don't have to.
- "The README covers it" — READMEs describe setup, not architecture or domain.
- "This repo is too small" — glossary and patterns are valuable even in small repos.

## Red Flags

- Knowledge docs that contain no file citations.
- Architecture description that doesn't match the actual module structure.
- Glossary terms that don't appear in the codebase.
- `decisions.md` that lists only obvious defaults (e.g. "we use Python").

## Output Contract

Five markdown files under `.ai-sdlc/knowledge/`: `architecture.md`,
`patterns.md`, `decisions.md`, `integrations.md`, `glossary.md`. Each section
cites the source file or config it was derived from. A gap list of areas
requiring human clarification. An updated `project-context.md` with a
`## Knowledge Base` link section.
