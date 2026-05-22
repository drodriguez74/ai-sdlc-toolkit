---
name: issue-tracker
description: Provider-neutral wrapper for issue tracker operations — search, read, groom, create, update. Use when working with issues across Jira, GitHub Issues, GitLab, etc.
---

# Issue Tracker (Integration Skill)

## Overview

Treat issue trackers as data sources. The toolkit's adapter contract abstracts
provider differences.

## When To Use

When the task involves searching, reading, creating, or updating issues. When
a story or bug needs context from the tracker.

## Workflow

1. Detect or confirm the active adapter (Jira, GitHub Issues, GitLab, etc.).
2. Use the adapter's `discover` and `health` commands to verify config.
3. Use `search`, `read`, `create`, `update` per task.
4. Cache results when iterating; don't re-query for the same record.
5. Never log issue body content that may include secrets.

## Evidence And Verification

- Adapter health passes.
- Operations cite the adapter used.
- Outputs include issue ID and URL.

## Common Rationalizations

- "I'll paste the title; that's enough" — context lives in body and comments.
- "I'll create now and update later" — leads to duplicates.

## Red Flags

- Hardcoded provider-specific calls bypassing the adapter.
- Logged issue body that contains credentials.

## Output Contract

Issue references with ID and URL; adapter name used; cached payload when
relevant.
