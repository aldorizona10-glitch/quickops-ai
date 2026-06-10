#!/usr/bin/env python3
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "bug_bounty_findings"
TEMPLATE = ROOT / "bug_bounty_report_template.md"
WIB = timezone(timedelta(hours=7), "WIB")


def slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "finding"


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/new_bug_case.py <program> <short-title>", file=sys.stderr)
        return 2
    program = sys.argv[1]
    title = " ".join(sys.argv[2:])
    now = datetime.now(WIB)
    case_id = f"{now.strftime('%Y%m%d-%H%M')}-{slug(program)}-{slug(title)[:50]}"
    case_dir = CASES / case_id
    evidence = case_dir / "evidence"
    screenshots = case_dir / "screenshots"
    evidence.mkdir(parents=True, exist_ok=True)
    screenshots.mkdir(parents=True, exist_ok=True)

    template = TEMPLATE.read_text(encoding="utf-8") if TEMPLATE.exists() else "# Bug Bounty Report\n"
    report = template.replace("Program:", f"Program: {program}")
    report = report.replace("[Vulnerability type] in [asset/feature] allows [impact]", title)
    report = report.replace("Submitted at:", f"Submitted at: draft created {now.strftime('%Y-%m-%d %H:%M %Z')}")
    (case_dir / "report.md").write_text(report, encoding="utf-8")
    (case_dir / "notes.md").write_text(
        "\n".join(
            [
                f"# {title}",
                "",
                f"Program: {program}",
                f"Created: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}",
                "",
                "## Validation Checklist",
                "",
                "- [ ] Confirm exact in-scope asset from official program page.",
                "- [ ] Use only accounts/assets controlled by researcher.",
                "- [ ] Capture request/response without secrets.",
                "- [ ] Capture screenshot or screen recording if UI impact exists.",
                "- [ ] Confirm no third-party data was accessed.",
                "- [ ] Confirm issue is not listed as out-of-scope/known issue.",
                "- [ ] Fill `report.md` with reproducible steps and impact.",
            ]
        ),
        encoding="utf-8",
    )
    print(case_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
