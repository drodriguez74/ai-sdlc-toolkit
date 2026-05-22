#!/usr/bin/env python3
"""Create a GitHub release. JSON on stdin: {"tag_name": "v1.2.3", "name": "...", "body": "...", "draft": false, "prerelease": false, "target_commitish": "main"}"""
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
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    if "tag_name" not in payload:
        print("ERROR: payload must include tag_name", file=sys.stderr)
        return 2

    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/releases",
        data=json.dumps(payload).encode(),
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
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        print(json.dumps({"status": "error", "code": exc.code, "detail": body}))
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({
        "id": data["id"],
        "tag_name": data["tag_name"],
        "name": data.get("name"),
        "draft": data["draft"],
        "prerelease": data["prerelease"],
        "url": data["html_url"],
        "upload_url": data.get("upload_url"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
