---
name: test-strategy
description: Assign scenarios to the right test layer (unit, integration, E2E). Use when planning the test approach for a feature or release.
---

# Test Strategy

## Overview

Tests at the wrong layer are expensive and slow. Push each scenario to the
lowest adequate layer.

## When To Use

When designing the testing approach for a feature, release, or refactor.

## Workflow

1. Inventory the behaviors and risk areas.
2. For each scenario, pick the lowest layer that can verify it adequately.
3. Keep E2E count small and focused on critical user journeys.
4. Identify gaps where current tests under-cover risk.
5. Flag pyramid anti-patterns: ice cream cone (E2E-heavy), hourglass (no integration).

## Evidence And Verification

- Each scenario is assigned a layer with justification.
- E2E coverage is bounded to critical journeys.
- Coverage map is explicit.

## Common Rationalizations

- "E2E gives the most confidence" — and the slowest feedback and the most flake.
- "Unit tests miss real bugs" — when they do, the unit boundary was wrong.

## Red Flags

- E2E suite that runs longer than the build.
- Unit tests that mock everything (test the wrong thing).
- No layer assigned for some scenarios.

## Output Contract

Layered scenario map: scenario → layer → rationale → existing or new test.
