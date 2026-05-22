---
name: git-workflow-and-versioning
description: Keep source control clean — atomic commits, clear messages, separated changes. Use when committing changes or preparing a PR.
---

# Git Workflow and Versioning

## Overview

A clean history is documentation for the future. Atomic commits with clear
messages save hours during incidents.

## When To Use

When committing, branching, or preparing PRs.

## Workflow

1. Inspect the working tree before staging.
2. Separate unrelated changes into separate commits.
3. Keep each commit atomic: one logical change.
4. Write commit messages that explain WHY, not just WHAT (the diff shows what).
5. Reference the issue or spec when applicable.

## Evidence And Verification

- Commits are atomic.
- Messages explain motivation.
- No "fix typo" or "wip" commits in shared history.

## Common Rationalizations

- "I'll squash later" — sometimes; usually history degrades.
- "The message doesn't matter; I'll remember" — you won't.

## Red Flags

- Commit message that just repeats the file name.
- One commit with mixed feature + refactor + tests + style.
- Force push to shared branch.

## Output Contract

Clean atomic commits with messages explaining motivation; no mixed-purpose
commits.
