#!/usr/bin/env python3
"""List GitHub Actions workflows. Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="List workflows defined in a GitHub repo.")
    parser.add_argument("--help-env", action="store_true", help="Show required env vars and exit.")
    args = parser.parse_args()

    if args.help_env:
        print("Required: GITHUB_TOKEN (PAT with actions:read), GITHUB_REPO (owner/repo)")
        return 0

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/actions/workflows",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    workflows = [
        {
            "id": w["id"],
            "name": w["name"],
            "path": w["path"],
            "state": w["state"],
            "url": w["html_url"],
        }
        for w in data.get("workflows", [])
    ]
    print(json.dumps(workflows, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
