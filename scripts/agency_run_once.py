#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print("$ " + " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    checks = [
        ["python3", "scripts/gmail_check_replies.py"],
        ["python3", "scripts/agency_status.py"],
    ]
    for cmd in checks:
        code = run(cmd)
        if code != 0:
            return code
    print("Agency run complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
