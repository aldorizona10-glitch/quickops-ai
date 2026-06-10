#!/usr/bin/env python3
import csv
import json
import mimetypes
import os
import sys
from pathlib import Path
from urllib import error, parse, request

from youtube_auth import refresh_access_token


ROOT = Path(__file__).resolve().parents[1]
FACTORY = ROOT / "trend_shorts_factory"
RENDERED = Path(os.environ.get("TREND_RENDERED_DIR", FACTORY / "rendered"))
METADATA = Path(os.environ.get("TREND_METADATA", FACTORY / "trend_metadata.csv"))
LOG_DIR = ROOT / "logs"
UPLOAD_LOG = Path(os.environ.get("TREND_UPLOAD_LOG", LOG_DIR / "youtube_trend_upload_log.csv"))


class YouTubeApiError(RuntimeError):
    pass


def format_youtube_error(stage: str, code: int, body: str) -> str:
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return f"YouTube {stage} failed HTTP {code}: {body}"

    err = data.get("error", {})
    message = err.get("message", body)
    reason = err.get("status", "")
    activation_url = ""
    for item in err.get("details", []):
        if item.get("@type", "").endswith("google.rpc.ErrorInfo"):
            reason = item.get("reason", reason)
            activation_url = item.get("metadata", {}).get("activationUrl", activation_url)
    lines = [f"YouTube {stage} failed HTTP {code}: {reason or 'API_ERROR'}", message]
    if activation_url:
        lines.extend(["", f"Enable API here: {activation_url}"])
    return "\n".join(lines)


def load_metadata() -> dict[str, dict[str, str]]:
    with METADATA.open(newline="", encoding="utf-8") as f:
        return {row["id"]: row for row in csv.DictReader(f)}


def already_uploaded() -> set[str]:
    if not UPLOAD_LOG.exists():
        return set()
    uploaded = set()
    for line in UPLOAD_LOG.read_text(encoding="utf-8").splitlines()[1:]:
        parts = line.split(",")
        if len(parts) >= 4 and parts[3]:
            uploaded.add(parts[0])
    return uploaded


def append_log(short_id: str, path: Path, title: str, video_id: str, privacy: str) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    if not UPLOAD_LOG.exists():
        UPLOAD_LOG.write_text("short_id,file,title,video_id,privacy\n", encoding="utf-8")
    row = [short_id, path.name, title.replace(",", " "), video_id, privacy]
    with UPLOAD_LOG.open("a", encoding="utf-8") as f:
        f.write(",".join(row) + "\n")


def start_resumable_upload(access_token: str, metadata: dict, file_size: int, mime: str) -> str:
    url = "https://www.googleapis.com/upload/youtube/v3/videos?" + parse.urlencode(
        {"uploadType": "resumable", "part": "snippet,status"}
    )
    req = request.Request(
        url,
        data=json.dumps(metadata).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Length": str(file_size),
            "X-Upload-Content-Type": mime,
        },
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            location = resp.headers.get("Location")
            if not location:
                raise RuntimeError("YouTube did not return resumable upload URL")
            return location
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise YouTubeApiError(format_youtube_error("upload init", exc.code, body)) from exc


def upload_file(access_token: str, upload_url: str, path: Path, mime: str) -> dict:
    data = path.read_bytes()
    req = request.Request(
        upload_url,
        data=data,
        method="PUT",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": mime,
            "Content-Length": str(len(data)),
        },
    )
    try:
        with request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise YouTubeApiError(format_youtube_error("upload", exc.code, body)) from exc


def build_youtube_metadata(row: dict[str, str], privacy: str) -> dict:
    description = "\n\n".join(
        [
            row["description"],
            row["hashtags"],
            "Trend explainer generated with a local zero-budget Shorts pipeline.",
            "Contact: aldorizona10@gmail.com",
        ]
    )
    tags = [tag.strip("#") for tag in row["hashtags"].split() if tag.startswith("#")]
    return {
        "snippet": {
            "title": row["title"],
            "description": description,
            "tags": tags,
            "categoryId": "28",
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/upload_trend_short.py <trend_id|all>", file=sys.stderr)
        return 2
    privacy = os.environ.get("YOUTUBE_PRIVACY_STATUS", "private").strip().lower()
    if privacy not in {"private", "unlisted", "public"}:
        raise RuntimeError("YOUTUBE_PRIVACY_STATUS must be private, unlisted, or public")
    if privacy == "public" and os.environ.get("CONFIRM_PUBLIC_YOUTUBE_UPLOAD") != "I_UNDERSTAND_PUBLIC_UPLOAD":
        raise RuntimeError("Set CONFIRM_PUBLIC_YOUTUBE_UPLOAD=I_UNDERSTAND_PUBLIC_UPLOAD to upload public videos")

    metadata = load_metadata()
    selected = list(metadata) if sys.argv[1] == "all" else [sys.argv[1]]
    uploaded = already_uploaded()
    access_token = refresh_access_token()

    for trend_id in selected:
        if trend_id not in metadata:
            raise RuntimeError(f"Unknown trend id: {trend_id}")
        if trend_id in uploaded:
            print(f"SKIP: {trend_id} already uploaded")
            continue
        path = RENDERED / f"{trend_id}-viral-trend.mp4"
        if not path.exists():
            raise RuntimeError(f"Missing rendered video: {path}. Run scripts/render_trend_shorts.py first.")
        mime = mimetypes.guess_type(path.name)[0] or "video/mp4"
        yt_metadata = build_youtube_metadata(metadata[trend_id], privacy)
        print(f"UPLOADING: {trend_id} -> {metadata[trend_id]['title']} ({privacy})", flush=True)
        upload_url = start_resumable_upload(access_token, yt_metadata, path.stat().st_size, mime)
        result = upload_file(access_token, upload_url, path, mime)
        video_id = result.get("id", "")
        append_log(trend_id, path, metadata[trend_id]["title"], video_id, privacy)
        print(f"UPLOADED: https://www.youtube.com/watch?v={video_id}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except YouTubeApiError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
