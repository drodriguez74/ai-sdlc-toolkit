---
name: workspace-analysis
description: Discover a repo before acting — languages, frameworks, tooling, tests, CI/CD, cloud, docs, APIs, data. Use at the start of work in any unfamiliar repo.
---

# Workspace Analysis

## Overview

Acting on a repo without analyzing it leads to misaligned changes. A 60-second
analysis prevents hours of cleanup.

## When To Use

At the start of work in an unfamiliar repo. When the project profile is missing
or stale.

## Workflow

1. Detect languages and primary frameworks from manifest files.
2. Detect build tools and package managers.
3. Detect test frameworks and test locations.
4. Detect CI/CD configuration.
5. Detect infrastructure as code (Terraform, Bicep, etc.).
6. Detect cloud provider hints.
7. Detect API contracts (OpenAPI, GraphQL, RPC).
8. Detect data stores and pipeline files.
9. Detect documentation: README, ADRs, docs/.
10. Write `.ai-sdlc/project-profile.yaml` (machine-readable).
11. Write `.ai-sdlc/project-context.md` (human-readable summary).
12. Flag any context the AI cannot detect (org context, runtime envs, etc.).

## Evidence And Verification

- Profile is valid against `schemas/project-profile.schema.json`.
- Detection is based on files actually present, not assumed.
- Gaps are reported explicitly.

## Common Rationalizations

- "I'll just start coding" — that's how patterns get violated.
- "I know this stack" — every repo bends the stack to its needs.

## Red Flags

- Profile that lists frameworks no manifest references.
- Context summary based on assumption, not files.

## Output Contract

`.ai-sdlc/project-profile.yaml` + `.ai-sdlc/project-context.md` + a list of
human-only context gaps.
