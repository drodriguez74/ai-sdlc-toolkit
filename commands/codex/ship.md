# /ship

Follow `prompts/ship.prompt.md`.

1. Load `skills/using-agent-skills/SKILL.md`.
2. Follow `skills/shipping-and-launch/SKILL.md`.
3. Fan out to `code-reviewer`, `security-auditor`, `test-engineer`,
   `performance-reviewer` (if performance-sensitive),
   `data-reviewer` (if data changed).
   If subagents aren't supported, run sequentially.
4. Adopt the `release-manager` agent for the merged decision.
