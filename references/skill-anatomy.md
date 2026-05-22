# Skill Anatomy

Every skill lives at `skills/<skill-name>/SKILL.md` with this structure:

## Frontmatter

```yaml
---
name: lowercase-hyphen-name
description: One sentence describing what the skill does and the trigger condition.
---
```

## Required Sections

```markdown
# Skill Title

## Overview
Brief: what problem does this skill solve, in 2-3 sentences.

## When To Use
Trigger conditions — when this skill applies vs. doesn't.

## Workflow
Numbered steps. Be specific. Reference other skills by name when composing.

## Evidence And Verification
What the agent must produce or check to demonstrate the skill was followed.

## Common Rationalizations
Excuses agents (and humans) use to skip the workflow. Name them so they're easier to resist.

## Red Flags
Patterns that indicate the skill is being skipped or misapplied.

## Output Contract
Exactly what the skill produces. What the next step consumes.
```

## Optional Directories

```text
skills/<name>/
  SKILL.md         # required
  scripts/         # helper scripts the workflow may invoke
  references/      # checklists, examples
  assets/          # templates
  requirements.txt # optional Python deps (adapter-level skills only)
  .env.example     # env vars needed
```

## Style Guide

- Skills are workflows, not essays. Tell the agent what to do, what evidence to
  collect, and when to stop.
- Lists beat prose for steps.
- Cite or link related skills rather than duplicating their content.
- If a skill's workflow is over 7 steps, consider splitting.

## Compliance

Skills are advisory workflow guidance. `doctor.sh` validates frontmatter and
structure only — it does not enforce execution. Compliance comes from the
agent and the awareness files.
