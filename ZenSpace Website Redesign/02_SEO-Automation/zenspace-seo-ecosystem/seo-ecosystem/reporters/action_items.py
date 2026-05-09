#!/usr/bin/env python3
"""
SEO Ecosystem — Action Items Generator
Analyzes all collected data and generates priority-ranked next actions.
"""

import json
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


def generate_action_items():
    """Analyze all data sources and generate prioritized actions."""
    actions = []

    # ─── Check ranking data ───
    ranking_files = sorted((DATA_DIR / "rankings").glob("serp_*.json"))
    if ranking_files:
        latest = json.loads(ranking_files[-1].read_text())
        summary = latest.get("summary", {})

        if summary.get("not_ranked", 0) > summary.get("ranked", 0):
            actions.append({
                "priority": 1,
                "category": "Rankings",
                "action": f"Most tracked keywords aren't ranking. Focus on creating dedicated landing pages for transactional keywords.",
                "detail": f"{summary['not_ranked']} of {summary['total_keywords']} keywords have no ranking.",
            })

        # Check for keywords close to page 1
        for kw in latest.get("keywords", []):
            rank = kw.get("rank")
            if rank and 11 <= rank <= 20:
                actions.append({
                    "priority": 2,
                    "category": "Quick Win",
                    "action": f"'{kw['keyword']}' is at position #{rank} — close to page 1. Optimize the ranking page with better content and internal links.",
                    "keyword": kw["keyword"],
                })

        # Check for ranking declines
        if len(ranking_files) >= 2:
            prev = json.loads(ranking_files[-2].read_text())
            for kw_new in latest.get("keywords", []):
                for kw_old in prev.get("keywords", []):
                    if kw_new["keyword"] == kw_old["keyword"]:
                        r_new = kw_new.get("rank")
                        r_old = kw_old.get("rank")
                        if r_old and r_new and r_new > r_old + 5:
                            actions.append({
                                "priority": 1,
                                "category": "Alert",
                                "action": f"'{kw_new['keyword']}' dropped from #{r_old} to #{r_new}. Investigate and fix.",
                            })
    else:
        actions.append({
            "priority": 1,
            "category": "Setup",
            "action": "Run SERP tracking: python3 collectors/serp_tracker.py",
            "detail": "No ranking data collected yet. Start tracking to measure progress.",
        })

    # ─── Check CWV data ───
    cwv_files = sorted((DATA_DIR / "audits").glob("cwv_*.json"))
    if cwv_files:
        latest_cwv = json.loads(cwv_files[-1].read_text())
        for page in latest_cwv.get("pages", []):
            score = page.get("score", 100)
            if score < 50 and "zenspace" in page.get("url", "").lower():
                actions.append({
                    "priority": 2,
                    "category": "Performance",
                    "action": f"Page score {score}/100 on {page['url']}. Review Wix apps and image sizes.",
                    "metrics": page.get("metrics"),
                })
    else:
        actions.append({
            "priority": 2,
            "category": "Setup",
            "action": "Run CWV check: python3 collectors/pagespeed.py",
        })

    # ─── Check competitor data ───
    comp_files = sorted((DATA_DIR / "competitors").glob("*_latest.json"))
    if comp_files:
        for f in comp_files:
            comp = json.loads(f.read_text())
            changes = comp.get("changes", {})
            for new_page in changes.get("new_pages", []):
                actions.append({
                    "priority": 2,
                    "category": "Competitor",
                    "action": f"Competitor added new page: {new_page}. Consider creating equivalent content.",
                })
            for schema_change in changes.get("schema_changes", []):
                added = schema_change.get("added", [])
                if added:
                    actions.append({
                        "priority": 2,
                        "category": "Competitor",
                        "action": f"Competitor added schema: {', '.join(added)} on {schema_change['url']}",
                    })
    else:
        actions.append({
            "priority": 2,
            "category": "Setup",
            "action": "Run competitor scan: python3 collectors/competitor_monitor.py",
        })

    # ─── Check task completion ───
    task_file = Path(__file__).parent.parent.parent / "skills" / "seo-agent" / "agent" / "task_status.json"
    if task_file.exists():
        status = json.loads(task_file.read_text())
        completed = len(status.get("completed", []))
        if completed < 20:
            remaining = 20 - completed
            actions.append({
                "priority": 1,
                "category": "Implementation",
                "action": f"{remaining} SEO fix tasks remaining. Run /next in Telegram bot to continue.",
                "detail": f"Completed {completed}/20 tasks. Schema and meta tag fixes pending.",
            })

    # ─── Standing recommendations ───
    actions.append({
        "priority": 3,
        "category": "Content",
        "action": "Create /event-pod-rental/ landing page targeting primary transactional keyword",
    })
    actions.append({
        "priority": 3,
        "category": "AIEO",
        "action": "Create /what-is-an-event-pod/ definitional page for AI citation eligibility",
    })
    actions.append({
        "priority": 3,
        "category": "Content",
        "action": "Publish 2 new blog posts targeting informational keywords this week",
    })
    actions.append({
        "priority": 3,
        "category": "Images",
        "action": "Add alt text to 50 images this week (product pages first)",
    })

    # Sort by priority
    actions.sort(key=lambda x: x["priority"])

    # Print
    print(f"\n{'='*60}")
    print(f"  ACTION ITEMS — {date.today().isoformat()}")
    print(f"  {len(actions)} items identified")
    print(f"{'='*60}\n")

    for i, a in enumerate(actions, 1):
        icon = {1: "🔴", 2: "🟠", 3: "🟡"}.get(a["priority"], "⚪")
        print(f"  {i:2d}. {icon} [{a['category']}] {a['action']}")
        if a.get("detail"):
            print(f"      ↳ {a['detail']}")

    # Save
    output = DATA_DIR / "reports" / f"actions_{date.today().isoformat()}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(actions, indent=2))

    return actions


if __name__ == "__main__":
    generate_action_items()
