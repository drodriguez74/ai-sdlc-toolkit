---
name: knowledge-base
description: Provider-neutral wrapper for knowledge bases — Confluence, wikis, local docs. Use when retrieving documentation for context.
---

# Knowledge Base (Integration Skill)

## Overview

Read-only access to org and project knowledge through a consistent interface.

## When To Use

When the task needs documentation context: architecture decisions, runbooks,
ADRs, prior incident reports.

## Workflow

1. Detect the active adapter (Confluence, local-docs, etc.).
2. Use the adapter's `search` and `read` commands.
3. Cite the source document in outputs.
4. Prefer linked docs over guessed knowledge.
5. Note when a relevant doc was not found.

## Evidence And Verification

- Outputs cite a specific document, not "the wiki".
- Search queries are documented.

## Common Rationalizations

- "I recall what the doc said" — recall drifts; check.
- "There's no doc, so I'll write something" — verify there really isn't one first.

## Red Flags

- Outputs based on assumed doc content.
- No citation when a doc is referenced.

## Output Contract

Cited document references; search queries used; explicit note if nothing
relevant was found.
