# Project Structure

Date: 2026-06-11

## Repo Scope

This repository is for QuickOps AI agency operations, outreach, security micro-audits, authorized bug bounty research, and revenue tracking.

YouTube automation lives in a separate local repo:

```text
/mnt/c/Users/user/quickops-youtube-lab
```

## Keep In This Repo

- `README.md`: operating overview and core commands.
- `landing/`: QuickOps public landing page.
- `security-audit/`: public security micro-audit page.
- `email_queue/`: reviewed outbound drafts.
- `lead_tracker.csv`: prospect and client pipeline.
- `daily_action_tracker.csv`: daily execution record.
- `bug_bounty_*`: bug bounty plans, targets, templates, and logs.
- `security_audit_reports/`: reusable security report examples.
- `docs/`: agency, security, revenue, and operating documentation.
- `scripts/agency_*`: agency command center and status workflows.
- `scripts/gmail_*`: Gmail OAuth, send, and reply workflows.
- `scripts/full_auto_revenue_scout.py`: opportunity scouting.
- `scripts/bug_bounty_research_run.py`: authorized security research workflow.

## Keep Out Of This Repo

- YouTube upload scripts.
- YouTube OAuth/token files.
- Shorts metadata and manifests.
- Rendered videos, audio work files, and subtitle work files.
- Channel strategy docs that are only about YouTube.

## Daily Commands

```bash
python3 scripts/automation_doctor.py
python3 scripts/agency_command_center.py
python3 scripts/agency_pipeline_status.py
python3 scripts/full_auto_revenue_scout.py
```

## Commit Discipline

- Commit agency/security code and docs together when they support one workflow.
- Keep generated logs separate when possible.
- Do not commit local credentials, OAuth tokens, `.env` files, rendered media, or private client evidence.
- Use the YouTube repo for content automation changes.
