# Non-Agency Revenue Log

Date: 2026-06-10

This file tracks revenue attempts that are not QuickOps agency outreach. These are still zero-cash-outlay paths, but payment is not guaranteed until a third party accepts the work and pays.

## Open-Source Bounty

### maifetch Elixir rewrite

- Bounty source: https://github.com/HutchyBen/maifetch/issues/1
- Latest maintainer direction: rewrite the project in Elixir for BEAM VM benefits.
- Latest stated amount before Elixir request: GBP 175; maintainer said the bounty is still in place.
- Fork branch: https://github.com/aldorizona10-glitch/maifetch/tree/elixir-rewrite-bounty-1
- Pull request: https://github.com/HutchyBen/maifetch/pull/12
- Claim comment: https://github.com/HutchyBen/maifetch/issues/1#issuecomment-4675809351
- Status: PR open and mergeable when checked.
- Local worktree: `/tmp/maifetch-elixir`
- Commit: `6f5d397 Rewrite maifetch in Elixir`
- Payment status: not paid; depends on maintainer acceptance/merge and payout follow-through.

Scope completed:

- Replaced Go project with Elixir/Mix escript project.
- Preserved CLI > env > config > default precedence.
- Supported `-a`, `-t`, `--access-token`, and `--token`.
- Supported `MAITEA_*` variables with `MAIFETCH_*` compatibility aliases.
- Added MaiTea API wrapper functions for profiles, plays, tracks, status, all plays, best scores, and all best scores.
- Added profile/recent-play terminal output, rank/difficulty mapping, full-width ASCII normalization, and focused ExUnit tests.

Validation:

```bash
git diff --check
```

Runtime validation note:

- `elixir` and `mix` are not installed in this WSL environment.
- `apt-get install elixir` was blocked by lack of root privileges.
- The PR body clearly disclosed this and listed reviewer validation commands: `mix deps.get`, `mix test`, `mix escript.build`.

Next actions:

1. Watch PR #12 for maintainer feedback.
2. If changes are requested, patch `/tmp/maifetch-elixir`, push `aldorizona10-glitch:elixir-rewrite-bounty-1`, and reply on the PR.
3. After merge/acceptance, ask maintainer for payout instructions.

### maifetch Rust rewrite

- Bounty source: https://github.com/HutchyBen/maifetch/issues/1
- Claimed task: rewrite the Go CLI in Rust while preserving command-line input/output behavior.
- Bounty amount stated by maintainer: GBP 50.
- Fork: https://github.com/aldorizona10-glitch/maifetch/tree/rewrite-in-rust
- Pull request: https://github.com/HutchyBen/maifetch/pull/10
- Status: PR open, mergeable when checked.
- Local clone: `/tmp/maifetch`
- Commit: `fef1c3c Rewrite maifetch in Rust`

Validation completed:

```bash
cargo build --release
./target/release/maifetch --help
./target/release/maifetch -a dummy --score-count 13 --logo-size 0
```

Notes:

- Rust was installed locally under `/tmp/maifetch-cargo` and `/tmp/maifetch-rustup`, not system-wide.
- The implementation supports both README-style `MAITEA_*` env vars and old Go-style `MAIFETCH_*` env vars.
- The implementation supports both `-a` and `-t` access-token short flags.
- Payment depends on maintainer acceptance and bounty payout follow-through.

Next actions:

1. Watch PR #10 for maintainer feedback.
2. If changes are requested, patch `/tmp/maifetch`, rebuild, and push to `aldorizona10-glitch:rewrite-in-rust`.
3. After merge/acceptance, ask maintainer where to provide payout details.

2026-06-11 update:

- PR #10 rechecked: open and mergeable.
- Follow-up comment added to clarify that `cargo build --release` passes and compatibility aliases are supported.
- No maintainer comments yet.

2026-06-11 second search update:

- PR #10 rechecked again: still open, mergeable, no new maintainer comments.
- Gmail reply check: 0 new replies logged.
- Zero capability search found paid discovery/search capabilities, but they were not called because the user requested zero cash outlay.
- Current closest non-agency payout remains maifetch GBP 50; not paid until maintainer accepts/merges and pays.

2026-06-11 agency-adjacent paid testing attempt:

