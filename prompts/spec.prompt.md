---
name: spec
description: Write a specification before implementation. Interview the user when requirements are unclear, then produce a complete spec.
skills:
  - using-agent-skills
  - interview-me
  - spec-driven-development
agent: product-manager
---

# /spec — Write a Specification

## Goal

Produce a complete, testable specification for the change requested.

## Instructions

1. Load and follow `skills/using-agent-skills/SKILL.md`.
2. If the request is vague or ambiguous, follow `skills/interview-me/SKILL.md`
   first to gather user, goal, constraints, scope, success criteria, and validation.
3. Follow `skills/spec-driven-development/SKILL.md` to produce the spec.
4. Adopt the perspective of the appropriate agent: `product-manager` for
   product features, `tech-lead` for technical changes.
5. Save the spec to a sensible location in the repo (e.g., `docs/specs/<name>.md`).

## Output

A specification document containing: objective, users, behavior, interfaces,
edge cases, errors, acceptance criteria, non-goals.
