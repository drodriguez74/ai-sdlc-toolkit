#!/usr/bin/env python3
"""Create a Jira issue.

Reads JSON payload from stdin:
  {"project": "PROJ", "summary": "...", "description": "...", "issuetype": "Task"}
"""
from __future__ import annotations
import base64
import json
import os
import sys
import urllib.request


def main() -> int:
    payload_in = json.load(sys.stdin)
    base_url = os.environ.get("JIRA_BASE_URL")
    email = os.environ.get("JIRA_EMAIL")
    token = os.environ.get("JIRA_API_TOKEN")
    if not (base_url and email and token):
        print("ERROR: set JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN", file=sys.stderr)
        return 2

    body = {
        "fields": {
            "project":   {"key": payload_in["project"]},
            "summary":   payload_in["summary"],
            "description": payload_in.get("description", ""),
            "issuetype": {"name": payload_in.get("issuetype", "Task")},
        }
    }
    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/rest/api/3/issue",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"id": data.get("key"), "self": data.get("self")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
