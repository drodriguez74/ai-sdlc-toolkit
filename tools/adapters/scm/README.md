# SCM Adapters

Provider-neutral wrappers for source control operations.

## Available

- `git/` — local git operations (diff, changed files)
- `github/` — GitHub PR read/review, releases, environments, check runs
- `gitlab/` — GitLab MR read/review

## GitHub Adapter Commands

| Command | Script | Purpose |
|---|---|---|
| `pr_read` | `scripts/pr_read.py <number>` | Read a PR by number |
| `pr_review` | `scripts/pr_review.py` | Post a review (APPROVE / REQUEST_CHANGES / COMMENT) via JSON stdin |
| `release_list` | `scripts/release_list.py` | List recent releases |
| `release_create` | `scripts/release_create.py` | Create a release via JSON stdin |
| `environment_list` | `scripts/environment_list.py` | List environments + protection rules |
| `check_runs` | `scripts/check_runs.py <ref>` | List check runs for a commit SHA or branch |

## Active Adapter Selection

Set `SCM_ADAPTER` env var or use the local `git` adapter by default.
