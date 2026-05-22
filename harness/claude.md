# Claude Code Harness Template

Use this template when generating `CLAUDE.md` for a linked project.
`link-to-project.sh` already does this.

## Managed Block

```markdown
<!-- AI-SDLC-TOOLKIT:BEGIN version="<VERSION>" -->
# Claude Code — AI SDLC Toolkit

Toolkit root: `<TOOLKIT_HOME>`

Discovery paths:
- Agents: `.github/agents/`
- Skills: `.github/skills/`
- Prompts: `.github/prompts/`
- Slash commands: `.claude/commands/`
- Project profile: `.ai-sdlc/project-profile.yaml`
- Project context: `.ai-sdlc/project-context.md`

Rules:
1. Follow the relevant skill before acting.
2. Adopt the relevant persona for perspective.
3. Project overrides under `.github/*-overrides/` beat global defaults.
4. Load only the minimum assets per task — not all agents and skills.
5. Subagents are supported; `/ship` should fan out in parallel.
<!-- AI-SDLC-TOOLKIT:END -->
```

## Discovery Behavior

Claude Code reads `CLAUDE.md` at the start of each session. Slash commands
under `.claude/commands/` are auto-discovered. Subagent fan-out is supported.
