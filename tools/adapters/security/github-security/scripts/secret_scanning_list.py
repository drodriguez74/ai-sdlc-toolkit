#!/usr/bin/env python3
"""List GitHub secret scanning alerts. Requires GITHUB_TOKEN and GITHUB_REPO."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="List secret scanning alerts for a GitHub repo.")
    parser.add_argument("--state", default="open", choices=["open", "resolved"], help="Alert state.")
    parser.add_argument("--secret-type", default="", help="Filter by secret type slug.")
    parser.add_argument("--max", type=int, default=30)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if not (token and repo):
        print("ERROR: set GITHUB_TOKEN and GITHUB_REPO (owner/repo)", file=sys.stderr)
        return 2

    qs: dict[str, str] = {"state": args.state, "per_page": str(min(args.max, 100))}
    if args.secret_type:
        qs["secret_type"] = args.secret_type
    url = f"https://api.github.com/repos/{repo}/secret-scanning/alerts?" + urllib.parse.urlencode(qs)

    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            print("ERROR: secret scanning requires repo admin access or secret_scanning_alerts scope", file=sys.stderr)
        elif exc.code == 404:
            print("ERROR: secret scanning not enabled for this repo or GitHub Advanced Security not active", file=sys.stderr)
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
            "secret_type": a["secret_type"],
            "secret_type_display_name": a.get("secret_type_display_name"),
            "resolution": a.get("resolution"),
            "created_at": a["created_at"],
            "url": a["html_url"],
        }
        for a in data
    ]
    print(json.dumps(alerts, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
