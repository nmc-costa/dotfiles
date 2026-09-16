#!/usr/bin/env python3
"""Community-index PoC (communityFirst.index in workspace-standards.yaml).

Reads topics.yaml, runs one GitHub code-search-repositories query per topic
(unauthenticated — 60 req/hour is enough at this scale, see workspace-
standards.yaml communityFirst.exceptions), and writes a snapshot JSON per
topic plus a human-readable SUMMARY.md.

Deliberately manual (cadence: manual in workspace-standards.yaml) — no
cron/systemd wiring here yet. Run by hand:

    python3 .agents/instructions/workspace-config/community-index/index_topics.py
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOPICS_FILE = HERE / "topics.yaml"
SNAPSHOTS_DIR = HERE / "snapshots"
SUMMARY_FILE = HERE / "SUMMARY.md"
TOP_N = 5
API_URL = "https://api.github.com/search/repositories"


def search_repos(query: str, top_n: int = TOP_N) -> list[dict]:
    params = urllib.parse.urlencode(
        {"q": query, "sort": "stars", "order": "desc", "per_page": top_n}
    )
    req = urllib.request.Request(
        f"{API_URL}?{params}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "dotfiles-community-index-poc",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub search failed ({exc.code}): {body}") from exc

    items = []
    for repo in data.get("items", [])[:top_n]:
        items.append(
            {
                "full_name": repo["full_name"],
                "html_url": repo["html_url"],
                "description": repo.get("description"),
                "stars": repo["stargazers_count"],
                "pushed_at": repo["pushed_at"],
                "language": repo.get("language"),
            }
        )
    return items


def main() -> int:
    if not TOPICS_FILE.exists():
        print(f"missing {TOPICS_FILE}", file=sys.stderr)
        return 1

    topics = yaml.safe_load(TOPICS_FILE.read_text())["topics"]
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    summary_lines = [
        "# Community index — snapshot summary",
        "",
        f"Generated {generated_at} by `index_topics.py` (manual run — see "
        "communityFirst.index.cadence in workspace-standards.yaml).",
        "",
    ]

    for topic in topics:
        slug = topic["slug"]
        query = topic["query"]
        print(f"searching: {slug} ({query!r})")
        repos = search_repos(query)

        snapshot = {
            "slug": slug,
            "query": query,
            "note": topic.get("note", "").strip(),
            "generated_at": generated_at,
            "top_repos": repos,
        }
        out_path = SNAPSHOTS_DIR / f"{slug}.json"
        out_path.write_text(json.dumps(snapshot, indent=2) + "\n")

        summary_lines.append(f"## {slug}")
        summary_lines.append("")
        if topic.get("note"):
            summary_lines.append(topic["note"].strip())
            summary_lines.append("")
        summary_lines.append(f"Query: `{query}`")
        summary_lines.append("")
        if repos:
            summary_lines.append("| Repo | Stars | Last push | Description |")
            summary_lines.append("|---|---|---|---|")
            for r in repos:
                desc = (r["description"] or "").replace("|", "\\|")
                summary_lines.append(
                    f"| [{r['full_name']}]({r['html_url']}) | {r['stars']} | "
                    f"{r['pushed_at'][:10]} | {desc} |"
                )
        else:
            summary_lines.append("_No results — genuine gap, not a query miss._")
        summary_lines.append("")

    SUMMARY_FILE.write_text("\n".join(summary_lines) + "\n")
    print(f"wrote {len(topics)} snapshot(s) and {SUMMARY_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
