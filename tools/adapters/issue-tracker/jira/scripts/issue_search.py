#!/usr/bin/env python3
"""Search Jira issues using JQL.

Requires JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN env vars.
Outputs JSON to stdout.
"""
from __future__ import annotations
import argparse
import base64
import json
import os
import sys
import urllib.parse
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Jira issues with JQL")
    parser.add_argument("--jql", required=False, default="resolution = Unresolved ORDER BY updated DESC",
                        help="JQL query string")
    parser.add_argument("--max", type=int, default=20)
    args = parser.parse_args()

    base_url = os.environ.get("JIRA_BASE_URL")
    email = os.environ.get("JIRA_EMAIL")
    token = os.environ.get("JIRA_API_TOKEN")
    if not (base_url and email and token):
        print("ERROR: set JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN", file=sys.stderr)
        return 2

    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    qs = urllib.parse.urlencode({"jql": args.jql, "maxResults": args.max})
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/rest/api/3/search?{qs}",
        headers={"Authorization": f"Basic {auth}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    summary = [
        {"id": i["key"], "title": i["fields"].get("summary", ""), "status": i["fields"].get("status", {}).get("name")}
        for i in data.get("issues", [])
    ]
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
