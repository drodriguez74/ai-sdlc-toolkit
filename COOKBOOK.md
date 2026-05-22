# AI SDLC Toolkit — Cookbook

Common recipes for the full SDLC workflow. Each recipe names the commands,
agents, and skills involved, and shows the sequence to follow.

---

## 1. Set Up a New Project

Run once after cloning or creating a repo.

```bash
# Install the toolkit globally (skip if already installed)
~/.copilot/ai-sdlc-toolkit/install.sh

# Link the toolkit to your project
~/.copilot/ai-sdlc-toolkit/link-to-project.sh /path/to/repo

# Inside your AI CLI session — profile the repo and generate the knowledge base
/onboard

# Tune agents and skills to your project's specific stack and conventions
/tune-agents
```

**What you get:** `.ai-sdlc/project-profile.yaml`, `.ai-sdlc/project-context.md`,
`.ai-sdlc/knowledge/` (architecture, patterns, decisions, integrations, glossary),
and project-specific agent/skill overrides under `.github/*-overrides/`.

---

## 2. Build a New Feature End-to-End

The standard SDLC loop from idea to shipped code.

```
/spec      → clarify requirements and write acceptance criteria
/plan      → break the spec into implementable tasks
/build     → implement incrementally, task by task
/test      → write and run tests for the new behavior
/review    → code review + security check before merge
/ship      → pre-flight checklist and GO/NO-GO decision
```

**Agents involved:** `product-manager` or `tech-lead` (spec) → `tech-lead`
(plan) → relevant developer (build) → `test-engineer` (test) → `code-reviewer`
+ `security-auditor` (review) → `release-manager` (ship).

**Tip:** For multi-phase tasks, invoke `/spec` first and let the
`orchestrator` agent produce a `workflow-plan.md` that sequences the rest.

---

## 3. Review a Pull Request

```
/review
```

Attach the diff or PR URL as context. The `code-reviewer` agent runs
`code-review-and-quality` and `security-and-hardening` skills and returns
prioritized findings with file/line references.

**With GitHub adapter:**
```bash
export GITHUB_TOKEN=ghp_...
export GITHUB_REPO=owner/repo
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/scm/github/scripts/pr_read.py 42 \
  > .ai-sdlc/adapter-out/pr-42.json
# Attach pr-42.json in your AI session, then run /review
```

**Post a review back to GitHub:**
```bash
echo '{"number": 42, "event": "REQUEST_CHANGES", "body": "..."}' | \
  python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/scm/github/scripts/pr_review.py
```

---

## 4. Debug a Production Issue

```
/debug
```

Provide the error message, stack trace, or log snippet as context. The
`debugging-and-error-recovery` skill drives: reproduce → localize → reduce →
fix → guard. Attach log output or a `.ai-sdlc/adapter-out/` search result for
richer context.

**With local logs adapter:**
```bash
# Point the log-search skill at your log file directly, or use the local-logs adapter
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/observability/local-logs/adapter.json
```

---

## 5. Work with GitHub Issues

### Search open issues
```bash
export GITHUB_TOKEN=ghp_...
export GITHUB_REPO=owner/repo
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/issue-tracker/github-issues/scripts/issue_search.py \
  --state open --max 30 > .ai-sdlc/adapter-out/issues.json
# Then: /issue-search
```

### Groom the backlog
```
/issue-groom
```
Attach `issues.json` as context. The `product-owner` agent prioritizes,
flags duplicates, and suggests acceptance criteria updates.

### Create a new issue
```bash
echo '{"title": "...", "body": "...", "labels": ["bug"]}' | \
  python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/issue-tracker/github-issues/scripts/issue_create.py
```
Or use `/issue-create` and let the `business-analyst` agent draft the payload.

### Update an existing issue (close, relabel, reassign)
```bash
echo '{"number": 42, "state": "closed", "labels": ["done"]}' | \
  python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/issue-tracker/github-issues/scripts/issue_update.py
```
Updatable fields: `state`, `title`, `body`, `labels`, `assignees`, `milestone`, `state_reason`.

---

## 6. Check CI Health and Debug Failures

```
/ci-health
```

**List recent runs and find failures:**
```bash
export GITHUB_TOKEN=ghp_...
export GITHUB_REPO=owner/repo

python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/ci-cd/github-actions/scripts/run_list.py \
  --branch main --status completed --max 10 > .ai-sdlc/adapter-out/runs.json

python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/ci-cd/github-actions/scripts/run_read.py \
  <run_id> > .ai-sdlc/adapter-out/run-detail.json
```

