---
name: tune-agents
description: Render project-specific overrides for agents, skills, prompts, and instructions.
skills:
  - using-agent-skills
  - agent-tuning
agent: agent-tuner
---

# /tune-agents — Tune Toolkit for This Project

## Goal

Render project-specific overrides where they add value; activate them.

## Instructions

1. Load and follow `skills/using-agent-skills/SKILL.md`.
2. Read `.ai-sdlc/project-profile.yaml`, `.ai-sdlc/project-context.md`, and
   `.ai-sdlc/tune-prompt.md` if present.
3. Follow `skills/agent-tuning/SKILL.md`.
4. Adopt the `agent-tuner` agent.
5. After writing overrides, run `refresh-project-links.sh` to activate them.

## Output

Override files in `.github/*-overrides/`; tuning report in
`.ai-sdlc/tuning-report.md`; refreshed link manifest.
