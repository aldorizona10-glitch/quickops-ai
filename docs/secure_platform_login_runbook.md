# Secure Platform Login Runbook

Last updated: 2026-06-12 WIB

Use this when a revenue lane needs a logged-in platform such as HackerOne, Bugcrowd, Intigriti, Google Bug Hunters, Microsoft MSRC, or a work marketplace.

## Rule

Never paste passwords, recovery codes, MFA codes, private cookies, or full browser session exports into chat, issue comments, PR comments, email, or repo files.

## Safe Pattern

1. The account owner logs in locally in the normal browser or CLI.
2. The session stays on the local machine only.
3. Only non-secret program facts are copied into repo notes:
   - in-scope assets
   - out-of-scope assets
   - reward table
   - safe harbor / testing rules
   - submission requirements
4. Active testing starts only after the official scope is recorded in the matching case folder.

## Browser Login

For browser-only platforms, open the site in Windows or WSL and log in manually:

```bash
xdg-open https://hackerone.com/users/sign_in
```

If `xdg-open` does not connect to the Windows browser, open the URL manually from Windows. Do not copy the password or cookie into any file.

After login, save only the scope notes into the correct local file, for example:

```bash
nano bug_bounty_cases/04-github-bug-bounty/scope_notes.md
nano bug_bounty_cases/05-shopify-bug-bounty/scope_notes.md
```

## CLI Login

For CLI tools, prefer device-flow or token login where the token remains in the tool's local config directory. Example already configured:

```bash
gh auth status
```

Required GitHub scopes for this workflow:

- `repo`
- `read:org`
- `workflow`

## Automation Boundary

Automation may:

- read public pages
- read non-secret local scope notes
- run passive checks on assets explicitly listed in scope
- draft reports
- submit comments or PR updates through authenticated CLI

Automation must not:

- request or store passwords
- bypass MFA
- export browser cookies
- run active security testing against assets without written authorization or official scope
- submit a report without a reproducible issue and impact

## Bug Bounty Start Checklist

Before testing any target:

- scope notes exist in `bug_bounty_cases/*/scope_notes.md`
- target asset is explicitly in scope
- method is allowed by rules
- rate limits and prohibited tests are known
- test account requirements are satisfied
- finding folder exists only for a concrete reproducible issue
