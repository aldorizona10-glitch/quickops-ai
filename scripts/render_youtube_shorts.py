#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FACTORY = ROOT / "youtube_shorts_factory"
MANIFEST = FACTORY / "content_manifest.json"
OUT = FACTORY / "rendered"
WORK = FACTORY / ".render_work"
LOCAL_FFMPEG = ROOT / ".local-tools" / "ffmpeg" / "ffmpeg"


def ffmpeg_bin() -> str:
    if LOCAL_FFMPEG.exists():
        return str(LOCAL_FFMPEG)
    found = shutil.which("ffmpeg")
    if found:
        return found
    raise SystemExit("ffmpeg not found. Expected .local-tools/ffmpeg/ffmpeg or ffmpeg on PATH.")


def ass_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace("\n", "\\N")


def ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def write_ass(item: dict) -> Path:
    WORK.mkdir(parents=True, exist_ok=True)
    path = WORK / f"{item['id']}.ass"
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "WrapStyle: 0",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Brand,DejaVu Sans,42,&H00D7E4F7,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,1,0,7,74,74,78,1",
        "Style: Hook,DejaVu Sans,78,&H00FFFFFF,&H000000FF,&H00212A38,&H80000000,1,0,0,0,100,100,0,0,1,4,0,7,74,74,250,1",
        "Style: Beat,DejaVu Sans,76,&H00F7F9FC,&H000000FF,&H00101824,&H90000000,1,0,0,0,100,100,0,0,1,4,0,5,100,100,0,1",
        "Style: Step,DejaVu Sans,44,&H0020D6A0,&H000000FF,&H00101824,&H90000000,1,0,0,0,100,100,0,0,1,2,0,7,110,110,882,1",
        "Style: CTA,DejaVu Sans,58,&H00FFFFFF,&H000000FF,&H00204988,&H90000000,1,0,0,0,100,100,0,0,1,3,0,5,110,110,0,1",
        "Style: URL,DejaVu Sans,30,&H00C6D0E1,&H000000FF,&H00101824,&H80000000,1,0,0,0,100,100,0,0,1,1,0,2,60,60,78,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 0,{ass_time(0)},{ass_time(15)},Brand,,0,0,0,,QUICKOPS AI LAB",
        f"Dialogue: 0,{ass_time(0.35)},{ass_time(4.2)},Hook,,0,0,0,,{ass_escape(item['hook'])}",
        f"Dialogue: 0,{ass_time(0)},{ass_time(15)},URL,,0,0,0,,aldorizona10-glitch.github.io/quickops-ai",
    ]
    start = 4.0
    for idx, beat in enumerate(item["beats"], start=1):
        s = start + (idx - 1) * 1.9
        e = min(s + 2.15, 13.4)
        lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Step,,0,0,0,,STEP {idx}")
        lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Beat,,0,0,0,,{ass_escape(beat)}")
    lines.append(f"Dialogue: 0,{ass_time(13.1)},{ass_time(15)},CTA,,0,0,0,,{ass_escape(item['cta'])}\\Nlink in description")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def render(item: dict, ffmpeg: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    ass = write_ass(item)
    out = OUT / f"{item['id']}-quickops-ai.mp4"
    vf = ",".join(
        [
            "format=yuv420p",
            "drawbox=x=58:y=848:w=964:h=390:color=white@0.08:t=fill",
            "drawbox=x=58:y=848:w=964:h=390:color=white@0.18:t=3",
            "drawbox=x=58:y=1450:w=964:h=260:color=0x204988@0.42:t=fill",
            "drawbox=x=70:y=1325:w=940:h=18:color=white@0.14:t=fill",
            "drawbox=x=70:y=1325:w=940:h=18:color=0x4f8cff@0.9:t=fill:enable='between(t,0,15)'",
            f"subtitles={ass.as_posix()}",
        ]
    )
    cmd = [
        ffmpeg,
        "-y",
        "-f",
        "lavfi",
        "-i",
        "color=c=0x090d14:s=1080x1920:d=15:r=30",
        "-f",
        "lavfi",
        "-i",
        "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-vf",
        vf,
        "-shortest",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "23",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(out),
    ]
    subprocess.run(cmd, check=True)
    return out


def main() -> int:
    ffmpeg = ffmpeg_bin()
    items = json.loads(MANIFEST.read_text(encoding="utf-8"))
    selected = set(sys.argv[1:])
    rendered = []
    for item in items:
        if selected and item["id"] not in selected:
            continue
        print(f"Rendering {item['id']}...")
        rendered.append(render(item, ffmpeg))
    print("Rendered:")
    for path in rendered:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
