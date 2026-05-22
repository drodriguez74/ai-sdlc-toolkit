# Security Checklist

Use during `security-and-hardening` skill execution.

## Identity and Access

- [ ] Identities have least privilege (no wildcards).
- [ ] Service-to-service auth is explicit (mTLS, signed tokens).
- [ ] Human access uses MFA and audit logging.
- [ ] No shared credentials between environments.

## Input Validation

- [ ] All inputs validated at trust boundaries.
- [ ] Validation uses an allowlist where feasible.
- [ ] Size limits applied to user-supplied data.
- [ ] Content type matches expectation.

## Secrets

- [ ] No secrets in source code, commit history, or build logs.
- [ ] Secrets sourced from managed services (AWS Secrets Manager, Vault, etc.).
- [ ] Secrets rotation strategy exists.
- [ ] Sample secrets in `.env.example` are obviously fake.

## Output and Logging

- [ ] Logs do not contain secrets, tokens, or sensitive PII.
- [ ] Error messages do not leak internal state to untrusted users.
- [ ] User-controlled data is encoded for output context (HTML, SQL, shell).

## Dependencies

- [ ] Dependency scan clean on production paths.
- [ ] Pinned versions in production lockfiles.
- [ ] License compatibility checked.

## Operational

- [ ] Rate limits in place on auth and write paths.
- [ ] Anomaly alerts wired for auth, payment, privilege change events.
- [ ] Backups exist and restore is tested.
