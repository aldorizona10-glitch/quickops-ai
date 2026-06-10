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

