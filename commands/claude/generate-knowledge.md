---
description: Analyze the codebase and generate a structured knowledge base under .ai-sdlc/knowledge/.
---

Follow `prompts/generate-knowledge.prompt.md`.

Steps:
1. Load `skills/using-agent-skills/SKILL.md`.
2. Check `.ai-sdlc/project-profile.yaml` — run `skills/workspace-analysis/SKILL.md` if missing or stale.
3. Follow `skills/repo-knowledge-generation/SKILL.md`.
4. Adopt the `workspace-analyzer` agent.
