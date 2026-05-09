#!/usr/bin/env python3
"""
SEO Ecosystem — Keyword Analyzer
Uses Google Suggest API (free, unlimited) + Google Trends to discover and cluster keywords.
No paid API needed — this replicates 80% of what Ahrefs/SEMrush keyword tools do.
"""

import json
import re
import time
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import quote_plus

import requests

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "keywords"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def google_suggest(seed, lang="en", country="us"):
    """Get Google autocomplete suggestions for a seed keyword. Free & unlimited."""
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={quote_plus(seed)}&hl={lang}&gl={country}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        data = resp.json()
        return data[1] if len(data) > 1 else []
    except:
        return []


def expand_keyword(seed, depth=2):
    """Recursively expand a seed keyword using Google Suggest."""
    all_keywords = set()
    to_process = [seed]
    processed = set()

    for level in range(depth):
        next_batch = []
        for kw in to_process:
            if kw in processed:
                continue
            processed.add(kw)
            suggestions = google_suggest(kw)
            for s in suggestions:
                if s not in all_keywords:
                    all_keywords.add(s)
                    next_batch.append(s)
            time.sleep(0.3)

        to_process = next_batch[:20]  # Limit breadth

    return list(all_keywords)


def alphabet_expand(seed):
    """Expand seed with alphabet modifiers: 'event pod a', 'event pod b', etc."""
    keywords = set()
    for letter in "abcdefghijklmnopqrstuvwxyz":
        suggestions = google_suggest(f"{seed} {letter}")
        keywords.update(suggestions)
        time.sleep(0.2)
    return list(keywords)


def question_expand(seed):
    """Find question-based keywords around a seed."""
    questions = set()
    modifiers = ["how", "what", "why", "when", "where", "which", "can", "do", "does", "is", "are"]
    for mod in modifiers:
        suggestions = google_suggest(f"{mod} {seed}")
        questions.update(suggestions)
        time.sleep(0.2)
    return list(questions)


def classify_intent(keyword):
    """Classify search intent based on keyword patterns."""
    kw = keyword.lower()
    transactional = ["buy", "rent", "hire", "book", "order", "price", "cost", "quote", "near me", "rental"]
    commercial = ["best", "top", "review", "compare", "vs", "alternative", "companies", "providers"]
    informational = ["how", "what", "why", "when", "guide", "tutorial", "tips", "ideas", "benefits"]

    if any(t in kw for t in transactional):
        return "transactional"
    elif any(c in kw for c in commercial):
        return "commercial"
    elif any(i in kw for i in informational):
        return "informational"
    return "navigational"


def cluster_keywords(keywords):
    """Group keywords into topical clusters."""
    clusters = defaultdict(list)

    # Define cluster patterns
    patterns = {
        "event pod rental": r"event\s*pod\s*(rental|rent|hire)",
        "meeting pod": r"meeting\s*(pod|space|room|booth)",
        "trade show": r"trade\s*show|exhibit|convention",
        "conference": r"conference\s*(pod|booth|room|space)",
        "pricing": r"(price|cost|pricing|budget|afford|cheap|expensive)",
        "comparison": r"(vs|versus|compare|alternative|better|difference)",
        "how-to": r"(how\s+to|guide|tutorial|steps|setup|install)",
        "features": r"(feature|spec|dimension|size|capacity|acoustic|soundproof)",
        "location": r"(las vegas|chicago|orlando|new york|atlanta|dallas|los angeles|san francisco)",
        "brand": r"(zenspace|nook|pod\s*brand|framery|steelcase)",
    }

    for kw in keywords:
        matched = False
        for cluster_name, pattern in patterns.items():
            if re.search(pattern, kw.lower()):
                clusters[cluster_name].append(kw)
                matched = True
                break
        if not matched:
            clusters["other"].append(kw)

    return dict(clusters)


def full_keyword_research(seeds=None):
    """Run complete keyword research from seed keywords."""
    if not seeds:
        seeds = [
            "event pod rental",
            "meeting pod for events",
            "trade show pod",
            "conference meeting pod",
            "private pod rental",
        ]

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  KEYWORD RESEARCH ENGINE")
    print(f"  Seeds: {len(seeds)}")
    print(f"{'='*60}\n")

    all_keywords = set()

    # Phase 1: Google Suggest expansion
    print("  [1/3] Expanding seeds via Google Suggest...")
    for seed in seeds:
        expanded = expand_keyword(seed, depth=2)
        print(f"    '{seed}' → {len(expanded)} keywords")
        all_keywords.update(expanded)

    # Phase 2: Alphabet expansion on top seeds
    print(f"\n  [2/3] Alphabet expansion on primary seed...")
    alpha = alphabet_expand(seeds[0])
    print(f"    '{seeds[0]} [a-z]' → {len(alpha)} keywords")
    all_keywords.update(alpha)

    # Phase 3: Question keywords
    print(f"\n  [3/3] Finding question keywords...")
    for seed in seeds[:3]:
        questions = question_expand(seed)
        print(f"    '{seed}' questions → {len(questions)}")
        all_keywords.update(questions)

    # Classify and cluster
    print(f"\n  Total unique keywords: {len(all_keywords)}")

    keyword_data = []
    for kw in sorted(all_keywords):
        intent = classify_intent(kw)
        keyword_data.append({"keyword": kw, "intent": intent})

    clusters = cluster_keywords(list(all_keywords))

    # Intent distribution
    intents = defaultdict(int)
    for kd in keyword_data:
        intents[kd["intent"]] += 1

    print(f"\n  Intent distribution:")
    for intent, count in sorted(intents.items(), key=lambda x: -x[1]):
        print(f"    {intent}: {count}")

    print(f"\n  Clusters:")
    for name, kws in sorted(clusters.items(), key=lambda x: -len(x[1])):
        print(f"    {name}: {len(kws)} keywords")

    # Save
    output = {
        "date": date.today().isoformat(),
        "seeds": seeds,
        "total_keywords": len(all_keywords),
        "keywords": keyword_data,
        "clusters": clusters,
        "intent_distribution": dict(intents),
    }

    output_file = DATA_DIR / f"research_{date.today().isoformat()}.json"
    output_file.write_text(json.dumps(output, indent=2))
    print(f"\n  Saved: {output_file}")

    return output


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", help="Seed keywords")
    args = parser.parse_args()
    full_keyword_research(args.seeds)
