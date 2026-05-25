---
name: audit-ai-harness
description: Audit all AI harness files in the project for context bloat, context rot, register violations, contradictions, and missing baselines. Produces a prioritised fix list.
skills:
  - using-agent-skills
  - ai-harness-hygiene
  - workspace-analysis
agent: documentation-specialist
---

# /audit-ai-harness — Audit AI Harness Files

## Goal

Inspect all AI harness files in this project and produce a prioritised,
actionable findings list. Eliminate context bloat, context rot, register
violations, and contradictions before they waste tokens or mislead agents.

This prompt is self-contained. No toolkit files are required — the audit
runs entirely from the repo's own harness files and filesystem state.

## Instructions

1. If toolkit skills are available, load and follow
   `skills/using-agent-skills/SKILL.md` then `skills/ai-harness-hygiene/SKILL.md`.
   If not, use the workflow defined below — this prompt is fully self-sufficient.
2. Adopt the `documentation-specialist` agent persona.
3. Do not modify any files during the audit. Report findings only.
   Apply fixes only if the user explicitly asks after seeing the report.

## Audit Workflow

### Step 1 — Inventory

Locate all harness files:
- `README.md` (project root)
- `AGENTS.md` (project root)
- `CLAUDE.md` (project root)
- `GEMINI.md` (project root)
- `.github/copilot-instructions.md`
- Any other root-level `*.md` files that appear to be agent instruction files

Read every file found. Record which expected files are absent.

### Step 2 — Baseline check

Does `AGENTS.md` exist?

- **No, but tool-specific files do** → flag **[CRITICAL] MISSING-BASELINE**.
  All tool files are carrying duplicated full context. Creating `AGENTS.md`
  is the highest-priority fix.
- **No files at all** → flag **[HIGH] NO-HARNESS**. The repo has no AI
  orientation. Recommend running `/generate-agents-md` first.
- **Yes** → proceed.

### Step 3 — Bloat (duplication across files)

Compare every harness file pair. For each pair, identify sections where the
content is substantially the same (same commands, same layout, same
conventions, same stack description):

- >70% overlap in a section → **[HIGH] BLOAT** — content belongs in
  `AGENTS.md`; tool-specific file should reference or extend, not repeat.
- Identical sentences or paragraphs copied verbatim → **[HIGH] BLOAT**.
- Tool-specific file is longer than `AGENTS.md` → **[HIGH] BLOAT** — the
  tool file has become the de-facto baseline.

### Step 4 — Rot (staleness)

For each factual claim across all harness files, verify against the current
repo state:

**Commands** — check that every listed command or script target exists:
- `package.json` `scripts` keys, `Makefile` targets, `justfile` tasks.
- Flag any command that cannot be verified as **[CRITICAL] ROT-COMMAND**.

**File and directory paths** — check that every path mentioned exists:
- Flag missing paths as **[CRITICAL] ROT-PATH**.

**Directory structure** — compare any layout or tree in harness files
against the actual top-level directory listing:
- Dirs listed but absent → **[HIGH] ROT-STRUCTURE**.
- Top-level dirs present but entirely unmentioned in any harness file →
  **[MEDIUM] ROT-STRUCTURE** (omission, not a wrong claim).

**Stack and dependencies** — compare listed languages, frameworks, and tools
against current manifest files:
- Flag mismatches as **[HIGH] ROT-STACK**.

### Step 5 — Register violations

Audit each file against its expected register:

- `README.md` contains imperative agent directives ("Do not modify",
  "Always run X before pushing", "Never commit to main") →
  **[MEDIUM] REGISTER-README**: these belong in `AGENTS.md`.
- `AGENTS.md` uses narrative prose instead of imperatives, or explains
  context at length instead of directing action →
  **[MEDIUM] REGISTER-AGENTS**: rewrite as directives.
- Tool-specific file contains universal instructions (no tool-specific
  constructs, applies equally to all agents) →
  **[MEDIUM] REGISTER-TOOL**: move to `AGENTS.md`.

### Step 6 — Contradictions

Compare instructions across all files for conflicts:
- Different commands for the same task (e.g., `npm test` vs `make test`).
- Conflicting naming conventions, branch strategies, or style rules.
- One file permitting what another prohibits.

Flag each conflict as **[CRITICAL] CONFLICT** with both file:line references
and the conflicting text quoted from each.

### Step 7 — Completeness of AGENTS.md

If `AGENTS.md` exists, verify it has the following sections:
- Repository layout
- Stack
- Build & test commands
- Key conventions
- What not to touch

Flag each missing section as **[MEDIUM] INCOMPLETE**.

## Output Format

Report findings in this format, sorted by severity (CRITICAL first):

```
[SEVERITY] TYPE  file:line-range
  Found:   <exact quote or description of the violation>
  Fix:     <specific, actionable instruction>
```

Example:

```
[CRITICAL] ROT-COMMAND  AGENTS.md:34
  Found:   "Run `make dev` to start the development server"
  Fix:     `make dev` target does not exist in Makefile. Replace with
           `npm run dev` (verified in package.json scripts).

[HIGH] BLOAT  CLAUDE.md:12–45 duplicates AGENTS.md:8–41
  Found:   Repository layout section is copied verbatim.
  Fix:     Remove from CLAUDE.md. Add one line: "See AGENTS.md for
           repository layout."

[MEDIUM] REGISTER-README  README.md:89–91
  Found:   "Never commit directly to main. Always open a PR."
  Fix:     Move to AGENTS.md ## Key Conventions section.
```

After all findings, output:

```
---
Status:   PASS | NEEDS-WORK
Files audited:   <list>
Files absent:    <list>
Total findings:  <n> (critical: n, high: n, medium: n, low: n)
Top issue:       <one sentence describing the most impactful finding>
```

## Quality Gates

- Every finding cites file and line range.
- Rot findings quote the harness claim and state the actual repo state.
- Bloat findings quote the duplicated passage from both files.
- No fixes are applied without explicit user instruction.
- If the repo is clean, say so explicitly — don't manufacture findings.

## Output

The findings report printed to the conversation. No files are written.
If the user asks to apply fixes after reviewing the report, make changes
file by file, confirming each before proceeding.
