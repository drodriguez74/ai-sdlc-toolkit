# Copilot Commands

GitHub Copilot discovers slash commands through prompt files in
`.github/prompts/*.prompt.md` in the linked project repo. The link farm
populated by `refresh-project-links.sh` exposes the toolkit prompts there.

## Available Commands

All slash commands map 1:1 to files in `prompts/`:

| Command | Prompt File |
|---|---|
| `/spec` | `prompts/spec.prompt.md` |
| `/plan` | `prompts/plan.prompt.md` |
| `/build` | `prompts/build.prompt.md` |
| `/test` | `prompts/test.prompt.md` |
| `/review` | `prompts/review.prompt.md` |
| `/ship` | `prompts/ship.prompt.md` |
| `/simplify` | `prompts/simplify.prompt.md` |
| `/debug` | `prompts/debug.prompt.md` |
| `/analyze-workspace` | `prompts/analyze-workspace.prompt.md` |
| `/tune-agents` | `prompts/tune-agents.prompt.md` |
| `/issue-search` | `prompts/issue-search.prompt.md` |
| `/issue-groom` | `prompts/issue-groom.prompt.md` |
| `/issue-create` | `prompts/issue-create.prompt.md` |
| `/scm-review` | `prompts/scm-review.prompt.md` |
| `/ci-health` | `prompts/ci-health.prompt.md` |
| `/logs` | `prompts/logs.prompt.md` |
| `/requirements-ingestion` | `prompts/requirements-ingestion.prompt.md` |

## Custom Project Overrides

To override a prompt for a specific project, drop a same-named file in
`.github/prompts-overrides/`. `refresh-project-links.sh` will link the override
into the active discovery path automatically.

## How Copilot Discovers These

When a project is linked via `link-to-project.sh`, prompt files are populated
at `.github/prompts/` and Copilot discovers them as slash commands automatically.

Agent and skill files are linked under `.github/agents/` and `.github/skills/`
but Copilot does not auto-load them. To use an agent persona or skill playbook,
attach the file manually as context: `#file:.github/agents/tech-lead.md`.
