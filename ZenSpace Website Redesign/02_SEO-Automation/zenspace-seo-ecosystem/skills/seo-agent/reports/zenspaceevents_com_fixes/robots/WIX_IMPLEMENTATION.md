# ROBOTS.TXT — Wix Implementation Guide

## IMPORTANT: Wix auto-generates robots.txt
You CANNOT fully replace it. You can only ADD custom rules.

WHERE: Wix Dashboard → Marketing & SEO → SEO Tools → robots.txt Editor

## What to ADD (paste these lines):
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

## What Wix handles automatically:
- Sitemap directive (auto-added)
- Default crawl rules
- Blocking of Wix system paths

## Verify after saving:
Visit https://yourdomain.com/robots.txt to confirm your additions are included.
