# AI SDLC Toolkit

A repo-agnostic, technology-agnostic AI-driven SDLC toolkit. Installs globally
under `~/.copilot/ai-sdlc-toolkit/` and exposes agents, skills, prompts, and
commands to any AI CLI (GitHub Copilot, Claude Code, Gemini CLI, Codex, Cursor,
or generic agents) through a project-linking workflow.

## What It Is

The toolkit is a collection of:

- **Agents** — Markdown persona files that define roles (product, engineering,
  QA, security, cloud, data, docs, orchestration).
- **Skills** — Markdown workflow guides that encode senior engineering practice
  (spec-driven dev, TDD, code review, shipping, debugging, etc.).
- **Prompts and commands** — slash-command entry points (`/spec`, `/plan`,
  `/build`, `/review`, `/ship`, `/debug`, etc.) wired to skills and agents.
- **Adapters** — provider-neutral integrations for issue trackers, SCM, CI/CD,
  knowledge bases, observability, cloud providers, and security alert surfaces.

The toolkit is opinionated about workflow and neutral about provider.

## Quick Start

```bash
# 1. Install the toolkit globally
./install.sh

# 2. Link a project repo to the toolkit
~/.copilot/ai-sdlc-toolkit/link-to-project.sh /path/to/repo

# 3. Tune agents and skills for the project (run from inside your AI CLI)
~/.copilot/ai-sdlc-toolkit/tune-project.sh /path/to/repo

# 4. Onboard — profile the repo and generate the knowledge base
/onboard

# 5. Use toolkit assets in your AI session
# Load .ai-sdlc/project-context.md, then invoke /spec, /plan, /build, /ship.
```

## Harness Compatibility

| Asset | GitHub Copilot | Claude Code | Gemini CLI | Codex |
|---|---|---|---|---|
| Agents | `#file` attachment only¹ | `.github/agents/` | `.github/agents/` | `.github/agents/` |
| Skills | `#file` attachment only¹ | `.github/skills/` | `.github/skills/` | `.github/skills/` |
| Prompts | `.github/prompts/` | `.claude/commands/` | `.gemini/commands/` | `.github/prompts/` |
| Instructions | `.github/instructions/` + `copilot-instructions.md` | `CLAUDE.md` | `GEMINI.md` | `CODEX.md` |

¹ GitHub Copilot `@` participants are VS Code extensions, not file-based definitions.
Agent and skill files are linked into `.github/agents/` and `.github/skills/` but must
be attached manually as context (e.g. `#file:.github/agents/tech-lead.md`).

## Directory Reference

```text
~/.copilot/ai-sdlc-toolkit/
  README.md                    # this file
  VERSION                      # semver
  manifest.json                # resolved at install time from manifest.json.tpl
  install.sh                   # global install
  upgrade.sh                   # in-place upgrade with backup
  doctor.sh                    # validate structure and detect secrets
  link-to-project.sh           # wire a repo to the toolkit
  refresh-project-links.sh     # rebuild link farms
  tune-project.sh              # two-phase project tuning
  AGENTS.md, CLAUDE.md, ...    # harness awareness files
  agents/                      # 28 persona files
  skills/                      # 36+ workflow guides
  prompts/                     # provider-neutral slash prompts
  commands/                    # harness-specific command bindings
  tools/                       # core helpers + adapter packs
  references/                  # patterns, checklists, anatomy docs
  schemas/                     # JSON schemas for validation
  harness/                     # per-harness awareness templates
```

## Manifest Reference

`manifest.json.tpl` is the source template. `install.sh` replaces
`__TOOLKIT_HOME__` with the resolved absolute path and writes `manifest.json`.

```jsonc
{
  "name": "ai-sdlc-toolkit",
  "version": "1.0.0",                    // semver; updated by upgrade.sh
  "install_root": "__TOOLKIT_HOME__",    // resolved at install time
  "agents_dir": "agents",
  "skills_dir": "skills",
  "prompts_dir": "prompts",
  "commands_dir": "commands",
  "tools_dir": "tools",
  "references_dir": "references",
  "schemas_dir": "schemas",
  "linking": {
    "default_mode": "symlink",           // "symlink" | "copy"
    "copy_fallback": true,
    "project_paths":    { ... },         // active discovery paths in a linked repo
    "override_paths":   { ... }          // project-local override folders
  }
}
```

## Override and Precedence Model

When `refresh-project-links.sh` runs, it walks each global asset and checks
whether a same-named file exists in the project's override folder. If yes, the
active discovery path links to the override; otherwise to the global default.
Users never edit global defaults; project-specific changes always go in
`*-overrides/` folders.

## Upgrade Notes

`upgrade.sh` backs up the current toolkit to
`~/.copilot/ai-sdlc-toolkit.bak.<timestamp>` before applying changes. User
override folders and `.ai-sdlc` project data are never modified by upgrade. Run
`doctor.sh` afterward.

## Contributing

- New agents → follow the standard in `references/agent-anatomy.md`.
- New skills → follow the standard in `references/skill-anatomy.md`.
- New adapters → follow the contract in `references/adapter-contract.md`.
