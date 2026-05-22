# GitHub Copilot — AI SDLC Toolkit Contributor Guidance

This is the **source repository** for the AI SDLC Toolkit. It is not a linked
project — it is the toolkit itself. Assets here are distributed to target
projects via `link-to-project.sh`.

## Repo Layout

| Path | Purpose |
|------|---------|
| `agents/` | Agent persona definitions |
| `skills/` | Skill playbooks (`SKILL.md` per skill) |
| `prompts/` | Reusable prompt templates |
| `commands/` | Slash-command definitions per AI tool (claude, codex, gemini, copilot) |
| `harness/` | Per-tool system-prompt harnesses |
| `references/` | Authoring standards (agent-anatomy, skill-anatomy, adapter-contract, …) |
| `schemas/` | JSON schemas for agents, skills, prompts, adapters, manifests |
| `tools/` | Core Python utilities and adapter definitions |

## Contributor Rules

1. Read `references/agent-anatomy.md` before editing any agent.
2. Read `references/skill-anatomy.md` before editing any skill.
3. Read `references/adapter-contract.md` before editing any adapter.
4. Run `./doctor.sh` before committing.
5. Bump `VERSION` for any change that affects linked projects.
6. Do **not** run `link-to-project.sh` against this directory — it is the source, not a target.
7. Override folders (`.github/*-overrides/`) belong in target project repos, not here.
