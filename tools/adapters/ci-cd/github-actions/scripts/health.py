#!/usr/bin/env python3
"""Verify GITHUB_TOKEN has actions:read access to GITHUB_REPO."""
from __future__ import annotations
import json
import os
import sys
import urllib.request


def main() -> int:
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
        count = data.get("total_count", 0)
        print(json.dumps({"status": "ok", "repo": repo, "workflow_count": count}))
        return 0
    except urllib.error.HTTPError as exc:
        print(json.dumps({"status": "error", "code": exc.code, "reason": exc.reason}))
        return 1
    except Exception as exc:
        print(json.dumps({"status": "error", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
