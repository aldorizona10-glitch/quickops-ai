#!/usr/bin/env python3
import csv
import html
import re
import sys
import textwrap
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "bug_bounty_targets_2026.csv"
OUT = ROOT / "bug_bounty_cases"
LOG = ROOT / "bug_bounty_daily_log.csv"
UA = "QuickOps-AI-Research/1.0 safe authorized bug bounty scope collector"
WIB = timezone(timedelta(hours=7), "WIB")


KEYWORDS = [
    "in progress",
    "pay_for_success",
    "safe harbor",
    "scope",
    "reward",
    "bounty",
    "out of scope",
    "vulnerability",
    "report",
    "disclosure",
    "authorized",
]


def slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "program"


def fetch(url: str) -> tuple[int | None, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as res:
            body = res.read(500_000)
            ctype = res.headers.get("content-type", "")
            return res.status, ctype, body.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read(100_000).decode("utf-8", errors="replace")
        return exc.code, exc.headers.get("content-type", ""), body
    except Exception as exc:
        return None, "", f"FETCH_ERROR: {type(exc).__name__}: {exc}"


def visible_text(raw: str) -> str:
    raw = re.sub(r"(?is)<script.*?</script>", " ", raw)
    raw = re.sub(r"(?is)<style.*?</style>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"\s+", " ", raw)
    return raw.strip()


def extract_title(raw: str) -> str:
    match = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
    if match:
        return re.sub(r"\s+", " ", html.unescape(match.group(1))).strip()
    match = re.search(r'(?is)<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', raw)
    if match:
        return html.unescape(match.group(1)).strip()
    return "Untitled"


def extract_embedded_policy(raw: str) -> tuple[dict[str, str], str]:
    match = re.search(r'data-props="(.*?)"', raw, re.S)
    if not match:
        return {}, ""
    try:
        import json

        data = json.loads(html.unescape(match.group(1)))
    except Exception:
        return {}, ""

    props = data.get("earlyFetchProps", {})
    header = props.get("headerProps", {})
    summary = {
        "program_name": str(header.get("name", "")),
        "program_state": str(header.get("state", "")),
        "status_label": str(header.get("statusLabel", "")),
        "reward_allocation": str(header.get("rewardAllocation", "")),
        "starts_at": str(header.get("startsAt", "")),
        "ends_at": str(header.get("endsAt", "")),
        "product_label": str(header.get("engagementTypeDetail", {}).get("productLabel", "")),
    }
    description = visible_text(props.get("description", ""))
    return {k: v for k, v in summary.items() if v and v != "None"}, description


def keyword_hits(text: str) -> list[str]:
    lowered = text.lower()
    return [k for k in KEYWORDS if k in lowered]


def write_case(target: dict[str, str], status: int | None, ctype: str, raw: str) -> Path:
    now = datetime.now(WIB).strftime("%Y-%m-%d %H:%M:%S %Z")
    case_dir = OUT / f"{target['priority'].zfill(2)}-{slug(target['program'])}"
    case_dir.mkdir(parents=True, exist_ok=True)
    text = visible_text(raw)
    title = extract_title(raw)
    embedded, policy_text = extract_embedded_policy(raw)
    combined_text = f"{text} {policy_text}"
    hits = keyword_hits(raw + " " + combined_text)
    snippet = textwrap.shorten(combined_text, width=4500, placeholder=" ...")

    (case_dir / "source_snapshot.html").write_text(raw, encoding="utf-8")
    (case_dir / "scope_notes.md").write_text(
        "\n".join(
            [
                f"# {target['program']} Scope Notes",
                "",
                f"Collected: {now}",
                f"Official URL: {target['official_url']}",
                f"HTTP status: {status}",
                f"Content-Type: {ctype}",
                f"Page title: {title}",
                f"Reward signal: {target['reward_signal']}",
                f"Initial focus: {target['initial_focus']}",
                "",
                "## Structured Program Signals",
                "",
                *(f"- {key}: {value}" for key, value in embedded.items()),
                "",
                "## Keyword Signals",
                "",
                *(f"- {hit}" for hit in hits),
                "",
                "## Safe Testing Boundary",
                "",
                target["safety_notes"],
                "",
                "## Page Text Snapshot",
                "",
                snippet,
                "",
                "## Decision",
                "",
                "- Do not run active validation until exact in-scope assets are confirmed.",
                "- Use only own accounts and non-destructive proof.",
                "- If an issue touches third-party data, stop and report immediately.",
            ]
        ),
        encoding="utf-8",
    )
    (case_dir / "report_draft.md").write_text(
        (ROOT / "bug_bounty_report_template.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return case_dir


def append_log(program: str, status: str, next_step: str) -> None:
    now = datetime.now(WIB).strftime("%Y-%m-%d %H:%M")
    exists = LOG.exists()
    with LOG.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["date_time_wib", "track", "program_or_client", "action", "status", "next_step"])
        writer.writerow([now, "Bug bounty", program, "Safe scope snapshot collected", status, next_step])


def main() -> int:
    if not TARGETS.exists():
        print(f"Missing {TARGETS}", file=sys.stderr)
        return 1
    OUT.mkdir(exist_ok=True)
    with TARGETS.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"BUG BOUNTY SAFE RESEARCH RUN: {datetime.now(WIB).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    for target in rows:
        program = target["program"]
        url = target["official_url"]
        print(f"COLLECTING: {program} -> {url}")
        status, ctype, raw = fetch(url)
        case_dir = write_case(target, status, ctype, raw)
        if status and 200 <= status < 400:
            append_log(program, "snapshot_collected", f"Review {case_dir / 'scope_notes.md'} before any active test")
        else:
            append_log(program, "needs_manual_review", f"Fetch status {status}; open official page manually")
        print(f"  saved: {case_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
