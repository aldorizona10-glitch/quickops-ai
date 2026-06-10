# Full Automation Tool Audit

Date: 2026-06-10

This repo already has the core zero-budget automation stack. The realistic goal is not magic income; it is a repeatable system that produces assets, sends safe outreach, tracks replies, and measures what happened.

## Current Automation Map

| Area | Current files | Status | Gap |
| --- | --- | --- | --- |
| Video editing/render | `scripts/render_trend_shorts.py`, `scripts/render_youtube_shorts.py` | Working with FFmpeg, ASS subtitles, TTS, vertical MP4 | Need better visual variety and optional local TTS fallback |
| Global trend Shorts | `trend_shorts_factory/global_geo_manifest.json`, `global_geo_metadata.csv` | 4 rendered videos ready locally | YouTube account upload limit blocks new upload |
| YouTube upload/delete | `scripts/upload_trend_short.py`, `scripts/delete_uploaded_youtube_videos.py` | OAuth upload/delete supported | Delete old uploads first; upload again after limit reset |
| Gmail outreach | `scripts/gmail_api_send_queue.py`, `scripts/gmail_check_replies.py` | OAuth/API path exists | Keep allowlist strict; avoid bulk spam |
| Agency sales ops | `lead_tracker.csv`, `daily_action_tracker.csv`, `email_queue/` | Working queue/tracker | Needs daily prospect refresh |
| Bug bounty desk | `bug_bounty_*`, `scripts/bug_bounty_research_run.py` | Safe scope snapshot workflow | Needs manual validation before any report |
| Website | `landing/`, `security-audit/`, `youtube/` | GitHub Pages-ready | Needs periodic copy/design refresh |
| Status/checks | `scripts/autopilot_status.py`, `scripts/automation_doctor.py` | Local status coverage | Scheduler can run it periodically |

## Free Tools Already Used

- FFmpeg / FFprobe: native video/audio rendering, compositing, subtitles, codec validation.
- ASS subtitles: professional text layout without paid editors.
- gTTS: free cloud TTS for English narration.
- Google OAuth + YouTube Data API: official upload/delete path.
- Gmail API: safer sending/checking than browser cookies.
- GitHub Pages: free hosting for landing pages.
- CSV/Markdown: simple local CRM, trackers, content manifests, and logs.

## Recommended Free Additions

These are optional and should only be added when needed:

- `yt-dlp`: download your own public videos or permitted source media for clipping; do not use copyrighted third-party clips without rights.
- `ImageMagick`: thumbnail/card generation and image overlays.
- `espeak-ng` or Piper TTS: local TTS fallback when gTTS/network fails.
- `Aegisub`: manual subtitle polish if a video needs human QA.
- `OBS Studio`: manual screen demos and handoff videos.
- Remotion: programmatic React video if the current FFmpeg layouts become too limiting.
- MoviePy: Python video composition when FFmpeg filtergraphs become hard to maintain.

## Operating Rules

1. Upload private first.
2. Do not reuse leaked cookies or passwords.
3. Do not mass-send email outside the allowlist.
4. Do not promise guaranteed revenue.
5. For YouTube, judge by retention and geography after public tests.
6. For bug bounty, only test in authorized scope and your own accounts.

## Commands

Status:

```bash
python3 scripts/automation_doctor.py
```

Delete old YouTube uploads from the trend upload log:

```bash
CONFIRM_DELETE_YOUTUBE_VIDEOS=I_UNDERSTAND_DELETE_YOUTUBE_VIDEOS \
python3 scripts/delete_uploaded_youtube_videos.py all
```

Upload global videos after the YouTube limit resets:

```bash
TREND_RENDERED_DIR=trend_shorts_factory/rendered_global \
TREND_METADATA=trend_shorts_factory/global_geo_metadata.csv \
TREND_UPLOAD_LOG=logs/youtube_global_geo_upload_log.csv \
python3 scripts/upload_trend_short.py all
```

Render global videos again:

```bash
TREND_MANIFEST=trend_shorts_factory/global_geo_manifest.json \
TREND_RENDERED_DIR=trend_shorts_factory/rendered_global \
TREND_RENDER_WORK_DIR=trend_shorts_factory/.render_work_global \
TREND_AUDIO_DIR=trend_shorts_factory/audio_global \
python3 scripts/render_trend_shorts.py
```
