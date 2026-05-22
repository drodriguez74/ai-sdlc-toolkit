---
name: performance-optimization
description: Improve performance through measurement, one change at a time. Use when performance is a known problem or when a change is performance-sensitive.
---

# Performance Optimization

## Overview

Premature optimization is the wrong instinct. Measure first, find the binding
constraint, change one thing.

## When To Use

When a performance issue is reported or measured. When a change touches a hot
path.

## Workflow

1. Define the target metric (latency, throughput, memory, etc.).
2. Measure the baseline with the same setup you'll use to measure the change.
3. Identify the binding constraint: CPU, memory, IO, network, lock contention, GC.
4. Change one thing.
5. Re-measure.
6. Repeat. Stop when the target is met or returns diminish.

## Evidence And Verification

- Baseline and result have the same setup.
- Each change has a measured effect.
- Constraint is identified, not guessed.

## Common Rationalizations

- "This will be faster" — without measurement, this is a hope.
- "Let me parallelize and add caching" — that's three changes; measure one.

## Red Flags

- Optimization without a baseline.
- "Just adding a cache" without measuring miss rate or invalidation.
- Multiple simultaneous changes.

## Output Contract

Baseline measurement, identified constraint, change made, post-change
measurement, decision on next iteration.
