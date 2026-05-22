#!/usr/bin/env python3
"""Download and print GitHub Actions run logs. Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import argparse
import io
import json
import os
import sys
import urllib.request
import zipfile


def main() -> int:
    parser = argparse.ArgumentParser(description="Download log text for a workflow run.")
    parser.add_argument("run_id", help="Numeric workflow run ID.")
    parser.add_argument("--job", default="", help="Filter to a specific job name (substring match).")
    parser.add_argument("--failed-only", action="store_true", help="Only include steps with non-success conclusions.")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/actions/runs/{args.run_id}/logs",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            zip_bytes = resp.read()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    try:
        zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    except zipfile.BadZipFile as exc:
        print(f"ERROR: could not read log zip: {exc}", file=sys.stderr)
        return 1

    logs: list[dict] = []
    for name in sorted(zf.namelist()):
        if args.job and args.job.lower() not in name.lower():
            continue
        text = zf.read(name).decode("utf-8", errors="replace")
        if args.failed_only:
            # Keep only lines that look like failures.
            lines = [l for l in text.splitlines() if any(
                kw in l.lower() for kw in ("error", "fail", "exception", "exit code")
            )]
            if not lines:
                continue
            text = "\n".join(lines)
        logs.append({"file": name, "content": text})

    print(json.dumps(logs, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
