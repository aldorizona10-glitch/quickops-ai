# Zero-Budget Agency Tool Stack

Date: 2026-06-10

This stack avoids paid subscriptions at the start. It is built for getting the first paid workflow deal, not for pretending revenue is guaranteed.

## Core Stack

| Function | Tool | Cost at start | Use |
| --- | --- | --- | --- |
| Public website/profile | GitHub Pages | Free for public repositories | Host profile, proof page, offers, and demos. |
| Source control/portfolio | GitHub | Free public repos | Show real work and keep deployment history. |
| Email sending/replies | Gmail API | Free with Google account quotas | Send allowlisted outreach and monitor replies. |
| CRM tracker | CSV + Google Sheets | Free | Track leads, status, next follow-up, and deal stage. |
| Client CRM option | HubSpot CRM | Free tier available | Deliver simple CRM setup if the client wants a hosted CRM. |
| Workflow automation | n8n self-host/local | No software fee for local/self-host use under its license limits | Build and document client workflow prototypes. |
| Lightweight scripts | Google Apps Script | Free quota limits | Sheets automations, email drafts, form follow-ups. |
| Delivery handover | Markdown/HTML notes | Free | Produce clear handover notes and operator checklists. |
| Static landing pages | HTML/CSS on GitHub Pages | Free | Create a client demo page or audit page. |
| Security proof | HackerOne letter summary | Free existing asset | Trust proof, sent only as summary unless original PDF is requested. |

## Official References

- GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- HubSpot CRM: https://www.hubspot.com/products/crm
- n8n hosting: https://docs.n8n.io/hosting/
- Google Apps Script quotas: https://developers.google.com/apps-script/guides/services/quotas

## Operating Model

The assistant acts as a small agency team:

| Role | Responsibility | Local automation |
| --- | --- | --- |
| Repo/Trust Engineer | Keep GitHub Pages, profile, and proof assets clean. | `profile/`, `index.html`, `docs/github_repo_asset_audit.md` |
| Prospect Researcher | Maintain target lists from public sources. | `lead_tracker.csv`, `public_opportunities.csv` |
| Outreach Operator | Send allowlisted personalized emails. | `email_queue/`, `scripts/gmail_api_send_queue.py` |
| Reply/CRM Operator | Monitor replies and next actions. | `scripts/gmail_check_replies.py`, `scripts/agency_status.py` |
| Closing Operator | Convert interested replies into USD 100 fixed-scope offers. | `docs/agency_closing_templates.md` |
| Delivery Engineer | Build the workflow/demo after payment or agreed starter scope. | `delivery_kit.md`, `proposal.md`, GitHub Pages demos |

## Revenue Path

1. Find public prospects with clear operations pain.
2. Send a short, specific message with one fixed offer.
3. When they reply interested, send a USD 100 fixed scope.
4. Ask for payment before full build.
5. Deliver one usable workflow within 24-48 hours.
6. Ask for testimonial and offer follow-up work.

## Guardrails

- No spam.
- No fake LinkedIn or fake work history.
- No paid services unless the user explicitly approves spending.
- No raw HackerOne PDF published publicly.
- No promise of guaranteed earnings.
