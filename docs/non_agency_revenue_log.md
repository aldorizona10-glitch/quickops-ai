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
- Hardening update comment: https://github.com/HutchyBen/maifetch/pull/12#issuecomment-4675902200
- Runtime validation update comment: https://github.com/HutchyBen/maifetch/pull/12#issuecomment-4676138777
- Status: PR open and mergeable when checked.
- Local worktree: `/tmp/maifetch-elixir`
- Latest commit: `d5c43a5 Use OTP HTTP client for Elixir rewrite`
- Original rewrite commit: `6f5d397 Rewrite maifetch in Elixir`
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

2026-06-11 hardening update:

- Pushed commit `7730097` to PR #12.
- Replaced map-guard CLI argument parsing with explicit `Map.fetch/2`.
- Replaced RGB ANSI helper call with a direct ANSI true-color sequence.
- Replaced `Exception.message/1` for Req errors with `inspect/1` to avoid assuming the error value is an exception struct.
- PR rechecked after push: open and mergeable, no status checks configured.
- PR comment posted after hardening so the maintainer can review the latest focused Elixir rewrite state.

2026-06-11 runtime validation update:

- Installed Elixir/Mix in WSL with user-assisted sudo.
- Removed `Req`/`Mint` and switched the Elixir API client to Erlang/OTP `:httpc`.
- Added `mix.lock` so dependency resolution is reproducible and only `jason` remains as a Hex dependency.
- Validation completed: `mix deps.get`, `mix format`, `mix test` -> 6 tests / 0 failures, `mix escript.build` -> generated escript.
- Pushed commit `d5c43a5` to PR #12 and posted validation comment.

Next actions:

1. Watch PR #12 for maintainer feedback.
2. If changes are requested, patch `/tmp/maifetch-elixir`, push `aldorizona10-glitch:elixir-rewrite-bounty-1`, and reply on the PR.
3. After merge/acceptance, ask maintainer for payout instructions.

### maifetch Emacs Lisp rewrite

- Bounty source: https://github.com/HutchyBen/maifetch/issues/1
- Latest maintainer direction: rewrite the project in Emacs Lisp so it can run inside the maintainer's editor.
- Latest stated amount: GBP 200.
- Fork branch: https://github.com/aldorizona10-glitch/maifetch/tree/emacs-lisp-rewrite-bounty-1
- Pull request: https://github.com/HutchyBen/maifetch/pull/13
- Claim comment: https://github.com/HutchyBen/maifetch/issues/1#issuecomment-4676131976
- Status: PR open and mergeable when checked.
- Local worktree: `/tmp/maifetch-elisp`
- Latest commit: `d915933 Rewrite maifetch in Emacs Lisp`
- Payment status: not paid; depends on maintainer acceptance/merge and payout follow-through.

Scope completed:

- Replaced Go project with single-file Emacs Lisp package `maifetch.el`.
- Added interactive `M-x maifetch` command for use inside Emacs.
- Added batch entrypoint through `maifetch-batch`.
- Preserved CLI/config/env precedence and `MAITEA_*` plus `MAIFETCH_*` env aliases.
- Added MaiTea API helpers for profiles, plays, all plays, best scores, and all best scores.
- Added focused ERT tests.

Validation completed:

```bash
git diff --check
emacs --version
emacs --batch -L . -l maifetch.el --eval '(byte-compile-file "maifetch.el")'
emacs --batch -L . -l maifetch-test.el -f ert-run-tests-batch-and-exit
emacs --batch -L . -l maifetch.el --funcall maifetch-batch -- --help
```

- GNU Emacs 30.2.
- ERT result: 4 tests / 0 unexpected.

Next actions:

1. Watch PR #13 for maintainer feedback.
2. If changes are requested, patch `/tmp/maifetch-elisp`, push `aldorizona10-glitch:emacs-lisp-rewrite-bounty-1`, and reply on the PR.
3. After merge/acceptance, ask maintainer for payout instructions.

2026-06-12 triage update:

