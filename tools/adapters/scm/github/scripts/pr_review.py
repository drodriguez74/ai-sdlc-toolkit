#!/usr/bin/env python3
"""Post a structured review comment on a GitHub PR.

Reads JSON on stdin: {"number": "123", "event": "COMMENT|APPROVE|REQUEST_CHANGES", "body": "..."}
"""
from __future__ import annotations
import json
import os
import sys
import urllib.request


def main() -> int:
    payload = json.load(sys.stdin)
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO", file=sys.stderr)
        return 2
    body = {"event": payload.get("event", "COMMENT"), "body": payload["body"]}
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/pulls/{payload['number']}/reviews",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"id": data.get("id"), "url": data.get("html_url")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
