---
name: deprecation-and-migration
description: Remove or migrate APIs and code safely with compatibility windows and consumer tracking. Use when deprecating an interface or migrating to a replacement.
---

# Deprecation and Migration

## Overview

Removing a thing in production is harder than adding it. Plan the compatibility
window and the evidence for removal.

## When To Use

When removing or replacing an API, library, schema, or feature with active
consumers.

## Workflow

1. Inventory consumers: who uses the thing being removed.
2. Define a compatibility window: how long both old and new exist.
3. Add a migration path: docs, codemod, or automated translation.
4. Add deprecation warnings or telemetry to track adoption.
5. Monitor adoption until consumer use is below the removal threshold.
6. Remove only with evidence, not on a schedule.

## Evidence And Verification

- Consumer inventory exists.
- Migration path is tested.
- Adoption metric is monitored.
- Removal happens after evidence, not before.

## Common Rationalizations

- "We've announced; people had time" — announcement isn't adoption.
- "The new way is clearly better" — that's not evidence consumers have moved.

## Red Flags

- Removal on a calendar date without measured adoption.
- No migration path.
- Deprecation warning that consumers can't actually act on.

## Output Contract

Migration plan: consumer inventory, compatibility window, migration path,
adoption metric, removal criteria.
