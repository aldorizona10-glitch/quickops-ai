#!/usr/bin/env python3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    log = ROOT / "docs" / "non_agency_revenue_log.md"
    print("QuickOps Non-Agency Revenue Status")
    print("==================================")
    print("Open bounty PR:")
    print("- maifetch Rust rewrite: https://github.com/HutchyBen/maifetch/pull/10")
    print("- Bounty issue: https://github.com/HutchyBen/maifetch/issues/1")
    print("- Stated bounty: GBP 50")
    print("- Status: PR open and mergeable; follow-up comment sent")
    print("- Payment depends on maintainer acceptance")
    print()
    print("Local worktree:")
    print("- /tmp/maifetch")
    print("- portable Rust: /tmp/maifetch-cargo and /tmp/maifetch-rustup")
    print()
    print("Next actions:")
    print("1. Monitor PR #10 for maintainer comments.")
    print("2. Patch and rebuild if review changes are requested.")
    print("3. Ask for payout instructions after acceptance/merge.")
    print("4. Avoid bounties that require leaking system prompts or starting before maintainer confirmation.")
    print()
    print(f"Log: {log}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
