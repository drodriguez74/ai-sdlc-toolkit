---
name: scm-provider
description: Provider-neutral wrapper for SCM operations — diffs, PRs/MRs, commits, branches, reviews. Use when interacting with GitHub, GitLab, Bitbucket, or local git.
---

# SCM Provider (Integration Skill)

## Overview

The toolkit treats SCM as a queryable data source. The adapter contract handles
provider differences.

## When To Use

When reading diffs, PRs/MRs, commits, or branches. When posting review
comments programmatically.

## Workflow

1. Detect or confirm the active adapter (git, GitHub, GitLab).
2. Use `health` to verify the adapter is configured.
3. Use `diff`, `changed_files`, `pr_read`, `pr_review`, `mr_read`, `mr_review`
   per task.
4. For reviews, post structured findings, not free-form essays.
5. Never log tokens or sensitive metadata.

## Evidence And Verification

- Adapter health passes.
- Outputs cite commit SHA, PR number, or branch name.

## Common Rationalizations

- "I'll just shell out to git directly" — works locally, breaks in CI containers without git.
- "GitHub-only is fine" — until the next repo is on GitLab.

## Red Flags

- Hardcoded GitHub URLs in provider-neutral code.
- Logged auth tokens.

## Output Contract

Diff or PR/MR data referenced by SHA or PR number; adapter name used.
