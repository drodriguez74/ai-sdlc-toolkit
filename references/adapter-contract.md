# Adapter Contract

Provider-neutral integrations follow this contract.

## Manifest

Each adapter has an `adapter.json` matching `schemas/adapter.schema.json`:

```json
{
  "name": "jira",
  "domain": "issue-tracker",
  "commands": {
    "health":  "scripts/issue_search.py --help",
    "search":  "scripts/issue_search.py",
    "read":    "scripts/issue_read.py",
    "create":  "scripts/issue_create.py",
    "update":  null,
    "discover": null
  },
  "env": [
    {"name": "JIRA_BASE_URL", "required": true, "description": "..."}
  ],
  "outputs": {"format": "json", "path": ".ai-sdlc/adapter-out/"}
}
```

## Domains

- `issue-tracker` — Jira, GitHub Issues, GitLab Issues
- `scm` — git, GitHub, GitLab, Bitbucket
- `ci-cd` — GitHub Actions, GitLab CI, Jenkins
- `knowledge` — Confluence, local-docs
- `observability` — Splunk, local-logs
- `cloud` — AWS, Azure, GCP

## Script Requirements

Each adapter script must:

1. Support `--help`.
2. Implement a `health` (or equivalent) check.
3. Return non-zero on hard failure.
4. Produce machine-readable JSON to stdout where possible.
5. Print Markdown summaries to stdout when JSON is not the natural form.
6. Never log secrets or tokens.
7. Read configuration from environment variables declared in the manifest.

## Adding a New Adapter

1. Pick the correct domain folder under `tools/adapters/`.
2. Create a new subfolder named after the provider.
3. Write `adapter.json` (declare commands, env vars, outputs).
4. Implement scripts.
5. Validate: `doctor.sh` will check the manifest against the schema.

## Optional Dependencies

Adapter scripts may use Python stdlib only OR declare optional dependencies in
a `requirements.txt` within the adapter folder. The "no mandatory third-party
deps" rule applies to `tools/core/`, not adapters.
