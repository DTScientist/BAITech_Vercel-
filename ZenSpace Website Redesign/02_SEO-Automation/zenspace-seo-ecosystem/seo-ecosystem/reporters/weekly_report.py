#!/usr/bin/env python3
"""
SEO Ecosystem — Weekly Report Generator
Compiles SERP, CWV, competitor, and audit data into a weekly summary.
Can output as Telegram message, markdown file, or JSON.
"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = DATA_DIR / "reports"


def get_latest_file(directory, prefix):
    """Get the most recent file matching a prefix."""
    files = sorted(Path(directory).glob(f"{prefix}*.json"))
    return json.loads(files[-1].read_text()) if files else None


def get_files_in_range(directory, prefix, days=7):
    """Get all files from the last N days."""
    cutoff = date.today() - timedelta(days=days)
    files = sorted(Path(directory).glob(f"{prefix}*.json"))
    results = []
    for f in files:
        # Extract date from filename
        parts = f.stem.split("_")
        for p in parts:
            try:
                file_date = date.fromisoformat(p)
                if file_date >= cutoff:
                    results.append(json.loads(f.read_text()))
                break
            except ValueError:
                continue
    return results


def generate_weekly_report():
    """Generate comprehensive weekly SEO report."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    report = {
        "type": "weekly",
        "date": today,
        "generated": datetime.now().isoformat(),
        "sections": {},
    }

    # ─── Rankings Section ───
    rankings_data = get_files_in_range(DATA_DIR / "rankings", "serp_", 7)
    if rankings_data:
        latest = rankings_data[-1]
        summary = latest.get("summary", {})

        # Calculate week-over-week changes
        rank_changes = []
        if len(rankings_data) >= 2:
            first = rankings_data[0]
            last = rankings_data[-1]
            for kw_last in last.get("keywords", []):
                for kw_first in first.get("keywords", []):
                    if kw_last["keyword"] == kw_first["keyword"]:
                        r1 = kw_first.get("rank")
                        r2 = kw_last.get("rank")
                        if r1 and r2 and r1 != r2:
                            rank_changes.append({
                                "keyword": kw_last["keyword"],
                                "from": r1, "to": r2,
                                "change": r1 - r2
                            })

        report["sections"]["rankings"] = {
            "total_tracked": summary.get("total_keywords", 0),
            "in_top_10": summary.get("top_10", 0),
            "in_top_3": summary.get("top_3", 0),
            "avg_rank": summary.get("avg_rank"),
            "improvements": [c for c in rank_changes if c["change"] > 0],
            "declines": [c for c in rank_changes if c["change"] < 0],
            "data_points": len(rankings_data),
        }
    else:
        report["sections"]["rankings"] = {"note": "No ranking data yet. Run: python3 collectors/serp_tracker.py"}

    # ─── Core Web Vitals Section ───
    cwv_data = get_latest_file(DATA_DIR / "audits", "cwv_")
    if cwv_data:
        pages = cwv_data.get("pages", [])
        our_pages = [p for p in pages if "zenspace" in p.get("url", "").lower()]
        comp_pages = [p for p in pages if "zenspace" not in p.get("url", "").lower()]

        our_avg_score = sum(p.get("score", 0) for p in our_pages) / max(len(our_pages), 1)
        comp_avg_score = sum(p.get("score", 0) for p in comp_pages) / max(len(comp_pages), 1)

        alerts = [p for p in our_pages if p.get("alert")]

        report["sections"]["cwv"] = {
            "our_avg_score": round(our_avg_score),
            "competitor_avg_score": round(comp_avg_score),
            "pages_tested": len(our_pages),
            "alerts": [p["alert"] for p in alerts],
            "worst_page": min(our_pages, key=lambda x: x.get("score", 100)) if our_pages else None,
        }
    else:
        report["sections"]["cwv"] = {"note": "No CWV data yet. Run: python3 collectors/pagespeed.py"}

    # ─── Competitor Section ───
    comp_files = sorted((DATA_DIR / "competitors").glob("*_latest.json"))
    if comp_files:
        comp_data = json.loads(comp_files[0].read_text())
        changes = comp_data.get("changes", {})
        has_changes = any(changes.get(k) for k in changes)

        report["sections"]["competitors"] = {
            "monitored": len(comp_files),
            "changes_detected": has_changes,
            "new_pages": changes.get("new_pages", []),
            "content_updates": len(changes.get("content_changes", [])),
            "schema_changes": len(changes.get("schema_changes", [])),
        }
    else:
        report["sections"]["competitors"] = {"note": "No competitor data yet. Run: python3 collectors/competitor_monitor.py"}

    # ─── Task Progress Section ───
    task_status_file = Path(__file__).parent.parent.parent / "skills" / "seo-agent" / "agent" / "task_status.json"
    if task_status_file.exists():
        status = json.loads(task_status_file.read_text())
        report["sections"]["tasks"] = {
            "completed": len(status.get("completed", [])),
            "total": 20,
            "recent_completions": [e for e in status.get("log", [])[-5:] if e["action"] == "completed"],
        }

    # ─── Generate Markdown ───
    md = generate_markdown(report)
    report["markdown"] = md

    # Save
    output = REPORT_DIR / f"weekly_{today}.json"
    output.write_text(json.dumps(report, indent=2))

    md_output = REPORT_DIR / f"weekly_{today}.md"
    md_output.write_text(md)

    print(md)
    return report


