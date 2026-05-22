#!/usr/bin/env python3
"""List items (cards) in a GitHub Projects v2 board. Requires GITHUB_TOKEN and GITHUB_OWNER."""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.request


GRAPHQL_URL = "https://api.github.com/graphql"

ITEMS_QUERY = """
query($owner: String!, $number: Int!, $first: Int!, $after: String) {
  organization(login: $owner) {
    projectV2(number: $number) {
      id
      title
      items(first: $first, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          type
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldTextValue        { text       field { ... on ProjectV2Field { name } } }
              ... on ProjectV2ItemFieldSingleSelectValue { name      field { ... on ProjectV2SingleSelectField { name } } }
              ... on ProjectV2ItemFieldDateValue         { date      field { ... on ProjectV2Field { name } } }
              ... on ProjectV2ItemFieldIterationValue    { title     field { ... on ProjectV2IterationField { name } } }
              ... on ProjectV2ItemFieldNumberValue       { number    field { ... on ProjectV2Field { name } } }
            }
          }
          content {
            ... on Issue      { number title state url assignees(first:3) { nodes { login } } }
            ... on PullRequest { number title state url }
            ... on DraftIssue { title body }
          }
        }
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


def flatten_fields(field_nodes: list) -> dict:
    fields: dict = {}
    for node in field_nodes:
        if not node:
            continue
        fname = (node.get("field") or {}).get("name", "unknown")
        value = node.get("text") or node.get("name") or node.get("date") or node.get("title") or node.get("number")
        if value is not None:
            fields[fname] = value
    return fields


def main() -> int:
    parser = argparse.ArgumentParser(description="List items in a GitHub Projects v2 board.")
    parser.add_argument("project_number", type=int, help="Project number (visible in the project URL).")
    parser.add_argument("--max", type=int, default=50, help="Max items to return.")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    owner = os.environ.get("GITHUB_OWNER")
    if not (token and owner):
        print("ERROR: set GITHUB_TOKEN and GITHUB_OWNER (org login)", file=sys.stderr)
        return 2

    items: list = []
    cursor = None
    remaining = args.max

    while remaining > 0:
        variables = {
            "owner": owner,
            "number": args.project_number,
            "first": min(remaining, 100),
            "after": cursor,
        }
        try:
            result = run_query(ITEMS_QUERY, variables, token)
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

        if "errors" in result:
            print(json.dumps({"status": "error", "errors": result["errors"]}))
            return 1

        project = result["data"]["organization"]["projectV2"]
        page = project["items"]

        for node in page["nodes"]:
            content = node.get("content") or {}
            fields = flatten_fields((node.get("fieldValues") or {}).get("nodes", []))
            items.append({
                "id": node["id"],
                "type": node["type"],
                "fields": fields,
                "content": {
                    "number": content.get("number"),
                    "title": content.get("title") or content.get("body", "")[:120],
                    "state": content.get("state"),
                    "url": content.get("url"),
                    "assignees": [a["login"] for a in (content.get("assignees") or {}).get("nodes", [])],
                },
            })
            remaining -= 1

        if not page["pageInfo"]["hasNextPage"] or remaining <= 0:
            break
        cursor = page["pageInfo"]["endCursor"]

    print(json.dumps({"project": project["title"], "items": items}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
