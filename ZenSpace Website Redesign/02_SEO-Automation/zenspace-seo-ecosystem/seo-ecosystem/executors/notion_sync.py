#!/usr/bin/env python3
"""
SEO Ecosystem — Notion Sync Executor
Pushes SEO tasks, content calendar, and reports to Notion via MCP.
Designed to be called from Claude Code/Cowork which has native Notion MCP access.

When run standalone, generates Notion-ready JSON that can be imported.
When called from Claude with MCP, directly creates/updates Notion pages.
"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "ecosystem.json"


def load_config():
    return json.loads(CONFIG_PATH.read_text())


def generate_seo_task_database():
    """Generate a Notion-compatible task database from pending SEO fixes."""
    task_file = BASE_DIR.parent / "skills" / "seo-agent" / "agent" / "tasks.py"
    
    # Import tasks
    import sys
    sys.path.insert(0, str(task_file.parent))
    from tasks import TASKS
    
    # Load completion status
    status_file = task_file.parent / "task_status.json"
    completed = []
    if status_file.exists():
        status = json.loads(status_file.read_text())
        completed = status.get("completed", [])

    notion_pages = []
    for task in TASKS:
        status = "Done" if task["id"] in completed else "To Do"
        priority_map = {1: "Critical", 2: "High", 3: "Medium"}
        
        notion_pages.append({
            "object": "page",
            "properties": {
                "Name": {"title": [{"text": {"content": task["name"]}}]},
                "Status": {"select": {"name": status}},
                "Priority": {"select": {"name": priority_map.get(task["priority"], "Medium")}},
                "Category": {"select": {"name": task["category"]}},
                "Time Estimate": {"rich_text": [{"text": {"content": task.get("time_estimate", "5 min")}}]},
                "Description": {"rich_text": [{"text": {"content": task["plain_explanation"][:2000]}}]},
            },
            "_meta": {
                "task_id": task["id"],
                "wix_steps": task.get("wix_steps", []),
                "code": task.get("code", "")[:500] + "..." if len(task.get("code", "")) > 500 else task.get("code", ""),
            }
        })

    return notion_pages


def generate_content_calendar():
    """Generate a content calendar for Notion with SEO-targeted posts."""
    today = date.today()
    
    content_items = [
        {
            "title": "The Complete Guide to Event Pod Rentals in 2026",
            "type": "Pillar Page",
            "target_keyword": "event pod rental",
            "intent": "transactional",
            "word_count": 3000,
            "due_date": (today + timedelta(days=7)).isoformat(),
            "status": "To Write",
            "url_slug": "/event-pod-rental",
            "notes": "Main landing page. Cluster 1 pillar. Target featured snippet with definition.",
        },
        {
            "title": "What Is an Event Pod? Everything You Need to Know",
            "type": "AIEO Page",
            "target_keyword": "what is an event pod",
            "intent": "informational",
            "word_count": 2000,
            "due_date": (today + timedelta(days=10)).isoformat(),
            "status": "To Write",
            "url_slug": "/what-is-an-event-pod",
            "notes": "Critical for AI citations. Clear definition in first paragraph. Add FAQPage schema.",
        },
        {
            "title": "Event Pod Rental Cost: Pricing Guide for 2026",
            "type": "Landing Page",
            "target_keyword": "event pod rental cost",
            "intent": "commercial",
            "word_count": 1500,
            "due_date": (today + timedelta(days=14)).isoformat(),
            "status": "To Write",
            "url_slug": "/event-pod-rental-cost",
            "notes": "Pricing transparency page. Include ranges, factors, ROI calculator reference.",
        },
        {
            "title": "5 Ways SmartPods Outperform Traditional Booths on ROI",
            "type": "Blog Post",
            "target_keyword": "event pod vs trade show booth",
            "intent": "commercial",
            "word_count": 1500,
            "due_date": (today + timedelta(days=17)).isoformat(),
            "status": "To Write",
            "url_slug": "/blog/smartpods-vs-traditional-booths",
            "notes": "Comparison content. Include real data from case studies. Link to /event-pod-rental.",
        },
        {
            "title": "How IoT-Enabled Pods Capture Lead Data at Scale",
            "type": "Blog Post",
            "target_keyword": "IoT event technology",
            "intent": "informational",
            "word_count": 1200,
            "due_date": (today + timedelta(days=21)).isoformat(),
            "status": "To Write",
            "url_slug": "/blog/iot-pods-lead-capture",
            "notes": "Top-of-funnel authority content. Link to booking software page.",
        },
        {
            "title": "Event Pod Rental: What to Expect from Pricing to Setup",
            "type": "Blog Post",
            "target_keyword": "rent event pod",
            "intent": "transactional",
            "word_count": 1500,
            "due_date": (today + timedelta(days=24)).isoformat(),
            "status": "To Write",
            "url_slug": "/blog/event-pod-rental-what-to-expect",
            "notes": "Process walkthrough. Great for featured snippets. Link to /our-process.",
        },
        {
            "title": "How Event Technology Directors Evaluate IoT Rental Solutions",
            "type": "Pillar Page",
            "target_keyword": "event technology solutions",
            "intent": "commercial",
            "word_count": 2500,
            "due_date": (today + timedelta(days=28)).isoformat(),
            "status": "To Write",
            "url_slug": "/event-technology-buyers-guide",
            "notes": "Cluster 2 pillar. Target decision-makers. Include evaluation framework.",
        },
        {
            "title": "Event Pod Rental Las Vegas — Trade Show Pod Solutions",
            "type": "City Page",
            "target_keyword": "event pod rental las vegas",
            "intent": "local",
            "word_count": 1000,
            "due_date": (today + timedelta(days=30)).isoformat(),
            "status": "To Write",
            "url_slug": "/event-pod-rental-las-vegas",
            "notes": "Local landing page. Mention specific venues (LVCC, Mandalay Bay). Add LocalBusiness schema.",
        },
    ]

    notion_pages = []
    for item in content_items:
        notion_pages.append({
            "object": "page",
            "properties": {
                "Name": {"title": [{"text": {"content": item["title"]}}]},
                "Status": {"select": {"name": item["status"]}},
                "Type": {"select": {"name": item["type"]}},
                "Target Keyword": {"rich_text": [{"text": {"content": item["target_keyword"]}}]},
                "Intent": {"select": {"name": item["intent"]}},
                "Word Count": {"number": item["word_count"]},
                "Due Date": {"date": {"start": item["due_date"]}},
                "URL Slug": {"rich_text": [{"text": {"content": item["url_slug"]}}]},
                "Notes": {"rich_text": [{"text": {"content": item["notes"]}}]},
            }
        })

    return notion_pages


def generate_competitor_tracker():
    """Generate competitor tracking board for Notion."""
    comp_dir = BASE_DIR / "data" / "competitors"
    entries = []
    
    for f in sorted(comp_dir.glob("*_latest.json")):
        data = json.loads(f.read_text())
        domain = data.get("domain", f.stem)
        pages = data.get("pages", {})
        changes = data.get("changes", {})
        
        entries.append({
            "object": "page",
            "properties": {
                "Competitor": {"title": [{"text": {"content": domain}}]},
                "Pages Indexed": {"number": len(pages)},
                "Last Scanned": {"date": {"start": data.get("date", date.today().isoformat())}},
                "New Pages": {"number": len(changes.get("new_pages", []))},
                "Content Changes": {"number": len(changes.get("content_changes", []))},
                "Schema Changes": {"number": len(changes.get("schema_changes", []))},
            }
        })
    
    return entries


def export_all_for_notion():
    """Export all Notion-ready data as JSON files for manual import or MCP push."""
    output_dir = BASE_DIR / "data" / "notion_export"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # SEO Tasks
    tasks = generate_seo_task_database()
    (output_dir / "seo_tasks.json").write_text(json.dumps(tasks, indent=2))
    print(f"  ✓ SEO tasks: {len(tasks)} items → notion_export/seo_tasks.json")
    
    # Content Calendar
    calendar = generate_content_calendar()
    (output_dir / "content_calendar.json").write_text(json.dumps(calendar, indent=2))
    print(f"  ✓ Content calendar: {len(calendar)} items → notion_export/content_calendar.json")
    
    # Competitor Tracker
    competitors = generate_competitor_tracker()
    (output_dir / "competitor_tracker.json").write_text(json.dumps(competitors, indent=2))
    print(f"  ✓ Competitor tracker: {len(competitors)} items → notion_export/competitor_tracker.json")
    
    print(f"\n  To push to Notion via Claude Code/Cowork:")
    print(f"  'Create Notion databases from the JSON files in data/notion_export/'")
    
    return output_dir


if __name__ == "__main__":
    print(f"\n{'='*55}")
    print(f"  NOTION SYNC — Generating Export")
    print(f"{'='*55}\n")
    export_all_for_notion()
