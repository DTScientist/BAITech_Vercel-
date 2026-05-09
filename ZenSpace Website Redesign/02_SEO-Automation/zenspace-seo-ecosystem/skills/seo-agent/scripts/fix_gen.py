#!/usr/bin/env python3
"""
SEO Agent — Fix Generator
Reads audit reports and generates actual implementation code.
Produces: schema markup, meta tags, robots.txt, sitemap, alt text, etc.
"""

import argparse
import json
import sys
import os
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"


def load_audit(domain):
    report_path = REPORTS_DIR / f"{domain.replace('.', '_')}_audit.json"
    if not report_path.exists():
        print(f"ERROR: No audit report for {domain}. Run audit.py first.")
        sys.exit(1)
    return json.loads(report_path.read_text())


def load_crawl_data(domain):
    crawl_path = DATA_DIR / domain.replace(".", "_") / "crawl_data.json"
    if not crawl_path.exists():
        return {}
    return json.loads(crawl_path.read_text())


def generate_schema_markup(audit, crawl_data, domain, output_dir):
    """Generate JSON-LD schema markup for all pages."""
    print("  [1] Generating Schema Markup (JSON-LD)...")

    base_url = crawl_data.get("base_url", f"https://{domain}")
    pages = crawl_data.get("pages", {})

    # Organization schema (site-wide)
    org_schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "[COMPANY_NAME]",
        "url": base_url,
        "logo": f"{base_url}/logo.png",
        "description": "[Company description — what you do, for whom]",
        "foundingDate": "[YYYY]",
        "numberOfEmployees": {"@type": "QuantitativeValue", "value": "[NUMBER]"},
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "[STREET]",
            "addressLocality": "[CITY]",
            "addressRegion": "[STATE]",
            "postalCode": "[ZIP]",
            "addressCountry": "US",
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "[PHONE]",
            "contactType": "sales",
            "email": "[EMAIL]",
        },
        "sameAs": [
            "[LINKEDIN_URL]",
            "[INSTAGRAM_URL]",
            "[FACEBOOK_URL]",
            "[TWITTER_URL]",
        ],
        "areaServed": {
            "@type": "Country",
            "name": "United States",
        },
    }

    # LocalBusiness schema
    local_schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "[COMPANY_NAME]",
        "url": base_url,
        "image": f"{base_url}/images/hero.jpg",
        "description": "[Short description of services]",
        "telephone": "[PHONE]",
        "priceRange": "$$-$$$",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "[STREET]",
            "addressLocality": "[CITY]",
            "addressRegion": "[STATE]",
            "postalCode": "[ZIP]",
            "addressCountry": "US",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "[LAT]",
            "longitude": "[LNG]",
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00",
            "closes": "17:00",
        },
        "areaServed": [
            {"@type": "City", "name": "Las Vegas"},
            {"@type": "City", "name": "Chicago"},
            {"@type": "City", "name": "Orlando"},
            {"@type": "City", "name": "New York"},
        ],
    }

    # Product schema for each pod type
    product_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "[POD_MODEL_NAME]",
        "description": "[Pod description with capacity, features, use case]",
        "brand": {"@type": "Brand", "name": "[COMPANY_NAME]"},
        "image": f"{base_url}/images/[pod-image].jpg",
        "category": "Event Equipment Rental",
        "offers": {
            "@type": "Offer",
            "priceCurrency": "USD",
            "price": "[DAILY_RATE]",
            "priceValidUntil": "2026-12-31",
            "availability": "https://schema.org/InStock",
            "url": f"{base_url}/[product-page]/",
        },
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "Capacity", "value": "[X] persons"},
            {"@type": "PropertyValue", "name": "Setup Time", "value": "Under 30 minutes"},
            {"@type": "PropertyValue", "name": "IoT Enabled", "value": "Yes"},
        ],
    }

    # WebSite schema with search action
    website_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "[COMPANY_NAME]",
        "url": base_url,
        "potentialAction": {
            "@type": "SearchAction",
            "target": {"@type": "EntryPoint", "urlTemplate": f"{base_url}/search?q={{search_term_string}}"},
            "query-input": "required name=search_term_string",
        },
    }

    # BreadcrumbList template
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": base_url},
            {"@type": "ListItem", "position": 2, "name": "[PAGE_CATEGORY]", "item": f"{base_url}/[category]/"},
            {"@type": "ListItem", "position": 3, "name": "[PAGE_TITLE]", "item": f"{base_url}/[category]/[page]/"},
        ],
    }

    # FAQPage schema template
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "How much does it cost to rent an event pod?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "[Specific pricing information with ranges, factors that affect cost]",
                },
            },
            {
                "@type": "Question",
                "name": "What is included in the event pod rental?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "[Delivery, setup, teardown, IoT features, branding options, technical support]",
                },
            },
            {
                "@type": "Question",
                "name": "How far in advance should I book event pods?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "[Booking timeline, peak seasons, rush availability]",
                },
            },
            {
                "@type": "Question",
                "name": "What types of events are pods suitable for?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "[Trade shows, conferences, corporate events, brand activations, etc.]",
                },
            },
            {
                "@type": "Question",
                "name": "How long does pod setup take?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "[Setup time, requirements, what's included in the service]",
                },
            },
        ],
    }

    # Service schema
    service_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "Event Pod Rental",
        "provider": {
            "@type": "Organization",
            "name": "[COMPANY_NAME]",
        },
        "areaServed": {"@type": "Country", "name": "United States"},
        "description": "[Service description]",
        "offers": {
            "@type": "Offer",
            "priceCurrency": "USD",
            "price": "[STARTING_PRICE]",
        },
    }

    # Save all schema files
    schema_dir = output_dir / "schema"
    schema_dir.mkdir(parents=True, exist_ok=True)

    schemas = {
        "organization.json": org_schema,
        "local_business.json": local_schema,
        "product_template.json": product_schema,
        "website.json": website_schema,
        "breadcrumb_template.json": breadcrumb_schema,
        "faq_page.json": faq_schema,
        "service.json": service_schema,
    }

    for filename, schema in schemas.items():
        (schema_dir / filename).write_text(json.dumps(schema, indent=2))

    # Generate injection snippet
    snippet = """<!-- SCHEMA MARKUP — Add to <head> section -->
<!-- Organization (all pages) -->
<script type="application/ld+json">
%s
</script>

<!-- LocalBusiness (homepage + contact page) -->
<script type="application/ld+json">
%s
</script>

<!-- WebSite (homepage only) -->
<script type="application/ld+json">
%s
</script>

<!-- FAQPage (FAQ page and any page with FAQ content) -->
<script type="application/ld+json">
%s
</script>

<!-- Product (each product/pod page) -->
<script type="application/ld+json">
%s
</script>

<!-- BreadcrumbList (all pages except homepage) -->
<script type="application/ld+json">
%s
</script>
""" % (
        json.dumps(org_schema, indent=2),
        json.dumps(local_schema, indent=2),
        json.dumps(website_schema, indent=2),
        json.dumps(faq_schema, indent=2),
        json.dumps(product_schema, indent=2),
        json.dumps(breadcrumb_schema, indent=2),
    )

    (schema_dir / "injection_snippet.html").write_text(snippet)

    # Wix implementation guide
    wix_guide = """# SCHEMA MARKUP — Wix Implementation Guide

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
"""
    (schema_dir / "WIX_IMPLEMENTATION.md").write_text(wix_guide)

    print(f"    ✓ 7 schema templates saved to {schema_dir}/")
    print(f"    ✓ HTML injection snippet: {schema_dir}/injection_snippet.html")
    print(f"    ✓ Wix implementation guide: {schema_dir}/WIX_IMPLEMENTATION.md")
    return schemas


