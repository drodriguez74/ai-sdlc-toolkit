---
name: incremental-implementation
description: Build in thin, verifiable slices. Use when implementing any task that will take more than a single small change.
---

# Incremental Implementation

## Overview

Thin slices each verified in isolation produce reliable systems. Big-bang
implementations produce regressions.

## When To Use

Any task longer than a single small change. Especially when touching shared
code or critical paths.

## Workflow

1. Select one task from the plan.
2. Read the local patterns: how does similar code in this repo work?
3. Implement minimum behavior to satisfy the task's acceptance criteria.
4. Verify with tests, build, or runtime evidence.
5. Keep the diff small and reversible.
6. Move to the next task; do not bundle.

## Evidence And Verification

- Tests pass for the new behavior.
- Build succeeds.
- Runtime evidence collected for behavior changes (logs, screenshots, request traces).

## Common Rationalizations

- "I'll just do all the related changes at once" — that's how PRs become unreviewable.
- "Tests can come at the end" — tests written after code rarely cover the bug-prone parts.

## Red Flags

- Diff touches many unrelated areas.
- No verification step.
- "I'll clean it up later" comments.

## Output Contract

A small, verified change with passing tests, build, and an explicit note of
how it was verified.
