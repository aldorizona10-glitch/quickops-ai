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
        ["python3", "scripts/automation_doctor.py"],
        ["python3", "scripts/autopilot_status.py"],
        ["python3", "scripts/gmail_check_replies.py"],
        ["python3", "scripts/agency_pipeline_status.py"],
        ["python3", "scripts/non_agency_status.py"],
        ["python3", "scripts/full_auto_revenue_scout.py"],
    ]
    for cmd in checks:
        code = run(cmd)
        if code != 0:
            return code
    print("Autopilot run complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
