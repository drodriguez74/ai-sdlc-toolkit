#!/usr/bin/env python3
"""List Dependabot vulnerability alerts. Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="List Dependabot alerts for a GitHub repo.")
    parser.add_argument("--state", default="open", choices=["open", "dismissed", "fixed", "auto_dismissed"], help="Alert state filter.")
    parser.add_argument("--severity", default="", help="Filter by severity: low, medium, high, critical.")
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
    url = f"https://api.github.com/repos/{repo}/dependabot/alerts?" + urllib.parse.urlencode(qs)

    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            print("ERROR: Dependabot alerts require repo admin access or security_events scope", file=sys.stderr)
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
            "severity": a["security_vulnerability"]["severity"],
            "package": a["security_vulnerability"]["package"]["name"],
            "ecosystem": a["security_vulnerability"]["package"]["ecosystem"],
            "vulnerable_version": a["security_vulnerability"]["vulnerable_version_range"],
            "patched_version": a["security_vulnerability"].get("first_patched_version", {}).get("identifier"),
            "cve": a["security_advisory"].get("cve_id"),
            "summary": a["security_advisory"]["summary"],
            "url": a["html_url"],
        }
        for a in data
    ]
    print(json.dumps(alerts, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
