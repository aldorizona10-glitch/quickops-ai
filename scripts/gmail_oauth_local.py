#!/usr/bin/env python3
import json
import secrets
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib import parse, request, error


ROOT = Path(__file__).resolve().parents[1]
CREDENTIALS_FILE = ROOT / "credentials.json"
TOKEN_FILE = ROOT / "token.json"
SCOPE = "https://www.googleapis.com/auth/gmail.send"


class OAuthHandler(BaseHTTPRequestHandler):
    server_version = "QuickOpsOAuth/1.0"

    def do_GET(self):
        parsed = parse.urlparse(self.path)
        params = parse.parse_qs(parsed.query)
        self.server.oauth_params = params
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<html><body><h1>QuickOps AI authorized.</h1>"
            b"<p>You can close this browser tab and return to the terminal.</p>"
            b"</body></html>"
        )

    def log_message(self, fmt, *args):
        return


def load_client() -> dict:
    if not CREDENTIALS_FILE.exists():
        raise RuntimeError(f"Missing {CREDENTIALS_FILE}")
    data = json.loads(CREDENTIALS_FILE.read_text(encoding="utf-8"))
    client = data.get("installed") or data.get("web")
    if not client:
        raise RuntimeError("credentials.json must contain an installed or web OAuth client")
    return client


def exchange_code(client: dict, code: str, redirect_uri: str) -> dict:
    payload = parse.urlencode(
        {
            "code": code,
            "client_id": client["client_id"],
            "client_secret": client["client_secret"],
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
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
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Token exchange failed HTTP {exc.code}: {body}") from exc


def main() -> int:
    client = load_client()
    server = HTTPServer(("127.0.0.1", 0), OAuthHandler)
    server.oauth_params = {}
    port = server.server_address[1]
    redirect_uri = f"http://127.0.0.1:{port}/"
    state = secrets.token_urlsafe(24)

    auth_url = client["auth_uri"] + "?" + parse.urlencode(
        {
            "client_id": client["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": SCOPE,
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
        }
    )

    thread = threading.Thread(target=server.handle_request, daemon=True)
    thread.start()

    print("Open this URL in your browser and approve Gmail send access:")
    print(auth_url)
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    deadline = time.time() + 180
    while time.time() < deadline and not server.oauth_params:
        time.sleep(0.25)

    if not server.oauth_params:
        raise RuntimeError("Timed out waiting for OAuth callback")

    params = server.oauth_params
    if params.get("state", [""])[0] != state:
        raise RuntimeError("OAuth state mismatch")
    if "error" in params:
        raise RuntimeError("OAuth error: " + params["error"][0])
    code = params.get("code", [""])[0]
    if not code:
        raise RuntimeError("OAuth callback did not include code")

    token = exchange_code(client, code, redirect_uri)
    token["created_at"] = int(time.time())
    token["scope"] = SCOPE
    TOKEN_FILE.write_text(json.dumps(token, indent=2), encoding="utf-8")
    print(f"Saved token to {TOKEN_FILE}")
    print("Now run: python3 scripts/gmail_api_send_queue.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
