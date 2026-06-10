#!/usr/bin/env python3
import csv
import json
import re
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "full_auto_revenue_scout.csv"
OUT_MD = ROOT / "docs" / "full_auto_revenue_scout_report.md"
WIB = timezone(timedelta(hours=7), "WIB")
UA = "QuickOps-AI-Revenue-Scout/1.0"
MAX_AGE_DAYS = 45
CONTACT_DISCOVERY_LIMIT = 12


HN_QUERIES = [
    ("Show HN AI automation", "HN Show HN product feedback"),
    ("Show HN CRM automation", "HN Show HN workflow buyer"),
    ("Show HN booking API", "HN Show HN testing buyer"),
    ("Show HN PDF API", "HN Show HN technical tester"),
    ("Ask HN freelancer automation", "HN freelance demand"),
    ("Who is hiring AI automation remote", "HN hiring"),
]

GH_QUERIES = [
    '"bounty" "$50" state:open archived:false',
    '"bounty" "$100" state:open archived:false',
    '"bounty" "$250" state:open archived:false',
    '"/bounty $" state:open archived:false',
    '"Bounty:" state:open archived:false',
    '"paid" "bounty" state:open archived:false',
    '"reward" "$" state:open archived:false',
    '"Algora" "bounty" state:open archived:false',
]

REMOTEOK_URL = "https://remoteok.com/api"
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)


def fetch_json(url: str) -> object:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def fetch_text(url: str, max_bytes: int = 350_000) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=18) as resp:
        return resp.read(max_bytes).decode("utf-8", errors="replace")


def clean(value: object) -> str:
    text = str(value or "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def score_text(text: str) -> int:
    text_l = text.lower()
    score = 0
    weights = {
        "bounty": 35,
        "$": 25,
        "paid": 25,
        "automation": 15,
        "ai": 10,
        "api": 10,
        "workflow": 15,
        "tester": 20,
        "testing": 18,
        "feedback": 15,
        "remote": 10,
        "contract": 15,
        "freelance": 20,
        "security": 10,
        "github": 5,
    }
    for word, weight in weights.items():
        if word in text_l:
            score += weight
    if "intern" in text_l or "unpaid" in text_l:
        score -= 30
    return max(score, 0)


def recent_enough(epoch_seconds: object, max_age_days: int = MAX_AGE_DAYS) -> bool:
    try:
        created = datetime.fromtimestamp(int(epoch_seconds), tz=timezone.utc)
    except Exception:
        return True
    age = datetime.now(timezone.utc) - created
    return age <= timedelta(days=max_age_days)


def append_unique(items: list[dict[str, str]], row: dict[str, str], seen: set[str]) -> None:
    key = row.get("url") or row.get("title", "")
    if not key or key in seen:
        return
    seen.add(key)
    items.append(row)


def discover_contact(url: str) -> tuple[str, str]:
    if not url.startswith("http") or "news.ycombinator.com" in url:
        return "", ""
    try:
        raw = fetch_text(url)
    except Exception:
        return "", ""
    emails = sorted(
        {
            email.lower()
            for email in EMAIL_RE.findall(raw)
            if not email.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".svg"))
            and not email.lower().endswith("@example.com")
            and not email.lower().endswith("@domain.com")
            and "example." not in email.lower()
        }
    )
    contact_links = re.findall(r'href=["\']([^"\']*(?:contact|support|about|get-in-touch|hello)[^"\']*)["\']', raw, re.I)
    contact_url = ""
    if contact_links:
        contact_url = urllib.parse.urljoin(url, contact_links[0])
    return (emails[0] if emails else ""), contact_url


def draft_offer(title: str, url: str, lane: str) -> tuple[str, str]:
    subject = "Show HN - practical workflow/testing pass"
    if "pdf" in title.lower():
        subject = "Show HN - PDF workflow testing pass"
    elif "sign" in title.lower() or "envelope" in title.lower():
        subject = "Show HN - e-signature workflow testing pass"
    elif "automation" in title.lower() or "agent" in title.lower():
        subject = "Show HN - AI workflow testing pass"
    body = (
        "Hi,\n\n"
        f"I saw your {title}. The product looks like a fit for a small fixed-scope external operator test.\n\n"
        "Offer: I can do one USD 100 pass and send back a concise report covering:\n"
        "- onboarding and first workflow friction\n"
        "- docs/API clarity from a technical operator perspective\n"
        "- edge cases and failure states worth testing\n"
        "- one practical checklist you can reuse with early users\n\n"
        "I will stay within public/demo flows unless you explicitly provide a sandbox. No production probing or noisy security testing.\n\n"
        "Proof/profile:\n"
        "https://aldorizona10-glitch.github.io/quickops-ai/profile/\n"
        "https://github.com/aldorizona10-glitch/quickops-ai\n\n"
        f"Context I found: {url}\n\n"
        "Best,\n"
        "Aldo\n"
    )
    return subject, body


