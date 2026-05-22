---
name: ship
description: Decide GO/NO-GO for a release using multi-dimensional review and produce a rollback plan.
skills:
  - using-agent-skills
  - shipping-and-launch
agent: release-manager
---

# /ship — Release Decision

## Goal

Produce a GO/NO-GO decision with specialist evidence and a rollback plan.

## Instructions

1. Load and follow `skills/using-agent-skills/SKILL.md`.
2. Follow `skills/shipping-and-launch/SKILL.md`.
3. Fan out to specialist agents when the harness supports subagents:
   - `code-reviewer`
   - `security-auditor`
   - `test-engineer`
   - `performance-reviewer` (if performance-sensitive)
   - `data-reviewer` (if data pipelines or schemas changed)
4. **Single-agent fallback**: when subagents are not supported, run specialists
   sequentially in the same order. Output format is identical.
5. Adopt the `release-manager` perspective for the merged decision.

## Output

```markdown
## Ship Decision: GO | NO-GO

### Blockers
### Recommended Fixes
### Acknowledged Risks
### Rollback Plan
### Specialist Reports
```
