---
name: ci-cd-and-automation
description: Automate validation and delivery with fast feedback, secure secret handling, and actionable failures. Use when modifying CI/CD configs.
---

# CI/CD and Automation

## Overview

The pipeline is the safety net. Make it fast, accurate, and informative.

## When To Use

When adding or modifying CI/CD configuration, build steps, or release
automation.

## Workflow

1. Detect the existing pipeline tooling.
2. Add gates in order from fast to slow: lint → unit → build → integration → security → packaging.
3. Fail fast: simple errors stop the pipeline before expensive jobs run.
4. Keep secrets out of logs.
5. Make failure messages actionable: include context, command, link to logs.
6. Optimize feedback speed: parallelize independent jobs, cache responsibly.

## Evidence And Verification

- Pipeline runs in reasonable time.
- Failures are actionable.
- No secrets in logs or artifacts.

## Common Rationalizations

- "We can speed it up later" — it never gets faster on its own.
- "The error message is fine" — the next on-call disagrees.

## Red Flags

- Single monolithic job that runs everything.
- Failure message that says only "exit 1".
- Secrets echoed in any step.

## Output Contract

Pipeline configuration with ordered gates, fast feedback, structured failure
output, and secret hygiene.
