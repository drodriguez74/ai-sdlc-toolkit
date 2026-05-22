# Security Adapters

Provider-neutral security alert integrations.

## Available Adapters

| Adapter | Covers |
|---|---|
| `github-security` | Dependabot, code scanning (CodeQL/SARIF), secret scanning alerts |

## Required Token Scopes

`github-security` needs a PAT with:
- `security_events` — for Dependabot and code scanning alerts
- `repo` admin access — for secret scanning alerts (or GitHub Advanced Security enabled)

## Usage

```bash
export GITHUB_TOKEN=ghp_...
export GITHUB_REPO=owner/repo

# Dependabot vulnerabilities (open, high+)
python3 github-security/scripts/dependabot_list.py --severity high

# Code scanning alerts (CodeQL, open)
python3 github-security/scripts/code_scanning_list.py --tool CodeQL

# Secret scanning alerts
python3 github-security/scripts/secret_scanning_list.py
```

Output is JSON written to `.ai-sdlc/adapter-out/` for consumption by the
`security-auditor` agent via `/review` or a dedicated security scan session.
