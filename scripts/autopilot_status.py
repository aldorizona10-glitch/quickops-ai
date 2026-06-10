#!/usr/bin/env python3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def count_lines(path: Path) -> int:
    if not path.exists():
        return 0
    return max(0, len(path.read_text(encoding="utf-8").splitlines()) - 1)


def main() -> int:
    queue = sorted((ROOT / "email_queue").glob("*.eml"))
    print("QuickOps AI Autopilot Status")
    print("============================")
    print(f"Email queue files: {len(queue)}")
    for item in queue:
        print(f"- {item.name}")
    print(f"Gmail OAuth token: {'ready' if (ROOT / 'token.json').exists() else 'not connected'}")
    print(f"Lead tracker rows: {count_lines(ROOT / 'lead_tracker.csv')}")
    print(f"Daily action rows: {count_lines(ROOT / 'daily_action_tracker.csv')}")
    print(f"HN opportunity rows: {count_lines(ROOT / 'hn_hiring_opportunities_june_2026.csv')}")
    print(f"Bug bounty log rows: {count_lines(ROOT / 'bug_bounty_daily_log.csv')}")
    print()
    print("Automation options:")
    print("- SMTP sender: scripts/send_email_queue.py")
    print("- Gmail API sender: scripts/gmail_api_send_queue.py")
    print("- Safe bug bounty scope snapshots: scripts/bug_bounty_research_run.py")
    print()
    print("Recommended now: Gmail API sender, because SMTP to Gmail is unreachable from this environment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
