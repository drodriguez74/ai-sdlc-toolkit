# Testing Patterns

## Test Pyramid

- **Unit**: fast, many, isolated. Cover branching logic, edge cases, error paths.
- **Integration**: medium speed, fewer, real dependencies (DB, queues).
- **Contract**: verify provider/consumer interface compatibility.
- **E2E**: slow, fewest, only critical user journeys.

## Anti-Patterns

- **Ice cream cone**: more E2E than unit. Symptom: slow, flaky suite.
- **Hourglass**: lots of unit + E2E, no integration. Symptom: bugs at component seams.
- **Mock-heavy unit**: testing the test, not the code. Symptom: refactors break many tests.

## When To Add Each Layer

- Branching logic → unit
- Validation rules → unit
- Boundary translations → integration
- Provider/consumer interfaces → contract
- Money paths, signup, checkout, auth → E2E
- Time-sensitive flows (cron, schedulers) → integration with time control

## Flake Hygiene

- Time and randomness must be injectable, not real-clock.
- External services must be sandboxed, not live.
- Order-dependent tests must be made order-independent or marked explicitly.
- Sleeps in tests are bugs.