def hn_search() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for query, lane in HN_QUERIES:
        params = urllib.parse.urlencode(
            {"query": query, "tags": "story", "hitsPerPage": 20}
        )
        data = fetch_json(f"https://hn.algolia.com/api/v1/search_by_date?{params}")
        for hit in data.get("hits", []):  # type: ignore[union-attr]
            if not recent_enough(hit.get("created_at_i")):
                continue
            title = clean(hit.get("title"))
            url = clean(hit.get("url")) or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            text = clean(hit.get("story_text"))
            created = clean(hit.get("created_at"))
            hn_url = f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            signal = f"{title} {text}"
            draft_subject, draft_body = draft_offer(title, hn_url, lane)
            append_unique(
                rows,
                {
                    "source": "hacker_news",
                    "lane": lane,
                    "title": title,
                    "url": url,
                    "context_url": hn_url,
                    "created_or_updated": created,
                    "score": str(score_text(signal)),
                    "automation_level": "auto_discover_auto_draft_manual_send",
                    "cash_path": "USD 50-100 paid feedback/testing/workflow offer if public contact exists",
                    "manual_blocker": "Send only if contact is public and relevant; no spam; no account/KYC bypass",
                    "contact_email": "",
                    "contact_url": "",
                    "draft_subject": draft_subject,
                    "draft_body": draft_body,
                    "next_action": "If contact exists, review draft and send one specific offer. If only contact URL exists, use form manually.",
                },
                seen,
            )
    return rows


def gh_search() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for query in GH_QUERIES:
        cmd = [
            "gh",
            "search",
            "issues",
            query,
            "--limit",
            "30",
            "--json",
            "repository,title,url,commentsCount,updatedAt,createdAt,labels",
        ]
        try:
            proc = subprocess.run(
                cmd,
                cwd=ROOT,
                text=True,
                capture_output=True,
                timeout=40,
                check=False,
            )
        except Exception as exc:
            append_unique(
                rows,
                {
                    "source": "github",
                    "lane": "GitHub bounty search",
                    "title": f"search failed: {query}",
                    "url": "",
                    "context_url": "",
                    "created_or_updated": "",
                    "score": "0",
                    "automation_level": "auto_discover_blocked",
                    "cash_path": "Open-source bounty if search succeeds",
                    "manual_blocker": type(exc).__name__,
                    "contact_email": "",
                    "contact_url": "",
                    "draft_subject": "",
                    "draft_body": "",
                    "next_action": "Retry gh search with network access.",
                },
                seen,
            )
            continue
        if proc.returncode != 0:
            continue
        try:
            data = json.loads(proc.stdout or "[]")
        except json.JSONDecodeError:
            continue
        for issue in data:
            repo = issue.get("repository") or {}
            repo_name = repo.get("nameWithOwner") or repo.get("name") or ""
            labels = ", ".join(label.get("name", "") for label in issue.get("labels", []))
            title = clean(issue.get("title"))
            title_l = title.lower()
            if "bounty claim" in title_l or "claim]" in title_l or "rewarded" in title_l:
                continue
            signal = f"{repo_name} {title} {labels}"
            append_unique(
                rows,
                {
                    "source": "github",
                    "lane": "Open-source paid bounty",
                    "title": f"{repo_name}: {title}",
                    "url": clean(issue.get("url")),
                    "context_url": clean(issue.get("url")),
                    "created_or_updated": clean(issue.get("updatedAt") or issue.get("createdAt")),
                    "score": str(score_text(signal) + 10),
                    "automation_level": "auto_discover_manual_claim_auto_pr_possible",
                    "cash_path": "Bounty payment only after maintainer accepts/merges and pays",
                    "manual_blocker": "Must inspect duplicate attempts and payout rules before coding",
                    "contact_email": "",
                    "contact_url": "",
                    "draft_subject": "",
                    "draft_body": "",
                    "next_action": "Open issue, check comments/claims, implement only if clean and bounty is explicit.",
                },
                seen,
            )
    return rows


