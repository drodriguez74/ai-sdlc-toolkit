---
name: cloud-engineering
description: Build cloud infrastructure with least privilege, IaC, and reversible changes. Use when designing or modifying cloud resources.
---

# Cloud Engineering

## Overview

Cloud changes have wide blast radius and slow rollback. Design for reversibility
and least privilege.

## When To Use

When designing or modifying any cloud resource: networking, compute, identity,
storage, secrets.

## Workflow

1. Detect provider and IaC tool.
2. Apply least privilege: identities have only what they need.
3. Use managed secrets services; never put secrets in code or env files in git.
4. Plan rollback before applying.
5. Plan drift detection.
6. Surface cost impact before deployment.

## Evidence And Verification

- IaC is the source of truth; manual console changes are flagged.
- Identities follow least privilege.
- Rollback path is automated.
- Drift detection is configured.

## Common Rationalizations

- "Just give it admin to ship faster" — that becomes the permanent state.
- "We'll add drift detection later" — drift compounds silently.

## Red Flags

- Wildcard IAM policies (`*`).
- Secrets in env files committed to repo.
- Changes applied via console without IaC update.

## Output Contract

IaC code with least-privilege identities, secret references (not values),
rollback plan, drift detection.
