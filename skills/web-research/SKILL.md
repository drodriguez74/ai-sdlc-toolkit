---
name: web-research
description: Search current public information through the harness's web tools when allowed by policy. Use when current external information is required.
---

# Web Research (Integration Skill)

## Overview

When the task depends on current external information (API docs, library
behavior, security advisories), use the harness's web tools — not memory.

## When To Use

When the task depends on information that may have changed since the model's
training cutoff. When verifying claims about external systems.

## Workflow

1. Confirm the harness allows web access for this task.
2. Construct queries that are specific: include version, date, exact terms.
3. Open the actual source, not just search snippets.
4. Note the URL and the date accessed.
5. Distinguish authoritative sources (official docs) from secondary (blog posts).
6. Prefer the official source for behavior claims.

## Evidence And Verification

- URLs are cited.
- Source authority is identified.
- Date of access is noted.

## Common Rationalizations

- "I remember reading…" — memory drifts; cite the source.
- "The first result is good enough" — sometimes; verify with the official source.

## Red Flags

- Claims about external systems without citation.
- Citations from outdated or low-authority sources for current behavior.

## Output Contract

URL citations with authority level and access date; explicit distinction
between official and secondary sources.
