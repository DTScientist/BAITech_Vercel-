#!/usr/bin/env python3
"""
SEO Agent — Audit Engine
Reads crawl data and produces scored technical SEO audit.
"""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"


def load_crawl_data(domain):
    """Load crawl data for a domain."""
    domain_dir = DATA_DIR / domain.replace(".", "_")
    crawl_file = domain_dir / "crawl_data.json"
    if not crawl_file.exists():
        print(f"ERROR: No crawl data for {domain}. Run crawl.py first.")
        sys.exit(1)
    return json.loads(crawl_file.read_text())


def audit_robots_txt(data):
    """Audit robots.txt configuration."""
    robots = data.get("robots_txt", {})
    findings = []
    score = 0
    max_score = 10

    if not robots.get("exists"):
        findings.append({"severity": "CRITICAL", "issue": "No robots.txt found", "fix": "Create a robots.txt file at the root of your domain with proper directives and sitemap reference."})
        return {"score": 0, "max_score": max_score, "findings": findings}

    content = robots.get("content", "")
    score = 4  # Base for existing

    # Check for sitemap directive
    if "sitemap:" in content.lower():
        score += 2
        findings.append({"severity": "OK", "issue": "Sitemap directive present"})
    else:
        findings.append({"severity": "HIGH", "issue": "No Sitemap directive in robots.txt", "fix": "Add 'Sitemap: https://yourdomain.com/sitemap.xml' to robots.txt"})

    # Check for User-agent
    if "user-agent:" in content.lower():
        score += 1
        findings.append({"severity": "OK", "issue": "User-agent directives present"})
    else:
        findings.append({"severity": "MEDIUM", "issue": "No User-agent directives", "fix": "Add 'User-agent: *' directive"})

    # Check not blocking important paths
    blocked_bad = []
    for line in content.split("\n"):
        line = line.strip().lower()
        if line.startswith("disallow:"):
            path = line.replace("disallow:", "").strip()
            if path in ["/", "/*", ""]:
                blocked_bad.append(path or "(empty = allow all)")
            elif any(bad in path for bad in ["/blog", "/products", "/services", "/about"]):
                blocked_bad.append(path)

    if blocked_bad:
        findings.append({"severity": "CRITICAL", "issue": f"Important paths may be blocked: {blocked_bad}", "fix": "Remove Disallow directives for important content paths"})
        score = max(score - 3, 0)
    else:
        score += 1
        findings.append({"severity": "OK", "issue": "No important paths blocked"})

    # Check for AI bot access
    ai_bots_blocked = []
    for bot in ["gptbot", "claudebot", "perplexitybot", "googleother"]:
        for line in content.lower().split("\n"):
            if bot in line and "disallow" in line:
                ai_bots_blocked.append(bot)
    if ai_bots_blocked:
        findings.append({"severity": "MEDIUM", "issue": f"AI crawlers blocked: {ai_bots_blocked}", "fix": "Consider allowing AI bot access for AIEO/GEO visibility. Remove Disallow for these bots."})
    else:
        score += 1
        findings.append({"severity": "OK", "issue": "AI crawlers not blocked (good for AIEO/GEO)"})

    # Check for crawl-delay
    if "crawl-delay" in content.lower():
        findings.append({"severity": "LOW", "issue": "Crawl-delay directive found — may slow indexing", "fix": "Remove crawl-delay unless server can't handle crawl traffic"})
    else:
        score += 1

    return {"score": min(score, max_score), "max_score": max_score, "findings": findings, "content": content}


