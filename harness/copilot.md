# GitHub Copilot Harness Template

Use this template when generating `.github/copilot-instructions.md` for a
linked project. `link-to-project.sh` already does this — this file documents
the expected content.

## Managed Block

```markdown
<!-- AI-SDLC-TOOLKIT:BEGIN version="<VERSION>" -->
# AI SDLC Toolkit

Toolkit root: `<TOOLKIT_HOME>`

Discovery paths:
- Agents: `.github/agents/` (and compat mirror `.github/AGENTS/`)
- Skills: `.github/skills/`
- Prompts: `.github/prompts/`
- Instructions: `.github/instructions/`
- Project profile: `.ai-sdlc/project-profile.yaml`
- Project context: `.ai-sdlc/project-context.md`

Rules:
1. If a relevant skill exists, follow it before acting.
2. If a relevant agent exists, use that persona for perspective.
3. Project overrides under `.github/*-overrides/` beat global defaults.
4. Do not edit global toolkit files from a project task.
5. Run `workspace-analysis` SKILL before broad architecture assumptions.
6. Run `code-review-and-quality` SKILL before merge.
7. Run `shipping-and-launch` SKILL before production release.
8. Load only relevant assets; do not load all agents and skills at once.
<!-- AI-SDLC-TOOLKIT:END -->
```

## Discovery Behavior

Copilot reads `.github/copilot-instructions.md` for global context and scans
`.github/prompts/` for slash commands. The link farm populates these paths from
global defaults or project overrides.

The supported references in Copilot Chat are:

- `/command-name` — Slash command from `.github/prompts/command-name.prompt.md`
- `#file:path` — Manually attach a skill or agent file as context (e.g. `#file:.github/skills/backend-engineering/SKILL.md`)

Note: `@agent-name` mentions are NOT supported via markdown files. Copilot `@`
participants are VS Code extensions, not file-based definitions. Agent personas
can only be used as manually attached `#file` context.
