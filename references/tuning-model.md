# Tuning Model

How the toolkit adapts to a specific project.

## Phases

### Phase 1 — Analysis (Scriptable)

`tune-project.sh` runs `detect_workspace.py` to write:

- `.ai-sdlc/project-profile.yaml` — machine-readable inventory
- `.ai-sdlc/project-context.md` — human-readable summary

This phase requires no AI session.

### Phase 2 — Generation (Harness-Driven)

`tune-project.sh` runs `tune_assets.py` to write
`.ai-sdlc/tune-prompt.md`. The user then opens this prompt in their running AI
CLI; the harness reads the prompt and produces override files. No API call is
made by the script.

## Override Locations

- `.github/agents-overrides/<name>.md`
- `.github/skills-overrides/<name>/SKILL.md`
- `.github/prompts-overrides/<name>.prompt.md`
- `.github/instructions-overrides/<name>.instructions.md`

## Override Frontmatter

Every override declares its base asset and tuning metadata:

```yaml
---
name: tech-lead
description: Tuned tech-lead for ProjectX (Python/FastAPI/AWS).
base_asset: agents/tech-lead.md
tuned_for_project: true
tuned_at: "2026-05-20T12:00:00Z"
project_profile: .ai-sdlc/project-profile.yaml
---
```

## Override Content Rules

1. Overrides are complete rendered files, not patches.
2. Project-specific rules come BEFORE generic defaults.
3. Universal safety and verification requirements MUST be preserved from base.
4. A `## Tuning Notes` section explains what was tuned and why.

## Activation

Overrides take effect only after `refresh-project-links.sh` runs. The script
links the active discovery path to the override when an override exists;
otherwise to the global default.

## When NOT To Tune

Don't override an asset just because the project exists. Override only when
project-specific facts (framework, language, conventions, infrastructure) add
concrete guidance the base asset cannot provide.

## Reverting

To revert a tuned override, delete the file in the `*-overrides/` folder and
re-run `refresh-project-links.sh`. The active link will fall back to the global
default.
