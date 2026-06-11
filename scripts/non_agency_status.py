#!/usr/bin/env python3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    log = ROOT / "docs" / "non_agency_revenue_log.md"
    print("QuickOps Non-Agency Revenue Status")
    print("==================================")
    print("Open bounty PRs:")
    print("- maifetch Emacs Lisp rewrite: https://github.com/HutchyBen/maifetch/pull/13")
    print("- Bounty issue: https://github.com/HutchyBen/maifetch/issues/1")
    print("- Latest stated bounty: GBP 200 for Emacs Lisp editor-runnable rewrite")
    print("- Status: PR open and mergeable; /claim comment sent on issue #1")
    print("- Validation: GNU Emacs 30.2, byte-compile passed, ERT 4/4 passed, batch help passed")
    print("- Payment depends on maintainer acceptance")
    print()
    print("- maifetch Elixir rewrite: https://github.com/HutchyBen/maifetch/pull/12")
    print("- Bounty issue: https://github.com/HutchyBen/maifetch/issues/1")
    print("- Latest stated bounty: GBP 175, then maintainer requested Elixir with bounty still in place")
    print("- Status: PR open and mergeable; /claim comment sent on issue #1; superseded by Emacs Lisp direction")
    print("- Validation: mix test 6/6 passed; mix escript.build passed after OTP HTTP client update")
    print("- Payment depends on maintainer acceptance")
    print()
    print("- ItzFireable Portfolio Haskell rewrite: https://github.com/ItzFireable/Portfolio/pull/10")
    print("- Bounty issue: https://github.com/ItzFireable/Portfolio/issues/7")
    print("- Latest stated bounty: GBP 200 for Haskell rewrite")
    print("- Status: PR submitted; /claim comment sent on issue #7")
    print("- Validation: git diff --check passed; local Haskell build blocked by missing ghc/cabal/stack/nix/ghcup")
    print("- Payment depends on maintainer acceptance; payout risk is elevated due repeated scope changes")
    print()
    print("- maifetch Rust rewrite: https://github.com/HutchyBen/maifetch/pull/10")
    print("- Bounty issue: https://github.com/HutchyBen/maifetch/issues/1")
    print("- Status: superseded by maintainer's later Elixir direction; PR remains open")
    print("- Payment unlikely unless maintainer accepts older Rust direction")
    print()
    print("- quantum-visualizer maintenance: https://github.com/Iskander-Agent/quantum-visualizer/pull/74")
    print("- Bounty context: https://github.com/1btc-news/news-client/issues/33")
    print("- Status: PR open and mergeable when checked")
    print("- Payment depends on reviewer/admin acceptance; no explicit payout commitment yet")
    print()
    print("Local worktree:")
    print("- /tmp/maifetch")
    print("- /tmp/maifetch-elixir")
    print("- /tmp/maifetch-elisp")
    print("- /tmp/itzfireable-portfolio")
    print("- /tmp/quantum-visualizer")
    print("- portable Rust: /tmp/maifetch-cargo and /tmp/maifetch-rustup")
    print()
    print("Next actions:")
    print("1. Monitor maifetch PR #13 for maintainer comments.")
    print("2. Patch the Emacs Lisp rewrite quickly if review changes are requested.")
    print("3. Monitor ItzFireable Portfolio PR #10 for maintainer comments.")
    print("4. Monitor PR #74 for DRI/reviewer comments.")
    print("5. Ask for payout instructions after acceptance/merge.")
    print("6. Avoid bounties that require leaking system prompts or starting before maintainer confirmation.")
    print()
    print(f"Log: {log}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
