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


def load_client() -> dict:
    if not CREDENTIALS_FILE.exists():
        raise RuntimeError("Missing credentials.json. Run scripts/gmail_oauth_local.py first.")
    data = json.loads(CREDENTIALS_FILE.read_text(encoding="utf-8"))
    client = data.get("installed") or data.get("web")
    if not client:
        raise RuntimeError("credentials.json must contain installed or web OAuth client")
    return client


def refresh_access_token() -> str:
    if not TOKEN_FILE.exists():
        raise RuntimeError("Missing token.json. Run scripts/gmail_oauth_local.py first.")
    token = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise RuntimeError("token.json has no refresh_token. Re-run scripts/gmail_oauth_local.py")
    client = load_client()
    payload = parse.urlencode(
        {
            "client_id": client["client_id"],
            "client_secret": client["client_secret"],
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
    ).encode("utf-8")
    req = request.Request(
        client["token_uri"],
        data=payload,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            update = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Token refresh failed HTTP {exc.code}: {body}") from exc
    token.update(update)
    token["created_at"] = int(time.time())
    TOKEN_FILE.write_text(json.dumps(token, indent=2), encoding="utf-8")
    return token["access_token"]


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

    for path in queue_files:
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
