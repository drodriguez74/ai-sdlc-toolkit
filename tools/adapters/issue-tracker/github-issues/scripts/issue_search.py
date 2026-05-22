#!/usr/bin/env python3
"""Search GitHub issues. Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", default="open", choices=["open", "closed", "all"])
    parser.add_argument("--labels", default="")
    parser.add_argument("--max", type=int, default=20)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    qs = {"state": args.state, "per_page": str(args.max)}
    if args.labels:
        qs["labels"] = args.labels
    url = f"https://api.github.com/repos/{repo}/issues?" + urllib.parse.urlencode(qs)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    summary = [
        {"id": str(i["number"]), "title": i["title"], "state": i["state"], "url": i["html_url"]}
        for i in data if "pull_request" not in i
    ]
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
