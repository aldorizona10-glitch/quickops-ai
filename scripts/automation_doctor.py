#!/usr/bin/env python3
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def count_glob(pattern: str) -> int:
    return len(list(ROOT.glob(pattern)))


def count_csv_rows(path: str) -> int:
    file = ROOT / path
    if not file.exists():
        return 0
    with file.open(newline="", encoding="utf-8") as f:
        return max(0, sum(1 for _ in csv.reader(f)) - 1)


def status_line(name: str, ok: bool, detail: str = "") -> None:
    mark = "OK" if ok else "MISSING"
    suffix = f" - {detail}" if detail else ""
    print(f"{mark:8} {name}{suffix}")


def main() -> int:
    print("QuickOps Full Automation Doctor")
    print("===============================")
    print()
    print("Account/API connections")
    print("-----------------------")
    status_line("Gmail OAuth token", exists("token.json"), "Gmail API send/read")
    status_line("Google OAuth client credentials", exists("credentials.json"), "local only, gitignored")
    print()

    print("Outreach and revenue ops")
    print("------------------------")
    status_line("email queue", count_glob("email_queue/*.eml") > 0, f"{count_glob('email_queue/*.eml')} queued")
    status_line("Gmail sent log", exists("logs/gmail_api_sent_log.csv"), f"{count_csv_rows('logs/gmail_api_sent_log.csv')} rows")
    status_line("reply log", exists("logs/replies.jsonl"))
    status_line("lead tracker", exists("lead_tracker.csv"), f"{count_csv_rows('lead_tracker.csv')} rows")
    status_line("daily tracker", exists("daily_action_tracker.csv"), f"{count_csv_rows('daily_action_tracker.csv')} rows")
    print()

    print("Bug bounty desk")
    print("---------------")
    status_line("targets CSV", exists("bug_bounty_targets_2026.csv"), f"{count_csv_rows('bug_bounty_targets_2026.csv')} rows")
    status_line("case folders", count_glob("bug_bounty_cases/*") > 0, f"{count_glob('bug_bounty_cases/*')} folders")
    status_line("findings folders", count_glob("bug_bounty_findings/*") > 0, f"{count_glob('bug_bounty_findings/*')} folders")
    print()

    print("Next actions")
    print("------------")
    print("1. Run status anytime:")
    print("   python3 scripts/automation_doctor.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