**Get the actual log output from a failed run:**
```bash
# Full logs
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/ci-cd/github-actions/scripts/run_logs.py \
  <run_id> > .ai-sdlc/adapter-out/run-logs.json

# Errors and failures only
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/ci-cd/github-actions/scripts/run_logs.py \
  <run_id> --failed-only > .ai-sdlc/adapter-out/run-errors.json
```
Attach `run-errors.json` and run `/debug`. The `devops-engineer` agent identifies
root causes and suggests fixes.

**Trigger or re-run after a fix:**
```bash
# Trigger a fresh workflow run
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/ci-cd/github-actions/scripts/run_trigger.py \
  ci.yml --ref main

# Re-run only the failed jobs
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/ci-cd/github-actions/scripts/run_rerun.py \
  <run_id> --failed-only
```

**Verify adapter access:**
```bash
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/ci-cd/github-actions/scripts/health.py
```

---

## 7. Check CI from Non-Actions Tools (Checks API)

For repos using CircleCI, Buildkite, or other CI that posts GitHub check runs:

```bash
# By branch tip
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/scm/github/scripts/check_runs.py main \
  > .ai-sdlc/adapter-out/checks.json

# By commit SHA, failures only
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/scm/github/scripts/check_runs.py \
  abc123def456 --status completed > .ai-sdlc/adapter-out/checks.json
```

Attach `checks.json` and run `/ci-health`.

---

## 8. Run a Security Audit

```
/review
```
Attach code diff + security alert output. The `security-auditor` agent covers
both static analysis and live vulnerability data.

**Pull live security data first:**
```bash
export GITHUB_TOKEN=ghp_...  # needs security_events scope
export GITHUB_REPO=owner/repo

# Dependabot vulnerabilities (high and critical)
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/security/github-security/scripts/dependabot_list.py \
  --severity high > .ai-sdlc/adapter-out/dependabot.json

# Code scanning alerts (CodeQL)
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/security/github-security/scripts/code_scanning_list.py \
  --tool CodeQL > .ai-sdlc/adapter-out/code-scanning.json

# Secret scanning alerts
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/security/github-security/scripts/secret_scanning_list.py \
  > .ai-sdlc/adapter-out/secrets.json
```

Attach the output files and let the `security-auditor` agent triage and prioritize.

**Token scopes required:**
- `security_events` for Dependabot + code scanning
- Repo admin or GitHub Advanced Security for secret scanning

---

## 9. Ship a Release

```
/ship
```

The `release-manager` runs a GO/NO-GO checklist. When the decision is GO:

**Create a GitHub release:**
```bash
echo '{
  "tag_name": "v1.2.0",
  "name": "v1.2.0 — Feature release",
  "body": "## What'\''s changed\n- ...",
  "draft": false,
  "prerelease": false,
  "target_commitish": "main"
}' | python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/scm/github/scripts/release_create.py
```

**List existing releases:**
```bash
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/scm/github/scripts/release_list.py --max 5
```

---

## 10. Inspect Deployment Environments

Useful before `/ship` to confirm protection rules and required reviewers are in place.

```bash
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/scm/github/scripts/environment_list.py \
  > .ai-sdlc/adapter-out/environments.json
```

Attach the output when running `/ship`. The `release-manager` agent will surface
any missing protection rules as blockers.

---

## 11. Work with GitHub Projects v2

For teams using GitHub Projects boards for sprint planning.

**List all projects for your org:**
```bash
export GITHUB_TOKEN=ghp_...  # needs read:project scope
export GITHUB_OWNER=my-org

python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/issue-tracker/github-projects/scripts/project_list.py \
  > .ai-sdlc/adapter-out/projects.json
```

**List all items in a project board (by project number from URL):**
```bash
python3 ~/.copilot/ai-sdlc-toolkit/tools/adapters/issue-tracker/github-projects/scripts/project_items.py \
  3 --max 100 > .ai-sdlc/adapter-out/project-items.json
```

Attach `project-items.json` and run `/issue-groom`. The `product-owner` or
`scrum-master` agent can prioritize, flag stale items, and suggest sprint allocation.

---

## 12. Simplify or Refactor Code

```
/simplify
```

Attach the file or selection as context. The `code-simplification` skill
removes duplication, flattens nesting, eliminates dead code, and improves
naming — without changing behavior. Tests must pass before and after.

---

## 13. Onboard to an Existing Repo

```
/onboard
```

Runs `workspace-analysis` then `repo-knowledge-generation` in sequence.
Produces `.ai-sdlc/project-profile.yaml`, `.ai-sdlc/project-context.md`, and
five knowledge documents under `.ai-sdlc/knowledge/`. Load `project-context.md`
at the start of every subsequent session.

If you only need the quick inventory without the full knowledge base:
```
/analyze-workspace
```

If the profile already exists and you only want to regenerate the knowledge base:
```
/generate-knowledge
```