- Maintainer changed the requested target again after the Emacs Lisp PR was submitted, now asking for F# / .NET.
- This is a moving-scope bounty pattern. Do not implement another rewrite unless the maintainer first fixes the final target and payout terms before work starts.
- Current automation position: keep PR #13 open, monitor for review/acceptance, and avoid additional unpaid rewrites.
- Auth limitation: no `GITHUB_TOKEN` / `GH_TOKEN` is available in the local environment, and `gh` is not installed, so automated GitHub issue comments cannot be posted from here until GitHub auth is provided.

Ready comment if GitHub auth becomes available:

```md
I submitted the Emacs Lisp rewrite for the latest direction at the time in #13, with local validation completed. Since the target changed again after submission, I am pausing additional rewrites until the current submitted work is reviewed or the final target and payout terms are fixed before implementation.
```

Posted: https://github.com/HutchyBen/maifetch/issues/1#issuecomment-4683140503

### ItzFireable Portfolio Haskell rewrite

- Bounty source: https://github.com/ItzFireable/Portfolio/issues/7
- Latest maintainer direction: rewrite the portfolio in Haskell.
- Latest stated amount: GBP 200.
- Fork branch: https://github.com/aldorizona10-glitch/Portfolio/tree/haskell-portfolio-rewrite-bounty-7
- Pull request: https://github.com/ItzFireable/Portfolio/pull/10
- Claim comment: https://github.com/ItzFireable/Portfolio/issues/7#issuecomment-4676324922
- Status: PR open when submitted.
- Local worktree: `/tmp/itzfireable-portfolio`
- Latest commit: `dd7e774 Rewrite portfolio in Haskell`
- Payment status: not paid; depends on maintainer acceptance/merge and payout follow-through.

Scope completed:

- Replaced the Vue/Vite frontend and Elysia/Bun backend with a single Haskell Scotty web app.
- Preserved the main routes `/` and `/arcade`, navigation, project content, and visual assets.
- Kept `/discord` and `/spotify` JSON endpoints with compatible error responses when private credentials are not configured.
- Moved retained image assets into `public/`.
- Removed obsolete frontend/backend build files, old Azure workflows, and stale submodule config.

Validation:

```bash
git diff --check
```

- Static scan of new text files passed for non-ASCII cleanup.
- Local Haskell build was not run because the current WSL tool environment has no `ghc`, `cabal`, `stack`, `nix`, or `ghcup`.
- Attempted to add a GitHub Actions Haskell workflow, but push was rejected because the available GitHub token lacks `workflow` scope. The workflow file was removed before PR submission.

Risk note:

- This bounty has visible payout risk because the maintainer changed scope repeatedly from C++ to Python to Haskell. The PR was still submitted because the latest issue comment states a GBP 200 bounty and the implementation cost was acceptable.

Next actions:

1. Watch PR #10 and issue #7 for maintainer feedback.
2. If a Haskell build failure is reported, patch `/tmp/itzfireable-portfolio`, push `aldorizona10-glitch:haskell-portfolio-rewrite-bounty-7`, and reply on the PR.
3. If accepted/merged, ask for payout instructions.

2026-06-12 triage update:

- Maintainer changed the requested target again after the Haskell PR was submitted, now asking for Fortran.
- This is a moving-scope bounty pattern. Do not implement the Fortran rewrite unless the maintainer first fixes the final target and payout terms before work starts.
- Current automation position: keep PR #10 open as submitted work, monitor for review/acceptance, and stop additional unpaid rewrites.

Ready comment if GitHub auth becomes available:

```md
I submitted the Haskell rewrite against the latest stated bounty direction at the time. Since the target has changed again after submission, I am pausing further rewrites unless the scope and payout terms are fixed before work starts.
```

Posted: https://github.com/ItzFireable/Portfolio/issues/7#issuecomment-4683140437

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

2026-06-12 additional USD 100 workflow/testing outreach:

- Target: SynCodeLive, Show HN live coding / AI collaboration product.
- Source: https://news.ycombinator.com/item?id=48487791
- Public contact: `hello@syncodelive.com`
- Offer sent: USD 100 fixed external workflow testing pass for first-session onboarding, invite/join flow, permission edge cases, AI handoff clarity, and early-tester checklist.
- Email queue file: `email_queue/syncodelive-workflow-testing-pass.eml`
- Gmail send status: sent, Gmail ID `19eb7c1f74d27196`.
- Payment status: not paid; depends on reply, acceptance, delivery, and payout agreement.

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