def generate_meta_tags(audit, crawl_data, domain, output_dir):
    """Generate optimized meta tags for all pages."""
    print("  [2] Generating Optimized Meta Tags...")

    pages = crawl_data.get("pages", {})
    base_url = crawl_data.get("base_url", f"https://{domain}")
    meta_fixes = []

    for url, page in pages.items():
        current_title = page.get("title", "")
        current_desc = page.get("meta_description", "")
        path = urlparse(url).path or "/"

        fix = {
            "url": url,
            "path": path,
            "current_title": current_title,
            "current_meta_description": current_desc,
            "issues": [],
        }

        # Title fixes
        if not current_title:
            fix["issues"].append("Missing title tag")
            fix["recommended_title"] = "[Primary Keyword] — [Secondary Keyword] | [Brand Name]"
        elif len(current_title) < 30:
            fix["issues"].append(f"Title too short ({len(current_title)} chars)")
            fix["recommended_title"] = f"{current_title} — [Add Primary Keyword] | [Brand Name]"
        elif len(current_title) > 60:
            fix["issues"].append(f"Title too long ({len(current_title)} chars)")
            fix["recommended_title"] = current_title[:57] + "..."

        # Description fixes
        if not current_desc:
            fix["issues"].append("Missing meta description")
            fix["recommended_description"] = "[Write 150-160 chars describing this page's content with primary keyword and CTA]"
        elif len(current_desc) < 80:
            fix["issues"].append(f"Description too short ({len(current_desc)} chars)")
        elif len(current_desc) > 160:
            fix["issues"].append(f"Description too long ({len(current_desc)} chars)")

        # Canonical
        if not page.get("canonical"):
            fix["issues"].append("Missing canonical tag")
            fix["recommended_canonical"] = url

        # Viewport
        if not page.get("has_viewport"):
            fix["issues"].append("Missing viewport meta tag")
            fix["recommended_viewport"] = "width=device-width, initial-scale=1"

        # OG tags
        if not page.get("og_tags"):
            fix["issues"].append("Missing Open Graph tags")
            fix["recommended_og"] = {
                "og:title": current_title or "[Page Title]",
                "og:description": current_desc or "[Page Description]",
                "og:type": "website",
                "og:url": url,
                "og:image": f"{base_url}/images/og-default.jpg",
                "og:site_name": "[Brand Name]",
            }

        if fix["issues"]:
            meta_fixes.append(fix)

    # Save
    meta_dir = output_dir / "meta_tags"
    meta_dir.mkdir(parents=True, exist_ok=True)
    (meta_dir / "meta_fixes.json").write_text(json.dumps(meta_fixes, indent=2))

    # Generate HTML template
    html_template = """<!-- META TAG TEMPLATE — Customize per page -->
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Primary Meta Tags -->
    <title>[Primary Keyword] — [Secondary Keyword] | [Brand Name]</title>
    <meta name="description" content="[150-160 char description with keyword and CTA]">
    <link rel="canonical" href="[CURRENT_PAGE_URL]">

    <!-- Robots -->
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="[CURRENT_PAGE_URL]">
    <meta property="og:title" content="[Same as title tag or slightly different]">
    <meta property="og:description" content="[Same as meta description or slightly different]">
    <meta property="og:image" content="[URL to 1200x630px image]">
    <meta property="og:site_name" content="[Brand Name]">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="[Same as title]">
    <meta name="twitter:description" content="[Same as description]">
    <meta name="twitter:image" content="[URL to image]">

    <!-- Schema Markup -->
    <script type="application/ld+json">
    { "@context": "https://schema.org", "@type": "WebPage", ... }
    </script>
</head>
"""
    (meta_dir / "head_template.html").write_text(html_template)

    # Wix implementation guide
    wix_meta_guide = """# META TAG FIXES — Wix Implementation Guide

## Title Tag & Meta Description (per page)
WHERE: Wix Editor → click page → Page Settings (gear icon) → SEO (Google)
  - "Page Title" = your title tag
  - "What's this page about?" = your meta description

## Open Graph / Social Share
WHERE: Wix Editor → Page Settings → Social Share
  - Customize the title, description, and image shown when shared on social media

## Canonical Tags
Wix auto-sets self-referencing canonicals. No action needed unless you have duplicate content.
WHERE (if needed): Page Settings → SEO → Advanced SEO → Additional Tags

## Viewport Meta
Wix auto-includes viewport meta on all pages. No action needed.

## IMPORTANT: Go page by page
Wix has no bulk meta tag editor. You must edit each page individually.
Prioritize: Homepage > Service pages > Product pages > Blog posts > Other pages
"""
    (meta_dir / "WIX_IMPLEMENTATION.md").write_text(wix_meta_guide)

    issues_count = sum(len(f["issues"]) for f in meta_fixes)
    print(f"    ✓ {issues_count} meta tag issues documented across {len(meta_fixes)} pages")
    print(f"    ✓ Fixes saved to {meta_dir}/")
    print(f"    ✓ Wix implementation guide: {meta_dir}/WIX_IMPLEMENTATION.md")
    return meta_fixes


