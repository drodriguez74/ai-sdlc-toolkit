---
name: accessibility-review
description: Verify inclusive UX via keyboard nav, semantic roles, labels, contrast, and screen-reader structure. Use on any user-facing change.
---

# Accessibility Review

## Overview

Accessibility is not optional; it's UX for the people most affected by your
choices. Build it in, don't bolt it on.

## When To Use

On any user-facing change. Especially on new components and form interactions.

## Workflow

1. Verify keyboard navigation: every action reachable and operable from keyboard.
2. Verify semantic structure: headings, landmarks, lists used semantically.
3. Verify labels and roles: form fields labeled; icons have accessible names.
4. Verify contrast: text meets WCAG AA minimum (4.5:1 normal, 3:1 large).
5. Verify focus visibility: focus indicator visible on all interactive elements.
6. Verify screen-reader-relevant structure: dynamic content announced.

## Evidence And Verification

- Keyboard nav was tested, not assumed.
- Contrast was measured, not eyeballed.
- Screen reader output is meaningful for the change.

## Common Rationalizations

- "Our users don't use screen readers" — you don't actually know that.
- "It works with a mouse" — a quarter of users prefer keyboard or assistive tech.

## Red Flags

- Click handlers on non-interactive elements without keyboard equivalents.
- Form fields without labels.
- Color as the only state indicator.
- `tabindex` greater than 0.

## Output Contract

A11y checklist results per area (keyboard, semantics, labels, contrast, focus,
screen reader) with pass/fail and notes.
