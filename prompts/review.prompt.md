---
name: review
description: Review a diff for correctness, security, performance, and test coverage.
skills:
  - using-agent-skills
  - code-review-and-quality
  - security-and-hardening
agent: code-reviewer
---

# /review — Code Review

## Goal

Produce prioritized findings before merge.

## Instructions

1. Load and follow `skills/using-agent-skills/SKILL.md`.
2. Load the diff (use `scm-provider` skill if needed).
3. Follow `skills/code-review-and-quality/SKILL.md`.
4. For security-sensitive areas, also follow `skills/security-and-hardening/SKILL.md`.
5. Adopt the `code-reviewer` agent perspective.

## Output

Prioritized findings (blocker / major / minor / nit) with file:line references
and concrete fixes. Explicit GO / REVIEW-AGAIN signal.
