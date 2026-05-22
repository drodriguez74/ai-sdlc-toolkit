---
name: spec-driven-development
description: Write a specification before implementation. Use for any change beyond trivial fixes — features, refactors with behavior implications, or new services.
---

# Spec-Driven Development

## Overview

A spec written before code prevents the most expensive class of bugs: building
the wrong thing.

## When To Use

Before any change that adds or modifies behavior. Skip only for typo fixes,
formatting, or pure rename refactors.

## Workflow

1. Discover repo context: read `project-context.md`, related code, prior ADRs.
2. Clarify objective: what changes, for whom, why now.
3. Define behavior: inputs, outputs, edge cases, error paths.
4. Define interfaces and data flow.
5. Define acceptance criteria — verifiable, not aspirational.
6. List explicit non-goals.
7. Save or present the spec.

## Evidence And Verification

- Spec sections are complete; no "TBD" in critical paths.
- Acceptance criteria are testable.
- Non-goals are stated.

## Common Rationalizations

- "This is too small for a spec" — if it changes behavior, it deserves five lines.
- "We'll figure it out as we code" — that's how regressions happen.

## Red Flags

- Implementation discussion before acceptance criteria.
- "It should just work like…" without examples.

## Output Contract

A spec containing: objective, users, behavior, interfaces, edge cases, errors,
acceptance criteria, non-goals.
