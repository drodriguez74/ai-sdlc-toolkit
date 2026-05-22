---
name: test-driven-development
description: Prove behavior through tests written before or alongside code. Use for any behavior change in code with existing test infrastructure.
---

# Test-Driven Development

## Overview

A failing test is the most reliable specification. TDD prevents drift between
intent and code.

## When To Use

Any behavior change in code that already has test infrastructure. Especially
on critical paths.

## Workflow

1. Write or identify a failing test for the behavior change.
2. Confirm the test fails for the expected reason.
3. Implement the minimum code to pass the test.
4. Confirm the test passes.
5. Run broader regression tests to confirm no breakage.
6. Refactor only with the test still green.

## Evidence And Verification

- The test failed first; you saw the failure message.
- The test passes after implementation.
- Broader test suite still passes.

## Common Rationalizations

- "I know what to write; tests are slower" — they aren't, over the whole cycle.
- "I'll add the test after" — tests added after rarely catch the right bug.

## Red Flags

- Implementation written first, test written after.
- Test that passes on first run (didn't actually verify failure mode).
- Skipping broader regression.

## Output Contract

The new test(s), the implementation, evidence the test failed initially and
passes now, and a note on regression test status.
