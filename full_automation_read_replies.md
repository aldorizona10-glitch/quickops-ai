# Full Automation: Read Replies

To let the agent monitor replies, OAuth must include both scopes:

```text
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.readonly
```

Re-authorize:

```bash
cd /mnt/c/Users/user/zero-to-100-agency
python3 -u scripts/gmail_oauth_local.py
```

Then run:

```bash
python3 scripts/gmail_check_replies.py
```

Or one-shot autopilot:

```bash
python3 scripts/autopilot_run_once.py
```

Reply logs are local only:

```text
logs/replies.jsonl
```

`logs/` is ignored by Git.

## What It Checks

Current monitored senders:

- jobs@goshopbrands.com
- steve@pango.ai
- careers@babou.ai

It does not read the entire mailbox indiscriminately. It searches recent messages from the outreach targets and logs only previews needed for follow-up.