def remoteok_search() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    try:
        data = fetch_json(REMOTEOK_URL)
    except Exception:
        return rows
    if not isinstance(data, list):
        return rows
    for job in data[1:80]:
        if not isinstance(job, dict):
            continue
        title = clean(job.get("position") or job.get("title"))
        company = clean(job.get("company"))
        tags = " ".join(clean(t) for t in job.get("tags", []) if t)
        signal = f"{title} {company} {tags}"
        if score_text(signal) < 20:
            continue
        url = clean(job.get("url")) or f"https://remoteok.com/remote-jobs/{job.get('id')}"
        append_unique(
            rows,
            {
                "source": "remoteok",
                "lane": "Remote job/contract lead",
                "title": f"{company}: {title}",
                "url": url,
                "context_url": url,
                "created_or_updated": clean(job.get("date")),
                "score": str(score_text(signal)),
                "automation_level": "auto_discover_manual_apply",
                "cash_path": "Contract/job payout after application/interview",
                "manual_blocker": "Applications often require forms, accounts, interviews, and personal data",
                "contact_email": "",
                "contact_url": "",
                "draft_subject": "",
                "draft_body": "",
                "next_action": "Apply manually only if global/async and matches AI/security/automation.",
            },
            seen,
        )
    return rows


def enrich_top_contacts(rows: list[dict[str, str]]) -> None:
    ranked = sorted(rows, key=lambda row: int(row.get("score", "0") or 0), reverse=True)
    checked = 0
    for row in ranked:
        if checked >= CONTACT_DISCOVERY_LIMIT:
            return
        if row.get("source") != "hacker_news":
            continue
        url = row.get("url", "")
        if not url or "news.ycombinator.com" in url:
            continue
        contact_email, contact_url = discover_contact(url)
        row["contact_email"] = contact_email
        row["contact_url"] = contact_url
        checked += 1


def write_outputs(rows: list[dict[str, str]]) -> None:
    rows.sort(key=lambda row: int(row.get("score", "0") or 0), reverse=True)
    fieldnames = [
        "source",
        "lane",
        "title",
        "url",
        "context_url",
        "created_or_updated",
        "score",
        "automation_level",
        "cash_path",
        "manual_blocker",
        "contact_email",
        "contact_url",
        "draft_subject",
        "draft_body",
        "next_action",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    now = datetime.now(WIB).strftime("%Y-%m-%d %H:%M:%S %Z")
    lines = [
        "# Full Automation Revenue Scout Report",
        "",
        f"Generated: {now}",
        "",
        "This report lists earning paths where discovery and triage can be automated. It does not claim money is earned until a platform/client/maintainer accepts and pays.",
        "",
        "## Automation Reality",
        "",
        "- Fully automatable: public search, scoring, duplicate filtering, draft generation, status tracking, reply checks.",
        "- Not fully automatable without risk: KYC, CAPTCHA, account signup, platform screening, interviews, live service calls, payout setup, maintainer acceptance.",
        "",
        "## Top Opportunities",
        "",
    ]
    for row in rows[:25]:
        lines.extend(
            [
                f"### {row['title']}",
                "",
                f"- Source: {row['source']}",
                f"- Lane: {row['lane']}",
                f"- Score: {row['score']}",
                f"- URL: {row['url']}",
                f"- Context: {row['context_url']}",
                f"- Automation: {row['automation_level']}",
                f"- Cash path: {row['cash_path']}",
                f"- Blocker: {row['manual_blocker']}",
                f"- Contact email: {row.get('contact_email', '')}",
                f"- Contact URL: {row.get('contact_url', '')}",
                f"- Draft subject: {row.get('draft_subject', '')}",
                f"- Next action: {row['next_action']}",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    rows: list[dict[str, str]] = []
    for collector in (gh_search, hn_search, remoteok_search):
        try:
            rows.extend(collector())
        except Exception as exc:
            rows.append(
                {
                    "source": collector.__name__,
                    "lane": "collector_error",
                    "title": f"{collector.__name__} failed",
                    "url": "",
                    "context_url": "",
                    "created_or_updated": "",
                    "score": "0",
                    "automation_level": "blocked",
                    "cash_path": "",
                    "manual_blocker": f"{type(exc).__name__}: {exc}",
                    "contact_email": "",
                    "contact_url": "",
                    "draft_subject": "",
                    "draft_body": "",
                    "next_action": "Retry with network access or inspect collector.",
                }
            )
    enrich_top_contacts(rows)
    write_outputs(rows)
    print(f"Wrote {len(rows)} opportunities")
    print(f"- {OUT_CSV}")
    print(f"- {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
