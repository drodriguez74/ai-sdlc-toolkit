---
name: using-agent-skills
description: Decide which skill applies to a task and enforce skill usage. Use at the start of any non-trivial task before acting.
---

# Using Agent Skills

## Overview

Skills exist so agents don't reinvent process per task. This meta-skill ensures
the right skill is loaded before work begins.

## When To Use

At the start of any non-trivial task — feature, fix, review, ship, debug,
refactor. Skip only for purely informational questions.

## Workflow

1. Read the user request.
2. Scan available skills under `.github/skills/` (or `skills/` globally).
3. Identify matching skills by task type. Multiple skills may apply.
4. Load the matching SKILL.md files.
5. Combine skills only when responsibilities are complementary, not redundant.
6. Never skip a skill because the task seems small.

## Evidence And Verification

- State which skills you loaded before acting.
- Reference the skill's Workflow sections you followed.
- If no skill matches, say so explicitly rather than improvising silently.

## Common Rationalizations

- "This is too small to need a skill" — small tasks are where skills prevent
  regressions.
- "I know the workflow already" — the skill is the workflow of record; load it.

## Red Flags

- Working without naming the skill being followed.
- Skipping `workspace-analysis` in an unfamiliar repo.
- Skipping `code-review-and-quality` before merge.

## Output Contract

When followed, the assistant's response should: (1) name the skill(s) loaded,
(2) reference the steps applied, (3) produce the outputs the skill specifies.