def audit_sitemap(data):
    """Audit XML sitemap."""
    sitemap = data.get("sitemap", {})
    findings = []
    score = 0
    max_score = 10

    if not sitemap.get("exists"):
        findings.append({"severity": "CRITICAL", "issue": "No XML sitemap found", "fix": "Create and submit an XML sitemap. Include all indexable pages with accurate <lastmod> dates."})
        return {"score": 0, "max_score": max_score, "findings": findings}

    score = 4
    parsed = sitemap.get("parsed", {})

    if parsed.get("type") == "urlset":
        urls = parsed.get("urls", [])
        findings.append({"severity": "OK", "issue": f"Sitemap found with {len(urls)} URLs"})

        if len(urls) < 5:
            findings.append({"severity": "HIGH", "issue": f"Very few URLs in sitemap ({len(urls)}). Likely missing pages.", "fix": "Add all indexable pages to sitemap"})
        elif len(urls) < 15:
            findings.append({"severity": "MEDIUM", "issue": f"Low URL count ({len(urls)}). Consider adding more content pages.", "fix": "Expand content and add new pages to sitemap"})
            score += 1
        else:
            score += 2

        # Check lastmod
        has_lastmod = sum(1 for u in urls if u.get("lastmod"))
        if has_lastmod == 0:
            findings.append({"severity": "MEDIUM", "issue": "No <lastmod> dates in sitemap", "fix": "Add accurate lastmod dates to signal content freshness"})
        elif has_lastmod < len(urls):
            findings.append({"severity": "LOW", "issue": f"Only {has_lastmod}/{len(urls)} URLs have lastmod dates", "fix": "Add lastmod to all URLs"})
            score += 1
        else:
            score += 2
            findings.append({"severity": "OK", "issue": "All URLs have lastmod dates"})

        # Check priority
        has_priority = sum(1 for u in urls if u.get("priority"))
        if has_priority > 0:
            score += 1

    elif parsed.get("type") == "index":
        sitemaps = parsed.get("sitemaps", [])
        findings.append({"severity": "OK", "issue": f"Sitemap index found with {len(sitemaps)} child sitemaps"})
        score += 3

    return {"score": min(score, max_score), "max_score": max_score, "findings": findings}


def audit_https_security(data):
    """Audit HTTPS and security."""
    findings = []
    score = 0
    max_score = 10

    base_url = data.get("base_url", "")
    is_https = base_url.startswith("https://")

    if is_https:
        score += 4
        findings.append({"severity": "OK", "issue": "Site uses HTTPS"})
    else:
        findings.append({"severity": "CRITICAL", "issue": "Site does not use HTTPS", "fix": "Install SSL certificate and redirect all HTTP to HTTPS"})
        return {"score": 0, "max_score": max_score, "findings": findings}

    # Check pages for mixed content signals, HSTS, etc.
    pages = data.get("pages", {})
    for url, page in pages.items():
        headers = page.get("headers", {})

        # HSTS
        if "strict-transport-security" in {k.lower(): v for k, v in headers.items()}:
            score += 2
            findings.append({"severity": "OK", "issue": "HSTS header present"})
        else:
            findings.append({"severity": "MEDIUM", "issue": "No HSTS header", "fix": "Add Strict-Transport-Security header: max-age=31536000; includeSubDomains"})

        # X-Content-Type-Options
        if "x-content-type-options" in {k.lower(): v for k, v in headers.items()}:
            score += 1
            findings.append({"severity": "OK", "issue": "X-Content-Type-Options header present"})

        # X-Frame-Options
        if "x-frame-options" in {k.lower(): v for k, v in headers.items()}:
            score += 1

        # Check redirects
        redirects = page.get("redirects", [])
        if redirects:
            chain_length = len(redirects)
            if chain_length > 2:
                findings.append({"severity": "HIGH", "issue": f"Redirect chain of {chain_length} hops for {url}", "fix": "Reduce to a single 301 redirect"})
                score = max(score - 1, 0)
            elif chain_length > 0:
                findings.append({"severity": "LOW", "issue": f"Redirect detected ({chain_length} hop) for {url}"})

        break  # Only check first page for headers

    score += 2  # Base for HTTPS working

    return {"score": min(score, max_score), "max_score": max_score, "findings": findings}


