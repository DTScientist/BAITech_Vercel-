#!/usr/bin/env python3
"""
SEO Agent — Browser Data Ingester
Converts browser-collected JSON into the standard crawl_data.json format
so the audit pipeline can process it seamlessly.
"""

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


def ingest_single_page(filepath, domain=None):
    """Ingest a single-page browser collection."""
    data = json.loads(Path(filepath).read_text())
    
    if not domain:
        domain = data.get("domain", "unknown")
    
    domain_dir = DATA_DIR / domain.replace(".", "_")
    domain_dir.mkdir(parents=True, exist_ok=True)
    
    base_url = f"https://{domain}"
    url = data.get("url", base_url)
    
    # Convert to crawl_data format
    crawl_data = {
        "domain": domain,
        "base_url": base_url,
        "crawl_time": data.get("timestamp", ""),
        "source": f"browser_single:{filepath}",
        "pages": {},
        "robots_txt": {"exists": False, "content": "", "note": "Not captured via browser collector"},
        "sitemap": {"exists": False, "note": "Not captured via browser collector"},
        "errors": [],
        "network_accessible": False,
    }
    
    # Map single page data
    page = {
        "url": url,
        "final_url": url,
        "status_code": 200,
        "content_length": data.get("html_length", 0),
        "elapsed_ms": data.get("performance", {}).get("full_load_ms", 0),
        "headers": {},
        "redirects": [],
        "title": data.get("title"),
        "meta_description": data.get("meta_description"),
        "meta_robots": data.get("meta_robots"),
        "canonical": data.get("canonical"),
        "has_viewport": bool(data.get("meta_viewport")),
        "has_charset": bool(data.get("meta_charset")),
        "headings": data.get("headings", {}),
        "images": data.get("images", []),
        "images_without_alt": data.get("summary", {}).get("images_missing_alt", 0),
        "internal_links_count": data.get("summary", {}).get("internal_links_count", 0),
        "external_links": data.get("external_links", []),
        "external_links_count": data.get("summary", {}).get("external_links_count", 0),
        "schema_markup": data.get("schema_markup", []),
        "schema_types": data.get("schema_types", []),
        "og_tags": data.get("og_tags", {}),
        "twitter_tags": data.get("twitter_tags", {}),
        "word_count": data.get("word_count", 0),
        "text_content_preview": data.get("text_preview", ""),
        "hreflang": data.get("hreflang", []),
        "preloads": data.get("preloads", []),
        "prefetches": data.get("prefetches", []),
        "css_files": data.get("css_count", 0),
        "js_files": data.get("js_count", 0),
        "inline_scripts": 0,
        "performance": data.get("performance", {}),
    }
    
    crawl_data["pages"][url] = page
    crawl_data["summary"] = {
        "total_pages_crawled": 1,
        "total_errors": 0,
        "unique_internal_links_found": page["internal_links_count"],
    }
    
    # Save
    output = domain_dir / "crawl_data.json"
    output.write_text(json.dumps(crawl_data, indent=2, default=str))
    
    print(f"\n✓ Ingested single page data for {domain}")
    print(f"  URL: {url}")
    print(f"  Title: {page['title']}")
    print(f"  Words: {page['word_count']}")
    print(f"  Schema: {page['schema_types'] or 'None'}")
    print(f"  Saved: {output}\n")
    
    return crawl_data


def ingest_multi_page(filepath, domain=None):
    """Ingest a multi-page browser crawl."""
    data = json.loads(Path(filepath).read_text())
    
    if not domain:
        domain = data.get("domain", "unknown")
    
    domain_dir = DATA_DIR / domain.replace(".", "_")
    domain_dir.mkdir(parents=True, exist_ok=True)
    
    base_url = data.get("base_url", f"https://{domain}")
    
    crawl_data = {
        "domain": domain,
        "base_url": base_url,
        "crawl_time": data.get("timestamp", ""),
        "source": f"browser_multi:{filepath}",
        "pages": {},
        "robots_txt": {"exists": False, "content": "", "note": "Not captured via browser collector"},
        "sitemap": {"exists": False, "note": "Not captured via browser collector"},
        "errors": [],
        "network_accessible": False,
    }
    
    pages_raw = data.get("pages", {})
    page_count = 0
    
    for url, pg in pages_raw.items():
        if pg.get("error"):
            crawl_data["errors"].append({"url": url, "error": pg["error"]})
            continue
        
        page = {
            "url": url,
            "final_url": url,
            "status_code": pg.get("status", 200),
            "content_length": 0,
            "elapsed_ms": 0,
            "headers": {},
            "redirects": [],
            "title": pg.get("title"),
            "meta_description": pg.get("meta_description"),
            "meta_robots": None,
            "canonical": pg.get("canonical"),
            "has_viewport": True,  # Assume modern sites have viewport
            "has_charset": True,
            "headings": {
                "h1": pg.get("h1", []),
                "h2": pg.get("h2", []),
                "h3": [], "h4": [], "h5": [], "h6": [],
            },
            "images": [{"src": "", "alt": "", "has_alt": False}] * pg.get("images_no_alt", 0) +
                      [{"src": "", "alt": "present", "has_alt": True}] * max(0, pg.get("images_total", 0) - pg.get("images_no_alt", 0)),
            "images_without_alt": pg.get("images_no_alt", 0),
            "internal_links_count": pg.get("internal_links", 0),
            "external_links": [],
            "external_links_count": 0,
            "schema_markup": pg.get("schema_markup", []),
            "schema_types": pg.get("schema_types", []),
            "og_tags": pg.get("og_tags", {}),
            "twitter_tags": {},
            "word_count": pg.get("word_count", 0),
            "text_content_preview": "",
            "hreflang": [],
            "preloads": [],
            "prefetches": [],
            "css_files": 0,
            "js_files": 0,
            "inline_scripts": 0,
        }
        
        crawl_data["pages"][url] = page
        page_count += 1
    
    crawl_data["summary"] = {
        "total_pages_crawled": page_count,
        "total_errors": len(crawl_data["errors"]),
    }
    
    # Save
    output = domain_dir / "crawl_data.json"
    output.write_text(json.dumps(crawl_data, indent=2, default=str))
    
    print(f"\n✓ Ingested multi-page crawl for {domain}")
    print(f"  Pages: {page_count}")
    print(f"  Errors: {len(crawl_data['errors'])}")
    print(f"  Saved: {output}\n")
    
    return crawl_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO Agent — Ingest browser-collected data")
    parser.add_argument("--file", required=True, help="Path to browser-collected JSON file")
    parser.add_argument("--domain", help="Override domain name")
    parser.add_argument("--type", choices=["single", "multi", "auto"], default="auto", help="Data type")
    args = parser.parse_args()
    
    data = json.loads(Path(args.file).read_text())
    collector_type = data.get("_collector", "")
    
    if args.type == "auto":
        if "multi" in collector_type or "pages" in data:
            ingest_multi_page(args.file, args.domain)
        else:
            ingest_single_page(args.file, args.domain)
    elif args.type == "multi":
        ingest_multi_page(args.file, args.domain)
    else:
        ingest_single_page(args.file, args.domain)
