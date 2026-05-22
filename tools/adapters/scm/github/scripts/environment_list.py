#!/usr/bin/env python3
"""List GitHub deployment environments and their protection rules. Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import json
import os
import sys
import urllib.request


def fetch(url: str, token: str) -> dict | list:
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    try:
        data = fetch(f"https://api.github.com/repos/{repo}/environments", token)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    environments = []
    for env in data.get("environments", []):
        protection = []
        for rule in env.get("protection_rules", []):
            entry: dict = {"type": rule["type"]}
            if rule["type"] == "required_reviewers":
                entry["reviewers"] = [
                    {"type": r["type"], "login": r["reviewer"].get("login") or r["reviewer"].get("name")}
                    for r in rule.get("reviewers", [])
                ]
            if rule["type"] == "wait_timer":
                entry["wait_minutes"] = rule.get("wait_timer")
            protection.append(entry)

        environments.append({
            "id": env["id"],
            "name": env["name"],
            "url": env.get("html_url"),
            "created_at": env.get("created_at"),
            "updated_at": env.get("updated_at"),
            "protection_rules": protection,
        })

    print(json.dumps(environments, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
