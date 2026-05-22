---
name: planning-and-task-breakdown
description: Turn a spec into implementable tasks with dependencies and acceptance. Use after a spec is ready and before implementation starts.
---

# Planning and Task Breakdown

## Overview

A good plan slices vertically: each task delivers a small, demonstrable behavior
change with its own verification.

## When To Use

After spec is ready, before implementation. Use any time work is larger than a
single change.

## Workflow

1. Read the spec and relevant code.
2. Identify the dependency graph: what must come before what.
3. Slice vertically: each task delivers a behavior, not a layer.
4. For each task: write acceptance criteria and a verification method.
5. Identify parallelizable work and blockers.
6. Order by value × dependency × risk.

## Evidence And Verification

- Each task has its own acceptance criteria.
- Tasks are small enough to verify independently.
- Critical path is identified.

## Common Rationalizations

- "Let's just figure out the order as we go" — discoverable order is the slowest order.
- "All tasks are equal priority" — they aren't.

## Red Flags

- Tasks defined by layer (controllers, services, models) instead of behavior.
- No acceptance criteria per task.
- Plan that fits everything in "phase 1".

## Output Contract

Ordered list of tasks with: title, behavior delivered, acceptance criteria,
verification method, dependencies, estimated risk.
