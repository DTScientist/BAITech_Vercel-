# ZenSpace Events — SEO Ecosystem

## What This Is

A self-running SEO operating system for zenspaceevents.com. It collects data, analyzes gaps, generates fixes, tracks rankings, monitors competitors, and reports results — with human approval via Telegram before any change goes live.

## Architecture

```
seo-ecosystem/
├── CLAUDE.md              ← You are here. The brain.
├── config/
│   └── ecosystem.json     ← API keys, domains, tracked keywords, schedules
├── collectors/            ← Data collection (SERP, CWV, crawl, competitors)
│   ├── serp_tracker.py    ← Tracks Google rankings for target keywords
│   ├── pagespeed.py       ← Core Web Vitals via Google PageSpeed API (free)
│   ├── site_crawler.py    ← Full site crawl + SEO element extraction
│   └── competitor_monitor.py ← Detects competitor page/schema/content changes
├── analyzers/             ← Analysis engines
│   ├── keyword_analyzer.py   ← Keyword research, clustering, gap detection
│   ├── onpage_auditor.py     ← Per-page SEO scoring (titles, headers, schema, etc.)
│   ├── content_gap.py        ← What competitors cover that we don't
│   └── aieo_scorer.py        ← AI Engine Optimization readiness scoring
├── executors/             ← Action takers
│   ├── telegram_bot.py    ← Approval workflow (approve/reject fixes via phone)
│   ├── notion_sync.py     ← Sync tasks + content calendar to Notion
│   ├── fix_generator.py   ← Generate ready-to-paste schema, meta tags, etc.
│   └── content_brief.py   ← Generate full SEO content briefs for writers
├── reporters/             ← Output generators
│   ├── weekly_report.py   ← Weekly SEO performance snapshot
│   ├── monthly_report.py  ← Monthly deep-dive with trends
│   └── action_items.py    ← Priority-ranked next actions
├── scheduler/
│   └── cron.py            ← Schedules all recurring jobs
└── data/                  ← All stored data (rankings, audits, reports)
```

## How Claude Code / Cowork Should Use This

When working on any SEO task for ZenSpace Events:

1. **Read this file first** — it has the current state, recent findings, and priorities
2. **Run the relevant script** — e.g., `python3 collectors/serp_tracker.py` for fresh ranking data
3. **Check data/ folder** — historical data lives here, JSON format, timestamped
4. **Generate outputs** — use reporters/ to build reports, executors/ to create fixes
5. **Push to Telegram** — all changes go through the approval bot before touching the live site

## Current State

- **Domain**: zenspaceevents.com (Wix-hosted)
- **Competitor**: nookeventpods.us
- **Overall SEO Score**: 45.4% (Grade D) — audited April 2026
- **Competitor Score**: 47.1% (Grade D)
- **Gap**: 1.7% — driven almost entirely by schema markup (they have 100%, we have 27%)
- **Content Strength**: EXCELLENT — 33 pages, avg 2000+ words, 5 case studies
- **Technical Debt**: Schema markup, meta descriptions, image alt text, heading structure

## Priority Queue (Current)

1. ⬜ Organization + LocalBusiness schema (site-wide)
2. ⬜ FAQPage schema on /faq
3. ⬜ Product schema on 6 pod pages
4. ⬜ AI bot rules in robots.txt
5. ⬜ Meta descriptions for 9 pages
6. ⬜ Fix homepage H1 (3 → 1)
7. ⬜ BreadcrumbList schema on all pages
8. ⬜ Image alt text (447 images)
9. ⬜ Create /event-pod-rental/ landing page
10. ⬜ Create /what-is-an-event-pod/ AIEO page

## Tracked Keywords

See config/ecosystem.json for full list. Core terms:
- "event pod rental" — current rank: unknown (need first SERP check)
- "meeting pod rental for events"
- "trade show pod rental"
- "conference meeting pod"
- "event pod rental cost"
- "nook event pods" (competitor brand)

## Scheduled Jobs

| Job | Frequency | Script | Description |
|-----|-----------|--------|-------------|
| SERP Tracker | Daily | collectors/serp_tracker.py | Track keyword rankings |
| Site Audit | Weekly (Mon) | collectors/site_crawler.py + analyzers/onpage_auditor.py | Full site health check |
| CWV Check | Weekly (Wed) | collectors/pagespeed.py | Core Web Vitals monitoring |
| Competitor Scan | Weekly (Fri) | collectors/competitor_monitor.py | Detect competitor changes |
| Weekly Report | Sunday | reporters/weekly_report.py | Performance summary → Telegram |
| Monthly Report | 1st of month | reporters/monthly_report.py | Deep dive with trends |

## MCP Integrations Available

- **Notion** → Content calendar, task tracking, SEO documentation
- **Asana** → Task assignment for dev fixes
- **Linear** → Engineering issues (technical SEO bugs)
- **HubSpot** → CRM pipeline attribution (SEO → lead → customer)
- **Google Calendar** → Content publishing schedule
- **Gmail** → Outreach sequences, link building communication

## Key Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-03 | Prioritize schema over content | Audit showed schema is the only gap vs Nook. 2-point deficit, fixable in days. |
| 2026-04-03 | Telegram for approvals | Wix API doesn't support schema injection. Human-in-loop via Telegram is fastest. |
| 2026-04-03 | Target FAQPage schema first | Neither we nor Nook have it. First-mover advantage for AI citations. |