def audit_meta_tags(data):
    """Audit title tags and meta descriptions across all pages."""
    pages = data.get("pages", {})
    findings = []
    score = 10
    max_score = 10

    if not pages:
        return {"score": 0, "max_score": max_score, "findings": [{"severity": "CRITICAL", "issue": "No pages to audit"}]}

    titles = {}
    descs = {}
    pages_detail = []

    for url, page in pages.items():
        title = page.get("title", "")
        desc = page.get("meta_description", "")
        pg_issues = []

        # Title checks
        if not title:
            pg_issues.append({"severity": "CRITICAL", "issue": "Missing title tag", "url": url})
            score -= 2
        else:
            titles[title] = titles.get(title, []) + [url]
            if len(title) < 30:
                pg_issues.append({"severity": "MEDIUM", "issue": f"Title too short ({len(title)} chars): '{title}'", "url": url})
                score -= 0.5
            elif len(title) > 60:
                pg_issues.append({"severity": "LOW", "issue": f"Title may be truncated ({len(title)} chars): '{title[:60]}...'", "url": url})
                score -= 0.25

        # Meta description checks
        if not desc:
            pg_issues.append({"severity": "HIGH", "issue": "Missing meta description", "url": url})
            score -= 1.5
        else:
            descs[desc] = descs.get(desc, []) + [url]
            if len(desc) < 80:
                pg_issues.append({"severity": "MEDIUM", "issue": f"Meta description too short ({len(desc)} chars)", "url": url})
                score -= 0.5
            elif len(desc) > 160:
                pg_issues.append({"severity": "LOW", "issue": f"Meta description may be truncated ({len(desc)} chars)", "url": url})
                score -= 0.25

        # Canonical
        canonical = page.get("canonical")
        if not canonical:
            pg_issues.append({"severity": "MEDIUM", "issue": "No canonical tag", "url": url})
            score -= 0.5

        # Viewport
        if not page.get("has_viewport"):
            pg_issues.append({"severity": "HIGH", "issue": "Missing viewport meta tag (mobile-friendliness)", "url": url})
            score -= 1

        # OG tags
        if not page.get("og_tags"):
            pg_issues.append({"severity": "LOW", "issue": "No Open Graph tags", "url": url})
            score -= 0.25

        findings.extend(pg_issues)
        pages_detail.append({"url": url, "title": title, "meta_description": desc, "issues": pg_issues})

    # Duplicate checks
    for title, urls in titles.items():
        if len(urls) > 1:
            findings.append({"severity": "HIGH", "issue": f"Duplicate title across {len(urls)} pages: '{title[:50]}...'", "fix": "Create unique title tags for each page"})
            score -= 1

    for desc, urls in descs.items():
        if len(urls) > 1 and desc:
            findings.append({"severity": "MEDIUM", "issue": f"Duplicate meta description across {len(urls)} pages", "fix": "Write unique descriptions for each page"})
            score -= 0.5

    return {"score": max(round(score, 1), 0), "max_score": max_score, "findings": findings, "pages_detail": pages_detail}


def audit_headings(data):
    """Audit heading hierarchy across all pages."""
    pages = data.get("pages", {})
    findings = []
    score = 10
    max_score = 10

    for url, page in pages.items():
        headings = page.get("headings", {})
        h1s = headings.get("h1", [])

        if len(h1s) == 0:
            findings.append({"severity": "CRITICAL", "issue": f"No H1 tag on {url}", "fix": "Add exactly one H1 that includes the page's primary keyword"})
            score -= 2
        elif len(h1s) > 1:
            findings.append({"severity": "MEDIUM", "issue": f"Multiple H1 tags ({len(h1s)}) on {url}: {h1s[:3]}", "fix": "Use only one H1 per page"})
            score -= 1

        h2s = headings.get("h2", [])
        if len(h2s) == 0:
            findings.append({"severity": "MEDIUM", "issue": f"No H2 tags on {url}", "fix": "Add H2 subheadings to structure content"})
            score -= 0.5

        # Check heading hierarchy (no skipping levels)
        levels_used = [i for i in range(1, 7) if headings.get(f"h{i}")]
        for i in range(len(levels_used) - 1):
            if levels_used[i + 1] - levels_used[i] > 1:
                findings.append({"severity": "LOW", "issue": f"Heading hierarchy skip on {url}: H{levels_used[i]} → H{levels_used[i+1]}", "fix": f"Don't skip from H{levels_used[i]} to H{levels_used[i+1]}"})
                score -= 0.25

    return {"score": max(round(score, 1), 0), "max_score": max_score, "findings": findings}


