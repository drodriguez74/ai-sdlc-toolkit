# Issue Tracker Adapters

Provider-neutral wrappers for issue trackers. Each subdirectory contains:

- `adapter.json` — manifest describing commands and env vars
- `scripts/` — executable scripts implementing the commands

## Active Adapter Selection

Set `ISSUE_TRACKER_ADAPTER` environment variable (e.g., `jira`, `github-issues`)
or specify in `.ai-sdlc/adapters.yaml`.

## Available

- `jira/` — Atlassian Jira
- `github-issues/` — GitHub Issues (search, read, create, update)
- `github-projects/` — GitHub Projects v2 boards via GraphQL (list projects, list items)

## GitHub Issues Commands

| Command | Script | Purpose |
|---|---|---|
| `search` | `scripts/issue_search.py` | Search issues by state/label |
| `read` | `scripts/issue_read.py <number>` | Read a single issue |
| `create` | `scripts/issue_create.py` | Create an issue via JSON stdin |
| `update` | `scripts/issue_update.py` | Update state, labels, assignees, milestone via JSON stdin |

## GitHub Projects v2 Commands

| Command | Script | Purpose |
|---|---|---|
| `discover` | `scripts/project_list.py` | List projects for an org or user |
| `read` | `scripts/project_items.py <number>` | List all items in a project with field values |

`github-projects` requires `GITHUB_OWNER` (org or user login) and a PAT with `read:project` scope.
Uses the GraphQL API (`https://api.github.com/graphql`).
