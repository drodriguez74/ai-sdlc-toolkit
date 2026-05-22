---
name: security-and-hardening
description: Reduce security risk via threat modeling, input validation, auth, secrets handling, and least privilege. Use on security-sensitive changes and before production releases.
---

# Security and Hardening

## Overview

Security review is adversarial: assume inputs are hostile, assume systems will
be probed. Default to least privilege.

## When To Use

On any change touching auth, authorization, secrets, network boundaries,
dependencies with security history, or data classification.

## Workflow

1. Identify trust boundaries: where untrusted data enters trusted systems.
2. Verify input validation at every boundary.
3. Check auth and authorization: who can do what, under what conditions.
4. Inventory secrets: never in code, never in logs, sourced from managed services.
5. Review dependencies for known CVEs.
6. Apply least privilege to identities and tokens.
7. Add abuse-case tests where feasible.

## Evidence And Verification

- Trust boundaries are documented.
- Inputs are validated at the boundary.
- No secrets in code or logs.
- Dependencies pass scan.

## Common Rationalizations

- "It's an internal service" — internal services are breached internally.
- "We'll tighten it after launch" — you won't.

## Red Flags

- Wildcard permissions.
- Secrets in env files committed to git.
- Auth checks duplicated and inconsistent across endpoints.
- Logging request bodies that may contain secrets.

## Output Contract

Findings with severity, exploitability, mitigation; threat model summary; list
of abuse-case tests recommended.