def audit_images(data):
    """Audit image optimization."""
    pages = data.get("pages", {})
    findings = []
    total_images = 0
    missing_alt = 0
    has_lazy = 0
    score = 10
    max_score = 10

    for url, page in pages.items():
        images = page.get("images", [])
        total_images += len(images)
        for img in images:
            if not img.get("has_alt"):
                missing_alt += 1
            if img.get("loading") == "lazy":
                has_lazy += 1

    if total_images == 0:
        findings.append({"severity": "MEDIUM", "issue": "No images found — images improve engagement and SEO"})
        return {"score": 5, "max_score": max_score, "findings": findings}

    # Alt text
    alt_pct = ((total_images - missing_alt) / total_images) * 100
    if missing_alt > 0:
        severity = "CRITICAL" if alt_pct < 50 else "HIGH" if alt_pct < 80 else "MEDIUM"
        findings.append({"severity": severity, "issue": f"{missing_alt}/{total_images} images missing alt text ({100-alt_pct:.0f}%)", "fix": "Add descriptive alt text to every image"})
        score -= min(missing_alt * 0.5, 4)
    else:
        findings.append({"severity": "OK", "issue": f"All {total_images} images have alt text"})

    # Lazy loading
    lazy_pct = (has_lazy / total_images) * 100
    if has_lazy == 0:
        findings.append({"severity": "MEDIUM", "issue": "No images use lazy loading", "fix": "Add loading='lazy' to below-the-fold images"})
        score -= 1
    elif lazy_pct < 50:
        findings.append({"severity": "LOW", "issue": f"Only {lazy_pct:.0f}% of images use lazy loading"})
        score -= 0.5

    # Check for non-optimized formats
    non_modern = 0
    for url, page in pages.items():
        for img in page.get("images", []):
            src = img.get("src", "").lower()
            if any(ext in src for ext in [".png", ".bmp", ".tiff"]):
                non_modern += 1
    if non_modern > 0:
        findings.append({"severity": "MEDIUM", "issue": f"{non_modern} images use non-optimized formats (PNG/BMP)", "fix": "Convert to WebP or AVIF for smaller file sizes"})
        score -= 1

    return {"score": max(round(score, 1), 0), "max_score": max_score, "findings": findings,
            "stats": {"total": total_images, "missing_alt": missing_alt, "lazy_loaded": has_lazy}}


def audit_content_depth(data):
    """Audit content depth and quality signals."""
    pages = data.get("pages", {})
    findings = []
    score = 10
    max_score = 10
    page_words = []

    for url, page in pages.items():
        wc = page.get("word_count", 0)
        page_words.append({"url": url, "words": wc})

        if wc < 100:
            findings.append({"severity": "CRITICAL", "issue": f"Extremely thin content on {url}: {wc} words", "fix": "Pages need minimum 300-500 words for indexing value"})
            score -= 2
        elif wc < 300:
            findings.append({"severity": "HIGH", "issue": f"Thin content on {url}: {wc} words", "fix": "Expand to 500+ words with relevant, valuable content"})
            score -= 1
        elif wc < 500:
            findings.append({"severity": "MEDIUM", "issue": f"Light content on {url}: {wc} words"})
            score -= 0.5

    avg_words = sum(p["words"] for p in page_words) / max(len(page_words), 1)
    findings.insert(0, {"severity": "INFO", "issue": f"Average word count across {len(page_words)} pages: {avg_words:.0f} words"})

    if avg_words < 200:
        findings.append({"severity": "HIGH", "issue": "Site average word count is very low — content depth is a major ranking factor", "fix": "Expand all key pages to 500+ words minimum"})

    return {"score": max(round(score, 1), 0), "max_score": max_score, "findings": findings, "page_words": page_words}


