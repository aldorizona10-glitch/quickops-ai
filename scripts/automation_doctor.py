#!/usr/bin/env python3
import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def count_glob(pattern: str) -> int:
    return len(list(ROOT.glob(pattern)))


def count_csv_rows(path: str) -> int:
    file = ROOT / path
    if not file.exists():
        return 0
    with file.open(newline="", encoding="utf-8") as f:
        return max(0, sum(1 for _ in csv.reader(f)) - 1)


def uploaded_ids(path: str) -> list[str]:
    file = ROOT / path
    if not file.exists():
        return []
    ids = []
    with file.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            video_id = (row.get("video_id") or "").strip()
            if video_id:
                ids.append(video_id)
    return ids


def deleted_ids(path: str) -> set[str]:
    file = ROOT / path
    if not file.exists():
        return set()
    ids = set()
    with file.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            video_id = (row.get("video_id") or "").strip()
            if video_id:
                ids.add(video_id)
    return ids


def status_line(name: str, ok: bool, detail: str = "") -> None:
    mark = "OK" if ok else "MISSING"
    suffix = f" - {detail}" if detail else ""
    print(f"{mark:8} {name}{suffix}")


def main() -> int:
    print("QuickOps Full Automation Doctor")
    print("===============================")
    print()
    print("Native editing/render tools")
    print("---------------------------")
    status_line("ffmpeg", bool(shutil.which("ffmpeg") or exists(".local-tools/ffmpeg/ffmpeg")), shutil.which("ffmpeg") or ".local-tools fallback")
    status_line("ffprobe", bool(shutil.which("ffprobe") or exists(".local-tools/ffmpeg/ffprobe")), shutil.which("ffprobe") or ".local-tools fallback")
    status_line("global trend rendered videos", count_glob("trend_shorts_factory/rendered_global/*.mp4") > 0, f"{count_glob('trend_shorts_factory/rendered_global/*.mp4')} files")
    status_line("agency Shorts rendered videos", count_glob("youtube_shorts_factory/rendered/*.mp4") > 0, f"{count_glob('youtube_shorts_factory/rendered/*.mp4')} files")
    status_line("trend audio cache", count_glob("trend_shorts_factory/audio_global/*.mp3") > 0, f"{count_glob('trend_shorts_factory/audio_global/*.mp3')} files")
    print()

    print("Account/API connections")
    print("-----------------------")
    status_line("YouTube OAuth token", exists("youtube_token.json"), "upload/delete scope required for cleanup")
    status_line("Gmail OAuth token", exists("token.json"), "Gmail API send/read")
    status_line("Google OAuth client credentials", exists("credentials.json"), "local only, gitignored")
    print()

    print("YouTube automation")
    print("------------------")
    old_uploads = uploaded_ids("logs/youtube_trend_upload_log.csv")
    deleted = deleted_ids("logs/youtube_deleted_log.csv")
    active_old_uploads = [video_id for video_id in old_uploads if video_id not in deleted]
    global_uploads = uploaded_ids("logs/youtube_global_geo_upload_log.csv")
    status_line("old uploaded trend videos", len(active_old_uploads) == 0, f"{len(active_old_uploads)} active old video ids, {len(deleted)} deleted ids logged")
    status_line("global uploaded videos", len(global_uploads) > 0, f"{len(global_uploads)} global video ids logged")
    status_line("global metadata", exists("trend_shorts_factory/global_geo_metadata.csv"), f"{count_csv_rows('trend_shorts_factory/global_geo_metadata.csv')} rows")
    status_line("global strategy doc", exists("docs/youtube_global_geo_strategy_2026.md"))
    print()

    print("Outreach and revenue ops")
    print("------------------------")
    status_line("email queue", count_glob("email_queue/*.eml") > 0, f"{count_glob('email_queue/*.eml')} queued")
    status_line("Gmail sent log", exists("logs/gmail_api_sent_log.csv"), f"{count_csv_rows('logs/gmail_api_sent_log.csv')} rows")
    status_line("reply log", exists("logs/replies.jsonl"))
    status_line("lead tracker", exists("lead_tracker.csv"), f"{count_csv_rows('lead_tracker.csv')} rows")
    status_line("daily tracker", exists("daily_action_tracker.csv"), f"{count_csv_rows('daily_action_tracker.csv')} rows")
    print()

    print("Bug bounty desk")
    print("---------------")
    status_line("targets CSV", exists("bug_bounty_targets_2026.csv"), f"{count_csv_rows('bug_bounty_targets_2026.csv')} rows")
    status_line("case folders", count_glob("bug_bounty_cases/*") > 0, f"{count_glob('bug_bounty_cases/*')} folders")
    status_line("findings folders", count_glob("bug_bounty_findings/*") > 0, f"{count_glob('bug_bounty_findings/*')} folders")
    print()

    print("Next actions")
    print("------------")
    if active_old_uploads:
        print("1. Delete old private uploads:")
        print("   CONFIRM_DELETE_YOUTUBE_VIDEOS=I_UNDERSTAND_DELETE_YOUTUBE_VIDEOS python3 scripts/delete_uploaded_youtube_videos.py all")
    if not global_uploads:
        print("2. Upload global Shorts when YouTube account limit resets:")
        print("   TREND_RENDERED_DIR=trend_shorts_factory/rendered_global TREND_METADATA=trend_shorts_factory/global_geo_metadata.csv TREND_UPLOAD_LOG=logs/youtube_global_geo_upload_log.csv python3 scripts/upload_trend_short.py all")
    print("3. Run status anytime:")
    print("   python3 scripts/automation_doctor.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
