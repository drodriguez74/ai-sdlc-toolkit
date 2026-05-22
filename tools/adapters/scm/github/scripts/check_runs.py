#!/usr/bin/env python3
"""List GitHub check runs for a commit SHA or ref. Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="List check runs for a commit SHA or branch tip.")
    parser.add_argument("ref", help="Commit SHA or branch name.")
    parser.add_argument("--status", default="", help="Filter by status: queued, in_progress, completed.")
    parser.add_argument("--filter", default="latest", choices=["latest", "all"], help="latest (default) or all check runs.")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    qs: dict[str, str] = {"filter": args.filter, "per_page": "100"}
    if args.status:
        qs["status"] = args.status
    url = f"https://api.github.com/repos/{repo}/commits/{args.ref}/check-runs?" + urllib.parse.urlencode(qs)

    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    runs = [
        {
            "id": r["id"],
            "name": r["name"],
            "app": r["app"]["slug"],
            "status": r["status"],
            "conclusion": r.get("conclusion"),
            "started_at": r.get("started_at"),
            "completed_at": r.get("completed_at"),
            "url": r["html_url"],
            "details_url": r.get("details_url"),
        }
        for r in data.get("check_runs", [])
    ]
    print(json.dumps(runs, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