def audit_schema_markup(data):
    """Audit structured data / schema markup."""
    pages = data.get("pages", {})
    findings = []
    score = 0
    max_score = 10

    all_types = set()
    pages_with_schema = 0
    pages_without = 0

    for url, page in pages.items():
        types = page.get("schema_types", [])
        schemas = page.get("schema_markup", [])
        if types:
            all_types.update(types)
            pages_with_schema += 1
        else:
            pages_without += 1
            findings.append({"severity": "HIGH", "issue": f"No schema markup on {url}", "fix": "Add JSON-LD structured data"})

    if pages_with_schema == 0:
        findings.insert(0, {"severity": "CRITICAL", "issue": "NO structured data found on any page. This is a major competitive disadvantage.", "fix": "Implement Organization, LocalBusiness, Product, FAQPage, and BreadcrumbList schema across the site"})
        return {"score": 0, "max_score": max_score, "findings": findings}

    score = 3
    findings.insert(0, {"severity": "INFO", "issue": f"Schema types found: {', '.join(all_types)}"})

    # Check for recommended types
    recommended = ["Organization", "LocalBusiness", "Product", "FAQPage", "BreadcrumbList", "WebSite"]
    present = [t for t in recommended if t in all_types]
    missing = [t for t in recommended if t not in all_types]

    for t in present:
        score += 1
        findings.append({"severity": "OK", "issue": f"✓ {t} schema present"})

    for t in missing:
        severity = "HIGH" if t in ["Organization", "LocalBusiness", "Product"] else "MEDIUM"
        findings.append({"severity": severity, "issue": f"Missing {t} schema", "fix": f"Add {t} JSON-LD structured data"})

    # Check for service/event specific schemas
    niche_types = ["Service", "Event", "AggregateRating", "Review", "Offer"]
    for t in niche_types:
        if t in all_types:
            score += 0.5
            findings.append({"severity": "OK", "issue": f"✓ {t} schema present (niche-relevant)"})

    return {"score": min(round(score, 1), max_score), "max_score": max_score, "findings": findings,
            "types_found": list(all_types), "recommended_missing": missing}


def audit_internal_linking(data):
    """Audit internal linking structure."""
    pages = data.get("pages", {})
    findings = []
    score = 10
    max_score = 10

    total_pages = len(pages)
    if total_pages == 0:
        return {"score": 0, "max_score": max_score, "findings": [{"severity": "CRITICAL", "issue": "No pages to audit"}]}

    link_counts = []
    for url, page in pages.items():
        count = page.get("internal_links_count", 0)
        link_counts.append({"url": url, "count": count})
        if count < 3:
            findings.append({"severity": "HIGH", "issue": f"Very few internal links on {url}: {count}", "fix": "Add contextual internal links to related pages"})
            score -= 1
        elif count < 5:
            findings.append({"severity": "MEDIUM", "issue": f"Low internal links on {url}: {count}"})
            score -= 0.5

    avg_links = sum(l["count"] for l in link_counts) / max(total_pages, 1)
    findings.insert(0, {"severity": "INFO", "issue": f"Average internal links per page: {avg_links:.1f}"})

    if avg_links < 5:
        findings.append({"severity": "HIGH", "issue": "Low average internal link density", "fix": "Target 8-15 contextual internal links per page"})
        score -= 1

    return {"score": max(round(score, 1), 0), "max_score": max_score, "findings": findings}


