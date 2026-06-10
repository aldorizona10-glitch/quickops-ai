#!/usr/bin/env python3
import argparse
import subprocess
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_once() -> int:
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] agency check")
    return subprocess.call(["python3", "scripts/agency_run_once.py"], cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run agency monitoring loop.")
    parser.add_argument("--interval-minutes", type=int, default=15)
    parser.add_argument("--max-runs", type=int, default=0, help="0 means run forever")
    args = parser.parse_args()

    runs = 0
    while True:
        code = run_once()
        runs += 1
        if code != 0:
            print(f"agency check failed with exit code {code}")
        if args.max_runs and runs >= args.max_runs:
            return code
        time.sleep(max(1, args.interval_minutes) * 60)


if __name__ == "__main__":
    raise SystemExit(main())
