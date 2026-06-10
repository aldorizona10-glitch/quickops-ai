#!/usr/bin/env python3
import base64
import json
import re
import sys
from pathlib import Path
from urllib import parse, request, error

from gmail_auth import refresh_access_token


def gmail_get(access_token: str, url: str) -> dict:
    req = request.Request(url, headers={"Authorization": f"Bearer {access_token}"})
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gmail API HTTP {exc.code}: {body}") from exc


def header_value(message: dict, name: str) -> str:
    for header in message.get("payload", {}).get("headers", []):
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
        text = extract_text(part)
        if text:
            texts.append(text)
    if texts:
        return "\n".join(texts)
    if payload.get("mimeType") == "text/html":
        return re.sub(r"<[^>]+>", " ", decode_body_part(payload))
    return ""


def main() -> int:
    query = sys.argv[1] if len(sys.argv) > 1 else "newer_than:2d -from:me"
    max_results = sys.argv[2] if len(sys.argv) > 2 else "30"
    access_token = refresh_access_token()
    url = "https://gmail.googleapis.com/gmail/v1/users/me/messages?" + parse.urlencode(
        {"q": query, "maxResults": max_results}
    )
    result = gmail_get(access_token, url)
    messages = result.get("messages", [])
    print(f"Query: {query}")
    print(f"Found: {len(messages)} message(s)")
    for item in messages:
        msg = gmail_get(
            access_token,
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{item['id']}?format=full",
        )
        labels = ",".join(msg.get("labelIds", []))
        text = re.sub(r"\s+", " ", extract_text(msg.get("payload", {}))).strip()
        print("\n---")
        print(f"id: {msg.get('id', '')}")
        print(f"thread: {msg.get('threadId', '')}")
        print(f"labels: {labels}")
        print(f"date: {header_value(msg, 'Date')}")
        print(f"from: {header_value(msg, 'From')}")
        print(f"to: {header_value(msg, 'To')}")
        print(f"subject: {header_value(msg, 'Subject')}")
        print(f"snippet: {msg.get('snippet', '')}")
        if text:
            print(f"preview: {text[:900]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
