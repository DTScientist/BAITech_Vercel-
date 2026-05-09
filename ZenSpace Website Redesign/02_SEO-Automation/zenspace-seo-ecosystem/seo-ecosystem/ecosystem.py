#!/usr/bin/env python3
"""
ZenSpace SEO Ecosystem — Master Orchestrator
Single entry point for all SEO operations.

Usage:
  python3 ecosystem.py run-all          # Run full daily routine
  python3 ecosystem.py track            # Track keyword rankings
  python3 ecosystem.py audit            # Run site audit + CWV
  python3 ecosystem.py competitors      # Scan competitors
  python3 ecosystem.py keywords         # Keyword research
  python3 ecosystem.py report           # Generate weekly report
  python3 ecosystem.py actions          # Generate action items
  python3 ecosystem.py bot              # Start Telegram approval bot
  python3 ecosystem.py status           # Show ecosystem status
  python3 ecosystem.py setup            # Interactive setup wizard
"""

import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config" / "ecosystem.json"


def load_config():
    return json.loads(CONFIG_PATH.read_text())


def run_script(script_path, desc, args_list=None):
    """Run a Python script and report results."""
    print(f"\n{'─'*55}")
    print(f"  ▸ {desc}")
    print(f"{'─'*55}\n")
    cmd = [sys.executable, str(script_path)]
    if args_list:
        cmd.extend(args_list)
    result = subprocess.run(cmd, cwd=str(BASE_DIR))
    return result.returncode == 0


def cmd_run_all(args):
    """Run complete daily SEO routine."""
    print(f"\n{'='*60}")
    print(f"  ZenSpace SEO Ecosystem — Full Daily Run")
    print(f"  Date: {date.today().isoformat()}")
    print(f"{'='*60}")

    steps = [
        (BASE_DIR / "collectors" / "serp_tracker.py", "Tracking keyword rankings"),
        (BASE_DIR / "collectors" / "pagespeed.py", "Checking Core Web Vitals"),
        (BASE_DIR / "collectors" / "competitor_monitor.py", "Scanning competitors"),
        (BASE_DIR / "reporters" / "action_items.py", "Generating action items"),
    ]

    results = []
    for script, desc in steps:
        if script.exists():
            ok = run_script(script, desc)
            results.append((desc, ok))
        else:
            print(f"  ⚠ Script not found: {script}")
            results.append((desc, False))

    print(f"\n{'='*60}")
    print(f"  RUN COMPLETE")
    print(f"{'='*60}")
    for desc, ok in results:
        icon = "✅" if ok else "❌"
        print(f"  {icon} {desc}")
    print(f"{'='*60}\n")


def cmd_track(args):
    run_script(BASE_DIR / "collectors" / "serp_tracker.py", "SERP Tracking",
               ["--compare"] if args.compare else None)


def cmd_audit(args):
    run_script(BASE_DIR / "collectors" / "pagespeed.py", "Core Web Vitals Check")


def cmd_competitors(args):
    run_script(BASE_DIR / "collectors" / "competitor_monitor.py", "Competitor Scan")


def cmd_keywords(args):
    run_script(BASE_DIR / "analyzers" / "keyword_analyzer.py", "Keyword Research",
               ["--seeds"] + (args.seeds if args.seeds else []) if args.seeds else None)


def cmd_report(args):
    run_script(BASE_DIR / "reporters" / "weekly_report.py", "Weekly Report")


def cmd_actions(args):
    run_script(BASE_DIR / "reporters" / "action_items.py", "Action Items")


def cmd_bot(args):
    bot_path = BASE_DIR.parent / "skills" / "seo-agent" / "agent" / "telegram_bot.py"
    if bot_path.exists():
        run_script(bot_path, "Telegram Approval Bot")
    else:
        print("Telegram bot not found. Check path.")


