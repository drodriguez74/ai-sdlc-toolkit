---
name: context-engineering
description: Manage the context an AI needs to work well — load relevant files, ignore irrelevant ones, refresh on scope change. Use whenever starting work or when scope shifts.
---

# Context Engineering

## Overview

The AI's quality is bounded by the context it has loaded. Curating that context
is a first-class engineering task.

## When To Use

At the start of any task. When the task scope changes. When the AI starts
producing irrelevant outputs.

## Workflow

1. Locate the source-of-truth files for this task: spec, related code, ADRs,
   recent changes, project-context.md.
2. Read only the parts needed; skip what's irrelevant.
3. Summarize what was loaded so the user can audit.
4. When scope changes, refresh context — drop stale items, load new ones.
5. Never assume context that wasn't explicitly loaded.

## Evidence And Verification

- The agent can name what was loaded.
- Outputs cite loaded files, not invented ones.
- Context refresh happens when scope shifts.

## Common Rationalizations

- "I'll just load everything" — context windows are finite; signal beats noise.
- "I remember the context from last task" — sessions and tasks shift; reload.

## Red Flags

- Output references files that weren't loaded.
- Stale information from a prior task leaking into a new one.

## Output Contract

Explicit list of files loaded for the task; one-line summary of each.
