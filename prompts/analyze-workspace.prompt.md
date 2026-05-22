---
name: analyze-workspace
description: Profile a repo and write project-profile.yaml and project-context.md.
skills:
  - using-agent-skills
  - workspace-analysis
agent: workspace-analyzer
---

# /analyze-workspace — Profile the Repo

## Goal

Produce machine-readable and human-readable project profile artifacts.

## Instructions

1. Load and follow `skills/using-agent-skills/SKILL.md`.
2. Follow `skills/workspace-analysis/SKILL.md`.
3. Adopt the `workspace-analyzer` agent.

## Output

`.ai-sdlc/project-profile.yaml`, `.ai-sdlc/project-context.md`, and a list of
human-only context gaps.