def generate_robots_txt(audit, crawl_data, domain, output_dir):
    """Generate optimized robots.txt."""
    print("  [3] Generating Optimized robots.txt...")

    base_url = crawl_data.get("base_url", f"https://{domain}")

    robots_content = f"""# robots.txt for {domain}
# Generated by SEO Agent

User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /private/
Disallow: /tmp/
Disallow: /*?s=
Disallow: /*?p=
Disallow: /wp-admin/

# Allow AI crawlers for AIEO/GEO visibility
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

# Sitemap
Sitemap: {base_url}/sitemap.xml
"""

    robots_dir = output_dir / "robots"
    robots_dir.mkdir(parents=True, exist_ok=True)
    (robots_dir / "robots.txt").write_text(robots_content)

    wix_robots_guide = """# ROBOTS.TXT — Wix Implementation Guide

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
"""
    (robots_dir / "WIX_IMPLEMENTATION.md").write_text(wix_robots_guide)
    print(f"    ✓ Optimized robots.txt saved to {robots_dir}/robots.txt")
    print(f"    ✓ Wix implementation guide: {robots_dir}/WIX_IMPLEMENTATION.md")
    return robots_content


def generate_sitemap(audit, crawl_data, domain, output_dir):
    """Generate XML sitemap from crawled pages."""
    print("  [4] Generating XML Sitemap...")

    pages = crawl_data.get("pages", {})
    base_url = crawl_data.get("base_url", f"https://{domain}")

    import datetime
    today = datetime.date.today().isoformat()

    xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # Add homepage with highest priority
    xml_parts.append(f"""  <url>
    <loc>{base_url}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>""")

    # Add all crawled pages
    for url, page in pages.items():
        if url.rstrip("/") == base_url.rstrip("/"):
            continue  # Skip homepage, already added
        path = urlparse(url).path
        priority = "0.8" if path.count("/") <= 2 else "0.6"
        xml_parts.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>""")

    # Add recommended pages that should exist
    recommended_pages = [
        "/about/", "/contact/", "/faq/", "/blog/",
        "/event-pod-rental/", "/trade-show-pods/",
        "/meeting-pod-rental/", "/privacy-pods/",
        "/event-pod-rental-cost/",
    ]
    existing_paths = [urlparse(u).path.rstrip("/") for u in pages.keys()]
    for rp in recommended_pages:
        if rp.rstrip("/") not in existing_paths:
            xml_parts.append(f"""  <!-- RECOMMENDED: Create this page -->
  <!-- <url>
    <loc>{base_url}{rp}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url> -->""")

    xml_parts.append("</urlset>")
    sitemap_content = "\n".join(xml_parts)

    sitemap_dir = output_dir / "sitemap"
    sitemap_dir.mkdir(parents=True, exist_ok=True)
    (sitemap_dir / "sitemap.xml").write_text(sitemap_content)
    print(f"    ✓ Sitemap with {len(pages)} pages saved to {sitemap_dir}/sitemap.xml")
    print(f"    ✓ Commented-out entries show recommended pages to create")
    return sitemap_content


def generate_image_alt_fixes(audit, crawl_data, domain, output_dir):
    """Generate alt text recommendations for images."""
    print("  [5] Generating Image Alt Text Fixes...")

    pages = crawl_data.get("pages", {})
    fixes = []

    for url, page in pages.items():
        for img in page.get("images", []):
            if not img.get("has_alt"):
                fixes.append({
                    "page_url": url,
                    "image_src": img.get("src", ""),
                    "current_alt": img.get("alt", ""),
                    "recommended_alt": f"[Describe what's in this image — include relevant keyword if natural. E.g., 'Event pod setup at CES trade show' or 'Meeting pod interior with IoT display']",
                    "loading_attr": "Add loading='lazy' for below-the-fold images",
                })

    img_dir = output_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    (img_dir / "alt_text_fixes.json").write_text(json.dumps(fixes, indent=2))
    print(f"    ✓ {len(fixes)} images need alt text fixes")
    return fixes


def generate_llms_txt(audit, crawl_data, domain, output_dir):
    """Generate llms.txt for AI engine optimization."""
    print("  [6] Generating llms.txt (AI Engine Optimization)...")

    base_url = crawl_data.get("base_url", f"https://{domain}")

    llms_content = f"""# {domain}

