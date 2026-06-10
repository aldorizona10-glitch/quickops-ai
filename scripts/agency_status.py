#!/usr/bin/env python3
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    sent_log = read_csv(ROOT / "logs" / "gmail_api_sent_log.csv")
    actions = read_csv(ROOT / "daily_action_tracker.csv")
    replies_path = ROOT / "logs" / "replies.jsonl"
    replies = []
    if replies_path.exists():
        for line in replies_path.read_text(encoding="utf-8").splitlines():
            try:
                replies.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    sent = [row for row in sent_log if row.get("mode") == "sent"]
    dry = [row for row in sent_log if row.get("mode") == "dry-run"]
    active = [row for row in actions if row.get("status") in {"Sent", "Ready"}]

    print("QuickOps AI Agency Status")
    print("=========================")
    print(f"Sent Gmail outreach: {len(sent)}")
    print(f"Dry-run records: {len(dry)}")
    print(f"Logged replies: {len(replies)}")
    print(f"Tracker rows active/ready: {len(active)}")
    print()
    print("Latest sent:")
    for row in sent[-8:]:
        print(f"- {row.get('to')} | {row.get('subject')} | {row.get('gmail_id')}")
    print()
    print("Latest replies:")
    for row in replies[-5:]:
        print(f"- {row.get('company')} | {row.get('subject')} | {row.get('from')}")
    print()
    print("Next agency actions:")
    print("- Core agency source of truth: https://aldorizona10-glitch.github.io/quickops-ai/landing/#services")
    print("- Main portfolio source of truth: https://aldorizona10-glitch.github.io/quickops-ai/")
    print("- Run `python3 scripts/agency_pipeline_status.py` for structured lane-by-lane status.")
    print("- If a prospect says yes/interested, send fixed USD 100 scope and payment instructions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
