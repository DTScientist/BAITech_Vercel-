#!/usr/bin/env python3
"""
SEO Ecosystem — Job Scheduler
Runs SEO jobs on schedule. Deploy on a server or use cron.

Usage:
  python3 scheduler/cron.py --daemon     # Run as background daemon
  python3 scheduler/cron.py --once       # Run all due jobs once
  python3 scheduler/cron.py --crontab    # Print crontab entries to install
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, date
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


def get_crontab_entries():
    """Generate crontab entries for all scheduled jobs."""
    py = sys.executable
    eco = BASE_DIR / "ecosystem.py"
    
    entries = f"""# ZenSpace SEO Ecosystem — Crontab
# Install with: crontab -e (paste these lines)

# Daily: Track keyword rankings (6 AM)
0 6 * * * cd {BASE_DIR} && {py} {eco} track >> /var/log/seo-ecosystem.log 2>&1

# Monday: Full site audit (7 AM)
0 7 * * 1 cd {BASE_DIR} && {py} collectors/pagespeed.py >> /var/log/seo-ecosystem.log 2>&1

# Wednesday: CWV check (7 AM)
0 7 * * 3 cd {BASE_DIR} && {py} {eco} audit >> /var/log/seo-ecosystem.log 2>&1

# Friday: Competitor scan (7 AM)
0 7 * * 5 cd {BASE_DIR} && {py} {eco} competitors >> /var/log/seo-ecosystem.log 2>&1

# Sunday: Weekly report (8 AM)
0 8 * * 0 cd {BASE_DIR} && {py} {eco} report >> /var/log/seo-ecosystem.log 2>&1

# 1st of month: Monthly deep-dive (9 AM)
0 9 1 * * cd {BASE_DIR} && {py} {eco} report >> /var/log/seo-ecosystem.log 2>&1
"""
    return entries


def run_due_jobs():
    """Check which jobs are due and run them."""
    now = datetime.now()
    today = date.today()
    weekday = today.weekday()  # 0=Monday

    jobs_run = []

    # Daily: SERP tracking
    print("  Checking: SERP tracking (daily)...")
    latest_serp = sorted((BASE_DIR / "data" / "rankings").glob("serp_*.json"))
    if not latest_serp or today.isoformat() not in latest_serp[-1].name:
        print("  → Running SERP tracker...")
        subprocess.run([sys.executable, str(BASE_DIR / "collectors" / "serp_tracker.py")])
        jobs_run.append("SERP tracking")
    else:
        print("  → Already ran today, skipping.")

    # Monday: Site audit
    if weekday == 0:
        print("  Checking: Site audit (Monday)...")
        subprocess.run([sys.executable, str(BASE_DIR / "collectors" / "pagespeed.py")])
        jobs_run.append("Site audit (CWV)")

    # Wednesday: CWV check
    if weekday == 2:
        print("  Checking: CWV check (Wednesday)...")
        subprocess.run([sys.executable, str(BASE_DIR / "collectors" / "pagespeed.py")])
        jobs_run.append("CWV check")

    # Friday: Competitor scan
    if weekday == 4:
        print("  Checking: Competitor scan (Friday)...")
        subprocess.run([sys.executable, str(BASE_DIR / "collectors" / "competitor_monitor.py")])
        jobs_run.append("Competitor scan")

    # Sunday: Weekly report
    if weekday == 6:
        print("  Checking: Weekly report (Sunday)...")
        subprocess.run([sys.executable, str(BASE_DIR / "reporters" / "weekly_report.py")])
        jobs_run.append("Weekly report")

    # Always: Action items
    subprocess.run([sys.executable, str(BASE_DIR / "reporters" / "action_items.py")])
    jobs_run.append("Action items")

    return jobs_run


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO Ecosystem Scheduler")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon (checks every hour)")
    parser.add_argument("--once", action="store_true", help="Run due jobs once and exit")
    parser.add_argument("--crontab", action="store_true", help="Print crontab entries")
    args = parser.parse_args()

    if args.crontab:
        print(get_crontab_entries())
    elif args.once:
        print(f"\n{'='*55}")
        print(f"  SCHEDULER — Running Due Jobs")
        print(f"{'='*55}\n")
        jobs = run_due_jobs()
        print(f"\n  Jobs run: {', '.join(jobs) or 'None due'}\n")
    elif args.daemon:
        print(f"  SEO Ecosystem Scheduler running as daemon...")
        print(f"  Checking for due jobs every hour. Ctrl+C to stop.\n")
        while True:
            run_due_jobs()
            time.sleep(3600)
    else:
        parser.print_help()
