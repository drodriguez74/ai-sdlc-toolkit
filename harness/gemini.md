# Gemini CLI Harness Template

Use this template when generating `GEMINI.md` for a linked project.
`link-to-project.sh` already does this.

## Managed Block

```markdown
<!-- AI-SDLC-TOOLKIT:BEGIN version="<VERSION>" -->
# Gemini CLI — AI SDLC Toolkit

Toolkit root: `<TOOLKIT_HOME>`

Discovery paths:
- Agents: `.github/agents/`
- Skills: `.github/skills/`
- Prompts: `.github/prompts/`
- Slash commands: `.gemini/commands/*.toml`
- Project profile: `.ai-sdlc/project-profile.yaml`
- Project context: `.ai-sdlc/project-context.md`

Rules:
1. Follow the relevant skill before acting.
2. Adopt the relevant persona for perspective.
3. Project overrides under `.github/*-overrides/` beat global defaults.
4. Load only the minimum assets per task.
5. When subagents are not supported, fan-out commands fall back to sequential.
<!-- AI-SDLC-TOOLKIT:END -->
```

## Discovery Behavior

Gemini CLI reads `GEMINI.md` and loads slash commands from
`.gemini/commands/*.toml`. Subagents are not always supported; commands
designed for fan-out (e.g., `/ship`) document a sequential fallback.
