# Bug Bounty Execution Queue

Last updated: 2026-06-10 11:41 WIB.

## Ready For Researcher Login

These need platform login before active testing because the exact scope/known issues are not fully exposed in the public HTML snapshot:

- GitHub Bug Bounty on HackerOne: https://hackerone.com/github
- Shopify Bug Bounty on HackerOne: https://hackerone.com/shopify

Action after login:

1. Read in-scope assets and out-of-scope list.
2. Copy allowed assets into the matching `bug_bounty_cases/*/scope_notes.md`.
3. Create a finding folder only if there is a concrete issue:

```bash
python3 scripts/new_bug_case.py "GitHub Bug Bounty" "Possible access control issue in own test repo workflow"
```

## Public Policy Parsed

OpenAI Bugcrowd:

- Public page confirms status `in_progress`, product label `Bug Bounty`, and reward allocation `pay_for_success`.
- Safe harbor applies only when policy is followed.
- Model-only jailbreaks, hallucinations, normal sandbox execution, and prompt/response content issues are not a payable path unless there is direct verifiable security impact on an in-scope service.
- Current decision: do not submit model-only findings. Prioritize web/API/security boundary issues.

Google / Alphabet VRP:

- Public page confirms Google VRP rules page and potential reward amounts.
- Current decision: active tests require exact product-specific scope from Google Bug Hunters before any validation.

Microsoft MSRC:

- Public MSRC researcher portal is reachable.
- Current decision: select a specific MSRC bounty program before testing; use coordinated disclosure only.

## First Valid Work Blocks

Block A: GitHub own-account workflow research

- Use only `aldorizona10-glitch` owned repos.
- Look for GitHub platform-level access control issues, not mistakes in the user's own repo.
- Evidence must show a GitHub security boundary failure, not a misconfigured repository.

Block B: OpenAI own-account security boundary research

- Use only own account and own content.
- Exclude jailbreak/model behavior.
- Look only for web/API authorization, session, OAuth, file isolation, or data exposure issues that have direct security impact.

Block C: Agency security micro-audit conversion

- If a startup is not in a bug bounty program, do not test without permission.
- Send paid micro-audit offer instead of testing:
  "I can run a fixed-scope AI workflow security review for USD 100 after written authorization."
