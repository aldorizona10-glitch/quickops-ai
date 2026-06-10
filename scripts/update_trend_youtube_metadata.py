#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path
from urllib import error, parse, request

from youtube_auth import refresh_access_token
from upload_trend_short import build_youtube_metadata, format_youtube_error


ROOT = Path(__file__).resolve().parents[1]
FACTORY = ROOT / "trend_shorts_factory"
METADATA = FACTORY / "trend_metadata.csv"
UPLOAD_LOG = ROOT / "logs" / "youtube_trend_upload_log.csv"


def load_metadata() -> dict[str, dict[str, str]]:
    with METADATA.open(newline="", encoding="utf-8") as f:
        return {row["id"]: row for row in csv.DictReader(f)}


def load_uploaded() -> dict[str, str]:
    uploaded = {}
    if not UPLOAD_LOG.exists():
        return uploaded
    with UPLOAD_LOG.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("short_id") and row.get("video_id"):
                uploaded[row["short_id"]] = row["video_id"]
    return uploaded


def update_video(access_token: str, video_id: str, row: dict[str, str], privacy: str) -> None:
    url = "https://www.googleapis.com/youtube/v3/videos?" + parse.urlencode({"part": "snippet,status"})
    body = build_youtube_metadata(row, privacy)
    body["id"] = video_id
    req = request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        method="PUT",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(format_youtube_error("metadata update", exc.code, body)) from exc


def main() -> int:
    privacy = "private"
    metadata = load_metadata()
    uploaded = load_uploaded()
    selected = list(metadata) if len(sys.argv) < 2 or sys.argv[1] == "all" else [sys.argv[1]]
    access_token = refresh_access_token()
    for trend_id in selected:
        video_id = uploaded.get(trend_id)
        if not video_id:
            print(f"SKIP: {trend_id} has no uploaded video id")
            continue
        update_video(access_token, video_id, metadata[trend_id], privacy)
        print(f"UPDATED: {trend_id} -> https://www.youtube.com/watch?v={video_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