2026-06-12 triage update:

- PR #74 is open, cleanly mergeable, and reviewed positively by `Iskander-Agent`.
- `arc0btc` also logged a code-correctness pass in the bounty issue and concurred that the PR is clean with no correctness issues.
- Current blocker is PC review / final approval from the maintainers named in the PR thread.
- This is the healthiest current bounty-adjacent item because the review says there are no diff issues and the PR is waiting on approval rather than a moving target.
- Current automation position: do not change the PR unless asked; monitor and be ready to patch quickly.
- Bounty issue reference: https://github.com/1btc-news/news-client/issues/33#issuecomment-4682653874

Ready comment if GitHub auth becomes available:

```md
Thanks for the review. I will keep this PR stable while it waits for PC review. If ThankNIXlater/lekanbams want any adjustment, I can patch it quickly.
```

Posted: https://github.com/Iskander-Agent/quantum-visualizer/pull/74#issuecomment-4683140581

### Quantum Visualizer Neha Narula history correction

- Bounty source: https://github.com/1btc-news/news-client/issues/33
- Active maintenance lane: narrow source-backed data-correctness pass.
- Pull request: https://github.com/Iskander-Agent/quantum-visualizer/pull/75
- Fork branch: https://github.com/aldorizona10-glitch/quantum-visualizer/tree/fix-neha-history-score
- Status: PR open and mergeable when checked.
- Commit: `aba224e Fix Neha Narula history score`
- Payout context: no explicit payout commitment for this small correction; Issue #33 says good data PRs still land, payout/admin eligibility depends on reviewer/admin approval.
- Work completed: corrected the `update_history` entry for Neha Narula from score `1→3` to `1→4`, matching the current developer record and the already cited April 3 primary source.
- Primary source: https://nehanarula.org/2026/04/03/bitcoin-and-quantum-computing.html

Validation completed:

```bash
npm run validate:data
npm run check:dashboard
npm run check:frontend
git diff --check
```

Next actions:

1. Watch PR #75 for DRI/reviewer feedback.
2. Patch quickly if a wording/source adjustment is requested.
3. If accepted/merged, ask whether it qualifies for the Issue #33 accepted data-correctness lane.

## Bounty Triage Notes

Skipped for now:

- `ItzFireable/Portfolio#7`: no longer skipped. Submitted Haskell rewrite PR #10 despite payout-risk because the latest stated amount is GBP 200.
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

2026-06-12 additional USD 100 app testing outreach:

- Target: Stiuvou / Grandpa Games, an ad-free game collection for older players and general family play.
- Source: https://news.ycombinator.com/item?id=48444267
- Public contact: `info@stiuvou.ch`.
- Offer sent: USD 100 external testing pass for first-download flow, first-three-games selection, older-player usability, App Store/Google Play trust signals, local-only progress and unlock-point edge cases, and early-tester checklist.
- Email queue file: `email_queue/stiuvou-grandpagames-testing-pass.eml`.
- Gmail send status: sent, Gmail ID `19eb7d53dff2debf`.
- Payment status: not paid; depends on reply, acceptance, delivery, and payout agreement.

2026-06-12 fast-response revenue triage:

