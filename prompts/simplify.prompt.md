---
name: simplify
description: Simplify code without changing behavior. Requires existing test coverage.
skills:
  - using-agent-skills
  - code-simplification
agent: tech-lead
---

# /simplify — Simplify Code

## Goal

Reduce complexity (duplication, nesting, dead code, unclear names) while
preserving behavior.

## Instructions

1. Load and follow `skills/using-agent-skills/SKILL.md`.
2. Follow `skills/code-simplification/SKILL.md`.
3. Verify test coverage before simplifying.
4. Keep diffs small and reviewable.

## Output

Behavior-preserving diff with passing tests and a one-line summary of changes.
