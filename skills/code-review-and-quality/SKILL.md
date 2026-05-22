---
name: code-review-and-quality
description: Review changes before merge for correctness, security, performance, and tests. Use on every PR or diff before merging.
---

# Code Review and Quality

## Overview

Review is the second most leveraged engineering activity, after writing the
spec. Prioritize, ground in evidence, be specific.

## When To Use

On every PR or diff before merging. Also before declaring a task done in
single-developer flows.

## Workflow

1. Gather the diff, the spec or story, and related code.
2. Review in priority order: correctness → security → architecture → readability → performance → tests.
3. Prioritize findings: blocker, major, minor, nit.
4. Provide file:line references and concrete fix suggestions.
5. Note what is good, not only what is wrong.
6. Identify missing tests.

## Evidence And Verification

- Findings are prioritized.
- Every finding has file:line and a concrete fix.
- Tests have been reviewed, not only code.

## Common Rationalizations

- "Looks good to me" without evidence — that's not review.
- "Style is the most important" — style is the least important.

## Red Flags

- Review that lists style issues but not correctness.
- No mention of test coverage.
- LGTM on a non-trivial diff.

## Output Contract

Prioritized findings list with file:line references and concrete fixes; one
note on test coverage; explicit GO/REVIEW-AGAIN signal.
