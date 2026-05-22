---
name: data-engineering
description: Build safe data pipelines, schemas, and transformations with idempotency, quality checks, and rollback. Use when building or modifying ETL/ELT, warehouse models, or data contracts.
---

# Data Engineering

## Overview

Data pipelines are stateful systems with replay requirements. Build them
idempotent and observable from day one.

## When To Use

When building or modifying any pipeline, transformation, schema, or
data-contract.

## Workflow

1. Identify sources, targets, contracts, freshness, and quality requirements.
2. Make pipelines idempotent: re-runs produce identical output.
3. Make pipelines replay-safe: late or duplicate events don't corrupt state.
4. Validate schema changes for backward compatibility and migration safety.
5. Add quality checks: row counts, nulls, duplicates, drift, reconciliation.
6. Plan rollback for schema and pipeline changes.

## Evidence And Verification

- Pipeline produces the same output when re-run on the same input.
- Schema changes have a documented migration and rollback.
- Quality checks fail loudly when data drifts.

## Common Rationalizations

- "We'll add quality checks later" — by then, bad data is downstream.
- "Replays won't happen" — they always do.

## Red Flags

- Pipeline that mutates state non-deterministically.
- Schema migration without rollback.
- No reconciliation between source and target counts.

## Output Contract

Pipeline code with quality checks, schema change with migration and rollback,
documented contract.
