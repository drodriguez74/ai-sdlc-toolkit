#!/usr/bin/env python3
"""Re-run a GitHub Actions workflow run (all jobs or failed jobs only). Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="Re-run a workflow run.")
    parser.add_argument("run_id", help="Numeric workflow run ID.")
    parser.add_argument("--failed-only", action="store_true", help="Re-run only failed jobs (default: re-run all).")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    if args.failed_only:
        url = f"https://api.github.com/repos/{repo}/actions/runs/{args.run_id}/rerun-failed-jobs"
    else:
        url = f"https://api.github.com/repos/{repo}/actions/runs/{args.run_id}/rerun"

    req = urllib.request.Request(
        url,
        data=b"{}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(json.dumps({
                "status": "rerun_requested",
                "run_id": args.run_id,
                "failed_only": args.failed_only,
                "http": resp.status,
            }))
            return 0
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        print(json.dumps({"status": "error", "code": exc.code, "reason": exc.reason, "detail": body}))
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
