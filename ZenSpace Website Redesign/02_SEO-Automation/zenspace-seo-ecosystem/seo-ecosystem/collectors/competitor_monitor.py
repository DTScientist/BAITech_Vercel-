#!/usr/bin/env python3
"""
SEO Ecosystem — Competitor Monitor
Detects changes on competitor sites: new pages, schema changes, content updates, ranking shifts.
"""

import json
import hashlib
import time
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "ecosystem.json"
DATA_DIR = BASE_DIR / "data" / "competitors"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; SEOEcosystem/1.0)"}


def load_config():
    return json.loads(CONFIG_PATH.read_text())


def crawl_competitor(comp_url, max_pages=30):
    """Crawl competitor site and extract SEO signals."""
    try:
        resp = requests.get(comp_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return {"error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)[:200]}

    soup = BeautifulSoup(resp.text, "lxml")
    base_domain = requests.utils.urlparse(comp_url).netloc

    # Extract all internal links
    links = set()
    for a in soup.find_all("a", href=True):
        full = urljoin(comp_url, a["href"])
        if base_domain in full and "#" not in full:
            links.add(full.rstrip("/"))

    # Extract page data
    pages = {}
    pages[comp_url] = extract_page_signals(soup, comp_url)

    for link in list(links)[:max_pages]:
        try:
            r = requests.get(link, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                s = BeautifulSoup(r.text, "lxml")
                pages[link] = extract_page_signals(s, link)
            time.sleep(1)
        except:
            pass

    return {"pages": pages, "total_links_found": len(links)}


def extract_page_signals(soup, url):
    """Extract SEO signals from a page."""
    title = soup.title.string.strip() if soup.title and soup.title.string else None
    meta_desc = None
    md = soup.find("meta", attrs={"name": "description"})
    if md and md.get("content"):
        meta_desc = md["content"]

    h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
    h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]

    schemas = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            schemas.append(json.loads(script.string))
        except:
            pass
    schema_types = set()
    for s in schemas:
        if isinstance(s, dict):
            if "@type" in s: schema_types.add(s["@type"])
            if "@graph" in s:
                for item in s["@graph"]:
                    if isinstance(item, dict) and "@type" in item:
                        schema_types.add(item["@type"])

    body = soup.find("body")
    word_count = 0
    if body:
        for tag in body.find_all(["script", "style", "noscript"]):
            tag.decompose()
        word_count = len(body.get_text(separator=" ", strip=True).split())

    # Content hash for change detection
    content = (title or "") + " ".join(h1s) + " ".join(h2s) + str(len(schemas))
    content_hash = hashlib.md5(content.encode()).hexdigest()

    return {
        "url": url,
        "title": title,
        "meta_description": meta_desc,
        "h1": h1s,
        "h2": h2s,
        "schema_types": list(schema_types),
        "word_count": word_count,
        "content_hash": content_hash,
    }


def detect_changes(domain):
    """Compare current crawl against last saved snapshot."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_file = DATA_DIR / f"{domain.replace('.', '_')}_latest.json"

    previous = json.loads(snapshot_file.read_text()) if snapshot_file.exists() else None

    config = load_config()
    comp = next((c for c in config.get("competitors", []) if c["domain"] == domain), None)
    if not comp:
        print(f"Competitor {domain} not found in config.")
        return None

    print(f"\n  Crawling {domain}...")
    current = crawl_competitor(comp["url"])
    if "error" in current:
        print(f"  Error: {current['error']}")
        return None

    current["date"] = date.today().isoformat()
    current["domain"] = domain

    changes = {"new_pages": [], "removed_pages": [], "content_changes": [], "schema_changes": []}

    if previous:
        prev_urls = set(previous.get("pages", {}).keys())
        curr_urls = set(current.get("pages", {}).keys())

        changes["new_pages"] = list(curr_urls - prev_urls)
        changes["removed_pages"] = list(prev_urls - curr_urls)

        for url in curr_urls & prev_urls:
            curr_page = current["pages"][url]
            prev_page = previous["pages"][url]

            if curr_page.get("content_hash") != prev_page.get("content_hash"):
                changes["content_changes"].append({
                    "url": url,
                    "old_title": prev_page.get("title"),
                    "new_title": curr_page.get("title"),
                    "old_words": prev_page.get("word_count"),
                    "new_words": curr_page.get("word_count"),
                })

            old_schema = set(prev_page.get("schema_types", []))
            new_schema = set(curr_page.get("schema_types", []))
            if old_schema != new_schema:
                changes["schema_changes"].append({
                    "url": url,
                    "added": list(new_schema - old_schema),
                    "removed": list(old_schema - new_schema),
                })

    current["changes"] = changes

    # Save
    snapshot_file.write_text(json.dumps(current, indent=2))
    history_file = DATA_DIR / f"{domain.replace('.', '_')}_{date.today().isoformat()}.json"
    history_file.write_text(json.dumps(current, indent=2))

    # Print changes
    has_changes = any(changes[k] for k in changes)
    if has_changes:
        print(f"\n  🔔 CHANGES DETECTED on {domain}:")
        for p in changes["new_pages"]:
            print(f"    🆕 New page: {p}")
        for p in changes["removed_pages"]:
            print(f"    🗑 Removed: {p}")
        for c in changes["content_changes"]:
            print(f"    ✏️ Updated: {c['url']} ({c['old_words']}→{c['new_words']} words)")
        for c in changes["schema_changes"]:
            print(f"    📋 Schema change: {c['url']} +{c['added']} -{c['removed']}")
    else:
        print(f"  ✓ No changes detected on {domain}")

    return current


def monitor_all_competitors():
    config = load_config()
    print(f"\n{'='*60}")
    print(f"  COMPETITOR MONITOR — {date.today().isoformat()}")
    print(f"{'='*60}")

    for comp in config.get("competitors", []):
        detect_changes(comp["domain"])

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    monitor_all_competitors()
