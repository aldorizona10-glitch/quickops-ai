# Zero-to-100 Agency Kit

Tujuan: mendapatkan USD 100 pertama tanpa modal iklan, tanpa produk fisik, dan tanpa langganan berbayar di awal.

Model agensi: Micro AI Operations Agency untuk bisnis kecil.

Nama kerja: QuickOps AI

Live page:

- https://aldorizona10-glitch.github.io/quickops-ai/
- https://aldorizona10-glitch.github.io/quickops-ai/landing/
- https://aldorizona10-glitch.github.io/quickops-ai/security-audit/
- https://aldorizona10-glitch.github.io/quickops-ai/youtube/

## Full Automation Runner

Satu perintah utama:

```bash
cd /mnt/c/Users/user/zero-to-100-agency
python3 scripts/autopilot_run_once.py
```

Autopilot akan:

- Menyiapkan native media tools. Jika sudo bisa dipakai tanpa prompt, script memakai `sudo -n apt-get install -y ffmpeg`; jika tidak, script otomatis memakai ffmpeg static lokal gratis.
- Render MP4 YouTube Shorts native ke `youtube_shorts_factory/rendered/`.
- Cek Gmail replies dari target outreach.
- Upload Shorts private hanya jika OAuth YouTube sudah tersambung dan `QUICKOPS_UPLOAD_YOUTUBE_PRIVATE=1` diset.

Setup YouTube resmi sekali saja:

```bash
python3 scripts/youtube_oauth_local.py
QUICKOPS_UPLOAD_YOUTUBE_PRIVATE=1 python3 scripts/autopilot_run_once.py
```

Security revenue desk:

- `bug_bounty_2026_plan.md`
- `bug_bounty_targets_2026.csv`
- `bug_bounty_report_template.md`
- `bug_bounty_daily_log.csv`

## Posisi

QuickOps AI membantu bisnis kecil menghemat waktu admin dengan setup CRM ringan, automasi follow-up, form lead, chatbot FAQ sederhana, spreadsheet dashboard, dan workflow n8n/Google Sheets.

Jangan jual "AI" sebagai teori. Jual hasil operasional:

- Lead dari form langsung masuk CRM/spreadsheet.
- Email atau WhatsApp draft follow-up siap dikirim.
- Pesanan atau inquiry masuk ke dashboard.
- FAQ bisnis dijawab otomatis dari dokumen mereka.
- Konten blog/social sederhana dibuat dari keyword dan review pelanggan.

## Penawaran USD 100 Pertama

Paket pertama harus kecil, jelas, dan selesai cepat.

### Paket 1 - Lead Capture Cleanup, USD 100

Untuk bisnis lokal, freelancer, klinik kecil, salon, bengkel, agen properti, kursus, atau toko online kecil.

Deliverable:

- Audit alur lead saat ini.
- Form lead gratis memakai Google Forms, Tally, HubSpot form, atau website existing.
- Database lead di Google Sheets, Airtable free, atau HubSpot CRM free.
- Template follow-up email/WhatsApp.
- Dashboard status lead sederhana: New, Contacted, Won, Lost.
- Video Loom/OBS 3-5 menit yang menjelaskan cara pakai.

Waktu pengerjaan: 24-48 jam.

Harga awal: USD 100 flat.

Upsell setelah selesai:

- USD 50 per workflow tambahan.
- USD 150-300 untuk chatbot FAQ atau automasi n8n.
- USD 100/bulan maintenance ringan.

### Paket 2 - Website Trust Fix, USD 100

Untuk bisnis yang punya website tapi tidak jelas CTA-nya.

Deliverable:

- Perbaikan copy hero, CTA, FAQ, dan kontak.
- Form lead tersambung ke email/spreadsheet.
- 1 halaman landing sederhana jika belum punya.
- Checklist trust: testimoni, lokasi, layanan, jam buka, link WhatsApp, email.

### Paket 3 - Content Repurpose Sprint, USD 100

Untuk coach, konsultan, real estate agent, restoran, gym, dan jasa lokal.

Deliverable:

- Ambil 1 artikel/video/review panjang.
- Buat 10 post pendek untuk LinkedIn/X/Instagram.
- Buat 5 ide Reels/Shorts.
- Buat caption dan CTA.

## Strategi Mendapatkan Klien

Jalur paling cepat adalah outbound manual, bukan menunggu website ranking.

Target global lebih penting daripada target lokal. Prioritas channel:

- Hacker News founder/product feedback.
- X search untuk keluhan Zapier, CRM, follow-up, spreadsheet.
- LinkedIn untuk consultant, agency owner, coach, real estate, clinic, B2B founder.
- Upwork/Fiverr/Contra untuk job yang sudah punya demand.
- Reddit hanya jika aturan subreddit mengizinkan bantuan atau promosi.

Target harian:

- 50 prospek per hari.
- 20 pesan personal per hari.
- 5 follow-up per hari.
- 1 audit mini gratis per hari.

Sumber prospek gratis:

- Google Maps: bisnis dengan website buruk, tidak ada form, atau CTA lemah.
- LinkedIn search: founder, coach, consultant, real estate, clinic owner.
- Facebook groups lokal: pemilik UMKM, komunitas bisnis.
- Reddit: cari keluhan tentang admin, lead tracking, CRM, support.
- GitHub/Product Hunt/Indie Hackers: founder kecil yang butuh ops.
- X/Twitter: cari posting tentang "too many leads", "manual follow up", "spreadsheet mess", "need CRM".

## Alur Kerja 7 Hari

Hari 1:

- Buka `tools.md`.
- Buat email profesional gratis.
- Buat HubSpot CRM free.
- Siapkan Google Sheets lead tracker.
- Upload `landing/index.html` ke GitHub Pages, Netlify, atau Cloudflare Pages gratis.

Hari 2:

- Buat demo untuk bisnis fiktif: form lead -> spreadsheet -> follow-up template.
- Rekam video demo 3 menit.
- Screenshot before/after.

Hari 3:

- Kumpulkan 100 prospek dari Google Maps dan LinkedIn.
- Isi `lead_tracker.csv`.

Hari 4:

- Kirim 20 pesan personal.
- Tawarkan audit mini gratis.

Hari 5:

- Kirim 20 pesan lagi.
- Follow-up prospek hari 4.
- Buat 3 audit mini nyata.

Hari 6:

- Closing pertama: minta pembayaran 50% upfront atau full USD 100.
- Kerjakan paket 24 jam.

Hari 7:

- Delivery.
- Minta testimoni.
- Tawarkan maintenance atau workflow tambahan.

## Aturan Penting

- Jangan spam. Personalisasi 1-2 kalimat pertama.
- Jangan scrape data pribadi yang tidak publik.
- Jangan kirim email massal tanpa opt-out.
- Jangan menjanjikan revenue untuk klien.
- Janjikan sistem kecil yang selesai dan bisa dipakai.
- Ambil pembayaran sebelum kerja penuh.

## Sumber Riset

- HubSpot CRM free: https://www.hubspot.com/products/crm
- Zoho Campaigns forever free: https://www.zoho.com/campaigns/pricing.html
- n8n GitHub: https://github.com/n8n-io/n8n
- Awesome n8n templates: https://github.com/enescingoz/awesome-n8n-templates
- Firecrawl GitHub: https://github.com/firecrawl/firecrawl
- Screenshot-to-code GitHub: https://github.com/abi/screenshot-to-code
- Free CRM comparison 2026: https://www.techradar.com/best/best-free-crm-software
