#!/usr/bin/env python3
import base64
import json
import re
import sys
import time
from pathlib import Path
from urllib import parse, request, error

from gmail_auth import refresh_access_token


ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
REPLY_LOG = LOG_DIR / "replies.jsonl"

TARGET_SENDERS = {
    "jobs@goshopbrands.com": "Go.Shop",
    "steve@pango.ai": "Pango",
    "careers@babou.ai": "Babou",
}


def gmail_get(access_token: str, url: str) -> dict:
    req = request.Request(url, headers={"Authorization": f"Bearer {access_token}"})
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gmail API HTTP {exc.code}: {body}") from exc


def header_value(message: dict, name: str) -> str:
    headers = message.get("payload", {}).get("headers", [])
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", "")
    return ""


def decode_body_part(part: dict) -> str:
    data = part.get("body", {}).get("data", "")
    if not data:
        return ""
    padded = data + ("=" * (-len(data) % 4))
    try:
        return base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8", errors="replace")
    except Exception:
        return ""


def extract_text(payload: dict) -> str:
    if payload.get("mimeType") == "text/plain":
        return decode_body_part(payload)
    texts = []
    for part in payload.get("parts", []) or []:
        texts.append(extract_text(part))
    text = "\n".join(t for t in texts if t)
    if text:
        return text
    if payload.get("mimeType") == "text/html":
        html = decode_body_part(payload)
        return re.sub(r"<[^>]+>", " ", html)
    return ""


def normalize_email(value: str) -> str:
    match = re.search(r"<([^>]+)>", value)
    if match:
        value = match.group(1)
    return value.strip().lower()


def append_reply(record: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    with REPLY_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def seen_ids() -> set[str]:
    if not REPLY_LOG.exists():
        return set()
    ids = set()
    for line in REPLY_LOG.read_text(encoding="utf-8").splitlines():
        try:
            ids.add(json.loads(line).get("id", ""))
        except json.JSONDecodeError:
            continue
    return ids


def main() -> int:
    access_token = refresh_access_token()
    query = " OR ".join(f"from:{sender}" for sender in TARGET_SENDERS)
    url = "https://gmail.googleapis.com/gmail/v1/users/me/messages?" + parse.urlencode(
        {"q": f"newer_than:14d ({query})", "maxResults": "20"}
    )
    result = gmail_get(access_token, url)
    messages = result.get("messages", [])
    if not messages:
        print("No replies found from target senders.")
        return 0

    known = seen_ids()
    new_count = 0
    for item in messages:
        mid = item["id"]
        if mid in known:
            continue
        msg = gmail_get(access_token, f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{mid}?format=full")
        from_header = header_value(msg, "From")
        sender = normalize_email(from_header)
        if sender not in TARGET_SENDERS:
            continue
        text = extract_text(msg.get("payload", {}))
        record = {
            "id": mid,
            "threadId": msg.get("threadId", ""),
            "timestamp": int(time.time()),
            "company": TARGET_SENDERS[sender],
            "from": from_header,
            "subject": header_value(msg, "Subject"),
            "date": header_value(msg, "Date"),
            "snippet": msg.get("snippet", ""),
            "text_preview": text.strip()[:2000],
        }
        append_reply(record)
        new_count += 1
        print(f"NEW REPLY: {record['company']} | {record['subject']} | {mid}")

    print(f"Logged {new_count} new repl(ies).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
