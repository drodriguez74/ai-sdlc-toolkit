---
name: debugging-and-error-recovery
description: Fix failures by root cause, not symptoms. Use when investigating a bug, failed test, or production incident.
---

# Debugging and Error Recovery

## Overview

A fix that doesn't explain the cause is a fix that will return. Debug by
narrowing the search space deliberately.

## When To Use

When investigating any bug, failed test, or unexpected behavior.

## Workflow

1. **Reproduce**: get a deterministic trigger. If you can't reproduce, fix that first.
2. **Localize**: narrow the search to a file or function via tests, logs, or git bisect.
3. **Reduce**: shrink the failing case to the smallest reproducer.
4. **Fix**: change the root cause, not the symptom.
5. **Guard**: add a test or monitoring that would catch the regression next time.

## Evidence And Verification

- The failure is reproducible.
- The fix targets the cause, not a symptom.
- A test now covers the failure case.

## Common Rationalizations

- "I can fix this without reproducing" — sometimes; usually you fix the wrong thing.
- "It's intermittent; we'll just retry" — intermittent failures are timing or state bugs.

## Red Flags

- Try-catch that swallows the error to "make it pass".
- Fix that says "this should work now" without reproducing.
- Adding sleep() to fix a test.

## Output Contract

Reproduction steps, root cause explanation, the fix, and a guard test or
monitor.
