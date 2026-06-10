# Non-Agency Revenue Log

Date: 2026-06-10

This file tracks revenue attempts that are not QuickOps agency outreach. These are still zero-cash-outlay paths, but payment is not guaranteed until a third party accepts the work and pays.

## Open-Source Bounty

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
