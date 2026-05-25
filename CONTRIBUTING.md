# Contributing to AI SDLC Toolkit

Thanks for your interest in improving the toolkit. Contributions of all kinds are welcome — new agents, skills, prompts, adapters, bug fixes, and docs.

## Before You Start

- Check open issues to avoid duplicate work.
- For large additions (new skill, new adapter category), open an issue first to align on scope.

## Local Setup

```bash
git clone <your-fork>
cd toolkit
./install.sh          # installs to ~/.copilot/ai-sdlc-toolkit/
./doctor.sh           # verifies the install
```

## Structure

| Path | Purpose |
|------|---------|
| `agents/*.md` | Role personas (frontmatter: `name`, `description`) |
| `skills/*/SKILL.md` | Workflow guides (frontmatter: `name`, `description`) |
| `prompts/*.prompt.md` | Slash-command prompts (frontmatter: `name`, `description`) |
| `commands/` | Per-AI-CLI command definitions |
| `tools/core/` | Validation and rendering scripts |
| `schemas/` | JSON schemas for agents, skills, prompts, manifests |

## Adding an Agent or Skill

1. Copy the anatomy reference: `references/agent-anatomy.md` or `references/skill-anatomy.md`.
2. Create your file in the appropriate directory.
3. Include the required frontmatter (`name`, `description`).
4. Run the frontmatter validator locally:
   ```bash
   python tools/core/validate_frontmatter.py
   ```
5. Open a PR against `main`.

## Adding an Adapter

Adapters live under `tools/adapters/<category>/`. See `references/adapter-contract.md` for the expected interface contract.

## Commit Style

- Use the imperative mood: `Add backend-developer agent`, `Fix manifest schema`.
- Reference an issue when relevant: `Fix #42: handle missing frontmatter`.

## CI

GitHub Actions runs on every push and PR:
- **Shellcheck** on all `.sh` scripts.
- **Frontmatter validation** on agents, skills, and prompts.
- **Manifest validation** on `manifest.json.tpl`.

PRs must pass all checks before merge.

## Versioning

The toolkit follows [Semantic Versioning](https://semver.org). The current version lives in `VERSION`. Releases are tagged `vMAJOR.MINOR.PATCH` on `main`.
