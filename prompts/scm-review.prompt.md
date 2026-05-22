---
name: scm-review
description: Read a PR/MR diff and produce a structured review comment.
skills:
  - using-agent-skills
  - scm-provider
  - code-review-and-quality
agent: code-reviewer
---

# /scm-review — Review a PR or MR

## Goal

Fetch and review a PR/MR using the SCM adapter.

## Instructions

1. Load `skills/using-agent-skills/SKILL.md`.
2. Follow `skills/scm-provider/SKILL.md` to fetch the diff.
3. Follow `skills/code-review-and-quality/SKILL.md` to review.
4. Post structured findings via the adapter when supported.

## Output

Review with prioritized findings, file:line references, and concrete fixes.
