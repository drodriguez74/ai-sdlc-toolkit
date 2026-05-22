#!/usr/bin/env python3
"""Read a GitHub PR by number."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("number")
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO", file=sys.stderr)
        return 2
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/pulls/{args.number}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "id": str(data["number"]),
        "title": data["title"],
        "state": data["state"],
        "body": data.get("body"),
        "base": data["base"]["ref"],
        "head": data["head"]["ref"],
        "url": data["html_url"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
