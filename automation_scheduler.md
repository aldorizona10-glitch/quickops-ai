# Automation Scheduler

The repo now has send + read automation.

## One-Shot Check

```bash
cd /mnt/c/Users/user/zero-to-100-agency
python3 scripts/autopilot_run_once.py
```

This checks:

- current queue status
- Gmail replies from outreach targets

## Run Every 30 Minutes In WSL

```bash
cd /mnt/c/Users/user/zero-to-100-agency
while true; do
  date
  python3 scripts/autopilot_run_once.py
  sleep 1800
done
```

Keep that terminal open.

## Send New Queued Emails

This sends allowlisted queue emails only:

```bash
cd /mnt/c/Users/user/zero-to-100-agency
CONFIRM_SEND_QUICKOPS=I_UNDERSTAND_SEND_REAL_EMAIL python3 scripts/gmail_api_send_queue.py
```

## Reply Logs

Local only:

```text
logs/replies.jsonl
```

If a reply appears, paste the relevant preview here and the agent can draft the next response, scope, proposal, or invoice message.

## Current Limitation

The agent can read replies from allowlisted targets. It does not read every Gmail message. That is intentional for privacy and account safety.