def audit_performance_indicators(data):
    """Audit performance indicators from crawl data (not CWV but proxy signals)."""
    pages = data.get("pages", {})
    findings = []
    score = 8  # Start generous since we can't measure actual CWV
    max_score = 10

    for url, page in pages.items():
        # Response time
        elapsed = page.get("elapsed_ms", 0)
        if elapsed > 3000:
            findings.append({"severity": "CRITICAL", "issue": f"Very slow response: {elapsed}ms for {url}", "fix": "Optimize server response time. Target < 500ms TTFB."})
            score -= 2
        elif elapsed > 1500:
            findings.append({"severity": "HIGH", "issue": f"Slow response: {elapsed}ms for {url}"})
            score -= 1
        elif elapsed > 0:
            findings.append({"severity": "OK", "issue": f"Response time: {elapsed}ms for {url}"})

        # Resource count
        css = page.get("css_files", 0)
        js = page.get("js_files", 0)
        if css + js > 20:
            findings.append({"severity": "HIGH", "issue": f"Too many external resources: {css} CSS + {js} JS files on {url}", "fix": "Combine and minify CSS/JS files"})
            score -= 1
        elif css + js > 10:
            findings.append({"severity": "MEDIUM", "issue": f"Consider reducing resources: {css} CSS + {js} JS files"})
            score -= 0.5

        # Content size
        content_length = page.get("content_length", 0)
        if content_length > 500000:  # 500KB HTML
            findings.append({"severity": "HIGH", "issue": f"Very large HTML: {content_length/1024:.0f}KB for {url}", "fix": "Reduce HTML size — defer non-critical content"})
            score -= 1

    findings.append({"severity": "INFO", "issue": "Note: Run PageSpeed Insights for actual Core Web Vitals (LCP, CLS, INP) measurements."})

    return {"score": max(round(score, 1), 0), "max_score": max_score, "findings": findings}


def audit_aieo_geo(data):
    """Audit AI Engine Optimization / Generative Engine Optimization readiness."""
    pages = data.get("pages", {})
    findings = []
    score = 0
    max_score = 10

    has_faq_schema = False
    has_definition_content = False
    has_numbers = False
    has_structured_data = False
    total_word_count = 0

    for url, page in pages.items():
        total_word_count += page.get("word_count", 0)
        types = page.get("schema_types", [])

        if "FAQPage" in types:
            has_faq_schema = True
        if types:
            has_structured_data = True

        text = page.get("text_content_preview", "").lower()
        # Check for definitional patterns
        if any(p in text for p in ["is a", "provides", "offers", "specializes", "founded in", "headquartered"]):
            has_definition_content = True
        # Check for specific numbers
        import re
        if re.search(r'\d+\+?\s*(events|clients|cities|pods|years|companies)', text):
            has_numbers = True

    # Scoring
    if has_structured_data:
        score += 2
        findings.append({"severity": "OK", "issue": "Has structured data (helps AI comprehension)"})
    else:
        findings.append({"severity": "CRITICAL", "issue": "No structured data — AI systems can't parse your offerings", "fix": "Add comprehensive JSON-LD schema markup"})

    if has_faq_schema:
        score += 2
        findings.append({"severity": "OK", "issue": "FAQPage schema present (strong AI citation signal)"})
    else:
        findings.append({"severity": "HIGH", "issue": "No FAQPage schema — major missed opportunity for AI citations", "fix": "Create FAQ content with FAQPage JSON-LD markup"})

    if has_definition_content:
        score += 1.5
        findings.append({"severity": "OK", "issue": "Definitional content found (good for AI extraction)"})
    else:
        findings.append({"severity": "HIGH", "issue": "No clear definitional content", "fix": "Add clear 'what is' content: '[Company] is a [what] that [does what] for [whom]'"})

    if has_numbers:
        score += 1.5
        findings.append({"severity": "OK", "issue": "Specific proof points with numbers found"})
    else:
        findings.append({"severity": "MEDIUM", "issue": "No specific quantitative proof points", "fix": "Add stats: events served, pod count, cities covered, setup time, etc."})

    if total_word_count > 3000:
        score += 1.5
        findings.append({"severity": "OK", "issue": f"Good content volume ({total_word_count} total words)"})
    elif total_word_count > 1000:
        score += 0.5
        findings.append({"severity": "MEDIUM", "issue": f"Moderate content volume ({total_word_count} words)", "fix": "Expand content for deeper topical coverage"})
    else:
        findings.append({"severity": "HIGH", "issue": f"Very low content volume ({total_word_count} words)", "fix": "AI systems need substantial, authoritative content to cite"})

    # Check robots.txt for AI bots
    robots = data.get("robots_txt", {})
    content = robots.get("content", "").lower()
    blocked_bots = []
    for bot in ["gptbot", "claudebot", "perplexitybot", "ccbot"]:
        if bot in content and "disallow" in content:
            blocked_bots.append(bot)
    if blocked_bots:
        findings.append({"severity": "HIGH", "issue": f"AI crawlers blocked in robots.txt: {blocked_bots}", "fix": "Allow AI bot access for citation eligibility"})
        score -= 1
    else:
        score += 1
        findings.append({"severity": "OK", "issue": "AI crawlers not blocked"})

    # Check for llms.txt
    findings.append({"severity": "LOW", "issue": "Consider creating an llms.txt file — emerging standard for AI-optimized site summaries", "fix": "Create /llms.txt with structured company info for AI systems"})

    return {"score": min(round(score, 1), max_score), "max_score": max_score, "findings": findings}


