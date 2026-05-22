---
name: api-and-interface-design
description: Design stable contracts for APIs and interfaces between components. Use before implementing an endpoint, RPC, library API, or event schema.
---

# API and Interface Design

## Overview

Contracts last longer than implementations. Designing them deliberately saves
breaking changes later.

## When To Use

Before implementing any externally visible interface: HTTP API, RPC, library
exports, event schemas, CLI flags.

## Workflow

1. Identify consumers (current and likely future).
2. Define inputs and outputs explicitly: types, validation, defaults.
3. Define error handling: error shapes, codes, retryability.
4. Define versioning strategy.
5. Define idempotency for write operations.
6. Add contract tests or examples.

## Evidence And Verification

- Interface has explicit input/output schema.
- Errors are typed and documented.
- Idempotency is defined for writes.
- Versioning strategy is stated.

## Common Rationalizations

- "We can change it later" — once consumers depend on it, you can't.
- "Errors are obvious" — they aren't to consumers.

## Red Flags

- API returns generic strings for errors.
- No versioning strategy.
- Writes that aren't idempotent without acknowledgment.

## Output Contract

Interface spec: signature, schema, errors, versioning, idempotency, plus a
contract test or example.
