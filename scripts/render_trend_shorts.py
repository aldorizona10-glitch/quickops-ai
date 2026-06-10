#!/usr/bin/env python3
import json
import math
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FACTORY = ROOT / "trend_shorts_factory"
MANIFEST = FACTORY / "trend_manifest.json"
OUT = FACTORY / "rendered"
WORK = FACTORY / ".render_work"
AUDIO = FACTORY / "audio"
LOCAL_FFMPEG = ROOT / ".local-tools" / "ffmpeg" / "ffmpeg"
LOCAL_FFPROBE = ROOT / ".local-tools" / "ffmpeg" / "ffprobe"


def bin_for(name: str, local: Path) -> str:
    if local.exists():
        return str(local)
    found = shutil.which(name)
    if found:
        return found
    raise SystemExit(f"{name} not found")


def ffmpeg_bin() -> str:
    return bin_for("ffmpeg", LOCAL_FFMPEG)


def ffprobe_bin() -> str:
    return bin_for("ffprobe", LOCAL_FFPROBE)


def ass_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace("\n", "\\N")


def ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def wrap(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def ensure_voice(item: dict) -> Path:
    AUDIO.mkdir(parents=True, exist_ok=True)
    mp3 = AUDIO / f"{item['id']}.mp3"
    if mp3.exists():
        return mp3
    try:
        from gtts import gTTS
    except ImportError as exc:
        raise SystemExit("Missing gTTS. Run: python3 -m pip install --user --break-system-packages gTTS") from exc
    print(f"TTS: {item['id']}")
    tts = gTTS(item["voice"], lang="en", tld="com", slow=False)
    tts.save(str(mp3))
    return mp3


def duration(path: Path) -> float:
    cmd = [
        ffprobe_bin(),
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    out = subprocess.check_output(cmd, text=True).strip()
    return float(out)


def write_ass(item: dict, dur: float) -> Path:
    WORK.mkdir(parents=True, exist_ok=True)
    path = WORK / f"{item['id']}.ass"
    end = max(20, dur + 1.2)
    beat_count = len(item["beats"])
    beat_start = 5.0
    beat_span = max(2.6, (end - 9.0) / max(1, beat_count))
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "WrapStyle: 0",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Label,DejaVu Sans,36,&H00D8DEE9,&H000000FF,&H00100F0D,&H90000000,1,0,0,0,100,100,0,0,1,2,0,7,72,72,72,1",
        "Style: Title,DejaVu Sans,66,&H00FFFFFF,&H000000FF,&H00100F0D,&H90000000,1,0,0,0,100,100,0,0,1,4,0,7,82,82,168,1",
        "Style: Topic,DejaVu Sans,36,&H0000D6A3,&H000000FF,&H00100F0D,&H90000000,1,0,0,0,100,100,0,0,1,2,0,7,88,88,430,1",
        "Style: Beat,DejaVu Sans,64,&H00F7F3EA,&H000000FF,&H00100F0D,&H90000000,1,0,0,0,100,100,0,0,1,4,0,5,96,96,0,1",
        "Style: Source,DejaVu Sans,28,&H00C4CAD4,&H000000FF,&H00100F0D,&H90000000,0,0,0,0,100,100,0,0,1,1,0,2,70,70,88,1",
        "Style: CTA,DejaVu Sans,46,&H00FFFFFF,&H000000FF,&H001A533E,&H90000000,1,0,0,0,100,100,0,0,1,3,0,5,96,96,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 0,{ass_time(0)},{ass_time(end)},Label,,0,0,0,,TREND SIGNAL",
        f"Dialogue: 0,{ass_time(0.25)},{ass_time(end)},Title,,0,0,0,,{ass_escape(wrap(item['title'], 22))}",
        f"Dialogue: 0,{ass_time(0.4)},{ass_time(end)},Topic,,0,0,0,,{ass_escape(item['topic'].upper())}",
        f"Dialogue: 0,{ass_time(0)},{ass_time(end)},Source,,0,0,0,,Source: {ass_escape(item['source_url'])}",
    ]
    for idx, beat in enumerate(item["beats"]):
        s = beat_start + idx * beat_span
        e = min(s + beat_span + 0.8, end - 3.0)
        lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Beat,,0,0,0,,{ass_escape(wrap(beat, 18))}")
    lines.append(f"Dialogue: 0,{ass_time(max(0, end - 4.0))},{ass_time(end)},CTA,,0,0,0,,{ass_escape(wrap(item['cta'], 24))}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def render(item: dict) -> Path:
    ffmpeg = ffmpeg_bin()
    OUT.mkdir(parents=True, exist_ok=True)
    voice = ensure_voice(item)
    dur = duration(voice)
    total = min(max(dur + 1.0, 22), 58)
    ass = write_ass(item, total)
    out = OUT / f"{item['id']}-viral-trend.mp4"
    # Editorial motion background: layered blocks, progress line, subtle grid, no external assets.
    vf = ",".join(
        [
            "format=yuv420p",
            "drawbox=x=0:y=0:w=1080:h=1920:color=0x0a0b0f:t=fill",
            "drawgrid=width=90:height=90:thickness=1:color=0xffffff@0.035",
            "drawbox=x=54:y=64:w=972:h=1792:color=0xffffff@0.035:t=fill",
            "drawbox=x=54:y=64:w=972:h=1792:color=0xffffff@0.11:t=2",
            "drawbox=x=78:y=146:w=924:h=330:color=0x111827@0.70:t=fill",
            "drawbox=x=78:y=146:w=924:h=330:color=0x00d6a3@0.18:t=2",
            "drawbox=x=74:y=536:w=932:h=3:color=0x00d6a3@0.85:t=fill",
            "drawbox=x='74+mod(t*92,840)':y=536:w=92:h=3:color=0xffffff@0.90:t=fill",
            "drawbox=x=78:y=690:w=924:h=470:color=0x111827@0.88:t=fill",
            "drawbox=x=78:y=690:w=924:h=470:color=0x00d6a3@0.33:t=3",
            "drawbox=x=78:y=1376:w=924:h=214:color=0x1a533e@0.78:t=fill",
            "drawbox=x=78:y=1634:w='924*t/{:.3f}':h=16:color=0x00d6a3@0.92:t=fill".format(total),
            f"subtitles={ass.as_posix()}",
        ]
    )
    cmd = [
        ffmpeg,
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=0x0a0b0f:s=1080x1920:d={total:.3f}:r=30",
        "-i",
        str(voice),
        "-f",
        "lavfi",
        "-i",
        f"sine=frequency=92:duration={total:.3f}:sample_rate=44100",
        "-filter_complex",
        "[1:a]volume=1.35[a1];[2:a]volume=0.035,afade=t=in:st=0:d=1.2,afade=t=out:st={:.3f}:d=1.2[a2];[a1][a2]amix=inputs=2:duration=first:dropout_transition=0[a]".format(max(0, total - 1.2)),
        "-map",
        "0:v",
        "-map",
        "[a]",
        "-vf",
        vf,
        "-t",
        f"{total:.3f}",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "21",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        "-movflags",
        "+faststart",
        str(out),
    ]
    subprocess.run(cmd, check=True)
    return out


def main() -> int:
    items = json.loads(MANIFEST.read_text(encoding="utf-8"))
    selected = set(sys.argv[1:])
    rendered = []
    for item in items:
        if selected and item["id"] not in selected:
            continue
        print(f"Rendering {item['id']}: {item['title']}")
        rendered.append(render(item))
    print("Rendered trend videos:")
    for path in rendered:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