- HackerOne fast-response preference applied: prioritize programs with short first-response/triage/bounty timelines over slow high-prestige targets.
- Airbnb HackerOne extracted from logged-in session: average first response shown as 0h, triage 12h, bounty 2w2d, payout SLA 5 business days after triage. Passive high-impact DNS takeover sweep checked 200 prioritized CT/DNS names and found 0 takeover candidates. No report submitted.
- Newegg HackerOne extracted from logged-in session: first response 4h, triage 1d23h, bounty 1w14h. Exact eligible assets recorded. Passive CT/DNS sweep returned 0 eligible CT names and 0 takeover candidates. No report submitted.
- GitHub HackerOne owned-asset boundary check covered 8 owned repos with 0 alerts. No report submitted.
- Shopify remains the highest payout campaign identified, but safe testing requires researcher-created Shopify store/account assets; do not touch live merchant stores.
- Shopify setup continuation: HackerOne handle verified as `acinfo`; alias used was `acinfo@wearehackerone.com`. Shopify accepted the alias far enough to redirect to `admin.shopify.com/signup`, but the admin endpoint returned `ERR_EMPTY_RESPONSE` in Edge and Windows curl showed Cloudflare challenge/403. No Shopify report submitted.
- Unico IDtech HackerOne extracted from logged-in session: response efficiency 99%, first response 14h, triage 1d5h, average time to bounty 1w5d. Active iOS liveness campaign has 1.5x multiplier but requires physical iOS/TestFlight. Web SDK docs/assets were extracted through Edge; a single negative `/createProcess` request with invalid token returned 400 empty, and bundle scan did not produce a reportable issue. No report submitted.
- Syfe HackerOne extracted from logged-in session: response efficiency 86%, first response 1d11h, triage 2d2h, rewards USD 50 to USD 1,500. Passive HEAD check over 7 in-scope roots returned expected web/API protected statuses; no finding and no report submitted. Production signup must use `acinfo@wearehackerone.com` before any account-bound testing.
- HN/outreach dedupe pass: `hello@inspectioncredit.com`, `os@ota.run`, and `hello@integuru.ai` were already contacted; `founders@clor.com` was skipped as same-domain duplicate because `support@clor.com` was already contacted.
- VisiSign is a clear product fit but no public email was found on the fetched pages; contact-form-only opportunities are tracked but not forced through automation.
- Fast scout improvement added: `scripts/fast_nonduplicate_revenue_scout.py` uses short network timeouts and domain-level dedupe. Initial broad run timed out before finding a new clean email; continue with smaller batches or alternate sources.

2026-06-12 additional USD 100 component-search testing outreach:

- Target: Stillwind, high-resolution electronic component search.
- Source: https://news.ycombinator.com/item?id=48494234
- Public contact: `contact@stillwind.ai`.
- Offer sent: USD 100 fixed-scope pass covering first-search onboarding, natural-language/spec-heavy search quality, datasheet/result clarity, sign-in/file-upload/feedback friction, and a reusable component-search QA checklist.
- Email queue file: `email_queue/stillwind-component-search-testing-pass.eml`.
- Gmail send status: sent, Gmail ID `19eb80efeb541d2e`.
- Payment status: not paid; depends on reply, acceptance, delivery, and payout agreement.

2026-06-12 additional USD 100 AI-coding workflow testing outreach:

- Target: Command Center, AI coding environment for quality-focused developers.
- Source: https://news.ycombinator.com/item?id=48453002
- Public contact: `contact@cc.dev`.
- Offer sent: USD 100 fixed-scope pass covering first-run setup, project import friction, agent task flow from prompt to diff to verification, review/rollback/failure-state handling, unclear quality/security expectations, and a reusable agent-workspace QA checklist.
- Email queue file: `email_queue/ccdev-command-center-workflow-testing.eml`.
- Gmail send status: sent, Gmail ID `19eb81f4925f3fb8`.
- Payment status: not paid; depends on reply, acceptance, delivery, and payout agreement.

2026-06-12 additional USD 100 transcription workflow testing outreach:

- Target: MimicScribe, on-device transcriber with speaker identification.
- Source: https://news.ycombinator.com/item?id=48415709
- Public contact: `support@mimicscribe.app`.
- Offer sent: USD 100 fixed-scope pass covering first-run onboarding and permissions, recording/import flow, speaker labeling and correction, privacy/trust wording, export/share friction, transcript cleanup expectations, and a reusable transcription QA checklist.
- Email queue file: `email_queue/mimicscribe-transcription-workflow-testing.eml`.
- Gmail send status: sent, Gmail ID `19eb820e9b67a233`.
- Payment status: not paid; depends on reply, acceptance, delivery, and payout agreement.

2026-06-12 additional USD 100 planning-workflow testing outreach:

- Target: Topolog, typed DAG planning and deadline computation.
- Source: https://news.ycombinator.com/item?id=48484353
- Public contact: `hello@topolog.co.uk`.
- Offer sent: USD 100 fixed-scope pass covering first-plan onboarding, parsing a messy real-world project brief, dependency/deadline/invalid-state feedback, DAG model clarity, export/share/handoff friction, and a reusable planning-workflow QA checklist.
- Email queue file: `email_queue/topolog-planning-workflow-testing.eml`.
- Gmail send status: sent, Gmail ID `19eb82a8d79dc31a`.
- Payment status: not paid; depends on reply, acceptance, delivery, and payout agreement.

