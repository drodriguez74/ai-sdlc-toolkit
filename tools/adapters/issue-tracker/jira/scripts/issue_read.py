#!/usr/bin/env python3
"""Read a Jira issue by key."""
from __future__ import annotations
import argparse
import base64
import json
import os
import sys
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("key", help="Jira issue key (e.g., PROJ-123)")
    args = parser.parse_args()

    base_url = os.environ.get("JIRA_BASE_URL")
    email = os.environ.get("JIRA_EMAIL")
    token = os.environ.get("JIRA_API_TOKEN")
    if not (base_url and email and token):
        print("ERROR: set JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN", file=sys.stderr)
        return 2

    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/rest/api/3/issue/{args.key}",
        headers={"Authorization": f"Basic {auth}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({
        "id": data.get("key"),
        "title": data.get("fields", {}).get("summary"),
        "status": data.get("fields", {}).get("status", {}).get("name"),
        "assignee": (data.get("fields", {}).get("assignee") or {}).get("displayName"),
        "description": data.get("fields", {}).get("description"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
