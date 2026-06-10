#!/usr/bin/env python3
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SENT_LOG = ROOT / "logs" / "gmail_api_sent_log.csv"
TRACKER = ROOT / "daily_action_tracker.csv"
REPLIES = ROOT / "logs" / "replies.jsonl"


CORE_AGENCY_KEYWORDS = (
    "workflow",
    "operations",
    "support",
    "lead",
    "gtm",
    "moderation",
    "booking",
    "servicing",
)
SECURITY_KEYWORDS = ("security", "audit", "control plane", "soc 2", "readiness")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_replies() -> list[dict[str, str]]:
    if not REPLIES.exists():
        return []
    rows: list[dict[str, str]] = []
    for line in REPLIES.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def lane_for(row: dict[str, str]) -> str:
    text = " ".join(
        [
            row.get("file", ""),
            row.get("to", ""),
            row.get("subject", ""),
            row.get("channel", ""),
            row.get("target", ""),
            row.get("action", ""),
            row.get("notes", ""),
        ]
    ).lower()
    if any(word in text for word in SECURITY_KEYWORDS):
        return "AI Security / Compliance"
    if any(word in text for word in CORE_AGENCY_KEYWORDS):
        return "Core Agency Workflow"
    if "starbridge" in text or "hiring" in text or "contractor" in text:
        return "Contract / Hiring"
    return "Other Outreach"


def main() -> int:
    sent_log = read_csv(SENT_LOG)
    tracker = read_csv(TRACKER)
    replies = read_replies()

    sent = [row for row in sent_log if row.get("mode") == "sent"]
    dry = [row for row in sent_log if row.get("mode") == "dry-run"]
    tracker_sent = [row for row in tracker if row.get("status") == "Sent"]
    tracker_ready = [row for row in tracker if row.get("status") == "Ready"]

    lane_counts = Counter(lane_for(row) for row in sent)

    print("QuickOps Agency Pipeline")
    print("========================")
    print("Public links:")
    print("- Core agency services: https://aldorizona10-glitch.github.io/quickops-ai/landing/#services")
    print("- Main studio page:     https://aldorizona10-glitch.github.io/quickops-ai/")
    print("- Profile/proof page:   https://aldorizona10-glitch.github.io/quickops-ai/profile/")
    print("- Security offer:       https://aldorizona10-glitch.github.io/quickops-ai/security-audit/")
    print("- USD 100 start page:   https://aldorizona10-glitch.github.io/quickops-ai/start/index.html")
    print()
    print("Counts:")
    print(f"- Real Gmail sent:       {len(sent)}")
    print(f"- Dry-run validations:   {len(dry)}")
    print(f"- Logged replies:        {len(replies)}")
    print(f"- Tracker sent rows:     {len(tracker_sent)}")
    print(f"- Tracker ready rows:    {len(tracker_ready)}")
    print()
    print("Sent by lane:")
    for lane, count in lane_counts.most_common():
        print(f"- {lane}: {count}")
    print()
    print("Latest real sends:")
    for row in sent[-12:]:
        print(f"- {lane_for(row)} | {row.get('to')} | {row.get('subject')} | {row.get('gmail_id')}")
    print()
    print("Open next actions:")
    print("- Keep core agency centered on /landing/#services: Lead Workflow Setup, Follow-Up System, Operational Handoff.")
    print("- Use /start/ for the fixed USD 100 pilot when a prospect is interested.")
    print("- Stop treating sent count as revenue; it is only outbound attempts.")
    print("- Monitor replies every loop; send closing template only after interest.")
    print("- Add new prospects only if they match core agency workflow or AI security/compliance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
