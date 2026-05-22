---
name: log-search
description: Provider-neutral log query and summary. Use when investigating production behavior or building evidence for an incident.
---

# Log Search (Integration Skill)

## Overview

Logs are evidence. The toolkit's adapter wraps Splunk, Cloud logs, local files,
etc., behind a consistent interface.

## When To Use

When investigating a bug, incident, or unexpected production behavior.

## Workflow

1. Detect or confirm the active adapter (Splunk, local-logs, etc.).
2. Use `health` to verify the adapter.
3. Construct a query tied to the symptom: time range, service, severity, key terms.
4. Search; sample; iterate to narrow.
5. Summarize: what's happening, when it started, what changed.
6. Quote log lines verbatim in evidence; do not paraphrase what they say.

## Evidence And Verification

- Query is reproducible.
- Summary distinguishes observations from inferences.
- Log lines are quoted verbatim, not paraphrased.

## Common Rationalizations

- "The logs basically say X" — quote them; basically isn't precise enough.
- "I'll trust the dashboard" — dashboards aggregate; logs have specifics.

## Red Flags

- Conclusions without log evidence.
- Logging of secrets in any summary output.

## Output Contract

Query used; representative log lines quoted; summary of observations; explicit
unknowns.
