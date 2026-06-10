# Safe Autonomous Sending

This repo includes a guarded sender:

```bash
python3 scripts/send_email_queue.py
```

Default mode is dry-run. It validates the `.eml` files in `email_queue/` and prints what would be sent.

## Why This Exists

The agent cannot use pasted Gmail cookies, passwords, or browser sessions. A safer path is:

- You authorize an SMTP/API sender locally.
- Credentials stay in environment variables, not chat and not git.
- The sender only sends allowlisted `.eml` files.
- Sending requires an explicit confirmation variable.

## Dry Run

```bash
cd /mnt/c/Users/user/zero-to-100-agency
python3 scripts/send_email_queue.py
```

## Live Send Requirements

Set these environment variables in your terminal, not in chat:

```bash
export SMTP_HOST="smtp.example.com"
export SMTP_PORT="587"
export SMTP_USER="your_sender@example.com"
export SMTP_PASSWORD="your_smtp_or_app_password"
export CONFIRM_SEND_QUICKOPS="I_UNDERSTAND_SEND_REAL_EMAIL"
python3 scripts/send_email_queue.py
```

For Gmail, use an official app password only if your account supports it and 2FA is enabled. Do not use normal account password and do not paste it into chat.

## Gmail SMTP Example

Use this shape, but put the real app password only in your own terminal:

```bash
cd /mnt/c/Users/user/zero-to-100-agency
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="aldorizona10@gmail.com"
export SMTP_PASSWORD="PASTE_GMAIL_APP_PASSWORD_HERE"
export CONFIRM_SEND_QUICKOPS="I_UNDERSTAND_SEND_REAL_EMAIL"
python3 scripts/send_email_queue.py
```

Google app password page:

https://myaccount.google.com/apppasswords

If that page is unavailable, first enable 2-Step Verification:

https://myaccount.google.com/signinoptions/two-step-verification

Do not use `smtp.example.com`; it is only a placeholder and will fail.

## Current Allowlist

- jobs@goshopbrands.com
- steve@pango.ai
- careers@babou.ai

`servicing-copilot.eml` is intentionally not sent because the recipient is not known yet.

## Logs

The script writes:

```text
logs/sent_email_log.csv
```

Do not commit logs if they contain sensitive delivery details.
