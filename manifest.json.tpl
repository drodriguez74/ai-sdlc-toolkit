{
  "name": "ai-sdlc-toolkit",
  "version": "1.0.0",
  "description": "Repo-agnostic and tech-agnostic AI-driven SDLC toolkit",
  "install_root": "__TOOLKIT_HOME__",
  "agents_dir": "agents",
  "skills_dir": "skills",
  "prompts_dir": "prompts",
  "commands_dir": "commands",
  "tools_dir": "tools",
  "references_dir": "references",
  "schemas_dir": "schemas",
  "linking": {
    "default_mode": "symlink",
    "copy_fallback": true,
    "project_paths": {
      "agents": ".github/agents",
      "agents_compat": ".github/AGENTS",
      "skills": ".github/skills",
      "prompts": ".github/prompts",
      "instructions": ".github/instructions"
    },
    "override_paths": {
      "agents": ".github/agents-overrides",
      "skills": ".github/skills-overrides",
      "prompts": ".github/prompts-overrides",
      "instructions": ".github/instructions-overrides"
    }
  }
}
