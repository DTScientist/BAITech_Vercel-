#!/usr/bin/env python3
"""
SEO Ecosystem — Core Web Vitals Collector
Uses Google PageSpeed Insights API (free, no key required for basic usage).
Monitors LCP, CLS, INP, FCP, TTFB across key pages.
"""

import json
import sys
import time
from datetime import date, datetime
from pathlib import Path

import requests

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "ecosystem.json"
DATA_DIR = BASE_DIR / "data" / "audits"


def load_config():
    return json.loads(CONFIG_PATH.read_text())


def check_pagespeed(url, strategy="mobile", api_key=""):
    """Check PageSpeed Insights for a URL."""
    api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {"url": url, "strategy": strategy, "category": "performance"}
    if api_key:
        params["key"] = api_key

    try:
        resp = requests.get(api_url, params=params, timeout=60)
        if resp.status_code != 200:
            return {"url": url, "error": f"HTTP {resp.status_code}", "strategy": strategy}

        data = resp.json()
        lr = data.get("lighthouseResult", {})
        audits = lr.get("audits", {})

        result = {
            "url": url,
            "strategy": strategy,
            "score": round((lr.get("categories", {}).get("performance", {}).get("score", 0)) * 100),
            "metrics": {
                "lcp_ms": round(audits.get("largest-contentful-paint", {}).get("numericValue", 0)),
                "fcp_ms": round(audits.get("first-contentful-paint", {}).get("numericValue", 0)),
                "cls": round(audits.get("cumulative-layout-shift", {}).get("numericValue", 0), 3),
                "tbt_ms": round(audits.get("total-blocking-time", {}).get("numericValue", 0)),
                "speed_index_ms": round(audits.get("speed-index", {}).get("numericValue", 0)),
            },
            "opportunities": [],
        }

        # Extract top optimization opportunities
        for key in ["render-blocking-resources", "unused-css", "unused-javascript",
                     "modern-image-formats", "uses-optimized-images", "efficient-animated-content"]:
            audit = audits.get(key, {})
            if audit.get("score") is not None and audit["score"] < 0.9:
                savings = audit.get("details", {}).get("overallSavingsMs", 0)
                if savings > 0:
                    result["opportunities"].append({
                        "id": key,
                        "title": audit.get("title", key),
                        "savings_ms": round(savings),
                    })

        return result

    except Exception as e:
        return {"url": url, "error": str(e)[:200], "strategy": strategy}


def run_cwv_check(config=None):
    """Check CWV for key pages on our site and competitors."""
    if not config:
        config = load_config()

    site_url = config["site_url"]
    api_key = config.get("apis", {}).get("pagespeed_insights", {}).get("api_key", "")

    # Key pages to test
    pages = [
        site_url + "/",
        site_url + "/4-seater",
        site_url + "/event-organizers",
        site_url + "/faq",
        site_url + "/contacts",
    ]

    # Add competitor homepage
    for comp in config.get("competitors", []):
        pages.append(comp["url"] + "/")

    today = date.today().isoformat()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  CORE WEB VITALS CHECK — {today}")
    print(f"{'='*60}\n")

    results = {"date": today, "timestamp": datetime.now().isoformat(), "pages": []}

    for url in pages:
        print(f"  Testing: {url}...")
        result = check_pagespeed(url, "mobile", api_key)
        results["pages"].append(result)

        if "error" not in result:
            score = result["score"]
            lcp = result["metrics"]["lcp_ms"]
            cls_val = result["metrics"]["cls"]

            grade = "🟢" if score >= 90 else "🟡" if score >= 50 else "🔴"
            lcp_grade = "🟢" if lcp <= 2500 else "🟡" if lcp <= 4000 else "🔴"
            cls_grade = "🟢" if cls_val <= 0.1 else "🟡" if cls_val <= 0.25 else "🔴"

            print(f"    {grade} Score: {score}/100 | {lcp_grade} LCP: {lcp}ms | {cls_grade} CLS: {cls_val}")

            # Alert on bad scores
            if score < 50:
                result["alert"] = f"CRITICAL: Performance score {score}/100 is very low"
            if lcp > config.get("alert_thresholds", {}).get("cwv_lcp_ms", 2500):
                result["alert"] = f"LCP {lcp}ms exceeds threshold"
        else:
            print(f"    ⚠ Error: {result['error'][:60]}")

        time.sleep(2)  # Rate limit

    # Save
    output = DATA_DIR / f"cwv_{today}.json"
    output.write_text(json.dumps(results, indent=2))
    print(f"\n  Saved: {output}")
    return results


if __name__ == "__main__":
    run_cwv_check()
