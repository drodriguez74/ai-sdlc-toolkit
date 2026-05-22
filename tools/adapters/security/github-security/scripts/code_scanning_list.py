#!/usr/bin/env python3
"""List GitHub code scanning alerts (CodeQL, SARIF). Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="List code scanning alerts for a GitHub repo.")
    parser.add_argument("--state", default="open", choices=["open", "dismissed", "fixed"], help="Alert state.")
    parser.add_argument("--severity", default="", help="Filter: critical, high, medium, low, warning, note, error.")
    parser.add_argument("--tool", default="", help="Filter by tool name (e.g. CodeQL).")
    parser.add_argument("--ref", default="", help="Filter by branch ref (e.g. refs/heads/main).")
    parser.add_argument("--max", type=int, default=30)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    qs: dict[str, str] = {"state": args.state, "per_page": str(min(args.max, 100))}
    if args.severity:
        qs["severity"] = args.severity
    if args.tool:
        qs["tool_name"] = args.tool
    if args.ref:
        qs["ref"] = args.ref
    url = f"https://api.github.com/repos/{repo}/code-scanning/alerts?" + urllib.parse.urlencode(qs)

    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            print("ERROR: code scanning requires security_events scope or repo admin access", file=sys.stderr)
        elif exc.code == 404:
            print("ERROR: code scanning not enabled for this repo", file=sys.stderr)
        else:
            print(f"ERROR: HTTP {exc.code} {exc.reason}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    alerts = [
        {
            "number": a["number"],
            "state": a["state"],
            "rule_id": a["rule"]["id"],
            "rule_name": a["rule"]["name"],
            "severity": a["rule"].get("severity"),
            "security_severity": a["rule"].get("security_severity_level"),
            "tool": a["tool"]["name"],
            "location": {
                "path": a["most_recent_instance"]["location"]["path"],
                "start_line": a["most_recent_instance"]["location"].get("start_line"),
            },
            "message": a["most_recent_instance"]["message"]["text"],
            "url": a["html_url"],
        }
        for a in data
    ]
    print(json.dumps(alerts, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
