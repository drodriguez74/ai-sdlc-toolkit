# Generic Harness Template

For AI tools without first-class support for one of the named harnesses, use
this generic guidance.

## Awareness File

Create or update `AGENTS.md` at the project root with this managed block:

```markdown
<!-- AI-SDLC-TOOLKIT:BEGIN version="<VERSION>" -->
# AI SDLC Toolkit (Generic Harness)

Toolkit root: `<TOOLKIT_HOME>`

Discovery paths:
- Agents: `.github/agents/`
- Skills: `.github/skills/`
- Prompts: `.github/prompts/`
- Instructions: `.github/instructions/`
- Project profile: `.ai-sdlc/project-profile.yaml`
- Project context: `.ai-sdlc/project-context.md`

Rules:
1. Read the awareness file at the start of every session.
2. Follow the relevant skill before acting.
3. Adopt the relevant persona for perspective.
4. Project overrides under `.github/*-overrides/` beat global defaults.
5. Load only the minimum assets per task.
6. Fan-out commands fall back to sequential execution.
<!-- AI-SDLC-TOOLKIT:END -->
```

## Discovery Behavior

The agent reads `AGENTS.md` at session start. Slash-style entry points map to
prompt files in `.github/prompts/`. The user invokes a prompt manually by
asking the agent to follow the named prompt file.
