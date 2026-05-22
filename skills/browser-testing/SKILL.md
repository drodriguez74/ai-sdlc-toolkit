---
name: browser-testing
description: Verify browser behavior with real runtime evidence — DOM, console, network, accessibility, screenshots. Use when a UI change must be confirmed in an actual browser.
---

# Browser Testing

## Overview

UI code can compile, type-check, and unit-test green yet still be broken at
runtime. Real browser verification catches that gap.

## When To Use

When a change is visual or interactive and the harness supports browser
automation or screenshots.

## Workflow

1. Start the app (or use the running instance).
2. Navigate to the affected path.
3. Inspect: DOM structure, console errors, network requests.
4. Validate the user flow end-to-end.
5. Capture evidence: screenshot, console log, request trace.
6. Run accessibility audit on the changed page.

## Evidence And Verification

- Real screenshot or console output exists.
- No new console errors on the affected pages.
- Network requests match expectations.

## Common Rationalizations

- "Tests pass; I don't need a screenshot" — tests can pass while the UI looks wrong.
- "I'll check after PR" — by then, reviewers have wasted time.

## Red Flags

- No runtime evidence captured.
- Console errors ignored.
- 404s or 500s in network ignored.

## Output Contract

Evidence artifact (screenshot, console log, or recording) plus a one-line
summary of what was verified.
