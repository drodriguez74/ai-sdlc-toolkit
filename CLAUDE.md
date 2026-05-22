<!-- AI-SDLC-TOOLKIT:BEGIN version="1.0.0" -->
# Claude Code Awareness — AI SDLC Toolkit

This is the global AI SDLC Toolkit source. Linked into projects via
`link-to-project.sh`.

## Discovery Paths in Linked Projects

- Agents: `agents/*.md`
- Skills: `skills/*/SKILL.md`
- Prompts: `prompts/*.prompt.md`
- Slash commands: `.claude/commands/*.md`
- Instructions: `.github/instructions/*.instructions.md`
- Project profile: `.ai-sdlc/project-profile.yaml`
- Project context: `.ai-sdlc/project-context.md`

## Rules

1. If a relevant skill exists, follow it before acting.
2. If a relevant agent exists, adopt that persona for perspective.
3. Project overrides under `.github/*-overrides/` beat global defaults.
4. Do not edit global toolkit files from a project task.
5. Context window discipline: load only `project-profile.yaml`,
   `project-context.md`, one task-relevant skill, and one agent per task —
   not all agents and skills.
<!-- AI-SDLC-TOOLKIT:END -->