---

## 14. Tune Agents and Skills for Your Project

```
/tune-agents
```

Or run the script directly (Phase 1 is standalone; Phase 2 needs an AI session):

```bash
~/.copilot/ai-sdlc-toolkit/tune-project.sh /path/to/repo
# Then open .ai-sdlc/tune-prompt.md in your AI CLI session
```

Produces project-specific overrides in `.github/*-overrides/` that layer on
top of global defaults. Overrides are never modified during toolkit upgrades.

---

## 15. Ingest Requirements from a Document

```
/requirements-ingestion
```

Attach a BRD, PDF, DOCX, or CSV. The `requirements-analyst` agent runs the
`requirements-ingestion` skill to extract structured requirements, identify
gaps, and produce a traceability summary.

---

## 16. Write or Update an ADR

```
/spec   (if the decision context isn't written yet)
```

Then ask the `documentation-specialist` agent to document the decision using
the `documentation-and-adrs` skill. Output: an ADR with context, options
considered, decision, consequences, and status.

---

## 17. Use an Agent for Perspective

Agents are not auto-invoked — attach them as context when you want their
perspective on a task.

**Claude Code / Gemini / Codex:** agents are discoverable under `.github/agents/`.
Load one explicitly:
```
Read .github/agents/tech-lead.md, then review this architecture proposal.
```

**GitHub Copilot:** attach manually:
```
#file:.github/agents/security-auditor.md  Review this authentication change.
```

**Key agents by use case:**

| Use case | Agent |
|---|---|
| Architecture / design decisions | `tech-lead` |
| Feature scoping and prioritization | `product-manager` |
| Acceptance criteria and backlog | `product-owner` |
| Security review | `security-auditor` |
| Performance bottlenecks | `performance-reviewer` |
| Test coverage gaps | `qa-lead` |
| Release readiness | `release-manager` |
| Multi-phase workflow routing | `orchestrator` |
| UX flows and component specs | `ux-designer` |
| Cloud/IaC review | `cloud-engineer` |
| Sprint planning and board grooming | `scrum-master` |

---

## 18. Refresh Links After a Toolkit Upgrade

```bash
# Upgrade the toolkit
~/.copilot/ai-sdlc-toolkit/upgrade.sh

# Rebuild link farms in each linked project
~/.copilot/ai-sdlc-toolkit/refresh-project-links.sh /path/to/repo

# Validate
~/.copilot/ai-sdlc-toolkit/doctor.sh /path/to/repo
```

---

## Quick Reference: All Commands

| Command | Purpose | Primary agent |
|---|---|---|
| `/onboard` | Profile repo + generate knowledge base | `workspace-analyzer` |
| `/analyze-workspace` | Profile repo only | `workspace-analyzer` |
| `/generate-knowledge` | Generate knowledge base (profile must exist) | `workspace-analyzer` |
| `/tune-agents` | Generate project-specific overrides | `agent-tuner` |
| `/spec` | Write a specification | `product-manager` / `tech-lead` |
| `/plan` | Break spec into tasks | `tech-lead` |
| `/build` | Implement incrementally | relevant developer |
| `/test` | Write and run tests | `test-engineer` |
| `/review` | Code + security review | `code-reviewer` |
| `/ship` | Pre-flight GO/NO-GO + create release | `release-manager` |
| `/debug` | Root-cause a failure | relevant engineer |
| `/simplify` | Refactor without behavior change | `tech-lead` |
| `/issue-search` | Search issues | `product-owner` |
| `/issue-groom` | Prioritize and clarify backlog | `product-owner` |
| `/issue-create` | Draft and create a new issue | `business-analyst` |
| `/scm-review` | Review a PR/MR from SCM adapter output | `code-reviewer` |
| `/ci-health` | Diagnose CI pipeline status | `devops-engineer` |
| `/logs` | Search and interpret logs | relevant engineer |
| `/requirements-ingestion` | Parse requirements documents | `requirements-analyst` |

## GitHub Adapter Quick Reference

| Surface | Adapter | Key env vars |
|---|---|---|
| Issues | `github-issues` | `GITHUB_TOKEN`, `GITHUB_REPO` |
| Pull requests + releases + environments + checks | `github` (scm) | `GITHUB_TOKEN`, `GITHUB_REPO` |
| Actions workflows + runs + logs + trigger | `github-actions` | `GITHUB_TOKEN`, `GITHUB_REPO` |
| Dependabot + code scanning + secret scanning | `github-security` | `GITHUB_TOKEN` (security_events scope), `GITHUB_REPO` |
| Projects v2 boards | `github-projects` | `GITHUB_TOKEN` (read:project scope), `GITHUB_OWNER` |
