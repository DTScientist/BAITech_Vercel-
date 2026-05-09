#!/usr/bin/env python3
"""
SEO Agent — Website Crawler
Fetches HTML, robots.txt, sitemap, HTTP headers for SEO analysis.
Supports live crawling and file-based input fallback.
"""

import argparse
import json
import os
import re
import sys
import time
from urllib.parse import urlparse, urljoin
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Install dependencies: pip install beautifulsoup4 lxml requests --break-system-packages")
    sys.exit(1)

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SEOAgentBot/1.0; +https://zenspaceevents.com)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


def get_domain(url):
    """Extract clean domain from URL."""
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    domain = domain.replace("www.", "")
    return domain


def ensure_url(url):
    """Ensure URL has scheme."""
    if not url.startswith("http"):
        url = "https://" + url
    return url.rstrip("/")


def fetch_url(url, timeout=15):
    """Fetch a URL and return response data."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return {
            "url": url,
            "final_url": resp.url,
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
            "content": resp.text,
            "content_length": len(resp.content),
            "elapsed_ms": int(resp.elapsed.total_seconds() * 1000),
            "redirects": [{"url": r.url, "status": r.status_code} for r in resp.history],
            "error": None,
        }
    except requests.exceptions.SSLError as e:
        return {"url": url, "status_code": None, "error": f"SSL Error: {str(e)[:200]}"}
    except requests.exceptions.ConnectionError as e:
        return {"url": url, "status_code": None, "error": f"Connection Error: {str(e)[:200]}"}
    except requests.exceptions.Timeout:
        return {"url": url, "status_code": None, "error": "Timeout"}
    except Exception as e:
        return {"url": url, "status_code": None, "error": str(e)[:200]}


def extract_internal_links(html, base_url):
    """Extract all internal links from HTML."""
    soup = BeautifulSoup(html, "lxml")
    domain = urlparse(base_url).netloc
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)
        if parsed.netloc == domain or parsed.netloc == "www." + domain or "www." + parsed.netloc == domain:
            clean = parsed.scheme + "://" + parsed.netloc + parsed.path.rstrip("/")
            if not any(ext in parsed.path.lower() for ext in [".pdf", ".jpg", ".png", ".gif", ".svg", ".css", ".js", ".zip"]):
                links.add(clean)
    return list(links)


def parse_sitemap(content, base_url):
    """Parse XML sitemap and extract URLs."""
    urls = []
    try:
        soup = BeautifulSoup(content, "lxml-xml")
        # Check for sitemap index
        sitemaps = soup.find_all("sitemap")
        if sitemaps:
            return {"type": "index", "sitemaps": [s.find("loc").text for s in sitemaps if s.find("loc")]}
        # Regular sitemap
        url_entries = soup.find_all("url")
        for entry in url_entries:
            loc = entry.find("loc")
            lastmod = entry.find("lastmod")
            priority = entry.find("priority")
            changefreq = entry.find("changefreq")
            if loc:
                urls.append({
                    "loc": loc.text,
                    "lastmod": lastmod.text if lastmod else None,
                    "priority": priority.text if priority else None,
                    "changefreq": changefreq.text if changefreq else None,
                })
        return {"type": "urlset", "urls": urls}
    except Exception as e:
        return {"type": "error", "error": str(e), "raw_length": len(content)}


def crawl_site(url, max_depth=2, max_pages=50):
    """Crawl a website starting from the given URL."""
    base_url = ensure_url(url)
    domain = get_domain(base_url)
    domain_dir = DATA_DIR / domain.replace(".", "_")
    domain_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  SEO AGENT CRAWLER — {domain}")
    print(f"{'='*60}\n")

    results = {
        "domain": domain,
        "base_url": base_url,
        "crawl_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pages": {},
        "robots_txt": None,
        "sitemap": None,
        "errors": [],
        "network_accessible": True,
    }

    # 1. Fetch robots.txt
    print("[1/4] Fetching robots.txt...")
    robots_url = base_url + "/robots.txt"
    robots_resp = fetch_url(robots_url)
    if robots_resp.get("error"):
        print(f"  ⚠ robots.txt: {robots_resp['error']}")
        results["robots_txt"] = {"exists": False, "error": robots_resp["error"], "content": ""}
        if "Connection Error" in str(robots_resp.get("error", "")) or "Timeout" in str(robots_resp.get("error", "")):
            results["network_accessible"] = False
            print(f"\n  ✗ Cannot reach {domain} — network restricted.")
            print(f"    Use --from-file to load saved HTML instead.\n")
    else:
        content = robots_resp.get("content", "")
        is_robots = robots_resp.get("status_code") == 200 and ("user-agent" in content.lower() or "sitemap" in content.lower() or "disallow" in content.lower() or content.strip() == "")
        results["robots_txt"] = {
            "exists": is_robots,
            "status_code": robots_resp.get("status_code"),
            "content": content if is_robots else "",
            "headers": robots_resp.get("headers", {}),
        }
        status = "✓ Found" if is_robots else "✗ Not found / not valid"
        print(f"  {status} (HTTP {robots_resp.get('status_code')})")
        # Save robots.txt
        (domain_dir / "robots.txt").write_text(content if is_robots else "# No robots.txt found")

    if not results["network_accessible"]:
        # Save partial results
        (domain_dir / "crawl_data.json").write_text(json.dumps(results, indent=2, default=str))
        print(f"\nPartial data saved to: {domain_dir}/")
        return results

    # 2. Fetch sitemap
    print("[2/4] Fetching sitemap.xml...")
    sitemap_urls_to_try = [base_url + "/sitemap.xml", base_url + "/sitemap_index.xml"]
    # Check robots.txt for sitemap directive
    if results["robots_txt"]["exists"]:
        for line in results["robots_txt"]["content"].split("\n"):
            if line.lower().startswith("sitemap:"):
                sm_url = line.split(":", 1)[1].strip()
                if sm_url and sm_url not in sitemap_urls_to_try:
                    sitemap_urls_to_try.insert(0, sm_url)

    sitemap_found = False
    for sm_url in sitemap_urls_to_try:
        sm_resp = fetch_url(sm_url)
        if sm_resp.get("status_code") == 200 and sm_resp.get("content", "").strip():
            parsed = parse_sitemap(sm_resp["content"], base_url)
            results["sitemap"] = {
                "url": sm_url,
                "exists": True,
                "parsed": parsed,
                "raw_content": sm_resp["content"][:5000],
            }
            count = len(parsed.get("urls", [])) or len(parsed.get("sitemaps", []))
            print(f"  ✓ Found at {sm_url} ({count} entries)")
            (domain_dir / "sitemap.xml").write_text(sm_resp["content"])
            sitemap_found = True
            break
    if not sitemap_found:
        results["sitemap"] = {"exists": False, "urls_tried": sitemap_urls_to_try}
        print(f"  ✗ No sitemap found")

    # 3. Crawl pages
    print(f"[3/4] Crawling pages (max depth={max_depth}, max pages={max_pages})...")
    visited = set()
    to_visit = [(base_url, 0)]
    page_count = 0

    while to_visit and page_count < max_pages:
        current_url, depth = to_visit.pop(0)
        normalized = current_url.rstrip("/")
        if normalized in visited:
            continue
        visited.add(normalized)

        resp = fetch_url(current_url)
        if resp.get("error"):
            results["errors"].append({"url": current_url, "error": resp["error"]})
            print(f"  ✗ {current_url} — {resp['error']}")
            continue

        page_count += 1
        page_data = {
            "url": current_url,
            "final_url": resp.get("final_url"),
            "status_code": resp.get("status_code"),
            "content_length": resp.get("content_length"),
            "elapsed_ms": resp.get("elapsed_ms"),
            "headers": resp.get("headers", {}),
            "redirects": resp.get("redirects", []),
        }

        # Parse HTML
        html = resp.get("content", "")
        soup = BeautifulSoup(html, "lxml")

        # Extract SEO elements
        page_data["title"] = soup.title.string.strip() if soup.title and soup.title.string else None
        meta_desc = soup.find("meta", attrs={"name": "description"})
        page_data["meta_description"] = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else None
        meta_robots = soup.find("meta", attrs={"name": "robots"})
        page_data["meta_robots"] = meta_robots["content"] if meta_robots and meta_robots.get("content") else None
        canonical = soup.find("link", attrs={"rel": "canonical"})
        page_data["canonical"] = canonical["href"] if canonical and canonical.get("href") else None
        viewport = soup.find("meta", attrs={"name": "viewport"})
        page_data["has_viewport"] = viewport is not None
        charset = soup.find("meta", attrs={"charset": True}) or soup.find("meta", attrs={"http-equiv": "Content-Type"})
        page_data["has_charset"] = charset is not None

        # Headers
        headers_data = {}
        for level in range(1, 7):
            tags = soup.find_all(f"h{level}")
            headers_data[f"h{level}"] = [tag.get_text(strip=True) for tag in tags]
        page_data["headings"] = headers_data

        # Images
        images = []
        for img in soup.find_all("img"):
            images.append({
                "src": img.get("src", ""),
                "alt": img.get("alt", ""),
                "has_alt": bool(img.get("alt", "").strip()),
                "loading": img.get("loading", ""),
                "width": img.get("width"),
                "height": img.get("height"),
            })
        page_data["images"] = images
        page_data["images_without_alt"] = sum(1 for i in images if not i["has_alt"])

        # Internal links
        internal_links = extract_internal_links(html, base_url)
        page_data["internal_links_count"] = len(internal_links)

        # External links
        ext_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full = urljoin(base_url, href)
            parsed = urlparse(full)
            if parsed.netloc and parsed.netloc != urlparse(base_url).netloc and parsed.netloc != "www." + urlparse(base_url).netloc:
                ext_links.append({"url": full, "text": a.get_text(strip=True)[:100], "rel": a.get("rel", [])})
        page_data["external_links"] = ext_links
        page_data["external_links_count"] = len(ext_links)

        # Schema / Structured data
        schemas = []
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                schema = json.loads(script.string)
                schemas.append(schema)
            except (json.JSONDecodeError, TypeError):
                schemas.append({"error": "Invalid JSON-LD", "raw": str(script.string)[:200]})
        page_data["schema_markup"] = schemas
        page_data["schema_types"] = []
        for s in schemas:
            if isinstance(s, dict) and "@type" in s:
                page_data["schema_types"].append(s["@type"])
            elif isinstance(s, dict) and "@graph" in s:
                for item in s["@graph"]:
                    if isinstance(item, dict) and "@type" in item:
                        page_data["schema_types"].append(item["@type"])

        # Open Graph
        og_tags = {}
        for meta in soup.find_all("meta", property=True):
            if meta["property"].startswith("og:"):
                og_tags[meta["property"]] = meta.get("content", "")
        page_data["og_tags"] = og_tags

        # Twitter Card
        tw_tags = {}
        for meta in soup.find_all("meta", attrs={"name": True}):
            if meta["name"].startswith("twitter:"):
                tw_tags[meta["name"]] = meta.get("content", "")
        page_data["twitter_tags"] = tw_tags

        # Content stats
        body = soup.find("body")
        if body:
            # Remove script and style tags for text extraction
            for tag in body.find_all(["script", "style", "noscript"]):
                tag.decompose()
            text = body.get_text(separator=" ", strip=True)
            words = text.split()
            page_data["word_count"] = len(words)
            page_data["text_content_preview"] = " ".join(words[:100])
        else:
            page_data["word_count"] = 0
            page_data["text_content_preview"] = ""

        # Hreflang
        hreflangs = []
        for link in soup.find_all("link", rel="alternate"):
            if link.get("hreflang"):
                hreflangs.append({"lang": link["hreflang"], "href": link.get("href", "")})
        page_data["hreflang"] = hreflangs

        # Resource hints
        preloads = [link.get("href", "") for link in soup.find_all("link", rel="preload")]
        prefetches = [link.get("href", "") for link in soup.find_all("link", rel="prefetch")]
        page_data["preloads"] = preloads
        page_data["prefetches"] = prefetches

        # CSS and JS count
        page_data["css_files"] = len(soup.find_all("link", rel="stylesheet"))
        page_data["js_files"] = len(soup.find_all("script", src=True))
        page_data["inline_scripts"] = len(soup.find_all("script", src=False))

        # Save page HTML
        safe_path = urlparse(current_url).path.strip("/").replace("/", "_") or "index"
        (domain_dir / f"page_{safe_path}.html").write_text(html)

        results["pages"][current_url] = page_data
        print(f"  ✓ [{page_count}/{max_pages}] {current_url} ({page_data['word_count']} words, {resp.get('elapsed_ms', 0)}ms)")

        # Queue internal links for deeper crawling
        if depth < max_depth:
            for link in internal_links:
                norm = link.rstrip("/")
                if norm not in visited:
                    to_visit.append((link, depth + 1))

        time.sleep(0.5)  # Be polite

    # 4. Summary
    print(f"\n[4/4] Crawl complete!")
    results["summary"] = {
        "total_pages_crawled": page_count,
        "total_errors": len(results["errors"]),
        "unique_internal_links_found": len(visited),
    }

    # Save results
    output_path = domain_dir / "crawl_data.json"
    output_path.write_text(json.dumps(results, indent=2, default=str))
    print(f"\n  Data saved to: {output_path}")

    # Print quick summary
    print(f"\n{'='*60}")
    print(f"  CRAWL SUMMARY — {domain}")
    print(f"{'='*60}")
    print(f"  Pages crawled:  {page_count}")
    print(f"  Errors:         {len(results['errors'])}")
    print(f"  Robots.txt:     {'✓ Found' if results['robots_txt'].get('exists') else '✗ Missing'}")
    print(f"  Sitemap:        {'✓ Found' if results.get('sitemap', {}).get('exists') else '✗ Missing'}")
    if results.get("sitemap", {}).get("exists"):
        sm = results["sitemap"]["parsed"]
        count = len(sm.get("urls", [])) or len(sm.get("sitemaps", []))
        print(f"  Sitemap entries: {count}")
    print(f"{'='*60}\n")

    return results


def load_from_file(filepath, domain):
    """Load HTML from a file and create crawl data structure."""
    domain_dir = DATA_DIR / domain.replace(".", "_")
    domain_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  SEO AGENT — Loading from file for {domain}")
    print(f"{'='*60}\n")

    html = Path(filepath).read_text(errors="replace")
    soup = BeautifulSoup(html, "lxml")
    base_url = f"https://{domain}"

    results = {
        "domain": domain,
        "base_url": base_url,
        "crawl_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": f"file:{filepath}",
        "pages": {},
        "robots_txt": {"exists": False, "content": "", "note": "Not available (loaded from file)"},
        "sitemap": {"exists": False, "note": "Not available (loaded from file)"},
        "errors": [],
        "network_accessible": False,
    }

    # Parse the same way as live crawl
    page_data = {"url": base_url, "status_code": 200}
    page_data["title"] = soup.title.string.strip() if soup.title and soup.title.string else None
    meta_desc = soup.find("meta", attrs={"name": "description"})
    page_data["meta_description"] = meta_desc["content"].strip() if meta_desc and meta_desc.get("content") else None
    meta_robots = soup.find("meta", attrs={"name": "robots"})
    page_data["meta_robots"] = meta_robots["content"] if meta_robots and meta_robots.get("content") else None
    canonical = soup.find("link", attrs={"rel": "canonical"})
    page_data["canonical"] = canonical["href"] if canonical and canonical.get("href") else None
    viewport = soup.find("meta", attrs={"name": "viewport"})
    page_data["has_viewport"] = viewport is not None

    # Headers
    headers_data = {}
    for level in range(1, 7):
        tags = soup.find_all(f"h{level}")
        headers_data[f"h{level}"] = [tag.get_text(strip=True) for tag in tags]
    page_data["headings"] = headers_data

    # Images
    images = []
    for img in soup.find_all("img"):
        images.append({
            "src": img.get("src", ""),
            "alt": img.get("alt", ""),
            "has_alt": bool(img.get("alt", "").strip()),
            "loading": img.get("loading", ""),
        })
    page_data["images"] = images
    page_data["images_without_alt"] = sum(1 for i in images if not i["has_alt"])

    # Schema
    schemas = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            schemas.append(json.loads(script.string))
        except:
            schemas.append({"error": "Invalid JSON-LD"})
    page_data["schema_markup"] = schemas
    page_data["schema_types"] = []
    for s in schemas:
        if isinstance(s, dict) and "@type" in s:
            page_data["schema_types"].append(s["@type"])

    # OG tags
    og_tags = {}
    for meta in soup.find_all("meta", property=True):
        if meta["property"].startswith("og:"):
            og_tags[meta["property"]] = meta.get("content", "")
    page_data["og_tags"] = og_tags

    # Content
    body = soup.find("body")
    if body:
        for tag in body.find_all(["script", "style", "noscript"]):
            tag.decompose()
        text = body.get_text(separator=" ", strip=True)
        words = text.split()
        page_data["word_count"] = len(words)
        page_data["text_content_preview"] = " ".join(words[:100])
    else:
        page_data["word_count"] = 0

    page_data["internal_links_count"] = len(extract_internal_links(html, base_url))
    page_data["css_files"] = len(soup.find_all("link", rel="stylesheet"))
    page_data["js_files"] = len(soup.find_all("script", src=True))

    results["pages"][base_url] = page_data
    results["summary"] = {"total_pages_crawled": 1, "total_errors": 0}

    # Save
    (domain_dir / "crawl_data.json").write_text(json.dumps(results, indent=2, default=str))
    (domain_dir / "page_index.html").write_text(html)
    print(f"  ✓ Parsed: {page_data.get('title', 'No title')}")
    print(f"  ✓ Words: {page_data['word_count']}")
    print(f"  ✓ Schema types: {page_data['schema_types'] or 'None found'}")
    print(f"  ✓ Data saved to: {domain_dir}/\n")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO Agent Crawler")
    parser.add_argument("--url", help="URL to crawl")
    parser.add_argument("--depth", type=int, default=2, help="Crawl depth (default: 2)")
    parser.add_argument("--max-pages", type=int, default=50, help="Max pages to crawl (default: 50)")
    parser.add_argument("--from-file", help="Load HTML from a file instead of crawling")
    parser.add_argument("--domain", help="Domain name (required with --from-file)")
    args = parser.parse_args()

    if args.from_file:
        if not args.domain:
            print("ERROR: --domain required when using --from-file")
            sys.exit(1)
        load_from_file(args.from_file, args.domain)
    elif args.url:
        crawl_site(args.url, max_depth=args.depth, max_pages=args.max_pages)
    else:
        print("ERROR: Provide --url or --from-file")
        sys.exit(1)
