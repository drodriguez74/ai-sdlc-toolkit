#!/usr/bin/env python3
"""List GitHub releases. Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="List releases for a GitHub repo.")
    parser.add_argument("--max", type=int, default=10, help="Max releases to return (default 10).")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    qs = urllib.parse.urlencode({"per_page": str(min(args.max, 100))})
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/releases?{qs}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    releases = [
        {
            "id": r["id"],
            "tag_name": r["tag_name"],
            "name": r.get("name"),
            "draft": r["draft"],
            "prerelease": r["prerelease"],
            "created_at": r["created_at"],
            "published_at": r.get("published_at"),
            "url": r["html_url"],
            "assets": len(r.get("assets", [])),
        }
        for r in data
    ]
    print(json.dumps(releases, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
