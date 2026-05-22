#!/usr/bin/env python3
"""Trigger a GitHub Actions workflow dispatch. Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="Trigger a workflow_dispatch event.")
    parser.add_argument("workflow", help="Workflow file name (e.g. ci.yml) or numeric ID.")
    parser.add_argument("--ref", default="main", help="Branch or tag to run on (default: main).")
    parser.add_argument("--inputs", default="{}", help="JSON object of workflow inputs.")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    try:
        inputs = json.loads(args.inputs)
    except json.JSONDecodeError as exc:
        print(f"ERROR: --inputs must be valid JSON: {exc}", file=sys.stderr)
        return 2

    payload = json.dumps({"ref": args.ref, "inputs": inputs}).encode()
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/actions/workflows/{args.workflow}/dispatches",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            # 204 No Content on success.
            print(json.dumps({"status": "triggered", "workflow": args.workflow, "ref": args.ref, "http": resp.status}))
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
