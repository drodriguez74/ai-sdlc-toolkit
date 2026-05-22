#!/usr/bin/env python3
"""Update a GitHub issue. JSON on stdin: {"number": 42, "state": "closed", "title": "...", "body": "...", "labels": [...], "assignees": [...], "milestone": 1}"""
from __future__ import annotations
import json
import os
import sys
import urllib.request

ALLOWED_FIELDS = {"state", "title", "body", "labels", "assignees", "milestone", "state_reason"}


def main() -> int:
    payload = json.load(sys.stdin)
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    number = payload.pop("number", None)
    if not number:
        print("ERROR: payload must include 'number'", file=sys.stderr)
        return 2

    update = {k: v for k, v in payload.items() if k in ALLOWED_FIELDS}
    if not update:
        print("ERROR: no updatable fields provided. Allowed: " + ", ".join(sorted(ALLOWED_FIELDS)), file=sys.stderr)
        return 2

    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/issues/{number}",
        data=json.dumps(update).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method="PATCH",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        print(json.dumps({"status": "error", "code": exc.code, "detail": body}))
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({
        "id": str(data["number"]),
        "title": data["title"],
        "state": data["state"],
        "url": data["html_url"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
