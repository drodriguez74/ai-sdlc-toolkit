---
name: onboard
description: Fully onboard to a repo — profile the workspace then generate the knowledge base in one pass.
skills:
  - using-agent-skills
  - workspace-analysis
  - repo-knowledge-generation
agent: workspace-analyzer
---

# /onboard — Profile and Document the Repo

## Goal

Produce a complete onboarding package: a machine-readable project profile,
a human-readable context summary, and a full knowledge base.

## Instructions

1. Load and follow `skills/using-agent-skills/SKILL.md`.
2. Follow `skills/workspace-analysis/SKILL.md`.
   - Write `.ai-sdlc/project-profile.yaml` and `.ai-sdlc/project-context.md`.
3. Follow `skills/repo-knowledge-generation/SKILL.md`.
   - Write `.ai-sdlc/knowledge/architecture.md`, `patterns.md`, `decisions.md`,
     `integrations.md`, `glossary.md`.
4. Adopt the `workspace-analyzer` agent throughout.

## Output

`.ai-sdlc/project-profile.yaml`, `.ai-sdlc/project-context.md`,
`.ai-sdlc/knowledge/` (5 documents), and a gap list of areas needing
human input.
