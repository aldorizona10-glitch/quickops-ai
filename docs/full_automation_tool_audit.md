# Full Automation Tool Audit

Date: 2026-06-10

This repo is the operating system for QuickOps agency work, security micro-audits, authorized bug bounty research, and revenue tracking. YouTube automation has been split out to `/mnt/c/Users/user/quickops-youtube-lab`.

## Current Automation Map

| Area | Current files | Status | Gap |
| --- | --- | --- | --- |
| Gmail outreach | `scripts/gmail_api_send_queue.py`, `scripts/gmail_check_replies.py`, `scripts/gmail_recent_messages.py` | Gmail OAuth/API path exists | Keep allowlist strict; avoid bulk spam |
| Agency sales ops | `lead_tracker.csv`, `daily_action_tracker.csv`, `email_queue/` | Working queue/tracker | Needs daily prospect refresh |
| Revenue scout | `scripts/full_auto_revenue_scout.py`, `full_auto_revenue_scout.csv`, `docs/full_auto_revenue_scout_report.md` | Working opportunity log | Needs manual qualification before outreach |
| Bug bounty desk | `bug_bounty_*`, `scripts/bug_bounty_research_run.py` | Safe scope snapshot workflow | Needs manual validation before any report |
| Website | `landing/`, `security-audit/` | GitHub Pages-ready | Needs periodic copy/design refresh |
| Status/checks | `scripts/autopilot_status.py`, `scripts/automation_doctor.py` | Local status coverage | Scheduler can run it periodically |

## Free Tools Already Used

- Gmail API: safer sending/checking than browser cookies.
- GitHub Pages: free hosting for landing pages.
- CSV/Markdown: simple local CRM, trackers, case notes, opportunity logs, and delivery docs.
- Local Python scripts: repeatable status checks, reply monitoring, and opportunity review.

## Operating Rules

1. Do not mass-send email outside the allowlist.
2. Do not promise guaranteed revenue.
3. For bug bounty, only test authorized scope and accounts you control.
4. Keep YouTube scripts, upload tokens, rendered files, and metadata out of this repo.
5. Commit agency/security work separately from generated logs when possible.

## Commands

Status:

```bash
python3 scripts/automation_doctor.py
```

Agency command center:

```bash
python3 scripts/agency_command_center.py
```

Revenue scout:

```bash
python3 scripts/full_auto_revenue_scout.py
```

Bug bounty research:

```bash
python3 scripts/bug_bounty_research_run.py
```
