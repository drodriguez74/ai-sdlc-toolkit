---
name: backend-engineering
description: Build robust backend behavior with proper validation, error handling, transactions, and observability. Use when implementing or modifying server-side logic.
---

# Backend Engineering

## Overview

Backend code runs forever, under load, with hostile inputs. Building for that
reality from the start beats retrofitting.

## When To Use

When implementing or modifying any server-side behavior: APIs, jobs, workers,
event handlers, persistence.

## Workflow

1. Identify service boundaries and data contracts.
2. Follow existing patterns for validation, logging, errors, and transactions.
3. Validate inputs at the boundary; trust internal calls.
4. Protect shared interfaces with tests.
5. Verify operational behavior: timeouts, retries, idempotency.
6. Make logs structured and free of secrets.

## Evidence And Verification

- Boundary inputs are validated.
- Errors are typed; logs include context but not secrets.
- Tests cover happy path and key failure modes.
- Timeouts and retries are explicit.

## Common Rationalizations

- "This won't fail in practice" — services fail; design for failure.
- "Logs will help me debug later" — only if they have structure and context.

## Red Flags

- Unvalidated input reaching business logic.
- Silent retries that mask failures.
- Logs that print full request bodies (often contain secrets).

## Output Contract

Code with explicit validation, structured logs, defined error handling, and
tests covering happy and failure paths.
