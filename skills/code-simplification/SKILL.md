---
name: code-simplification
description: Simplify code without behavior change. Use when reading code reveals duplication, dead paths, or excessive nesting in stable areas.
---

# Code Simplification

## Overview

Simpler code is cheaper to maintain. Simplification is safe only when behavior
is verified preserved.

## When To Use

When code is hard to read, when duplication is obvious, when nesting is deep,
when names obscure intent. Only in code with adequate tests or characterization.

## Workflow

1. Understand current behavior fully before changing it.
2. Ensure tests or characterization tests exist.
3. Remove duplication, dead code, unused parameters, unclear names.
4. Reduce nesting via early return, guard clauses, extraction.
5. Verify behavior is unchanged — tests still pass.
6. Keep the diff small and reviewable.

## Evidence And Verification

- Tests pass before and after.
- No new behavior is introduced.
- Diff is small enough to review.

## Common Rationalizations

- "While I'm here, I'll fix this too" — that's how simplifications cause regressions.
- "I'll improve the test as I refactor" — refactor and test changes belong in separate diffs.

## Red Flags

- Simplifying code with no tests.
- Combining a refactor with a behavior change.
- Diff that touches many unrelated areas.

## Output Contract

Behavior-preserving diff; passing tests; one-line note on what was simplified
and why.