2026-06-12 additional USD 100 quiz-conversion testing outreach:

- Target: LittleTough / "Which AI agent are you?"
- Source: https://news.ycombinator.com/item?id=48494173
- Public contact: `info@littletough.com`.
- Offer sent: USD 100 fixed-scope pass covering first-screen clarity, mobile flow friction, question wording and pacing, result-page clarity/shareability/CTA placement, trust signals, and a reusable quiz/landing-page QA checklist.
- Email queue file: `email_queue/littletough-agent-quiz-conversion-testing.eml`.
- Gmail send status: sent, Gmail ID `19eb82bc3774f23a`.
- Payment status: not paid; depends on reply, acceptance, delivery, and payout agreement.

2026-06-12 GitHub bounty execution:

- Target: `HutchyBen/maifetch#1`, latest maintainer direction: F# rewrite applying relevant paradigms.
- PR opened: `HutchyBen/maifetch#15` - https://github.com/HutchyBen/maifetch/pull/15
- Scope: .NET 8 F# rewrite replacing Go module, preserving CLI/config/env precedence, MaiTea API wrapper, profile/recent-play output, score-count cap, ANSI labels, focused tests, and GitHub Actions build/test workflow.
- Maintainer LLM rule handled: every F# source file starts with `LLM-assisted development: OpenAI GPT-5 Codex`.
- Local validation update: installed .NET SDK 8.0.422 locally under workspace without sudo; `git diff --check` passed; `dotnet build Maifetch.sln --configuration Release --no-restore --verbosity minimal -m:1` passed; `dotnet run --project tests/Maifetch.Tests/Maifetch.Tests.fsproj --configuration Release --no-restore` passed; `dotnet run --project src/Maifetch/Maifetch.fsproj --configuration Release --no-build -- --help` passed. PR validation comment posted: https://github.com/HutchyBen/maifetch/pull/15#issuecomment-4684633196
- Payment status: not paid; depends on maintainer review/merge/bounty decision.

2026-06-12 GitHub bounty triage after maifetch:

