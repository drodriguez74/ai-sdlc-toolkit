# Orchestration Patterns

Patterns for sequencing agents and skills across an SDLC workflow.

## Linear Pipeline

Used for: greenfield features.

`product-manager` → `tech-lead` → `ux-designer` (when UI) → developer(s) →
`test-engineer` → `code-reviewer` → `release-manager`.

Each phase produces a documented artifact the next phase consumes. The
`orchestrator` agent maintains the handoff log.

## Fan-Out for Review

Used for: `/ship` and high-risk merges.

`code-reviewer` ∥ `security-auditor` ∥ `test-engineer` ∥ `performance-reviewer`
(when relevant) ∥ `data-reviewer` (when data changed). Main agent merges into
a single GO/NO-GO output.

### Single-Agent Fallback

When subagents aren't supported, run the same agents sequentially in the order
listed above. The merged output format is identical.

## Quick Track

Used for: bug fixes, renames, single-file edits.

`debugging-and-error-recovery` skill (for bugs) or
`incremental-implementation` skill (for small changes). No `orchestrator`,
no fan-out review — just `code-reviewer` at the end.

## Brownfield Discovery

Used for: any unfamiliar repo.

`workspace-analyzer` first, always. Then `agent-tuner` to render project
overrides. Then proceed with the matching track above.

## Gates

The `orchestrator` evaluates these gates between phases:

| Gate | When | Pass Criteria |
|---|---|---|
| spec-ready | before `/plan` | Spec has all required sections; acceptance criteria are testable |
| plan-ready | before `/build` | Plan has ordered tasks with acceptance per task |
| build-ready | before `/review` | Tests pass; build green; behavior verified |
| review-clean | before `/ship` | No blockers; majors have plan |
| ship-ready | before merge to production | All `/ship` dimensions GO |

On gate failure, route to the remediation agent (e.g., `interview-me` for missing
spec, `tech-lead` for missing plan, the relevant developer for failing build).
