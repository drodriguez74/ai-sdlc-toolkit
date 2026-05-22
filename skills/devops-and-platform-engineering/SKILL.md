---
name: devops-and-platform-engineering
description: Build reliable pipelines and platform automation with fast feedback and safe rollback. Use when modifying CI/CD or deployment automation.
---

# DevOps and Platform Engineering

## Overview

Pipelines are code that runs every change. They deserve the same engineering
rigor as the application.

## When To Use

When building or modifying CI/CD pipelines, deployment automation, or platform
tooling.

## Workflow

1. Detect CI/CD system and deployment model.
2. Add quality gates that fail fast: build, lint, unit tests, security scan.
3. Slower gates (integration, E2E) run after fast gates pass.
4. Keep secrets out of logs and artifacts.
5. Add observability: build duration, failure rate, flake rate.
6. Define rollback as part of the deployment pipeline, not as a manual step.

## Evidence And Verification

- Pipeline fails fast on simple errors.
- No secrets visible in logs.
- Rollback path is exercised, not assumed.
- Failure messages are actionable.

## Common Rationalizations

- "Pipelines are infrastructure; quick fixes are fine" — pipeline quality is feedback quality.
- "Manual rollback is good enough" — it is until the day it isn't.

## Red Flags

- Secrets printed in any log line.
- Failure that says only "test failed" with no link to logs.
- Rollback documented as "redeploy previous version" without scripts.

## Output Contract

Pipeline config with ordered gates, structured failure messages, and an
automated rollback step.
