#!/usr/bin/env python3
"""Passive CT-log and DNS takeover triage for Airbnb HackerOne scope."""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DOMAINS = [
    "airbnb.com",
    "airbnb.org",
    "musta.ch",
    "airbnbpayments.com",
    "atairbnb.com",
    "withairbnb.com",
    "airbnbcitizen.com",
    "byairbnb.com",
    "muscache.com",
    "airbnb-aws.com",
    "luxuryretreats.com",
    "airbnbopen.com",
    "hoteltonight.com",
    "hoteltonight-test.com",
]

FAST_DOMAINS = [
    "airbnb.com",
    "airbnb.org",
    "musta.ch",
    "airbnbpayments.com",
]

TAKEOVER_HINTS = [
    "amazonaws.com",
    "azurewebsites.net",
    "cloudapp.net",
    "cloudfront.net",
    "fastly.net",
    "github.io",
    "herokuapp.com",
    "netlify.app",
    "pages.dev",
    "readme.io",
    "s3.amazonaws.com",
    "surge.sh",
    "vercel.app",
]

OUT_DIR = Path("bug_bounty_cases/06-airbnb-bug-bounty/research")
OUT_PATH = OUT_DIR / "passive_takeover_check.json"


def fetch_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"User-Agent": "quickops-passive-bb-research"})
    with urllib.request.urlopen(request, timeout=40) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def crtsh_names(domain: str) -> set[str]:
    query = urllib.parse.quote(f"%.{domain}")
    url = f"https://crt.sh/?q={query}&output=json"
    try:
        rows = fetch_json(url)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return set()
    names: set[str] = set()
    if not isinstance(rows, list):
        return names
    for row in rows[:5000]:
        value = str(row.get("name_value", "")) if isinstance(row, dict) else ""
        for raw_name in value.splitlines():
            name = raw_name.strip().lower().lstrip("*.").rstrip(".")
            if not name or not name.endswith(domain):
                continue
            if re.search(r"[^a-z0-9._-]", name):
                continue
            names.add(name)
    return names


def dns_google(name: str, record_type: str) -> dict[str, object]:
    url = "https://dns.google/resolve?" + urllib.parse.urlencode(
        {"name": name, "type": record_type}
    )
    try:
        data = fetch_json(url)
    except Exception as error:  # noqa: BLE001 - result is diagnostic only
        return {"error": str(error)}
    return data if isinstance(data, dict) else {"error": "unexpected DNS response"}


def answer_values(data: dict[str, object]) -> list[str]:
    answers = data.get("Answer")
    if not isinstance(answers, list):
        return []
    values = []
    for answer in answers:
        if isinstance(answer, dict) and "data" in answer:
            values.append(str(answer["data"]).rstrip(".").lower())
    return values


def main() -> int:
    max_checks = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    domains = FAST_DOMAINS if len(sys.argv) <= 2 else sys.argv[2:]
    all_names: set[str] = set()
    per_domain_counts = {}
    for domain in domains:
        names = crtsh_names(domain)
        per_domain_counts[domain] = len(names)
        all_names.update(names)
        time.sleep(1)

    priority_terms = ("dev", "stage", "staging", "test", "preview", "review", "qa", "sandbox")
    candidates = sorted(
        all_names,
        key=lambda value: (
            not any(term in value for term in priority_terms),
            value.count("."),
            value,
        ),
    )[:max_checks]
    findings = []
    checked = []
    for name in candidates:
        cname_data = dns_google(name, "CNAME")
        cnames = answer_values(cname_data)
        a_data = dns_google(name, "A")
        a_values = answer_values(a_data)
        cname_text = " ".join(cnames)
        hint_matches = [hint for hint in TAKEOVER_HINTS if hint in cname_text]
        status = {
            "name": name,
            "cnames": cnames,
            "a_records": a_values,
            "cname_status": cname_data.get("Status"),
            "a_status": a_data.get("Status"),
            "takeover_hint_matches": hint_matches,
        }
        checked.append(status)
        if hint_matches and not a_values:
            findings.append(status)
        time.sleep(0.08)

    report = {
        "program": "Airbnb HackerOne",
        "method": "passive crt.sh plus DNS-over-HTTPS CNAME/A checks",
        "scope_file": "bug_bounty_cases/06-airbnb-bug-bounty/scope_notes.md",
        "domains": domains,
        "max_checks": max_checks,
        "per_domain_ct_name_counts": per_domain_counts,
        "checked_count": len(checked),
        "candidate_count": len(findings),
        "candidates_needing_manual_takeover_validation": findings,
        "checked": checked,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"CT names discovered: {len(all_names)}")
    print(f"DNS names checked: {len(checked)}")
    print(f"Takeover candidates needing validation: {len(findings)}")
    print(f"Wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