- Target: Odeva Booking, Show HN founder request for testers.
- Source: https://news.ycombinator.com/item?id=48376362
- Official contact found in Odeva `llms-full.txt`: `hallo@odeva.nl`
- Offer sent: USD 100 operator/API/docs testing pass for booking lifecycle, payments/refunds, guest confirmations, tourist tax, group reservations, and founding-partner workflow handoff.
- Email queue file: `email_queue/odeva-booking-workflow-testing.eml`
- Gmail send status: sent, Gmail ID `19eb2f0202fc0d9e`.
- Payment status: not paid; depends on reply, acceptance, and paid agreement.

2026-06-11 full-automation scout + paid testing outreach:

- Built `scripts/full_auto_revenue_scout.py` to discover, score, dedupe, and draft zero-budget earning paths from public GitHub bounty issues, Hacker News product posts, and remote work feeds.
- Latest run wrote 76 opportunities to `full_auto_revenue_scout.csv` and `docs/full_auto_revenue_scout_report.md`.
- Contact discovery is limited to top-ranked public product leads to avoid slow broad scraping and mass spam.
- Four targeted USD 100 workflow/testing offers were sent from public contacts found by the scout:
  - Inspection Credit: `hello@inspectioncredit.com`, Gmail ID `19eb319c1a65f3dc`
  - OTA: `os@ota.run`, Gmail ID `19eb31d44f02be26`
  - Clor: `support@clor.com`, Gmail ID `19eb31d98eb2dd3a`
  - Integuru: `hello@integuru.ai`, Gmail ID `19eb31e3aa0a834f`
- Payment status: not paid; depends on reply, acceptance, delivery, and invoice/payout agreement.

2026-06-11 additional USD 100 security/workflow outreach:

- Target: Loxea / verifiable open-source SoC 2 readiness scanner.
- Source: https://news.ycombinator.com/item?id=48164906
- Offer sent: USD 100 external testing pass for first-run friction, evidence/readiness output clarity, compliance handoff edge cases, and early-user checklist.
- Email queue file: `email_queue/loxeai-soc2-readiness-testing.eml`
- Gmail send status: sent, Gmail ID `19eb354163dc2ab7`.
- Payment status: not paid; depends on reply, acceptance, delivery, and invoice/payout agreement.

### Quantum Visualizer data/product maintenance

- Bounty source: https://github.com/1btc-news/news-client/issues/33
- Active maintenance lane: data-correctness / narrow source-backed contributions.
- Pull request: https://github.com/Iskander-Agent/quantum-visualizer/pull/74
- Fork branch: https://github.com/aldorizona10-glitch/quantum-visualizer/tree/fix-root-readiness-index-normalization
- Status: PR open and mergeable when checked.
- Payout context: no explicit payout commitment for this PR; Issue #33 pays accepted features/data updates only after reviewer/admin approval.
- Work completed: root `index.html` now handles numeric `metadata.quantum_readiness_index` from v3.5 data, matching the compatibility behavior already present in `public/index.html`.

Validation completed:

```bash
npm run validate:data
npm run check:dashboard
npm run check:frontend
node -e root index.html inline script syntax check
```

Next actions:

1. Watch PR #74 for DRI/reviewer feedback.
2. Patch quickly if review changes are requested.
3. If accepted/merged, ask whether it qualifies for the Issue #33 accepted-feature/data-update payout lane.

## Bounty Triage Notes

Skipped for now:

