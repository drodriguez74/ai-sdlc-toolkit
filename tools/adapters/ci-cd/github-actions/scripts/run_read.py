#!/usr/bin/env python3
"""Read a GitHub Actions workflow run and its jobs. Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.request


def fetch(url: str, token: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read a workflow run and its jobs by run ID.")
    parser.add_argument("run_id", help="Numeric workflow run ID.")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    try:
        run = fetch(f"https://api.github.com/repos/{repo}/actions/runs/{args.run_id}", token)
        jobs_data = fetch(f"https://api.github.com/repos/{repo}/actions/runs/{args.run_id}/jobs", token)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    jobs = [
        {
            "id": j["id"],
            "name": j["name"],
            "status": j["status"],
            "conclusion": j.get("conclusion"),
            "started_at": j.get("started_at"),
            "completed_at": j.get("completed_at"),
            "steps": [
                {
                    "name": s["name"],
                    "status": s["status"],
                    "conclusion": s.get("conclusion"),
                    "number": s["number"],
                }
                for s in j.get("steps", [])
            ],
        }
        for j in jobs_data.get("jobs", [])
    ]

    output = {
        "id": run["id"],
        "name": run["name"],
        "workflow_id": run["workflow_id"],
        "head_branch": run["head_branch"],
        "head_sha": run["head_sha"][:12],
        "status": run["status"],
        "conclusion": run.get("conclusion"),
        "created_at": run["created_at"],
        "updated_at": run["updated_at"],
        "url": run["html_url"],
        "jobs": jobs,
    }
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
