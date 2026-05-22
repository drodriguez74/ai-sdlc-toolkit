---
name: generate-knowledge
description: Analyze the codebase and generate a structured knowledge base under .ai-sdlc/knowledge/.
skills:
  - using-agent-skills
  - workspace-analysis
  - repo-knowledge-generation
agent: workspace-analyzer
---

# /generate-knowledge — Generate Repo Knowledge Base

## Goal

Produce a structured, citable knowledge base from the codebase covering
architecture, patterns, decisions, integrations, and domain glossary.

## Instructions

1. Load and follow `skills/using-agent-skills/SKILL.md`.
2. Check for `.ai-sdlc/project-profile.yaml` — if missing or stale, follow
   `skills/workspace-analysis/SKILL.md` first.
3. Follow `skills/repo-knowledge-generation/SKILL.md`.
4. Adopt the `workspace-analyzer` agent.

## Output

`.ai-sdlc/knowledge/architecture.md`, `patterns.md`, `decisions.md`,
`integrations.md`, `glossary.md`. Updated `project-context.md` with a
`## Knowledge Base` section. A gap list of areas needing human input.