- `HutchyBen/maifetch#15` status after validation push: open, non-draft, mergeable, no failing checks shown by GitHub.
- Gmail reply check after GitHub push: 0 new replies; agency pipeline count remains 51 real sent, 1 logged reply.
- `ClankerNation/OpenAgents#50` reviewed because it advertised `/bounty $4300`; rejected for execution because acceptance criteria require pasting the complete session initialization text into modified files, which would disclose internal instructions. Also has prior competing claim/PR evidence, so duplicate risk is high.
- `p0s/clankergigs#4` reviewed; skipped for real revenue because issue explicitly says it is not real USD and only uses Sepolia testnet bounty flow.
- `zkldi/Tachi#1650` reviewed; value is £600, but maintainer requires the whole `typescript/server` module rewritten in Haskell in one PR with no milestone/reservation. GitHub tree scan shows 1,047 entries under `typescript/server/src`, so this is high-value but not a fast-response quick win.
- Started local Tachi work after confirming no PR currently targets `#1650`: branch `haskell-server-rewrite-1650` in `tmp/tachi-haskell-shallow`, commits `2c62570 Start Haskell server rewrite` and `d7b7d82 Document Haskell porting gate`. Current work is a local scaffold only, not pushed or claimed, because a professional submission must satisfy the maintainer requirement for a full `typescript/server` Haskell rewrite in one PR.
- Tachi Haskell toolchain update: WSL now has GHC 9.10.3, cabal-install 3.12.1.0, stack 3.7.1, plus Ubuntu-packaged Scotty/Aeson/Warp/WAI dependencies. Local validation now passes for scaffold build and smoke endpoints: `cabal build all --offline`, `/.deploy/up` 200, `/api/v1/status` success envelope, `/api/v1/config` deliberate 501 placeholder envelope.
- Tachi Haskell implementation update: `/api/v1/config`, `/api/v1/config/beatoraja-queue-size`, `/api/v1/config/max-rivals`, and GET/POST `/api/v1/status` now return TypeScript-compatible success envelopes and config/status body fields. Revalidated with offline Cabal build plus local smoke checks for query echo, JSON body echo, config fields, numeric config endpoints, and deliberate 501 on an unported route. Still not pushed or claimed because full bounty eligibility requires the complete server rewrite, not partial endpoint parity.
- Tachi route coverage update: generated 218 API v1 placeholder registrations directly from `src/server/router/api/v1/spec.ts`, excluding the five real status/config handlers already ported. Revalidated `cabal build all --offline`, real config route, a newly covered catalog route (`GET /api/v1/games/:game/charts`), and a late proposal webhook route (`POST /api/v1/proposals/webhook/merged`) returning explicit 501 envelopes instead of accidental 404s. Still not payout-eligible until the placeholders are replaced with real Haskell handlers.
- Tachi parity update: added explicit guest auth context matching TypeScript unauthenticated API requests, TypeScript-style JSON failure envelopes for unknown routes, and real game support handlers for `/api/v1/games`, `/api/v1/games/:gameGroup`, and `/api/v1/games/:game` with enabled-game validation. Revalidated offline Cabal build plus smoke tests for support config, enabled game stats stub, disabled game 400, invalid game 400, and unknown-route 404.
- Tachi empty-state API update: ported real minimal handlers for `/api/v1/activity`, `/api/v1/ublock-blocks-this`, `/api/v1/search`, and `/api/v1/search/chart-hash`. These return TypeScript-compatible success envelopes with empty data while DB-backed search/activity internals are still pending, and validate missing `search` with a 400 failure envelope. Revalidated offline Cabal build plus smoke tests for all four endpoints.
- Tachi users update: ported `GET /api/v1/users` as a TypeScript-compatible empty-state handler returning `Returned 0 users.` and `[]`, leaving per-user DB-backed routes as explicit 501 placeholders. Revalidated offline Cabal build and smoke-tested `/api/v1/users` plus `/api/v1/users/:userID` placeholder behavior.
- Tachi imports update: ported `GET /api/v1/imports` and `GET /api/v1/imports/failed` as TypeScript-compatible empty-state handlers returning `{imports:[], users:[]}` and `{failedImports:[], users:[]}`. Revalidated offline Cabal build and smoke-tested both endpoints plus per-import placeholder behavior.
- Tachi clients auth update: ported unauthenticated `GET /api/v1/clients` behavior to return the same session-level 401 JSON failure as the TypeScript route. Revalidated offline Cabal build and smoke-tested the endpoint.
- Tachi auth update: ported unauthenticated `POST /api/v1/auth/logout` behavior to return the same 409 JSON failure (`You are not logged in.`) as the TypeScript route. Revalidated offline Cabal build and smoke-tested the endpoint.
- Tachi validation update: added a Cabal/HUnit test suite covering guest auth shape, serialized game support config, display names, and enabled-game expansion. `cabal test all --offline` passes cleanly with 3 HUnit cases.
- Tachi auth timing-safe update: ported `POST /api/v1/auth/resend-verify-email` and `POST /api/v1/auth/forgot-password` safe responses, preserving the 200/202 success-envelope behavior without disclosing account existence. Revalidated offline Cabal build and smoke-tested both endpoints.
- Tachi DB users update: installed Haskell PostgreSQL client dependency, added optional `POSTGRES_URL` connection helper and `UserDocument` row mapping for the `account` table. `GET /api/v1/users` and `GET /api/v1/users/:userID` now use Postgres when configured, with local no-DB fallback preserved. Revalidated offline Cabal build/test; HUnit coverage is now 4 cases including user JSON shape.
- Tachi USC IR update: ported `GET /ir/usc/:playtype` heartbeat/auth response behavior with playtype validation, no-token/malformed-token responses, and `priv_api_token` bearer-token lookup when `POSTGRES_URL` is configured. Revalidated `git diff --check`, `cabal test all --offline`, `cabal build all --offline`, and smoke-tested no-token, malformed-token, and invalid-playtype responses on local port 18080.
- Tachi USC chart update: ported `GET /ir/usc/:playtype/charts/:chartHash` acceptance-check behavior with playtype-to-game mapping, shared USC bearer-token validation, optional Postgres chart hash lookup, and TypeScript-compatible chart-not-found message using `TACHI_USC_QUEUE_SIZE`. Revalidated `git diff --check`, `cabal test all --offline`, `cabal build all --offline`, and smoke-tested no-token, malformed-token, invalid-token, and invalid-playtype responses on local port 18080.
- Tachi localdev update: ported `GET /api/v1/seeds` and `GET /api/v1/localdev/song-seed-status` with `NODE_ENV`-based local-dev/test gating and optional Postgres song-count lookup. Revalidated `git diff --check`, `cabal test all --offline`, `cabal build all --offline`, smoke-tested success responses under `NODE_ENV=dev`, and smoke-tested matching 403 local-dev-only failures under `NODE_ENV=production`.
- Tachi startup mode update: added explicit Haskell executable mode parsing for default HTTP server, `--cron-worker`, and `--job-queue-worker`, so worker scripts no longer accidentally start the HTTP API. Worker modes currently fail loudly as an honest remaining porting boundary. Revalidated `git diff --check`, `cabal test all --offline`, `cabal build all --offline`, and command-line behavior for both worker flags plus an invalid argument.
- Tachi session-auth parity update: ported unauthenticated guest behavior for `GET /api/v1/users/:userID/api-tokens` and `GET /api/v1/users/:userID/notifications`, returning the TypeScript-compatible 401 session-level auth failure instead of placeholder 501. Revalidated `git diff --check`, `cabal test all --offline`, `cabal build all --offline`, and smoke-tested both routes on local port 18080.
- Tachi user settings update: ported `GET /api/v1/users/:userID/settings` to a Postgres-backed Haskell reader over `account_settings` plus `account_following`, preserving local no-DB 501 fallback, and ported unauthenticated `PATCH /api/v1/users/:userID/settings` to the TypeScript-compatible 401 session-level auth failure. Revalidated `git diff --check`, `cabal test all --offline`, `cabal build all --offline`, and smoke-tested GET no-DB fallback plus PATCH 401 on local port 18080.
- Tachi migration foundation update: added `Tachi.Migrations` with `_migration` table setup, advisory lock `7461636869`, lexicographic plain/up SQL discovery, raw SHA-256 checksum storage, checksum mismatch protection, failed migration retry, and success/failure recording. Wired the HTTP startup to run migrations only when both `POSTGRES_URL` and `MIGRATIONS_DIR` are configured; local no-env smoke startup skips migrations and still serves `/.deploy/up`. Revalidated `git diff --check`, `cabal build all --offline`, `cabal test all --offline`, and local smoke health check.
- Tachi game profiles update: ported `GET /api/v1/users/:userID/game-profiles` to a Postgres-backed Haskell reader over `game_profile`, including JSONB `ratings`/`classes` serialization and a route-level `__rankingData` field placeholder pending full ranking query parity. Revalidated `git diff --check`, `cabal build all --offline`, `cabal test all --offline`, and smoke-tested the no-DB fallback on local port 18080.
- Tachi email self-auth update: ported unauthenticated guest behavior for `GET /api/v1/users/:userID/is-email-verified` and `GET /api/v1/users/:userID/email`, returning the TypeScript-compatible 401 session-level auth failure instead of placeholder 501. Revalidated `git diff --check`, `cabal build all --offline`, `cabal test all --offline`, and smoke-tested both routes on local port 18080.
- Tachi recent imports update: ported `GET /api/v1/users/:userID/recent-imports` to a Postgres-backed Haskell aggregation over one-month recent user-intent imports, excluding the two mypagescraper import types and returning `{importType,count}` rows sorted by count. Revalidated `git diff --check`, `cabal build all --offline`, `cabal test all --offline`, and smoke-tested the no-DB fallback on local port 18080.
- Tachi job queue foundation update: added typed Haskell `job_queue` primitives for `FOR UPDATE SKIP LOCKED` claiming, marking jobs done/failed, and requeueing 409 attempts without wiring the score-import processor yet. This preserves worker safety by not claiming real jobs before importer parity exists. Revalidated `git diff --check`, `cabal build all --offline`, and `cabal test all --offline`.
- Tachi user stats update: ported `GET /api/v1/users/:userID/stats` to a Postgres-backed Haskell count over `score` and `session` rows. Revalidated `git diff --check`, `cabal build all --offline`, and `cabal test all --offline`.
- Tachi user mutation auth update: ported unauthenticated guest behavior for `POST /api/v1/users/:userID/change-email`, `POST /api/v1/users/:userID/change-password`, `POST /api/v1/users/:userID/change-username`, and `GET /api/v1/users/:userID/last-username-change`, returning TypeScript-compatible 401 session-level auth failures instead of placeholders. Revalidated `git diff --check`, `cabal build all --offline`, `cabal test all --offline`, and smoke-tested representative POST/GET routes on local port 18080.
- Tachi import timestop auth update: ported unauthenticated guest behavior for `GET`, `DELETE`, and `PUT /api/v1/users/:userID/import-timestops`, returning TypeScript-compatible 401 session-level auth failures instead of placeholders. Revalidated `git diff --check`, `cabal build all --offline`, `cabal test all --offline`, and smoke-tested GET/PUT routes on local port 18080.
- Tachi invite/following auth update: ported unauthenticated guest behavior for invite routes and following add/remove routes, returning TypeScript-compatible 401 session-level auth failures instead of placeholders. Revalidated `git diff --check`, `cabal build all --offline`, and `cabal test all --offline`.
- Tachi integration auth update: ported unauthenticated guest behavior for MYT, KAI, CG, Fervidex, and KSHook SV6C user integration routes, returning TypeScript-compatible 401 session-level auth failures instead of placeholder 501 responses. Revalidated `git diff --check`, `cabal build all --offline`, `cabal test all --offline`, and smoke-tested representative GET/PUT/DELETE routes on local port 18080.
- Tachi self-auth expansion update: ported unauthenticated guest behavior for user profile patch, pfp/banner delete, API token create/delete, notification mark/delete, OAuth code creation, and client creation routes, preserving the distinct TypeScript 401 messages for direct session checks versus session-level auth middleware. Validation is running locally before commit.
- Tachi following read update: ported `GET /api/v1/users/:userID/following` to a Postgres-backed Haskell reader over `account_following` plus `account`, returning the TypeScript-compatible `{ friends }` response when DB env is configured while keeping no-DB local fallback explicit.
- Tachi session calendar update: ported `GET /api/v1/users/:userID/sessions/calendar` to a Postgres-backed Haskell reader over `session`, serializing compact calendar rows with `sessionID`, `name`, `desc`, `highlight`, `timeStarted`, `timeEnded`, and `game`.
- Tachi failed import tracker update: ported `GET /api/v1/users/:userID/imports/failed` to a Postgres-backed Haskell reader over `import_tracker`, preserving `FAILED` tracker document shape and `importType`/`userIntent` filters.
- Tachi job queue pure parity update: added Haskell job kind/status/retry constants, deterministic 409 backoff base calculation with overflow-safe cap, and worker-count option parsing matching TypeScript CLI/env precedence including `parseInt`-style leading digits. Offline HUnit coverage now includes these worker contract checks.
- Tachi static game metadata update: ported `GET /api/v1/games/:game/playlists` and `GET /api/v1/games/:game/custom-tables` for DB-free IIDX/BMS metadata, including enabled-game validation and non-supported game 404 behavior. Playlist payload generation and BMS header/body routes remain pending because they depend on DB/external table loaders.
- Tachi BMS table HTML update: ported `GET /api/v1/games/:game/custom-tables/:tableUrlName` for DB-free BMS HTML stub behavior with table lookup, wrong-playtype/user-specific-table errors, non-BMS 404, and invalid-game validation. Added `OUR_URL` config fallback for generated `bmstable` meta links.
- Tachi playlist detail validation update: ported `GET /api/v1/games/:game/playlists/:playlistID` validation for unsupported games and unknown playlists, leaving the known `aaa-bpi` payload as an explicit placeholder until DB-backed chart/BPI generation is ported.
- Tachi user imports update: ported `GET /api/v1/users/:userID/imports` to a Postgres-backed Haskell reader over completed `import` rows and related games/errors/classes/sessions/score IDs, preserving the TypeScript `ImportDocument` shape and `importType`/`userIntent` filters.
