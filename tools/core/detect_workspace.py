#!/usr/bin/env python3
"""Detect workspace characteristics and write project-profile.yaml + project-context.md.

Phase 1 of tune-project.sh. Fully scriptable; no AI required.
"""
from __future__ import annotations
import datetime
import pathlib
import sys

DETECTORS = {
    "package.json":         ("languages", "javascript"),
    "tsconfig.json":        ("languages", "typescript"),
    "pyproject.toml":       ("languages", "python"),
    "requirements.txt":     ("languages", "python"),
    "setup.py":             ("languages", "python"),
    "Cargo.toml":           ("languages", "rust"),
    "go.mod":               ("languages", "go"),
    "pom.xml":              ("languages", "java"),
    "build.gradle":         ("languages", "java"),
    "build.gradle.kts":     ("languages", "kotlin"),
    "Gemfile":              ("languages", "ruby"),
    "composer.json":        ("languages", "php"),
    ".csproj":              ("languages", "csharp"),
    "next.config.js":       ("frameworks", "next.js"),
    "next.config.mjs":      ("frameworks", "next.js"),
    "nuxt.config.ts":       ("frameworks", "nuxt"),
    "svelte.config.js":     ("frameworks", "svelte"),
    "angular.json":         ("frameworks", "angular"),
    "vue.config.js":        ("frameworks", "vue"),
    "manage.py":            ("frameworks", "django"),
    "Pipfile":              ("frameworks", "pipenv"),
    "Dockerfile":           ("infrastructure", "docker"),
    "docker-compose.yml":   ("infrastructure", "docker-compose"),
    "docker-compose.yaml":  ("infrastructure", "docker-compose"),
    ".github/workflows":    ("ci_cd", "github-actions"),
    ".gitlab-ci.yml":       ("ci_cd", "gitlab-ci"),
    "Jenkinsfile":          ("ci_cd", "jenkins"),
    "azure-pipelines.yml":  ("ci_cd", "azure-pipelines"),
    "main.tf":              ("infrastructure", "terraform"),
    "Chart.yaml":           ("infrastructure", "helm"),
    "kustomization.yaml":   ("infrastructure", "kustomize"),
    "serverless.yml":       ("infrastructure", "serverless"),
    "Pulumi.yaml":          ("infrastructure", "pulumi"),
    "cloudformation.yaml": ("infrastructure", "cloudformation"),
    "openapi.yaml":         ("api_contracts", "openapi"),
    "openapi.json":         ("api_contracts", "openapi"),
    "schema.graphql":       ("api_contracts", "graphql"),
    "schema.prisma":        ("data_stores", "prisma"),
    "knexfile.js":          ("data_stores", "knex"),
    "alembic.ini":          ("data_stores", "alembic"),
}

TEST_HINTS = {
    "jest.config.js":   "jest",
    "jest.config.ts":   "jest",
    "vitest.config.ts": "vitest",
    "vitest.config.js": "vitest",
    "playwright.config.ts": "playwright",
    "cypress.config.js": "cypress",
    "pytest.ini":       "pytest",
    "phpunit.xml":      "phpunit",
    "go.test":          "go-test",
}


def detect(root: pathlib.Path) -> dict:
    profile: dict = {
        "project_root": str(root),
        "detected_at": datetime.datetime.utcnow().isoformat() + "Z",
        "languages": [],
        "frameworks": [],
        "build_tools": [],
        "test_frameworks": [],
        "ci_cd": [],
        "infrastructure": [],
        "cloud": [],
        "api_contracts": [],
        "data_stores": [],
        "docs": [],
        "notes": "",
    }
    seen = {k: set() for k in profile if isinstance(profile[k], list)}

    skip_dirs = {".git", "node_modules", "__pycache__", "dist", "build", ".venv"}
    for path in root.rglob("*"):
        if not path.exists():
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        rel = path.relative_to(root)
        rel_str = str(rel)
        # Match any registered detector.
        for marker, (bucket, value) in DETECTORS.items():
            if marker.startswith(".") or "/" in marker:
                if rel_str == marker or rel_str.startswith(marker + "/") or rel_str.endswith(marker):
                    if value not in seen[bucket]:
                        seen[bucket].add(value)
                        profile[bucket].append(value)
            elif path.name == marker or rel_str.endswith(marker):
                if value not in seen[bucket]:
                    seen[bucket].add(value)
                    profile[bucket].append(value)
        if path.name in TEST_HINTS:
            tf = TEST_HINTS[path.name]
            if tf not in seen["test_frameworks"]:
                seen["test_frameworks"].add(tf)
                profile["test_frameworks"].append(tf)

    # Docs
    for doc in ["README.md", "README", "CHANGELOG.md", "ARCHITECTURE.md"]:
        if (root / doc).exists():
            profile["docs"].append(doc)
    if (root / "docs").is_dir():
        profile["docs"].append("docs/")
    if (root / "docs" / "adr").is_dir():
        profile["docs"].append("docs/adr/")

    # Cloud hints from CI/IaC.
    cloud_hints = {
        "aws": ["aws-", "amazon-"],
        "azure": ["azure-", "az-"],
        "gcp": ["gcp-", "google-", "gcloud"],
    }
    text_signals = ""
    for ci in (root / ".github" / "workflows").glob("*.yml") if (root / ".github" / "workflows").is_dir() else []:
        try:
            text_signals += ci.read_text().lower()
        except Exception:
            pass
    for provider, needles in cloud_hints.items():
        if any(n in text_signals for n in needles):
            profile["cloud"].append(provider)

    return profile


def write_profile_yaml(profile: dict, target: pathlib.Path) -> None:
    """Write the profile as YAML. Hand-rolled to avoid PyYAML dependency."""
    lines = []
    for key, value in profile.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value!r}" if isinstance(value, str) and ":" in value else f"{key}: {value}")
    target.write_text("\n".join(lines) + "\n")


def write_context_md(profile: dict, target: pathlib.Path) -> None:
    lines = [
        "# Project Context",
        "",
        f"Generated: {profile['detected_at']}",
        f"Root: {profile['project_root']}",
        "",
        "## Detected",
        "",
    ]
    for key in ["languages", "frameworks", "build_tools", "test_frameworks",
                "ci_cd", "infrastructure", "cloud", "api_contracts",
                "data_stores", "docs"]:
        values = profile.get(key) or []
        lines.append(f"- **{key.replace('_', ' ')}**: {', '.join(values) if values else '(none detected)'}")
    lines.extend([
        "",
        "## Gaps (Human-Only Context)",
        "",
        "The following cannot be detected automatically; please confirm or annotate:",
        "",
        "- Production runtime environments and ownership",
        "- On-call and incident escalation paths",
        "- Compliance constraints (PCI, HIPAA, SOC2, etc.) if any",
        "- Team conventions not encoded in linters or docs",
        "- Stakeholder map and decision authority",
        "",
    ])
    target.write_text("\n".join(lines))


def main(target_arg: str) -> int:
    target = pathlib.Path(target_arg).resolve()
    ai_dir = target / ".ai-sdlc"
    ai_dir.mkdir(parents=True, exist_ok=True)
    profile = detect(target)
    write_profile_yaml(profile, ai_dir / "project-profile.yaml")
    write_context_md(profile, ai_dir / "project-context.md")
    print(f"  wrote {ai_dir / 'project-profile.yaml'}")
    print(f"  wrote {ai_dir / 'project-context.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
