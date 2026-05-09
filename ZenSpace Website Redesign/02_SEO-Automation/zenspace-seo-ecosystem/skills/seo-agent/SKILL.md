---
name: seo-agent
description: "End-to-end SEO Expert Agent. Crawls websites, performs technical SEO audits, on-page analysis, schema validation, competitive comparison, and generates actual fix code. Use this skill ANY time the user asks about SEO auditing, website analysis, technical SEO fixes, competitive SEO comparison, schema markup, meta tag optimization, or wants to analyze any website's SEO health. This is not a suggestion engine — it executes. It crawls, parses, scores, compares, and writes fix code."
version: "1.0.0"
---

# SEO Agent — End-to-End Technical SEO Toolkit

An autonomous SEO analysis and fix-generation system. Crawls live websites, extracts every SEO signal, scores against best practices, compares against competitors, and generates ready-to-deploy fix code.

## Architecture

```
seo-agent/
├── SKILL.md                    # This file
├── scripts/
│   ├── crawl.py               # Website crawler — fetches HTML, robots.txt, sitemap, headers
│   ├── audit.py               # Master audit engine — technical SEO, on-page, schema, CWV
│   ├── compare.py             # Side-by-side competitive comparison
│   └── fix_gen.py             # Generates actual fix code (schema, meta tags, robots.txt, sitemap)
├── data/                       # Stores crawled data per domain (auto-created)
└── reports/                    # Stores audit reports (auto-created)
```

## Workflow

### Step 1: Crawl
```bash
python3 /home/claude/skills/seo-agent/scripts/crawl.py --url https://example.com --depth 2
```
This fetches the homepage + all internal links up to `--depth` levels. Stores raw HTML, headers, robots.txt, and sitemap data in `data/{domain}/`.

If network is restricted, use `--from-file /path/to/saved.html` to load HTML from a file the user uploaded.

### Step 2: Audit
```bash
python3 /home/claude/skills/seo-agent/scripts/audit.py --domain example.com
```
Reads crawled data from `data/{domain}/` and produces a scored audit report covering:
- Technical SEO (robots.txt, sitemap, HTTPS, canonicals, redirects)
- On-Page SEO (titles, metas, headers, images, content depth, internal links)
- Schema Markup (present types, missing opportunities, validation)
- Core Web Vitals indicators (resource sizes, render-blocking, image optimization)
- AIEO/GEO readiness (structured data, definitional content, FAQ presence)

Output: `reports/{domain}_audit.json` + human-readable summary to stdout.

### Step 3: Compare
```bash
python3 /home/claude/skills/seo-agent/scripts/compare.py --our example.com --competitor rival.com
```
Reads audits for both domains and produces a gap analysis showing exactly where the competitor wins and what to fix first.

### Step 4: Generate Fixes
```bash
python3 /home/claude/skills/seo-agent/scripts/fix_gen.py --domain example.com --fixes all
```
Reads the audit report and generates actual implementation code:
- Schema markup (JSON-LD) for every page
- Optimized title tags and meta descriptions
- Recommended robots.txt
- XML sitemap
- Image alt text suggestions
- Internal linking recommendations
- FAQ page content with schema

Output: `reports/{domain}_fixes/` directory with all fix files.

## Fallback: Manual HTML Input

If the crawler can't reach a site (network restrictions), the user can:
1. Save the webpage as HTML from their browser
2. Upload the HTML file
3. Run: `python3 scripts/crawl.py --from-file /path/to/file.html --domain example.com`

This parses the uploaded HTML through the same pipeline.

## Scoring System

Each audit category is scored 0-10:
- **9-10**: Excellent — no action needed
- **7-8**: Good — minor optimizations available
- **5-6**: Needs Work — clear gaps affecting rankings
- **3-4**: Poor — significant issues blocking performance
- **0-2**: Critical — fundamental problems must fix immediately

Overall Technical SEO Score = weighted average across all categories.
