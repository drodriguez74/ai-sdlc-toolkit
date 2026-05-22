# Codex Harness Template

Use this template when generating `CODEX.md` for a linked project.
`link-to-project.sh` already does this.

## Managed Block

```markdown
<!-- AI-SDLC-TOOLKIT:BEGIN version="<VERSION>" -->
# Codex — AI SDLC Toolkit

Toolkit root: `<TOOLKIT_HOME>`

Discovery paths:
- Agents: `.github/agents/`
- Skills: `.github/skills/`
- Prompts: `.github/prompts/`
- Slash commands: `<TOOLKIT_HOME>/commands/codex/`
- Project profile: `.ai-sdlc/project-profile.yaml`
- Project context: `.ai-sdlc/project-context.md`

Rules:
1. Follow the relevant skill before acting.
2. Adopt the relevant persona for perspective.
3. Project overrides under `.github/*-overrides/` beat global defaults.
4. Load only the minimum assets per task.
5. Subagents are not supported in standard Codex; fan-out commands run sequentially.
<!-- AI-SDLC-TOOLKIT:END -->
```

## Discovery Behavior

Codex reads `CODEX.md` at the start of each session. Commands live under
`commands/codex/` in the toolkit; the harness references them via the awareness
file.