def audit_wix_platform(data):
    """Audit Wix-specific SEO concerns."""
    pages = data.get("pages", {})
    findings = []
    score = 7  # Start mid-range — Wix has inherent limitations
    max_score = 10

    for url, page in pages.items():
        html_preview = page.get("text_content_preview", "").lower()
        headers = page.get("headers", {})

        # Check for excessive JS (Wix is JS-heavy)
        js_count = page.get("js_files", 0)
        if js_count > 15:
            findings.append({"severity": "MEDIUM", "issue": f"High JS file count ({js_count}) — typical for Wix but review installed apps", "fix": "Remove unused Wix apps/plugins. Each app adds JS bloat. Dashboard → Apps → remove anything not essential."})
            score -= 1
        elif js_count > 25:
            findings.append({"severity": "HIGH", "issue": f"Very high JS file count ({js_count}) — likely too many Wix apps", "fix": "Audit and remove non-essential Wix apps immediately"})
            score -= 2

        # Check for Wix-specific rendering issues
        content_length = page.get("content_length", 0)
        word_count = page.get("word_count", 0)
        if content_length > 0 and word_count < 50 and content_length > 50000:
            findings.append({"severity": "HIGH", "issue": "Large HTML but very few words — possible JS rendering issue", "fix": "Wix may be rendering content via JS that crawlers can't see. Check: Google Search Console → URL Inspection → View Crawled Page to verify Google sees your content."})
            score -= 1

        # Check for Wix lightboxes (affect CLS)
        css_count = page.get("css_files", 0)
        if css_count > 10:
            findings.append({"severity": "LOW", "issue": f"Multiple CSS files ({css_count}) — Wix-managed, limited control", "fix": "Minimize custom CSS injections. Wix handles base CSS."})

        break  # Check first page only for platform-level issues

    # General Wix recommendations
    findings.append({"severity": "INFO", "issue": "Wix platform detected — applying platform-specific checks"})
    findings.append({"severity": "MEDIUM", "issue": "Wix auto-generates sitemap — verify all important pages are included", "fix": "Check: yourdomain.com/sitemap.xml — ensure key pages appear. Use Page Settings → SEO → Advanced to control visibility."})
    findings.append({"severity": "MEDIUM", "issue": "Wix's JavaScript-heavy rendering can delay content visibility to crawlers", "fix": "Use Google Search Console → URL Inspection → test each key page to confirm Googlebot sees full content."})
    findings.append({"severity": "LOW", "issue": "Consider Wix Velo for advanced SEO customization (dynamic schema, custom routes)", "fix": "Wix Velo (Dev Mode) enables programmatic schema injection, custom routing for llms.txt, and dynamic meta tags."})

    return {"score": max(round(score, 1), 0), "max_score": max_score, "findings": findings}


