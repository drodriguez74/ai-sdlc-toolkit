---
name: documentation-and-adrs
description: Preserve why decisions were made via ADRs and operational docs. Use when making non-obvious architectural decisions or onboarding new operators.
---

# Documentation and ADRs

## Overview

Code shows what; docs preserve why. ADRs are the cheapest way to keep that
knowledge.

## When To Use

When making any non-obvious decision: architecture, vendor choice, deprecation,
contract change. When writing onboarding or operational runbooks.

## Workflow

1. Identify audience and decision scope.
2. For ADRs: record context, options, decision, consequences, status.
3. For runbooks: write for the on-call who hasn't seen the system before.
4. Keep examples runnable and verified.
5. Link docs back to code and operations.

## Evidence And Verification

- ADRs have all five sections.
- Examples in docs are runnable.
- Doc is dated and has a status.

## Common Rationalizations

- "Everyone knows this" — not in two years they won't.
- "Docs will rot" — undocumented decisions rot faster.

## Red Flags

- Decision made without an ADR.
- Runbook step that says "do the usual".
- Doc with no date and no status.

## Output Contract

ADR or runbook with all required sections, dated, with status, linked from
relevant code.
