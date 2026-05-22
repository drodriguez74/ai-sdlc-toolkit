---
name: shipping-and-launch
description: Decide GO/NO-GO for a release using multi-dimensional checks and a rollback plan. Use before any production release.
---

# Shipping and Launch

## Overview

Shipping is a yes/no decision based on evidence across many dimensions. The
output is GO, NO-GO, or specific blockers.

## When To Use

Before any production release. Before merging a high-risk change to main.

## Workflow

1. Check tests: pass rate, coverage of the change, recent flake.
2. Check CI: pipeline green; required gates passed.
3. Check docs: user-facing docs updated; ADRs filed for material decisions.
4. Check security: review complete; no unresolved findings above threshold.
5. Check performance: no regression on key metrics.
6. Check accessibility: review complete for user-facing changes.
7. Check observability: logs, metrics, traces in place for new behavior.
8. Check feature flags / rollout plan: gradual rollout configured if applicable.
9. Check migrations: forward and rollback paths exist.
10. Use parallel review fan-out when supported. Sequential fallback otherwise.
11. Produce GO/NO-GO with blockers, recommended fixes, acknowledged risks,
    rollback plan.

## Evidence And Verification

- Every dimension has an explicit check.
- Blockers are specific and actionable.
- Rollback plan exists and is testable.

## Common Rationalizations

- "We can patch after launch" — for some things; not for all.
- "Tests are flaky but the change is safe" — investigate flake before shipping.

## Red Flags

- Shipping with unresolved security findings above policy threshold.
- No rollback plan.
- Skipping any dimension because it's "fine for this one".

## Output Contract

```markdown
## Ship Decision: GO | NO-GO

### Blockers
### Recommended Fixes
### Acknowledged Risks
### Rollback Plan
### Specialist Reports
```
