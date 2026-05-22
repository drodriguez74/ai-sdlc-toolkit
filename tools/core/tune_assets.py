#!/usr/bin/env python3
"""Assemble the Phase 2 tune-prompt.md for an AI CLI to consume.

This script never calls an AI API. It produces a prompt file that the running
AI harness (Claude Code, Copilot, Gemini CLI, etc.) reads to generate
project-specific overrides.
"""
from __future__ import annotations
import argparse
import pathlib
import sys


PROMPT_TEMPLATE = """# Project Tuning Prompt

You are running inside an AI CLI session. The user has linked this project to
the AI SDLC Toolkit at:

    {toolkit_home}

Your job is to render project-specific OVERRIDE files for agents, skills,
prompts, and instructions where doing so adds concrete value. Do NOT duplicate
every global asset; only override where project facts genuinely help.

## Inputs

Read these files first:

1. `{target}/.ai-sdlc/project-profile.yaml`
2. `{target}/.ai-sdlc/project-context.md`

Then survey the toolkit:

- Global agents: `{toolkit_home}/agents/*.md`
- Global skills: `{toolkit_home}/skills/*/SKILL.md`
- Global prompts: `{toolkit_home}/prompts/*.prompt.md`

## Output Locations

Write overrides as COMPLETE rendered files (not patches) into:

- `{target}/.github/agents-overrides/<name>.md`
- `{target}/.github/skills-overrides/<name>/SKILL.md`
- `{target}/.github/prompts-overrides/<name>.prompt.md`
- `{target}/.github/instructions-overrides/<name>.instructions.md`

Each override MUST include this frontmatter at the top:

```yaml
---
name: <same-as-base>
description: <project-tuned one-liner>
base_asset: <relative path to global default>
tuned_for_project: true
tuned_at: <ISO-8601 UTC>
project_profile: .ai-sdlc/project-profile.yaml
---
```

Each override SHOULD include a `## Tuning Notes` section explaining what
project-specific facts were applied and why.

## Rules

1. Project-specific rules come BEFORE generic defaults in each override.
2. Preserve universal safety, verification, and quality-gate requirements from
   the base asset. Never remove a safety rule.
3. Tune only assets where project facts add value. For example, override the
   `backend-developer` agent if the project uses a specific framework that
   needs framework-specific guidance; skip if a generic backend-developer is
   already accurate.
4. Write a tuning report to `{target}/.ai-sdlc/tuning-report.md` summarizing
   what was overridden and why.

## After Generation

The user will run:

    {toolkit_home}/refresh-project-links.sh {target}

to activate the overrides. You do NOT need to run that yourself.

## Begin

Start by reading the profile and context files, then survey the global toolkit
to identify candidates for override. Render overrides one at a time, justifying
each.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--toolkit-home", required=True)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()

    toolkit = pathlib.Path(args.toolkit_home).resolve()
    target = pathlib.Path(args.target).resolve()
    out = target / ".ai-sdlc" / "tune-prompt.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(PROMPT_TEMPLATE.format(toolkit_home=toolkit, target=target))
    print(f"  wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
