#!/usr/bin/env python3
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REPO_AUDIT = [
    {
        "name": "quickops-ai",
        "visibility": "Public",
        "language": "Python",
        "decision": "main agency asset; show to prospects",
    },
    {
        "name": "westore-cel",
        "visibility": "Private",
        "language": "TypeScript",
        "decision": "inspect privately before using as portfolio",
    },
    {
        "name": "claude-action-poc",
        "visibility": "Public",
        "language": "unknown",
        "decision": "test repo; do not pin or pitch",
    },
    {
        "name": "repo-a-test",
        "visibility": "Public",
        "language": "unknown",
        "decision": "test repo; do not pin or pitch",
    },
    {
        "name": "repo-b-test",
        "visibility": "Public",
        "language": "unknown",
        "decision": "test repo; do not pin or pitch",
    },
]


TEAM = [
    ("Repo/Trust Engineer", "Keep profile, GitHub Pages, and proof assets clean."),
    ("Prospect Researcher", "Find public prospects with clear automation pain."),
    ("Outreach Operator", "Send allowlisted, personalized emails."),
    ("Reply/CRM Operator", "Monitor replies and update next actions."),
    ("Closing Operator", "Turn interested replies into USD 100 fixed scopes."),
    ("Delivery Engineer", "Build and document the paid workflow."),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_replies(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    replies = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            replies.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return replies


def print_section(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


def main() -> int:
    sent_log = read_csv(ROOT / "logs" / "gmail_api_sent_log.csv")
    tracker = read_csv(ROOT / "daily_action_tracker.csv")
    leads = read_csv(ROOT / "lead_tracker.csv")
    opportunities = read_csv(ROOT / "public_opportunities.csv")
    replies = read_replies(ROOT / "logs" / "replies.jsonl")

    sent = [row for row in sent_log if row.get("mode") == "sent"]
    queued = sorted((ROOT / "email_queue").glob("*.eml"))
    status_counts = Counter(row.get("status", "Unknown") for row in tracker)
    lead_counts = Counter(row.get("status", "Unknown") for row in leads)

    print("QuickOps Agency Command Center")
    print("==============================")
    print("Mode: agency only; YouTube automation skipped.")
    print("Goal: convert public trust + outreach + reply handling into the first USD 100 deal.")

    print_section("Developer Team")
    for role, job in TEAM:
        print(f"- {role}: {job}")

    print_section("GitHub Asset Decision")
    for repo in REPO_AUDIT:
        print(
            f"- {repo['name']} ({repo['visibility']}, {repo['language']}): "
            f"{repo['decision']}"
        )

    print_section("Current Metrics")
    print(f"- Sent outreach: {len(sent)}")
    print(f"- Reply log entries: {len(replies)}")
    print(f"- Email queue files: {len(queued)}")
    print(f"- Lead tracker rows: {len(leads)}")
    print(f"- Public opportunities: {len(opportunities)}")
    print(f"- Tracker statuses: {dict(status_counts)}")
    print(f"- Lead statuses: {dict(lead_counts)}")

    print_section("Live Trust Links")
    print("- Profile: https://aldorizona10-glitch.github.io/quickops-ai/profile/")
    print("- Start pilot: https://aldorizona10-glitch.github.io/quickops-ai/start/")
    print("- Agency site: https://aldorizona10-glitch.github.io/quickops-ai/")
    print("- Security audit: https://aldorizona10-glitch.github.io/quickops-ai/security-audit/")
    print("- GitHub repo: https://github.com/aldorizona10-glitch/quickops-ai")

    print_section("Next Money Actions")
    print("1. Keep monitoring replies every 15 minutes.")
    print("2. When any reply says interested/yes, send the USD 100 fixed-scope close.")
    print("3. Do not build full client work before payment or explicit paid agreement.")
    print("4. Use HackerOne proof as trust summary; send original PDF only if requested.")
    print("5. Add fresh public prospects daily, but keep sending allowlisted and personalized.")

    print_section("Commands")
    print("python3 scripts/agency_run_once.py")
    print("python3 scripts/agency_status.py")
    print("python3 scripts/gmail_check_replies.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
