#!/usr/bin/env python3
"""Read a GitLab MR by IID."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("iid")
    args = parser.parse_args()
    token = os.environ.get("GITLAB_TOKEN")
    project = os.environ.get("GITLAB_PROJECT")
    base = os.environ.get("GITLAB_BASE_URL", "https://gitlab.com")
    if not (token and project):
        print("ERROR: set GITLAB_TOKEN and GITLAB_PROJECT", file=sys.stderr)
        return 2
    proj_enc = urllib.parse.quote(project, safe="")
    req = urllib.request.Request(
        f"{base.rstrip('/')}/api/v4/projects/{proj_enc}/merge_requests/{args.iid}",
        headers={"PRIVATE-TOKEN": token, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "id": str(data["iid"]),
        "title": data["title"],
        "state": data["state"],
        "description": data.get("description"),
        "source_branch": data["source_branch"],
        "target_branch": data["target_branch"],
        "url": data["web_url"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
