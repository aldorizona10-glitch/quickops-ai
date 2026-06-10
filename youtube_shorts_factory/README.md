# YouTube Shorts Factory

Built: 2026-06-10 12:09 WIB.

Goal: create original Shorts without paid tools, then convert attention into QuickOps AI leads. YouTube ad monetization is a long path; client conversion is the faster money path.

## Channel Position

Channel name idea: QuickOps AI Lab

Promise: short practical breakdowns of AI workflow mistakes, security risks, and small automation fixes for founders and operators.

CTA:

- AI security micro-audit: https://aldorizona10-glitch.github.io/quickops-ai/security-audit/
- Operations workflow pilot: https://aldorizona10-glitch.github.io/quickops-ai/

## No-Cost Workflow

Native MP4 render:

```bash
python3 scripts/render_youtube_shorts.py
```

Rendered videos are written to `youtube_shorts_factory/rendered/`.

YouTube upload automation:

1. In Google Cloud, enable YouTube Data API v3 on the same project as `credentials.json`.
2. Run `python3 scripts/youtube_oauth_local.py` once and approve YouTube upload access.
3. Upload one Short privately:

```bash
python3 scripts/upload_youtube_short.py short_001
```

4. Upload public only when intentionally confirmed:

```bash
YOUTUBE_PRIVACY_STATUS=public CONFIRM_PUBLIC_YOUTUBE_UPLOAD=I_UNDERSTAND_PUBLIC_UPLOAD python3 scripts/upload_youtube_short.py short_001
```

Browser recorder fallback:

1. Open `shorts_recorder.html` in Chrome or Edge.
2. Pick a Short from the dropdown.
3. Click `Record WebM`.
4. When recording finishes, download the `.webm`.
5. Upload as YouTube Short.
6. Use title/description from `shorts_metadata.csv`.

## Monetization Reality

YouTube ads require channel eligibility and original content. This factory avoids reused footage and low-effort AI compilation. Every Short uses original text, original motion graphics, and a clear educational angle.

Direct revenue path:

- 1 Short per day for credibility.
- 10 targeted outreach emails per day for direct sales.
- Pin/comment CTA: "I do fixed-scope AI workflow/security audits for USD 100. Link in description."
