<!-- AI-SDLC-TOOLKIT:BEGIN version="1.0.0" -->
# Gemini CLI Awareness — AI SDLC Toolkit

This is the global AI SDLC Toolkit source. Linked into projects via
`link-to-project.sh`.

## Discovery Paths in Linked Projects

- Agents: `agents/*.md`
- Skills: `skills/*/SKILL.md`
- Prompts: `prompts/*.prompt.md`
- Slash commands: `.gemini/commands/*.toml`
- Instructions: `.github/instructions/*.instructions.md`
- Project profile: `.ai-sdlc/project-profile.yaml`
- Project context: `.ai-sdlc/project-context.md`

## Rules

1. Follow the relevant skill before acting.
2. Adopt the relevant persona for perspective.
3. Overrides beat defaults.
4. Do not edit global toolkit files from a project task.
5. Load minimum context; do not load all agents and skills at once.
<!-- AI-SDLC-TOOLKIT:END -->