- `ItzFireable/Portfolio#7`: bounty target changed from C++ to Python to Haskell, with public concern about payout reliability.
- `ItzFireable/Portfolio#7` rechecked 2026-06-11: still open, but owner changed bounty scope repeatedly; skip as payout-risk.
- `PG-AGI/toingg-jarvis#13`: Algora USD 5 bounty is real, but already has many attempts/claimed PRs/reward rows; poor ROI and likely duplicate.
- `PG-AGI/toingg-jarvis#11`: Algora USD 5 bounty is real, but existing PRs already cover the clarified Pipecat/Gemini tool-calling scope; poor ROI and likely duplicate.
- `SecureBananaLabs/bug-bounty#743`: Algora USD 700 parent bounty is real, but the repo has extreme duplicate activity. Common low-hanging issues such as auth gaps, upload auth, proposal validation, OAuth provider validation, refresh-token validation, job budget validation, and search query validation already have many duplicate child issues/attempts.
- `SecureBananaLabs/bug-bounty#30`: Algora USD 750 benchmark bounty is real, but heavily saturated with many prior attempts, rewards, and open claims.
- `UnitOneAI/SecuritySkills#598`, `#599`, `#600`: stated USD 350 proposals say to wait for maintainer approval before implementation; do not start until approved.
- `charles-openclaw/charles-microbounties`: 200 latest open issues checked; no zero-comment issue found. Recent candidates already had `/attempt`, `/opire try`, or upstream PR links.
- `Scottcjn/Rustchain` and `Scottcjn/bottube`: token/RTC claims, not direct cash; recent candidates already claimed by original reporters.
- `Clawland-AI/clawland-ai.github.io#2` and `Clawland-AI/picclaw#24`: bounty-shaped tasks, but multiple PRs/claims already exist.
- `Expensify/App#75982`: nominal USD 250 issue is closed and internal; not actionable.
- `UnsafeLabs/Bounty-Hunters#571` and `#569`: requires publishing full system/session prompt or complete runtime initialization text. This is not acceptable.
- `claude-builders-bounty#5`: nominal $200, but heavily saturated with many existing PRs and repeated claim comments.
- `warpspeedopen-source/warpspeed-bounties#5`: nominal $660, but requires external signup and maintainer confirmation before work begins.
- `watney-ai/open-source-bounties#1`: nominal EUR 2, but target file is missing and the issue already has many noisy PR attempts.
- `eigenwallet/core#727`: bounty exists, but explicitly requires exclusively human-written communication and no AI-generated PRs.
- `ubiquity/business-development#89` and `#90`: nominal USD 400/USD 200, but UbiquityOS requires core-team/admin status to start; outside contributor attempts are rejected by the bot.
- `ritik4ever/stellar-bounty-board#288`: medium 150-point task, but an implementation PR already exists and later claim comments are present; skip as duplicate-risk.
- `Expensify/App` Help Wanted search: 200 open issues checked; no clean unassigned external issue found after filtering out assigned/Internal/Reviewing tasks.
- `aLexzzz430/Cognitive-OS#5`: nominal USD 3,000, but many attempts/PRs already exist and the thread is saturated; skip unless maintainer explicitly requests a new round.
- `charles-openclaw/charles-microbounties#1`: nominal USD 5 XMR, first verified useful submission wins; already has many high-quality submissions. Inspected fresh small CLI repos, but no strong reproducible candidate found.
- Small CLI repo scan: `Himanshu507/cgcone`, `yopie-org/mailtarget`, `Vani2130/mcp_ctl`, `himanshuskukla/mcp-audit`, `alaas4989/cc-update-all`, and `RefuseHQ/refuse` inspected for quick CLI metadata/help/version bugs; no clean payout-worthy PoC produced in this pass.

2026-06-11 additional live triage:

- `SecureBananaLabs/bug-bounty#743`: confirmed Algora USD 700 parent bounty is real and has historical reward links, but obvious fixes are now duplicate-heavy. Checked whitespace-password, user password storage, job budget range, proposal/message/notification auth, message payload validation, notification server-owned fields, search validation, admin role self-assignment, and Zod 400 handling. Each candidate already has existing issues and/or PRs. Do not submit duplicates.
- `SecureBananaLabs/bug-bounty#6336`: whitespace-only password issue has open PR `#6337` plus many same-scope historical PRs; skipped.
- `SecureBananaLabs/bug-bounty#6334`: user password storage is already covered by child issue `#6526` and PR `#6527`; skipped.
- `SecureBananaLabs/bug-bounty` budget range bug: many duplicate issues/PRs exist (`#2853`, `#5350`, `#5803`, and others); skipped.
- `charles-openclaw/charles-microbounties`: latest open issues rechecked. No zero-comment open candidate found; newest issues already have `/attempt`, `/opire try`, or upstream PRs by other contributors. Do not duplicate.
- Current active payout attempts remain maifetch GBP 50 and the quantum visualizer maintenance PR. No new cash has been received.
