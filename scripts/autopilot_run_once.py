#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print("$ " + " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    checks = [
        ["bash", "scripts/setup_native_tools.sh"],
        ["python3", "scripts/autopilot_status.py"],
        ["python3", "scripts/render_youtube_shorts.py"],
        ["python3", "scripts/gmail_check_replies.py"],
    ]
    for cmd in checks:
        code = run(cmd)
        if code != 0:
            return code
    if (ROOT / "youtube_token.json").exists() and os.environ.get("QUICKOPS_UPLOAD_YOUTUBE_PRIVATE") == "1":
        code = run(["python3", "scripts/upload_youtube_short.py", "all"])
        if code != 0:
            return code
    elif not (ROOT / "youtube_token.json").exists():
        print("YouTube upload skipped: run scripts/youtube_oauth_local.py once after enabling YouTube Data API v3.")
    else:
        print("YouTube upload skipped: set QUICKOPS_UPLOAD_YOUTUBE_PRIVATE=1 to upload rendered Shorts privately.")
    print("Autopilot run complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
