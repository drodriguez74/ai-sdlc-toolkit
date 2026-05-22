#!/usr/bin/env python3
"""List GitHub Projects v2 for an org or user. Requires GITHUB_TOKEN and GITHUB_OWNER."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.request


GRAPHQL_URL = "https://api.github.com/graphql"

ORG_QUERY = """
query($owner: String!, $first: Int!) {
  organization(login: $owner) {
    projectsV2(first: $first) {
      nodes {
        id
        number
        title
        shortDescription
        public
        closed
        url
        updatedAt
      }
    }
  }
}
"""

USER_QUERY = """
query($owner: String!, $first: Int!) {
  user(login: $owner) {
    projectsV2(first: $first) {
      nodes {
        id
        number
        title
        shortDescription
        public
        closed
        url
        updatedAt
      }
    }
  }
}
"""


def run_query(query: str, variables: dict, token: str) -> dict:
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def main() -> int:
    parser = argparse.ArgumentParser(description="List GitHub Projects v2 for an org or user.")
    parser.add_argument("--type", default="org", choices=["org", "user"], help="Owner type (default: org).")
    parser.add_argument("--max", type=int, default=20)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    owner = os.environ.get("GITHUB_OWNER")
    if not (token and owner):
        print("ERROR: set GITHUB_TOKEN and GITHUB_OWNER (org login or username)", file=sys.stderr)
        return 2

    query = ORG_QUERY if args.type == "org" else USER_QUERY
    try:
        result = run_query(query, {"owner": owner, "first": min(args.max, 100)}, token)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if "errors" in result:
        print(json.dumps({"status": "error", "errors": result["errors"]}))
        return 1

    data = result["data"]
    root = data.get("organization") or data.get("user") or {}
    projects = root.get("projectsV2", {}).get("nodes", [])
    print(json.dumps(projects, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
