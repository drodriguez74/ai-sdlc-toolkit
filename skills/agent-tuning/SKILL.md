---
name: agent-tuning
description: Create project-specific overrides for agents, skills, prompts, and instructions. Use after workspace analysis to adapt the toolkit to a specific project.
---

# Agent Tuning

## Overview

Generic agents and skills work; project-tuned ones work better. Tune only where
project facts genuinely help.

## When To Use

After `workspace-analysis` produces a profile. When the toolkit is first linked
to a project. When project facts change materially.

## Workflow

1. Read `.ai-sdlc/project-profile.yaml` and `.ai-sdlc/project-context.md`.
2. Read `.ai-sdlc/tune-prompt.md` if present (assembled by `tune-project.sh`).
3. Identify which agents and skills need project facts to be useful — not all do.
4. For each candidate, render a complete override file (not a patch).
5. Include frontmatter: `base_asset`, `tuned_for_project: true`, `tuned_at`,
   `project_profile`.
6. Add a `Tuning Notes` section explaining what was tuned and why.
7. Put project-specific rules before generic defaults; preserve universal safety
   and verification requirements.
8. Save overrides to `.github/agents-overrides/`, `.github/skills-overrides/`,
   `.github/prompts-overrides/`, `.github/instructions-overrides/`.
9. Write `.ai-sdlc/tuning-report.md` summarizing what was overridden and why.
10. Run `refresh-project-links.sh` to activate overrides.

## Evidence And Verification

- Every override has required frontmatter.
- Tuning report justifies each override.
- Universal safety rules from base assets are preserved.

## Common Rationalizations

- "Override everything to be safe" — that creates maintenance burden, not safety.
- "Tuning isn't needed" — sometimes true; check, don't assume.

## Red Flags

- Override that strips a safety rule from the base.
- Override with no `base_asset` frontmatter.
- Wholesale duplication of global assets.

## Output Contract

Override files with valid frontmatter; tuning report; refreshed link manifest.