> [COMPANY_NAME] provides premium event pod and meeting pod rentals for trade shows, conferences, and corporate events. Our IoT-enabled SmartPods offer private, bookable workspaces with built-in lead capture, digital branding, and real-time analytics.

## Key Pages

- [{base_url}/]({base_url}/): Homepage — overview of event pod rental services
- [{base_url}/event-pod-rental/]({base_url}/event-pod-rental/): Event pod rental services and pricing
- [{base_url}/trade-show-pods/]({base_url}/trade-show-pods/): Trade show specific pod solutions
- [{base_url}/about/]({base_url}/about/): Company background and team
- [{base_url}/faq/]({base_url}/faq/): Frequently asked questions about pod rentals
- [{base_url}/blog/]({base_url}/blog/): Industry insights and event technology articles

## Quick Facts

- **Service**: Event pod and meeting pod rentals
- **Coverage**: Nationwide (United States)
- **Pod Types**: Privacy pods, meeting pods, conference pods, phone booths
- **Capacity**: 1-person to 6-person configurations
- **Features**: IoT-enabled, digital branding, lead capture, booking software
- **Setup**: Under 30 minutes, includes delivery and teardown
- **Events Served**: [X]+ events
- **Key Markets**: Trade shows, conferences, corporate events, brand activations