def cmd_status(args):
    """Show complete ecosystem status."""
    config = load_config()

    print(f"\n{'='*60}")
    print(f"  ZenSpace SEO Ecosystem — Status")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    # Config status
    print(f"  📋 Configuration:")
    print(f"     Domain: {config.get('domain')}")
    print(f"     Competitors: {len(config.get('competitors', []))}")
    print(f"     Tracked keywords: {len(config.get('tracked_keywords', []))}")
    tg = config.get("telegram", {})
    print(f"     Telegram: {'✅ Configured' if tg.get('bot_token') else '❌ Not configured'}")
    psi = config.get("apis", {}).get("pagespeed_insights", {})
    print(f"     PageSpeed API: {'✅ Key set' if psi.get('api_key') else '⚠ Using free tier (no key needed)'}")

    # Data status
    print(f"\n  📊 Data Collected:")
    dirs = {
        "Rankings": BASE_DIR / "data" / "rankings",
        "Audits (CWV)": BASE_DIR / "data" / "audits",
        "Competitors": BASE_DIR / "data" / "competitors",
        "Keywords": BASE_DIR / "data" / "keywords",
        "Reports": BASE_DIR / "data" / "reports",
    }
    for name, d in dirs.items():
        files = list(d.glob("*.json")) if d.exists() else []
        latest = max(files, key=lambda f: f.stat().st_mtime).name if files else "none"
        print(f"     {name}: {len(files)} files (latest: {latest})")

    # Task progress
    task_file = BASE_DIR.parent / "skills" / "seo-agent" / "agent" / "task_status.json"
    if task_file.exists():
        status = json.loads(task_file.read_text())
        done = len(status.get("completed", []))
        print(f"\n  ✅ Task Progress: {done}/20 ({round(done/20*100)}%)")
    else:
        print(f"\n  ✅ Task Progress: Not started")

    # Available commands
    print(f"\n  🔧 Available Commands:")
    print(f"     python3 ecosystem.py run-all      — Full daily routine")
    print(f"     python3 ecosystem.py track         — Track rankings")
    print(f"     python3 ecosystem.py audit         — CWV check")
    print(f"     python3 ecosystem.py competitors   — Scan competitors")
    print(f"     python3 ecosystem.py keywords      — Keyword research")
    print(f"     python3 ecosystem.py report        — Weekly report")
    print(f"     python3 ecosystem.py actions       — Priority action items")
    print(f"     python3 ecosystem.py bot           — Start Telegram bot")
    print(f"{'='*60}\n")


def cmd_setup(args):
    """Interactive setup wizard."""
    print(f"\n  ZenSpace SEO Ecosystem — Setup Wizard\n")

    config = load_config()

    print(f"  Current domain: {config['domain']}")
    print(f"  Current competitors: {[c['domain'] for c in config.get('competitors', [])]}")

    print(f"\n  For Telegram bot setup, run:")
    print(f"  python3 ../skills/seo-agent/agent/setup.py --token YOUR_TOKEN --chat-id YOUR_ID")

    print(f"\n  For PageSpeed API key (optional, improves rate limits):")
    print(f"  1. Go to console.cloud.google.com")
    print(f"  2. Enable 'PageSpeed Insights API'")
    print(f"  3. Create credentials → API key")
    print(f"  4. Add to config/ecosystem.json → apis → pagespeed_insights → api_key")

    print(f"\n  Everything else works out of the box with zero configuration.\n")


def main():
    parser = argparse.ArgumentParser(description="ZenSpace SEO Ecosystem")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("run-all", help="Full daily routine")

    track_p = subparsers.add_parser("track", help="Track keyword rankings")
    track_p.add_argument("--compare", action="store_true")

    subparsers.add_parser("audit", help="Core Web Vitals check")
    subparsers.add_parser("competitors", help="Scan competitors")

    kw_p = subparsers.add_parser("keywords", help="Keyword research")
    kw_p.add_argument("--seeds", nargs="+")

    subparsers.add_parser("report", help="Weekly report")
    subparsers.add_parser("actions", help="Priority action items")
    subparsers.add_parser("bot", help="Start Telegram bot")
    subparsers.add_parser("status", help="Ecosystem status")
    subparsers.add_parser("setup", help="Setup wizard")

    args = parser.parse_args()

    commands = {
        "run-all": cmd_run_all,
        "track": cmd_track,
        "audit": cmd_audit,
        "competitors": cmd_competitors,
        "keywords": cmd_keywords,
        "report": cmd_report,
        "actions": cmd_actions,
        "bot": cmd_bot,
        "status": cmd_status,
        "setup": cmd_setup,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()
        print(f"\n  Quick start: python3 ecosystem.py status\n")


if __name__ == "__main__":
    main()
