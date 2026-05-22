# Accessibility Checklist

Use during `accessibility-review` skill execution. Targets WCAG 2.1 AA.

## Keyboard

- [ ] All interactive elements reachable via Tab.
- [ ] Tab order matches visual order.
- [ ] Focus is visible (not hidden by CSS).
- [ ] Enter and Space activate buttons and links.
- [ ] Esc closes modals and menus.
- [ ] No keyboard traps.

## Semantics

- [ ] Headings used in order (h1, h2, h3 — no skipping).
- [ ] Landmarks present (main, nav, header, footer).
- [ ] Lists used for lists; tables used for tabular data.
- [ ] Buttons used for actions; links used for navigation.

## Labels and ARIA

- [ ] Every form field has a label (visible or aria-label).
- [ ] Icons used as buttons have aria-label.
- [ ] aria-live used for dynamic content updates.
- [ ] aria-expanded reflects state for collapsible elements.
- [ ] No tabindex > 0.

## Color and Contrast

- [ ] Text contrast ≥ 4.5:1 (normal) or 3:1 (large/bold).
- [ ] State not communicated by color alone (add icon or text).
- [ ] Focus indicator contrast ≥ 3:1 against background.

## Media

- [ ] Images have descriptive alt or empty alt for decorative.
- [ ] Videos have captions.
- [ ] No auto-playing audio.
