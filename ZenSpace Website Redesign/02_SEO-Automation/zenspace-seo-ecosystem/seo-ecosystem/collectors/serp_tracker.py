#!/usr/bin/env python3
"""
SEO Ecosystem — SERP Tracker
Tracks Google search rankings for target keywords.
Uses Google Custom Search API (free tier: 100 queries/day) or scraping fallback.
Stores historical data for trend analysis.
"""

import json
import os
import re
import sys
import time
from datetime import datetime, date
from pathlib import Path
from urllib.parse import quote_plus, urlparse

import requests

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "ecosystem.json"
DATA_DIR = BASE_DIR / "data" / "rankings"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def load_config():
    return json.loads(CONFIG_PATH.read_text())


def check_serp_google_api(keyword, domain, api_key, cx_id=None):
    """Check ranking via Google Custom Search JSON API (free: 100/day)."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "q": keyword, "num": 10}
    if cx_id:
        params["cx"] = cx_id

    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code != 200:
            return {"keyword": keyword, "rank": None, "error": f"API {resp.status_code}"}

        data = resp.json()
        items = data.get("items", [])
        for i, item in enumerate(items):
            link = item.get("link", "")
            if domain in link:
                return {
                    "keyword": keyword,
                    "rank": i + 1,
                    "url": link,
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                }
        return {"keyword": keyword, "rank": None, "note": "Not in top 10"}

    except Exception as e:
        return {"keyword": keyword, "rank": None, "error": str(e)[:200]}


def check_serp_scrape(keyword, domain, num_results=30):
    """
    Check ranking by scraping Google search results.
    Falls back to this when no API key is configured.
    Respectful: 2-second delays, standard headers.
    """
    url = f"https://www.google.com/search?q={quote_plus(keyword)}&num={num_results}&hl=en&gl=us"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return {"keyword": keyword, "rank": None, "error": f"HTTP {resp.status_code}"}

        html = resp.text

        # Extract search result URLs from Google's HTML
        # Pattern: /url?q=https://...&
        urls_found = re.findall(r'/url\?q=(https?://[^&]+)&', html)
        # Also try: href="https://..." in result divs
        urls_found += re.findall(r'href="(https?://(?:www\.)?[^"]*' + re.escape(domain) + r'[^"]*)"', html)

        # Deduplicate while preserving order
        seen = set()
        unique_urls = []
        for u in urls_found:
            parsed = urlparse(u)
            # Skip Google's own domains
            if "google." in parsed.netloc:
                continue
            if u not in seen:
                seen.add(u)
                unique_urls.append(u)

        # Find our domain
        for i, url in enumerate(unique_urls):
            if domain in url:
                return {
                    "keyword": keyword,
                    "rank": i + 1,
                    "url": url,
                    "method": "scrape",
                }

        # Also check for competitors
        competitor_positions = {}
        for i, url in enumerate(unique_urls[:10]):
            competitor_positions[urlparse(url).netloc] = i + 1

        return {
            "keyword": keyword,
            "rank": None,
            "note": f"Not in top {min(len(unique_urls), num_results)}",
            "top_domains": competitor_positions,
            "method": "scrape",
        }

    except Exception as e:
        return {"keyword": keyword, "rank": None, "error": str(e)[:200]}


def track_all_keywords(config=None):
    """Track rankings for all configured keywords."""
    if not config:
        config = load_config()

    domain = config["domain"]
    keywords = config.get("tracked_keywords", [])
    api_key = config.get("apis", {}).get("google_custom_search", {}).get("api_key", "")

    today = date.today().isoformat()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  SERP TRACKER — {domain}")
    print(f"  Date: {today} | Keywords: {len(keywords)}")
    print(f"{'='*60}\n")

    results = {
        "date": today,
        "domain": domain,
        "timestamp": datetime.now().isoformat(),
        "keywords": [],
        "summary": {},
    }

    ranked_count = 0
    total_rank = 0

    for i, kw_config in enumerate(keywords):
        keyword = kw_config["keyword"]
        priority = kw_config.get("priority", 3)

        if api_key:
            result = check_serp_google_api(keyword, domain, api_key)
        else:
            result = check_serp_scrape(keyword, domain)
            time.sleep(2)  # Be respectful

        result["priority"] = priority
        result["intent"] = kw_config.get("intent", "unknown")

        rank = result.get("rank")
        rank_str = f"#{rank}" if rank else "—"
        icon = "🟢" if rank and rank <= 3 else "🟡" if rank and rank <= 10 else "🔴"

        print(f"  {icon} {rank_str:>4s}  {keyword}")

        results["keywords"].append(result)

        if rank:
            ranked_count += 1
            total_rank += rank

    # Summary
    total = len(keywords)
    in_top3 = sum(1 for r in results["keywords"] if r.get("rank") and r["rank"] <= 3)
    in_top10 = sum(1 for r in results["keywords"] if r.get("rank") and r["rank"] <= 10)
    in_top30 = sum(1 for r in results["keywords"] if r.get("rank") and r["rank"] <= 30)
    avg_rank = round(total_rank / ranked_count, 1) if ranked_count > 0 else None

    results["summary"] = {
        "total_keywords": total,
        "ranked": ranked_count,
        "not_ranked": total - ranked_count,
        "top_3": in_top3,
        "top_10": in_top10,
        "top_30": in_top30,
        "avg_rank": avg_rank,
    }

    # Save
    output_file = DATA_DIR / f"serp_{today}.json"
    output_file.write_text(json.dumps(results, indent=2))

    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"  Ranked: {ranked_count}/{total} | Top 3: {in_top3} | Top 10: {in_top10}")
    if avg_rank:
        print(f"  Average rank: #{avg_rank}")
    print(f"  Saved: {output_file}")
    print(f"{'='*60}\n")

    return results


def compare_rankings(date1=None, date2=None):
    """Compare rankings between two dates to detect movement."""
    files = sorted(DATA_DIR.glob("serp_*.json"))
    if len(files) < 2:
        print("Need at least 2 days of data to compare.")
        return None

    data1 = json.loads(files[-2].read_text()) if not date1 else json.loads((DATA_DIR / f"serp_{date1}.json").read_text())
    data2 = json.loads(files[-1].read_text()) if not date2 else json.loads((DATA_DIR / f"serp_{date2}.json").read_text())

    changes = []
    for kw2 in data2["keywords"]:
        keyword = kw2["keyword"]
        rank2 = kw2.get("rank")
        rank1 = None
        for kw1 in data1["keywords"]:
            if kw1["keyword"] == keyword:
                rank1 = kw1.get("rank")
                break

        if rank1 and rank2:
            change = rank1 - rank2  # Positive = improved
            if abs(change) >= 1:
                changes.append({"keyword": keyword, "old_rank": rank1, "new_rank": rank2, "change": change})
        elif rank2 and not rank1:
            changes.append({"keyword": keyword, "old_rank": None, "new_rank": rank2, "change": "NEW"})
        elif rank1 and not rank2:
            changes.append({"keyword": keyword, "old_rank": rank1, "new_rank": None, "change": "LOST"})

    return changes


def get_ranking_history(keyword, days=30):
    """Get historical rankings for a specific keyword."""
    files = sorted(DATA_DIR.glob("serp_*.json"))
    history = []
    for f in files[-days:]:
        data = json.loads(f.read_text())
        for kw in data["keywords"]:
            if kw["keyword"] == keyword:
                history.append({"date": data["date"], "rank": kw.get("rank")})
                break
    return history


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SERP Tracker")
    parser.add_argument("--compare", action="store_true", help="Compare latest two days")
    parser.add_argument("--history", help="Show ranking history for a keyword")
    args = parser.parse_args()

    if args.compare:
        changes = compare_rankings()
        if changes:
            for c in sorted(changes, key=lambda x: abs(x["change"]) if isinstance(x["change"], int) else 999, reverse=True):
                icon = "📈" if isinstance(c["change"], int) and c["change"] > 0 else "📉" if isinstance(c["change"], int) else "🆕" if c["change"] == "NEW" else "💀"
                print(f"  {icon} {c['keyword']}: {c['old_rank'] or '—'} → {c['new_rank'] or '—'} ({c['change']})")
    elif args.history:
        history = get_ranking_history(args.history)
        for h in history:
            print(f"  {h['date']}: #{h['rank'] or '—'}")
    else:
        track_all_keywords()