def generate_markdown(report):
    """Convert report data to readable markdown."""
    d = report["date"]
    md = f"# ZenSpace SEO Weekly Report — {d}\n\n"

    # Rankings
    r = report["sections"].get("rankings", {})
    if "note" not in r:
        md += f"## Rankings\n"
        md += f"- Keywords tracked: {r['total_tracked']}\n"
        md += f"- In top 10: {r['in_top_10']}\n"
        md += f"- In top 3: {r['in_top_3']}\n"
        if r.get("avg_rank"):
            md += f"- Average rank: #{r['avg_rank']}\n"
        if r.get("improvements"):
            md += f"\n**Improved this week:**\n"
            for c in r["improvements"][:5]:
                md += f"- {c['keyword']}: #{c['from']} → #{c['to']} (+{c['change']})\n"
        if r.get("declines"):
            md += f"\n**Declined this week:**\n"
            for c in r["declines"][:5]:
                md += f"- {c['keyword']}: #{c['from']} → #{c['to']} ({c['change']})\n"
    else:
        md += f"## Rankings\n{r['note']}\n"

    # CWV
    c = report["sections"].get("cwv", {})
    if "note" not in c:
        md += f"\n## Core Web Vitals\n"
        md += f"- Our avg score: {c['our_avg_score']}/100\n"
        md += f"- Competitor avg: {c['competitor_avg_score']}/100\n"
        if c.get("alerts"):
            md += f"- Alerts: {', '.join(c['alerts'])}\n"
    else:
        md += f"\n## Core Web Vitals\n{c['note']}\n"

    # Competitors
    comp = report["sections"].get("competitors", {})
    if "note" not in comp:
        md += f"\n## Competitor Activity\n"
        if comp.get("changes_detected"):
            md += f"- New pages: {len(comp.get('new_pages', []))}\n"
            md += f"- Content updates: {comp.get('content_updates', 0)}\n"
            md += f"- Schema changes: {comp.get('schema_changes', 0)}\n"
        else:
            md += f"- No changes detected this week\n"

    # Tasks
    t = report["sections"].get("tasks", {})
    if t:
        md += f"\n## Task Progress\n"
        md += f"- Completed: {t.get('completed', 0)}/{t.get('total', 20)}\n"
        pct = round((t.get('completed', 0) / t.get('total', 20)) * 100)
        md += f"- Progress: {pct}%\n"

    md += f"\n---\n*Generated {report['generated'][:16]}*\n"
    return md


def generate_telegram_summary(report):
    """Format report for Telegram (shorter, emoji-rich)."""
    d = report["date"]
    msg = f"📊 *Weekly SEO Report — {d}*\n\n"

    r = report["sections"].get("rankings", {})
    if "note" not in r:
        msg += f"🔍 *Rankings*: {r.get('in_top_10', 0)} keywords in top 10\n"
        up = len(r.get("improvements", []))
        down = len(r.get("declines", []))
        if up: msg += f"  📈 {up} improved\n"
        if down: msg += f"  📉 {down} declined\n"

    c = report["sections"].get("cwv", {})
    if "note" not in c:
        msg += f"\n⚡ *Performance*: {c.get('our_avg_score', '?')}/100\n"

    comp = report["sections"].get("competitors", {})
    if "note" not in comp:
        if comp.get("changes_detected"):
            msg += f"\n👀 *Competitor*: Changes detected!\n"
        else:
            msg += f"\n👀 *Competitor*: No changes\n"

    t = report["sections"].get("tasks", {})
    if t:
        pct = round((t.get('completed', 0) / t.get('total', 20)) * 100)
        msg += f"\n✅ *Tasks*: {t.get('completed', 0)}/{t.get('total', 20)} ({pct}%)\n"

    msg += f"\nUse /next to continue fixing. Full report saved."
    return msg


if __name__ == "__main__":
    generate_weekly_report()
