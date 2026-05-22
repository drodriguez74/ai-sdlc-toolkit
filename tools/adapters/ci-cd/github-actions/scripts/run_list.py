#!/usr/bin/env python3
"""List recent GitHub Actions workflow runs. Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="List recent workflow runs for a GitHub repo.")
    parser.add_argument("--workflow", default="", help="Workflow file name or ID to filter by.")
    parser.add_argument("--branch", default="", help="Branch name to filter by.")
    parser.add_argument("--status", default="", help="Filter by status: queued, in_progress, completed, failure, success, cancelled.")
    parser.add_argument("--max", type=int, default=20, help="Max runs to return (default 20).")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    qs: dict[str, str] = {"per_page": str(min(args.max, 100))}
    if args.branch:
        qs["branch"] = args.branch
    if args.status:
        qs["status"] = args.status

    if args.workflow:
        base = f"https://api.github.com/repos/{repo}/actions/workflows/{args.workflow}/runs"
    else:
        base = f"https://api.github.com/repos/{repo}/actions/runs"

    url = base + ("?" + urllib.parse.urlencode(qs) if qs else "")
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
            "workflow_id": r["workflow_id"],
            "head_branch": r["head_branch"],
            "head_sha": r["head_sha"][:12],
            "status": r["status"],
            "conclusion": r.get("conclusion"),
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
            "url": r["html_url"],
        }
        for r in data.get("workflow_runs", [])
    ]
    print(json.dumps(runs, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