## Contact

- Website: {base_url}
- Email: [EMAIL]
- Phone: [PHONE]
"""

    llms_dir = output_dir / "llms_txt"
    llms_dir.mkdir(parents=True, exist_ok=True)
    (llms_dir / "llms.txt").write_text(llms_content)
    print(f"    ✓ llms.txt saved — deploy to {base_url}/llms.txt")
    return llms_content


def generate_all_fixes(domain, fix_types="all"):
    """Generate all fix implementations."""
    audit = load_audit(domain)
    crawl_data = load_crawl_data(domain)

    output_dir = REPORTS_DIR / f"{domain.replace('.', '_')}_fixes"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*70}")
    print(f"  SEO AGENT — FIX GENERATOR: {domain}")
    print(f"{'='*70}\n")

    generators = [
        generate_schema_markup,
        generate_meta_tags,
        generate_robots_txt,
        generate_sitemap,
        generate_image_alt_fixes,
        generate_llms_txt,
    ]

    for gen in generators:
        try:
            gen(audit, crawl_data, domain, output_dir)
        except Exception as e:
            print(f"    ⚠ Error in {gen.__name__}: {e}")

    # Summary
    print(f"\n{'='*70}")
    print(f"  ALL FIXES GENERATED")
    print(f"  Output directory: {output_dir}/")
    print(f"{'='*70}")
    print(f"  📁 schema/           — JSON-LD structured data for all pages")
    print(f"  📁 meta_tags/        — Optimized title tags, descriptions, OG tags")
    print(f"  📁 robots/           — Production-ready robots.txt")
    print(f"  📁 sitemap/          — XML sitemap with recommended pages")
    print(f"  📁 images/           — Alt text fixes for all images")
    print(f"  📁 llms_txt/         — AI Engine Optimization file")
    print(f"{'='*70}\n")

    return output_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO Agent Fix Generator")
    parser.add_argument("--domain", required=True, help="Domain to generate fixes for")
    parser.add_argument("--fixes", default="all", help="Fix types: all, schema, meta, robots, sitemap, images, llms")
    args = parser.parse_args()
    generate_all_fixes(args.domain, args.fixes)
