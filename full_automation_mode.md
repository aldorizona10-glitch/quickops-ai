# Full Automation Mode

Full automation means:

- prospect queue exists
- messages exist
- allowlist exists
- sender runs without manual copy/paste
- logs are written
- follow-up tracker is updated

It does not mean using leaked Gmail cookies, account passwords, or browser sessions.

## Current Network Reality

SMTP to Gmail is blocked/unreachable from this environment:

```text
smtp.gmail.com:587 -> Network is unreachable
```

Gmail API over HTTPS is reachable:

```text
gmail.googleapis.com:443 -> ok
```

So the correct full automation path is Gmail API, not SMTP.

## Dry Run

```bash
cd /mnt/c/Users/user/zero-to-100-agency
python3 scripts/gmail_api_send_queue.py
```

## Live Send

You need a real OAuth access token with Gmail send scope. Put it only in your terminal:

```bash
cd /mnt/c/Users/user/zero-to-100-agency
export GMAIL_ACCESS_TOKEN="PASTE_REAL_GMAIL_OAUTH_ACCESS_TOKEN_HERE"
export CONFIRM_SEND_QUICKOPS="I_UNDERSTAND_SEND_REAL_EMAIL"
python3 scripts/gmail_api_send_queue.py
```

Required scope:

```text
https://www.googleapis.com/auth/gmail.send
```

The script only sends to allowlisted recipients:

- jobs@goshopbrands.com
- steve@pango.ai
- careers@babou.ai

The unknown Servicing Copilot recipient is skipped until a recipient is known.

## Why One-Time Authorization Is Still Required

No agent can safely send from your Gmail without an official authorization path. Once you authorize Gmail API and export a valid token, the script can send the queue automatically.

## After Sending

Check:

```text
logs/gmail_api_sent_log.csv
```

Then track replies in:

```text
daily_action_tracker.csv
```
