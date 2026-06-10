#!/usr/bin/env python3
import csv
import json
import os
import sys
from pathlib import Path
from urllib import error, parse, request

from youtube_auth import refresh_access_token


ROOT = Path(__file__).resolve().parents[1]
LOG = Path(os.environ.get("YOUTUBE_DELETE_LOG", ROOT / "logs" / "youtube_trend_upload_log.csv"))
CONFIRM = "I_UNDERSTAND_DELETE_YOUTUBE_VIDEOS"


class YouTubeApiError(RuntimeError):
    pass


def format_youtube_error(code: int, body: str) -> str:
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return f"YouTube delete failed HTTP {code}: {body}"
    err = data.get("error", {})
    return f"YouTube delete failed HTTP {code}: {err.get('status', 'API_ERROR')}\n{err.get('message', body)}"


def load_video_ids() -> list[tuple[str, str, str]]:
    if not LOG.exists():
        raise RuntimeError(f"Missing upload log: {LOG}")
    rows = []
    with LOG.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            video_id = (row.get("video_id") or "").strip()
            if video_id:
                rows.append((row.get("short_id", ""), video_id, row.get("title", "")))
    return rows


def delete_video(access_token: str, video_id: str) -> None:
    url = "https://www.googleapis.com/youtube/v3/videos?" + parse.urlencode({"id": video_id})
    req = request.Request(
        url,
        method="DELETE",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            if resp.status != 204:
                raise YouTubeApiError(f"YouTube delete returned HTTP {resp.status} for {video_id}")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise YouTubeApiError(format_youtube_error(exc.code, body)) from exc


def main() -> int:
    if os.environ.get("CONFIRM_DELETE_YOUTUBE_VIDEOS") != CONFIRM:
        raise RuntimeError(f"Set CONFIRM_DELETE_YOUTUBE_VIDEOS={CONFIRM} to delete YouTube videos.")

    rows = load_video_ids()
    if len(sys.argv) > 1 and sys.argv[1] != "all":
        selected = set(sys.argv[1:])
        rows = [row for row in rows if row[0] in selected or row[1] in selected]
    if not rows:
        print("No matching uploaded videos found.")
        return 0

    access_token = refresh_access_token()
    for short_id, video_id, title in rows:
        print(f"DELETING: {short_id} {video_id} {title}", flush=True)
        delete_video(access_token, video_id)
        print(f"DELETED: {video_id}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except YouTubeApiError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
