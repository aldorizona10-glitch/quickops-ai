#!/usr/bin/env python3
import email
import os
import smtplib
import ssl
import sys
import time
from email.message import EmailMessage
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE_DIR = ROOT / "email_queue"
LOG_DIR = ROOT / "logs"
SENT_LOG = LOG_DIR / "sent_email_log.csv"

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
        body = "\n".join(part.get_payload(decode=False) for part in payload)
    else:
        body = payload or ""
    out.set_content(body)
    return out


def recipients_for(msg: EmailMessage) -> list[str]:
    raw = msg.get("To", "")
    return [r.strip().lower() for r in raw.split(",") if r.strip()]


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


def smtp_config() -> dict[str, str]:
    required = ["SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD"]
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise RuntimeError("Missing env vars: " + ", ".join(missing))
    placeholders = {
        "SMTP_HOST": {"smtp.example.com", "example.com"},
        "SMTP_USER": {"your_sender@example.com", "your_email@example.com"},
        "SMTP_PASSWORD": {"your_smtp_or_app_password", "password", "app_password"},
    }
    for name, bad_values in placeholders.items():
        value = os.environ.get(name, "").strip()
        if value in bad_values or value.startswith("your_"):
            raise RuntimeError(f"{name} still contains a placeholder value")
    try:
        port = int(os.environ["SMTP_PORT"])
    except ValueError as exc:
        raise RuntimeError("SMTP_PORT must be a number") from exc
    if port not in {465, 587}:
        raise RuntimeError("SMTP_PORT must be 465 or 587")
    return {
        "host": os.environ["SMTP_HOST"],
        "port": str(port),
        "user": os.environ["SMTP_USER"],
        "password": os.environ["SMTP_PASSWORD"],
    }


def send_message(msg: EmailMessage, cfg: dict[str, str]) -> None:
    context = ssl.create_default_context()
    port = int(cfg["port"])
    if port == 465:
        with smtplib.SMTP_SSL(cfg["host"], port, context=context) as server:
            server.login(cfg["user"], cfg["password"])
            server.send_message(msg)
    else:
        with smtplib.SMTP(cfg["host"], port) as server:
            server.starttls(context=context)
            server.login(cfg["user"], cfg["password"])
            server.send_message(msg)


def log_sent(path: Path, msg: EmailMessage, dry_run: bool) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    if not SENT_LOG.exists():
        SENT_LOG.write_text("timestamp,file,to,subject,mode\n", encoding="utf-8")
    row = [
        str(int(time.time())),
        path.name.replace(",", " "),
        msg.get("To", "").replace(",", " "),
        msg.get("Subject", "").replace(",", " "),
        "dry-run" if dry_run else "sent",
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

    dry_run = os.environ.get("CONFIRM_SEND_QUICKOPS") != "I_UNDERSTAND_SEND_REAL_EMAIL"
    if dry_run:
        print("DRY RUN: no email will be sent.")
        print("To send real email, set CONFIRM_SEND_QUICKOPS=I_UNDERSTAND_SEND_REAL_EMAIL")
    else:
        print("LIVE SEND MODE: real emails will be sent to allowlisted recipients only.")

    cfg = None if dry_run else smtp_config()
    sent_count = 0
    already_sent = sent_files()

    for path in queue_files:
        if not dry_run and path.name in already_sent:
            print(f"SKIP: {path.name} already sent")
            continue
        msg = read_eml(path)
        try:
            validate_message(path, msg)
        except ValueError as exc:
            print(f"SKIP: {exc}")
            continue

        print(f"{'WOULD SEND' if dry_run else 'SENDING'}: {path.name} -> {msg.get('To')} | {msg.get('Subject')}")
        if not dry_run:
            send_message(msg, cfg)
            time.sleep(8)
        log_sent(path, msg, dry_run)
        sent_count += 1

    print(f"Processed {sent_count} message(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
