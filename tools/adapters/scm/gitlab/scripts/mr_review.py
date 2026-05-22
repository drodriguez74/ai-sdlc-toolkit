#!/usr/bin/env python3
"""Post a comment on a GitLab MR. JSON on stdin: {"iid": "123", "body": "..."}"""
from __future__ import annotations
import json
import os
import sys
import urllib.parse
import urllib.request


def main() -> int:
    payload = json.load(sys.stdin)
    token = os.environ.get("GITLAB_TOKEN")
    project = os.environ.get("GITLAB_PROJECT")
    base = os.environ.get("GITLAB_BASE_URL", "https://gitlab.com")
    if not (token and project):
        print("ERROR: set GITLAB_TOKEN and GITLAB_PROJECT", file=sys.stderr)
        return 2
    proj_enc = urllib.parse.quote(project, safe="")
    body = {"body": payload["body"]}
    req = urllib.request.Request(
        f"{base.rstrip('/')}/api/v4/projects/{proj_enc}/merge_requests/{payload['iid']}/notes",
        data=json.dumps(body).encode(),
        headers={
            "PRIVATE-TOKEN": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"id": data.get("id")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
