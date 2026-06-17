#!/usr/bin/env python3
"""Read-only GitHub HackerOne checks against owned assets only."""

from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


OWNER = "aldorizona10-glitch"
OUT_DIR = Path("bug_bounty_cases/04-github-bug-bounty/research")
OUT_PATH = OUT_DIR / "owned_asset_boundary_check.json"


def gh_json(args: list[str]) -> object:
    proc = subprocess.run(
        ["gh", *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return json.loads(proc.stdout)


def unauth_get(url: str) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "quickops-owned-asset-boundary-check",
        },
    )
    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read(4096).decode("utf-8", errors="replace")
            return {
                "url": url,
                "status": response.status,
                "elapsed_ms": round((time.time() - started) * 1000),
                "body_prefix": body[:240],
            }
    except urllib.error.HTTPError as error:
        body = error.read(4096).decode("utf-8", errors="replace")
        return {
            "url": url,
            "status": error.code,
            "elapsed_ms": round((time.time() - started) * 1000),
            "body_prefix": body[:240],
        }


def expected_status(repo: dict[str, object], endpoint: str) -> set[int]:
    private = bool(repo.get("private"))
    if private:
        return {404}
    if endpoint == "metadata":
        return {200}
    if endpoint in {"contents", "tree"}:
        return {200, 404}
    return {401, 403, 404}


def main() -> int:
    repos = gh_json(
        [
            "api",
            f"users/{OWNER}/repos?per_page=100&type=owner",
        ]
    )
    if not isinstance(repos, list):
        raise RuntimeError("GitHub API did not return a repo list")

    results = []
    alerts = []
    for repo in repos:
        if not isinstance(repo, dict) or repo.get("archived"):
            continue
        full_name = str(repo["full_name"])
        default_branch = str(repo.get("default_branch") or "main")
        checks = {
            "metadata": f"https://api.github.com/repos/{full_name}",
            "contents": f"https://api.github.com/repos/{full_name}/contents",
            "tree": f"https://api.github.com/repos/{full_name}/git/trees/{default_branch}?recursive=1",
            "actions_secrets": f"https://api.github.com/repos/{full_name}/actions/secrets",
            "actions_variables": f"https://api.github.com/repos/{full_name}/actions/variables",
        }
        repo_result = {
            "full_name": full_name,
            "private": bool(repo.get("private")),
            "visibility": repo.get("visibility"),
            "default_branch": default_branch,
            "checks": [],
        }
        for endpoint, url in checks.items():
            outcome = unauth_get(url)
            allowed = expected_status(repo, endpoint)
            status = int(outcome["status"])
            ok = status in allowed
            outcome["endpoint"] = endpoint
            outcome["expected_status_any_of"] = sorted(allowed)
            outcome["ok"] = ok
            repo_result["checks"].append(outcome)
            if not ok:
                alerts.append(
                    {
                        "repo": full_name,
                        "private": bool(repo.get("private")),
                        "endpoint": endpoint,
                        "status": status,
                        "expected": sorted(allowed),
                        "url": url,
                    }
                )
        results.append(repo_result)

    report = {
        "program": "GitHub HackerOne",
        "scope_file": "bug_bounty_cases/04-github-bug-bounty/scope_notes.md",
        "boundary": "owned repos only; unauthenticated read-only HTTP requests",
        "repo_count": len(results),
        "alert_count": len(alerts),
        "alerts": alerts,
        "results": results,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Checked {len(results)} owned repos")
    print(f"Alerts: {len(alerts)}")
    print(f"Wrote {OUT_PATH}")
    if alerts:
        print(json.dumps(alerts, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
