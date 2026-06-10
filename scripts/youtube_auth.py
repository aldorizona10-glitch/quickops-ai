import json
import time
from pathlib import Path
from urllib import parse, request, error


ROOT = Path(__file__).resolve().parents[1]
TOKEN_FILE = ROOT / "youtube_token.json"
CREDENTIALS_FILE = ROOT / "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def scope_string() -> str:
    return " ".join(SCOPES)


def load_client() -> dict:
    if not CREDENTIALS_FILE.exists():
        raise RuntimeError("Missing credentials.json. Create a Google OAuth Desktop client first.")
    data = json.loads(CREDENTIALS_FILE.read_text(encoding="utf-8"))
    client = data.get("installed") or data.get("web")
    if not client:
        raise RuntimeError("credentials.json must contain installed or web OAuth client")
    return client


def refresh_access_token() -> str:
    if not TOKEN_FILE.exists():
        raise RuntimeError("Missing youtube_token.json. Run scripts/youtube_oauth_local.py first.")
    token = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise RuntimeError("youtube_token.json has no refresh_token. Re-run scripts/youtube_oauth_local.py")
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
        raise RuntimeError(f"YouTube token refresh failed HTTP {exc.code}: {body}") from exc
    token.update(update)
    token["created_at"] = int(time.time())
    TOKEN_FILE.write_text(json.dumps(token, indent=2), encoding="utf-8")
    return token["access_token"]
