#!/usr/bin/env python3
import base64
import email
import json
import os
import sys
import time
from email.message import EmailMessage
from pathlib import Path
from urllib import parse, request, error

from gmail_auth import refresh_access_token


ROOT = Path(__file__).resolve().parents[1]
QUEUE_DIR = ROOT / "email_queue"
LOG_DIR = ROOT / "logs"
SENT_LOG = LOG_DIR / "gmail_api_sent_log.csv"
TOKEN_FILE = ROOT / "token.json"
CREDENTIALS_FILE = ROOT / "credentials.json"

ALLOWED_RECIPIENTS = {
    "jobs@goshopbrands.com",
    "steve@pango.ai",
    "careers@babou.ai",
    "info@readifinancial.com",
    "recruiting@starbridge.ai",
    "hiring@reef.pl",
    "cprabala@techmahindra.com",
    "jobs@thisdot.co",
    "steven@kanary.com",
    "eddie.hammond@kepler.ai",
    "jobs@drswarm.com",
    "talent+hn@cwai.co",
    "careers@coder.com",
    "sagar@speakeasy.com",
    "jobs@kinelo.com",
    "hiring@hotwash.com",
}


def read_eml(path: Path) -> EmailMessage:
    raw = path.read_text(encoding="utf-8")
    msg = email.message_from_string(raw)
    out = EmailMessage()
    out["From"] = msg.get("From", "")
    out["To"] = msg.get("To", "")
    out["Subject"] = msg.get("Subject", "")
    payload = msg.get_payload()
    if isinstance(payload, list):
        body = "\n".join(str(part.get_payload(decode=False)) for part in payload)
    else:
        body = str(payload or "")
    out.set_content(body)
    return out


def recipients_for(msg: EmailMessage) -> list[str]:
    return [r.strip().lower() for r in msg.get("To", "").split(",") if r.strip()]


def validate_message(path: Path, msg: EmailMessage) -> None:
    recipients = recipients_for(msg)
    if not recipients:
        raise ValueError(f"{path.name}: missing To recipient")
    disallowed = [r for r in recipients if r not in ALLOWED_RECIPIENTS]
    if disallowed:
        raise ValueError(f"{path.name}: recipient not allowlisted: {', '.join(disallowed)}")
    if not msg.get("Subject"):
        raise ValueError(f"{path.name}: missing subject")
    body = msg.get_body(preferencelist=("plain",))
    if body is None or len(body.get_content().strip()) < 100:
        raise ValueError(f"{path.name}: body too short")


def gmail_raw(msg: EmailMessage) -> str:
    encoded = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    return encoded.rstrip("=")


def gmail_send(access_token: str, msg: EmailMessage) -> dict:
    payload = json.dumps({"raw": gmail_raw(msg)}).encode("utf-8")
    req = request.Request(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gmail API HTTP {exc.code}: {body}") from exc


def log_result(path: Path, msg: EmailMessage, mode: str, result_id: str = "") -> None:
    LOG_DIR.mkdir(exist_ok=True)
    if not SENT_LOG.exists():
        SENT_LOG.write_text("timestamp,file,to,subject,mode,gmail_id\n", encoding="utf-8")
    row = [
        str(int(time.time())),
        path.name.replace(",", " "),
        msg.get("To", "").replace(",", " "),
        msg.get("Subject", "").replace(",", " "),
        mode,
        result_id,
    ]
    with SENT_LOG.open("a", encoding="utf-8") as f:
        f.write(",".join(row) + "\n")


def sent_files() -> set[str]:
    if not SENT_LOG.exists():
        return set()
    sent = set()
    for line in SENT_LOG.read_text(encoding="utf-8").splitlines()[1:]:
        parts = line.split(",")
        if len(parts) >= 5 and parts[4] == "sent":
            sent.add(parts[1])
    return sent


def main() -> int:
    queue_files = sorted(QUEUE_DIR.glob("*.eml"))
    if not queue_files:
        print("No .eml files found in email_queue/")
        return 1

    live_send = os.environ.get("CONFIRM_SEND_QUICKOPS") == "I_UNDERSTAND_SEND_REAL_EMAIL"
    access_token = os.environ.get("GMAIL_ACCESS_TOKEN", "").strip()
    if live_send and not access_token:
        access_token = refresh_access_token()

    print("LIVE GMAIL API SEND MODE" if live_send else "DRY RUN: no email will be sent")
    sent_count = 0
    already_sent = sent_files()

    for path in queue_files:
        if live_send and path.name in already_sent:
            print(f"SKIP: {path.name} already sent")
            continue
        msg = read_eml(path)
        try:
            validate_message(path, msg)
        except ValueError as exc:
            print(f"SKIP: {exc}")
            continue

        print(f"{'SENDING' if live_send else 'WOULD SEND'}: {path.name} -> {msg.get('To')} | {msg.get('Subject')}")
        gmail_id = ""
        if live_send:
            result = gmail_send(access_token, msg)
            gmail_id = result.get("id", "")
            time.sleep(8)
        log_result(path, msg, "sent" if live_send else "dry-run", gmail_id)
        sent_count += 1

    print(f"Processed {sent_count} message(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
