# SCHEMA MARKUP — Wix Implementation Guide

## Site-Wide Schema (Organization, WebSite)
WHERE: Wix Dashboard → Settings → Custom Code → + Add Custom Code
HOW:
  1. Paste the <script type="application/ld+json"> block from organization.json
  2. Name it "Organization Schema"
  3. Place code in: HEAD
  4. Apply to: ALL PAGES
  5. Save

## Per-Page Schema (Product, FAQPage, BreadcrumbList)
WHERE: Wix Editor → select page → Page Settings (gear icon) → SEO (Google) → Advanced SEO → Structured Data Markup
HOW:
  1. Open the page in Wix Editor
  2. Click Page Settings → SEO → Advanced SEO
  3. Find "Structured Data Markup" section
  4. Click "Edit" or "Add Markup"
  5. Paste the JSON-LD (without the <script> tags — just the JSON object)
  6. Save and Publish

## LocalBusiness Schema
WHERE: Same as site-wide (Custom Code → Head → All Pages)
NOTE: Only include on homepage and contact page. Use per-page method if you want it on specific pages only.

## Testing
After adding schema, validate at: https://search.google.com/test/rich-results
