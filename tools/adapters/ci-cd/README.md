# CI/CD Adapters

Read pipeline state, trigger runs, and fetch failure logs from a CI/CD system.

## Available

- `github-actions/` — workflow runs via GitHub REST API
- `gitlab-ci/` — pipeline status via GitLab REST API
- `jenkins/` — Jenkins job status via REST/JSON API

## GitHub Actions Adapter Commands

| Command | Script | Purpose |
|---|---|---|
| `health` | `scripts/health.py` | Verify token access |
| `discover` | `scripts/workflow_list.py` | List all workflows in the repo |
| `search` | `scripts/run_list.py` | List runs (filter by workflow, branch, status) |
| `read` | `scripts/run_read.py <run_id>` | Read a run's jobs and step conclusions |
| `logs` | `scripts/run_logs.py <run_id>` | Download and extract log text (`--failed-only` to filter) |
| `trigger` | `scripts/run_trigger.py <workflow>` | Trigger a workflow_dispatch event |
| `rerun` | `scripts/run_rerun.py <run_id>` | Re-run all or failed jobs only (`--failed-only`) |

## Required Token Scopes

- `actions:read` — health, discover, search, read, logs
- `actions:write` — additionally required for trigger and rerun
