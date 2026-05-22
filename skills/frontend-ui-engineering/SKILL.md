---
name: frontend-ui-engineering
description: Build production-quality user interfaces with attention to states, accessibility, and runtime verification. Use when implementing or modifying UI components.
---

# Frontend UI Engineering

## Overview

UIs that look right in dev are not the same as UIs that work for users.
Verification beats optimism.

## When To Use

When implementing or modifying any user-facing component or flow.

## Workflow

1. Follow the existing design system and component patterns.
2. Implement all required states: idle, loading, empty, error, success.
3. Verify responsive behavior at target breakpoints.
4. Use stable selectors so tests survive refactors.
5. Verify in a real browser when the change is visual.
6. Check the change against `accessibility-review` skill before declaring done.

## Evidence And Verification

- All required states render correctly.
- Real browser verification was done for visual changes.
- Keyboard navigation works.
- No new accessibility violations.

## Common Rationalizations

- "It looks right in the editor" — editor preview is not the user's browser.
- "Accessibility can come later" — it's exponentially more expensive later.

## Red Flags

- Component missing error or empty state.
- Test selectors coupled to implementation classes.
- No keyboard nav path.

## Output Contract

Component code plus evidence of runtime verification (screenshot, test output,
or behavior log) and accessibility check.
