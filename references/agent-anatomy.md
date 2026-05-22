# Agent Anatomy

Every agent lives at `agents/<agent-name>.md` with this structure:

## Frontmatter

```yaml
---
name: agent-name
description: One sentence on the role and when to use it.
tools:
  - read
  - search
  - execute
  - edit
---
```

## Required Sections

```markdown
# Agent Title

## Identity
1-2 sentences on who this agent is and how they think.

## Owns
What outputs and decisions this agent is responsible for.

## Does Not Own
Explicit boundaries to avoid responsibility ambiguity.

## Inputs
What this agent reads or receives from upstream.

## Outputs
What this agent produces. Filename and structure when relevant.

## Workflow
Numbered steps. References to relevant skills.

## Quality Gates
What the agent must check before declaring done.

## Composition
Who hands off to this agent; who this agent hands off to.
```

## Composition Rules

- **Agents provide perspective.** Skills provide workflow. Commands orchestrate.
- **Personas do not invoke other personas directly from task context.**
  Orchestration commands (e.g., `/ship`) may explicitly fan out to multiple
  personas; this is the only sanctioned multi-persona invocation pattern.
- An agent should be able to deliver its outputs by following its own workflow
  plus the skills it cites.

## Tuned Overrides

Project-specific overrides add this frontmatter:

```yaml
---
name: tech-lead
description: ...
tools: [...]
base_asset: agents/tech-lead.md
tuned_for_project: true
tuned_at: "2026-05-20T12:00:00Z"
project_profile: .ai-sdlc/project-profile.yaml
---
```

Plus a `## Tuning Notes` section explaining what was tuned and why.
