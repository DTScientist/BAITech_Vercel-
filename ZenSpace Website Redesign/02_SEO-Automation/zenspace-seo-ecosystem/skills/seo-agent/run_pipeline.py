#!/usr/bin/env python3
"""
SEO Agent — Master Pipeline Runner
Orchestrates: Ingest → Audit → Compare → Fix Generation
Usage: python3 run_pipeline.py --our zenspaceevents.com --competitor nookeventpods.us
"""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent / "scripts"


def run(cmd, desc):
    print(f"\n{'─'*60}")
    print(f"  STEP: {desc}")
    print(f"{'─'*60}\n")
    result = subprocess.run(cmd, shell=True, capture_output=False)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="SEO Agent — Full Pipeline")
    parser.add_argument("--our", required=True, help="Our domain")
    parser.add_argument("--competitor", help="Competitor domain")
    parser.add_argument("--our-file", help="Uploaded JSON for our site")
    parser.add_argument("--competitor-file", help="Uploaded JSON for competitor site")
    parser.add_argument("--skip-crawl", action="store_true", help="Skip crawl (use existing data)")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  SEO AGENT — FULL PIPELINE")
    print(f"{'='*60}")
    print(f"  Our site:     {args.our}")
    if args.competitor:
        print(f"  Competitor:   {args.competitor}")
    print(f"{'='*60}\n")

    # Step 1: Ingest/Crawl our site
    if args.our_file:
        run(f"python3 {SCRIPTS}/ingest.py --file {args.our_file} --domain {args.our}", f"Ingesting browser data for {args.our}")
    elif not args.skip_crawl:
        run(f"python3 {SCRIPTS}/crawl.py --url https://{args.our} --depth 2 --max-pages 30", f"Crawling {args.our}")

    # Step 2: Ingest/Crawl competitor
    if args.competitor:
        if args.competitor_file:
            run(f"python3 {SCRIPTS}/ingest.py --file {args.competitor_file} --domain {args.competitor}", f"Ingesting browser data for {args.competitor}")
        elif not args.skip_crawl:
            run(f"python3 {SCRIPTS}/crawl.py --url https://{args.competitor} --depth 2 --max-pages 30", f"Crawling {args.competitor}")

    # Step 3: Audit our site
    run(f"python3 {SCRIPTS}/audit.py --domain {args.our}", f"Auditing {args.our}")

    # Step 4: Audit competitor
    if args.competitor:
        run(f"python3 {SCRIPTS}/audit.py --domain {args.competitor}", f"Auditing {args.competitor}")

    # Step 5: Compare
    if args.competitor:
        run(f"python3 {SCRIPTS}/compare.py --our {args.our} --competitor {args.competitor}", f"Comparing {args.our} vs {args.competitor}")

    # Step 6: Generate fixes
    run(f"python3 {SCRIPTS}/fix_gen.py --domain {args.our}", f"Generating fixes for {args.our}")

    print(f"\n{'='*60}")
    print(f"  PIPELINE COMPLETE")
    print(f"{'='*60}")
    print(f"  Results in: /home/claude/skills/seo-agent/reports/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
