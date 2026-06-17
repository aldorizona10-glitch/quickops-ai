#!/usr/bin/env python3
"""Fast, timeout-heavy scout for non-duplicate outreach candidates."""

from __future__ import annotations

import csv
import json
import re
import socket
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "tmp" / "fast_nonduplicate_revenue_scout.csv"
UA = "QuickOps-AI-Fast-Revenue-Scout/1.0"
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
SKIP_PREFIXES = ("privacy@", "legal@", "security@", "abuse@", "noreply@", "no-reply@")
CONTACT_PATHS = ("/contact", "/support", "/about", "/team")
MAX_TARGETS = 8
socket.setdefaulttimeout(3)
QUERIES = (
    "Show HN AI workflow",
    "Show HN API",
    "Show HN automation",
    "Show HN developer tool",
    "Launch HN AI",
    "Ask HN feedback startup",
)


def sent_text() -> str:
    chunks = []
    for rel in ("logs/gmail_api_sent_log.csv", "logs/sent_email_log.csv", "daily_action_tracker.csv"):
        path = ROOT / rel
        if path.exists():
            chunks.append(path.read_text(encoding="utf-8", errors="ignore").lower())
    return "\n".join(chunks)


def fetch_json(url: str, timeout: float = 4) -> object:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def fetch_text(url: str, timeout: float = 3, max_bytes: int = 90_000) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(max_bytes).decode("utf-8", errors="replace")


def valid_email(email: str) -> bool:
    email_l = email.lower()
    return (
        not email_l.startswith(SKIP_PREFIXES)
        and "example." not in email_l
        and not email_l.endswith((".png", ".jpg", ".jpeg", ".svg", ".webp"))
    )


def emails_from(raw: str) -> list[str]:
    return sorted({email.lower() for email in EMAIL_RE.findall(raw) if valid_email(email)})


def first_external_link(text: str) -> str:
    for link in re.findall(r"https?://[^\s<>\"']+", text or ""):
        cleaned = link.rstrip(").,;]")
        if "news.ycombinator.com" not in cleaned:
            return cleaned
    return ""


def write_rows(rows: list[dict[str, object]]) -> None:
    OUT_CSV.parent.mkdir(exist_ok=True)
    rows.sort(key=lambda row: int(row["score"]), reverse=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["score", "email", "domain", "title", "url", "context_url", "contact_url"])
        writer.writeheader()
        writer.writerows(rows)


def discover_contact(url: str) -> tuple[str, str]:
    if not url.startswith("http") or "news.ycombinator.com" in url:
        return "", ""
    try:
        raw = fetch_text(url)
    except Exception:
        return "", ""
    found = emails_from(raw)
    parsed = urllib.parse.urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    contact_url = ""
    hrefs = re.findall(r"href=[\"']([^\"']*(?:contact|support|about|get-in-touch|hello)[^\"']*)[\"']", raw, re.I)
    candidates = []
    for href in hrefs[:4]:
        resolved = urllib.parse.urljoin(url, href)
        if resolved.startswith("http"):
            candidates.append(resolved)
    candidates.extend(base + path for path in CONTACT_PATHS)
    seen = set()
    for candidate in candidates[:6]:
        if candidate in seen:
            continue
        seen.add(candidate)
        if not contact_url:
            contact_url = candidate
        try:
            found.extend(emails_from(fetch_text(candidate, timeout=2, max_bytes=60_000)))
        except Exception:
            continue
    found = sorted(set(found))
    return (found[0] if found else ""), contact_url


def score(title: str, url: str) -> int:
    text = f"{title} {url}".lower()
    weights = {
        "ai": 10,
        "api": 12,
        "automation": 15,
        "workflow": 15,
        "developer": 10,
        "sign": 10,
        "pdf": 8,
        "crm": 8,
        "security": 8,
    }
    return sum(weight for key, weight in weights.items() if key in text)


def main() -> int:
    logged = sent_text()
    sent_emails = {email.lower() for email in EMAIL_RE.findall(logged)}
    sent_domains = {email.split("@", 1)[1] for email in sent_emails}
    rows = []
    seen_urls = set()
    checked_targets = 0

    for query in QUERIES:
        if checked_targets >= MAX_TARGETS:
            break
        params = urllib.parse.urlencode({"query": query, "tags": "story", "hitsPerPage": 8})
        try:
            data = fetch_json(f"https://hn.algolia.com/api/v1/search_by_date?{params}")
        except Exception:
            continue
        hits = data.get("hits", []) if isinstance(data, dict) else []
        for hit in hits:
            if checked_targets >= MAX_TARGETS:
                break
            title = str(hit.get("title") or "").strip()
            if not title:
                continue
            story_text = str(hit.get("story_text") or "")
            target_url = str(hit.get("url") or "").strip() or first_external_link(story_text)
            if not target_url or target_url in seen_urls:
                continue
            seen_urls.add(target_url)
            checked_targets += 1
            print(f"checking={checked_targets}/{MAX_TARGETS} {target_url}", flush=True)
            email, contact_url = discover_contact(target_url)
            if not email:
                continue
            domain = email.split("@", 1)[1]
            if email in sent_emails or domain in sent_domains:
                continue
            hn_url = f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            rows.append(
                {
                    "score": score(title, target_url),
                    "email": email,
                    "domain": domain,
                    "title": title,
                    "url": target_url,
                    "context_url": hn_url,
                    "contact_url": contact_url,
                }
            )
            write_rows(rows)
            print(f"candidate={email} {title}", flush=True)

    write_rows(rows)
    print(f"fast_scout_checked_targets={checked_targets}")
    print(f"fast_scout_candidates={len(rows)}")
    print(f"wrote={OUT_CSV}")
    for row in rows[:10]:
        print(f"{row['score']}\t{row['email']}\t{row['title']}\t{row['url']}\t{row['context_url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
