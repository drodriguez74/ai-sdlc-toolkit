<!-- AI-SDLC-TOOLKIT:BEGIN version="1.0.0" -->
# AI SDLC Toolkit Agent Guidance

This is the global AI SDLC Toolkit. It provides agents, skills, prompts, and
commands that are linked into target project repos via `link-to-project.sh`.

## For Toolkit Maintenance

When editing files in this directory:

- Follow the agent standard documented in `references/agent-anatomy.md`.
- Follow the skill standard in `references/skill-anatomy.md`.
- Follow the adapter contract in `references/adapter-contract.md`.
- Run `./doctor.sh` before committing.
- Bump `VERSION` for any change that affects linked projects.

## For Project Work

Do not edit toolkit files from a project task. Use project override folders:

- `.github/agents-overrides/`
- `.github/skills-overrides/`
- `.github/prompts-overrides/`
- `.github/instructions-overrides/`

Start every task by checking:

1. `.ai-sdlc/project-profile.yaml`
2. `.ai-sdlc/project-context.md`
3. `.github/skills/using-agent-skills/SKILL.md`
4. The task-specific skill under `.github/skills/`
5. The relevant persona under `.github/agents/`

Load only what you need. Do not load all agents and skills at once.
<!-- AI-SDLC-TOOLKIT:END -->