def run_full_audit(domain):
    """Run complete SEO audit for a domain."""
    data = load_crawl_data(domain)

    print(f"\n{'='*70}")
    print(f"  SEO AGENT — FULL TECHNICAL AUDIT: {domain}")
    print(f"{'='*70}\n")

    audit = {
        "domain": domain,
        "base_url": data.get("base_url"),
        "pages_analyzed": len(data.get("pages", {})),
        "network_accessible": data.get("network_accessible", True),
        "categories": {},
    }

    # Run all audit modules
    modules = [
        ("robots_txt", "Robots.txt", audit_robots_txt),
        ("sitemap", "XML Sitemap", audit_sitemap),
        ("https_security", "HTTPS & Security", audit_https_security),
        ("meta_tags", "Title Tags & Meta Descriptions", audit_meta_tags),
        ("headings", "Heading Structure", audit_headings),
        ("images", "Image Optimization", audit_images),
        ("content_depth", "Content Depth", audit_content_depth),
        ("schema_markup", "Schema / Structured Data", audit_schema_markup),
        ("internal_linking", "Internal Linking", audit_internal_linking),
        ("performance", "Performance Indicators", audit_performance_indicators),
        ("aieo_geo", "AIEO / GEO Readiness", audit_aieo_geo),
        ("wix_platform", "Wix Platform Checks", audit_wix_platform),
    ]

    total_score = 0
    total_max = 0

    for key, name, func in modules:
        result = func(data)
        audit["categories"][key] = {"name": name, **result}
        total_score += result["score"]
        total_max += result["max_score"]

        # Print summary
        pct = (result["score"] / result["max_score"]) * 100
        bar_len = 20
        filled = int(bar_len * result["score"] / result["max_score"])
        bar = "█" * filled + "░" * (bar_len - filled)
        grade = "EXCELLENT" if pct >= 90 else "GOOD" if pct >= 70 else "NEEDS WORK" if pct >= 50 else "POOR" if pct >= 30 else "CRITICAL"
        print(f"  {name:35s} [{bar}] {result['score']:4.1f}/{result['max_score']:2d}  {grade}")

        # Print findings
        critical_high = [f for f in result.get("findings", []) if f.get("severity") in ["CRITICAL", "HIGH"]]
        for f in critical_high[:3]:
            icon = "🔴" if f["severity"] == "CRITICAL" else "🟠"
            print(f"    {icon} {f['issue'][:80]}")

    # Overall score
    overall_pct = (total_score / total_max) * 100 if total_max > 0 else 0
    audit["overall_score"] = round(total_score, 1)
    audit["overall_max"] = total_max
    audit["overall_percentage"] = round(overall_pct, 1)
    audit["overall_grade"] = "A" if overall_pct >= 90 else "B" if overall_pct >= 75 else "C" if overall_pct >= 60 else "D" if overall_pct >= 40 else "F"

    print(f"\n{'='*70}")
    print(f"  OVERALL SCORE: {total_score:.1f}/{total_max} ({overall_pct:.1f}%) — Grade: {audit['overall_grade']}")
    print(f"{'='*70}")

    # Priority fix list
    all_findings = []
    for key, cat in audit["categories"].items():
        for f in cat.get("findings", []):
            if f.get("fix"):
                f["category"] = cat["name"]
                all_findings.append(f)

    critical = [f for f in all_findings if f["severity"] == "CRITICAL"]
    high = [f for f in all_findings if f["severity"] == "HIGH"]
    medium = [f for f in all_findings if f["severity"] == "MEDIUM"]

    print(f"\n  PRIORITY FIX LIST:")
    print(f"  {'─'*50}")
    for i, f in enumerate(critical + high + medium, 1):
        icon = "🔴" if f["severity"] == "CRITICAL" else "🟠" if f["severity"] == "HIGH" else "🟡"
        print(f"  {icon} [{f['severity']:8s}] [{f['category']}]")
        print(f"     Issue: {f['issue'][:90]}")
        print(f"     Fix:   {f['fix'][:90]}")
        if i > 15:
            remaining = len(critical) + len(high) + len(medium) - 15
            print(f"  ... and {remaining} more items")
            break

    # Save report
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{domain.replace('.', '_')}_audit.json"
    report_path.write_text(json.dumps(audit, indent=2, default=str))
    print(f"\n  Full report saved: {report_path}")

    return audit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO Agent Audit Engine")
    parser.add_argument("--domain", required=True, help="Domain to audit (must be crawled first)")
    args = parser.parse_args()
    run_full_audit(args.domain)
