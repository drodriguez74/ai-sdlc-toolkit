---
name: source-driven-development
description: Ground framework and library decisions in authoritative sources, not stale memory. Use when a non-trivial decision depends on framework or library behavior.
---

# Source-Driven Development

## Overview

LLM and human memory of framework behavior drifts with version changes. When
behavior matters, check the authoritative source.

## When To Use

When the change depends on framework or library semantics: hooks, lifecycle,
threading, concurrency, error handling, deprecation.

## Workflow

1. Identify the library/framework and the installed version.
2. Locate the authoritative source: official docs for that version, source code,
   or release notes.
3. Verify the behavior you're relying on is current — not deprecated, not removed.
4. Avoid patterns that were idiomatic in earlier versions but are now anti-patterns.
5. Cite or note the source consulted.

## Evidence And Verification

- The version is confirmed (from package manifest, not assumed).
- The pattern used matches current docs.
- Cited source can be re-checked later.

## Common Rationalizations

- "I've used this pattern for years" — versions moved on; you may not have.
- "The docs are the same" — they often aren't.

## Red Flags

- Using deprecated APIs without acknowledgment.
- Pattern advice that doesn't reference a version.
- Mixing patterns from major versions of the same library.

## Output Contract

The code change plus a note of which source was consulted and which version
applies.
