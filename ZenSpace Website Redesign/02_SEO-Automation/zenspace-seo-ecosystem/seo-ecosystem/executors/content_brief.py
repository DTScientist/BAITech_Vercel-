#!/usr/bin/env python3
"""
SEO Ecosystem — Content Brief Generator
Creates comprehensive content briefs for writers, pre-loaded with:
- Target keyword + related terms
- Competitor analysis (what's ranking)
- Suggested H2 structure
- Internal linking targets
- Schema markup template
- AIEO optimization notes
"""

import json
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "ecosystem.json"
DATA_DIR = BASE_DIR / "data"


def load_config():
    return json.loads(CONFIG_PATH.read_text())


def generate_brief(target_keyword, page_type="blog", word_count=1500):
    """Generate a full content brief for a target keyword."""
    config = load_config()
    site_url = config["site_url"]

    # Load keyword data if available
    kw_files = sorted((DATA_DIR / "keywords").glob("research_*.json"))
    related_keywords = []
    if kw_files:
        kw_data = json.loads(kw_files[-1].read_text())
        all_kws = [k["keyword"] for k in kw_data.get("keywords", [])]
        # Find related keywords
        target_words = set(target_keyword.lower().split())
        for kw in all_kws:
            kw_words = set(kw.lower().split())
            overlap = len(target_words & kw_words)
            if overlap > 0 and kw.lower() != target_keyword.lower():
                related_keywords.append(kw)
        related_keywords = related_keywords[:15]

    # Load existing pages for internal linking
    crawl_file = BASE_DIR.parent / "skills" / "seo-agent" / "data" / "zenspaceevents_com" / "crawl_data.json"
    internal_link_targets = []
    if crawl_file.exists():
        crawl = json.loads(crawl_file.read_text())
        for url, pg in crawl.get("pages", {}).items():
            title = pg.get("title", "")
            if title:
                internal_link_targets.append({"url": url, "title": title})

    # Build the brief
    brief = {
        "generated": date.today().isoformat(),
        "target_keyword": target_keyword,
        "page_type": page_type,
        "target_word_count": word_count,
        "url_slug": f"/{target_keyword.replace(' ', '-').lower()}",

        "seo_title": f"{target_keyword.title()} — [Benefit/Year] | ZenSpace Event Solutions",
        "seo_title_notes": "50-60 characters. Include primary keyword near the start. Add year or benefit.",

        "meta_description": f"[Write 150-160 chars about {target_keyword}. Include a CTA like 'Get a free quote' or 'Learn more'.]",

        "h1": f"{target_keyword.title()} — [Compelling Angle]",
        "h1_notes": "Exactly one H1. Include primary keyword. Make it specific and benefit-driven.",

        "suggested_h2_structure": generate_h2_structure(target_keyword, page_type),

        "primary_keyword": target_keyword,
        "secondary_keywords": related_keywords[:8],
        "lsi_keywords": related_keywords[8:15],

        "content_guidelines": {
            "opening": "Start with a clear definition or value statement in the first paragraph. AI systems extract this for citations.",
            "proof_points": "Include specific numbers: events served (250+), pod types (6), setup time (under 30 min), acoustic privacy (-29dB).",
            "cta": "Include at least 2 CTAs — one mid-content, one at the end. Link to /contacts for quote requests.",
            "internal_links": "Link to 5-8 internal pages naturally within the content.",
            "images": "Include 3-5 images with descriptive alt text containing the target keyword.",
            "readability": "Short paragraphs (3-4 sentences). Use subheadings every 200-300 words.",
        },

        "internal_link_targets": [
            {"url": il["url"], "anchor_suggestion": il["title"][:50]}
            for il in internal_link_targets[:10]
        ],

        "schema_markup": {
            "type": "FAQPage" if page_type == "faq" else "Article" if page_type == "blog" else "WebPage",
            "note": "Add the appropriate schema type after publishing. See the schema implementation guide.",
        },

        "aieo_optimization": {
            "definitional_sentence": f"Write one clear sentence defining {target_keyword} in the first paragraph. Format: '[Topic] is [definition] that [benefit] for [audience].'",
            "faq_section": "Add 3-5 FAQ questions at the end with FAQPage schema markup.",
            "data_points": "Include at least 3 specific statistics or data points that AI systems can cite.",
            "authoritative_framing": "Position ZenSpace as the expert source. Reference 250+ events delivered, founded 2017, nationwide service.",
        },

        "competitor_notes": "Check what currently ranks for this keyword. Match or exceed their content depth. Add what they're missing: specific data, real case studies, interactive elements.",
    }

    return brief


def generate_h2_structure(keyword, page_type):
    """Generate suggested H2 headings based on keyword and page type."""
    kw = keyword.lower()

    if page_type == "pillar":
        return [
            f"What is {keyword.title()}?",
            f"How {keyword.title()} works",
            f"Types of {keyword.title().split()[0]} pods available",
            f"Benefits of {keyword.title()} for events",
            f"{keyword.title()} pricing and packages",
            "How to choose the right pod for your event",
            "Setup and logistics",
            "Case studies and real results",
            "Frequently asked questions",
        ]
    elif page_type == "blog":
        return [
            f"Why {keyword.title()} matters for event organizers",
            "The current landscape",
            "Key benefits you should know",
            "Real-world examples",
            "How to get started",
            "What to look for when choosing a provider",
        ]
    elif page_type == "city":
        city = kw.split()[-1] if len(kw.split()) > 3 else "your city"
        return [
            f"Event pod rental in {city.title()}",
            f"Top venues in {city.title()} for pod deployments",
            "Pod types available",
            "Pricing for events in this market",
            "Setup and delivery details",
            "Recent events we've served",
            "Get a quote",
        ]
    else:
        return [
            f"Understanding {keyword.title()}",
            "Key features and specifications",
            "Use cases",
            "Pricing overview",
            "How to get started",
            "Frequently asked questions",
        ]


def generate_batch_briefs():
    """Generate briefs for all planned content from the calendar."""
    briefs_dir = DATA_DIR / "reports" / "content_briefs"
    briefs_dir.mkdir(parents=True, exist_ok=True)

    planned_content = [
        ("event pod rental", "pillar", 3000),
        ("what is an event pod", "pillar", 2000),
        ("event pod rental cost", "landing", 1500),
        ("event pod vs trade show booth", "blog", 1500),
        ("IoT event technology", "blog", 1200),
        ("event pod rental las vegas", "city", 1000),
        ("event pod rental chicago", "city", 1000),
    ]

    print(f"\n{'='*55}")
    print(f"  CONTENT BRIEF GENERATOR")
    print(f"{'='*55}\n")

    for keyword, ptype, wc in planned_content:
        brief = generate_brief(keyword, ptype, wc)
        filename = keyword.replace(" ", "_") + "_brief.json"
        (briefs_dir / filename).write_text(json.dumps(brief, indent=2))
        print(f"  ✓ {keyword} ({ptype}, {wc} words)")

    print(f"\n  Briefs saved to: {briefs_dir}/")
    print(f"  Total: {len(planned_content)} briefs generated\n")


if __name__ == "__main__":
    generate_batch_briefs()
