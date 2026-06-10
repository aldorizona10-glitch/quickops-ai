# Security And Account Operations

Goal: operate QuickOps AI without exposing personal account credentials.

## Rules

- Do not share Gmail password, GitHub password, recovery codes, or crypto wallet private keys in chat.
- Do not paste GitHub personal access tokens into chat.
- Do not give anyone remote control of your email unless you understand the risk.
- Keep 2FA enabled on Gmail and GitHub.
- Use a separate business email when possible.
- Confirm project scope before payment.
- For USDT, always state: BEP20 / BNB Smart Chain only.

## What The Agent Can Safely Do

- Build the website.
- Push code to GitHub after your credential cache is active.
- Research public opportunities.
- Write outreach messages.
- Create `.eml` draft files.
- Create tracking sheets.
- Draft replies to prospects.
- Prepare proposals and delivery docs.

## What Must Stay Human-Controlled

- Logging in to Gmail.
- Sending emails from your account.
- Sending DMs from LinkedIn, X, HN, Reddit, or Upwork.
- Receiving and moving money.
- Approving app permissions.
- Sharing sensitive identity/payment information.

## Safer Sending Workflow

1. Open `email_queue/`.
2. Open an `.eml` file.
3. Review recipient, subject, and body.
4. Send from your email client.
5. Mark the row in `daily_action_tracker.csv` as `Sent`.
6. When a prospect replies, paste the reply into this workspace and the agent can draft the next response.

## GitHub Workflow

Credential cache is now working for push through the agent when escalation is allowed.

If push fails later, run:

```bash
git config --global credential.helper 'cache --timeout=86400'
cd /mnt/c/Users/user/zero-to-100-agency
git push
```

## Gmail Delegation Alternative

If you want more automation later, create a separate business account only for QuickOps AI. Do not use your main personal Gmail.

Recommended:

- Email: quickopsai or similar.
- Strong unique password.
- 2FA enabled.
- Recovery email set to your main account.
- No banking/crypto/private accounts connected.

Even then, approve sending manually until the first paid client is real.
