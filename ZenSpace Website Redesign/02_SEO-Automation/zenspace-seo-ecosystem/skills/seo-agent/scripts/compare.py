#!/usr/bin/env python3
"""
SEO Agent — Competitive Comparison
Compares two audit reports side-by-side and identifies gaps.
"""

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / "reports"


def load_audit(domain):
    """Load audit report for a domain."""
    report_path = REPORTS_DIR / f"{domain.replace('.', '_')}_audit.json"
    if not report_path.exists():
        print(f"ERROR: No audit report for {domain}. Run audit.py first.")
        sys.exit(1)
    return json.loads(report_path.read_text())


def compare_audits(our_domain, competitor_domain):
    """Compare two audit reports."""
    ours = load_audit(our_domain)
    theirs = load_audit(competitor_domain)

    print(f"\n{'='*75}")
    print(f"  SEO COMPETITIVE ANALYSIS")
    print(f"  {our_domain} vs {competitor_domain}")
    print(f"{'='*75}\n")

    # Overall comparison
    our_score = ours.get("overall_score", 0)
    our_max = ours.get("overall_max", 1)
    their_score = theirs.get("overall_score", 0)
    their_max = theirs.get("overall_max", 1)

    our_pct = (our_score / our_max) * 100
    their_pct = (their_score / their_max) * 100

    print(f"  OVERALL SCORES:")
    print(f"  {'─'*55}")
    print(f"  {our_domain:30s}  {our_score:5.1f}/{our_max} ({our_pct:5.1f}%)  Grade: {ours.get('overall_grade', 'N/A')}")
    print(f"  {competitor_domain:30s}  {their_score:5.1f}/{their_max} ({their_pct:5.1f}%)  Grade: {theirs.get('overall_grade', 'N/A')}")
    diff = our_pct - their_pct
    leader = our_domain if diff > 0 else competitor_domain
    print(f"  Gap: {abs(diff):.1f}% in favor of {leader}")

    # Category comparison
    print(f"\n  CATEGORY-BY-CATEGORY BREAKDOWN:")
    print(f"  {'─'*75}")
    print(f"  {'Category':35s} {'Ours':>8s} {'Theirs':>8s} {'Gap':>8s} {'Winner':>12s}")
    print(f"  {'─'*75}")

    gaps = []
    our_cats = ours.get("categories", {})
    their_cats = theirs.get("categories", {})

    all_keys = set(list(our_cats.keys()) + list(their_cats.keys()))

    for key in all_keys:
        our_cat = our_cats.get(key, {})
        their_cat = their_cats.get(key, {})
        name = our_cat.get("name") or their_cat.get("name", key)
        our_s = our_cat.get("score", 0)
        their_s = their_cat.get("score", 0)
        our_m = our_cat.get("max_score", 10)

        gap = our_s - their_s
        winner = "→ US" if gap > 0 else "→ THEM" if gap < 0 else "TIE"
        icon = "✅" if gap > 0 else "❌" if gap < 0 else "➖"

        print(f"  {icon} {name:33s} {our_s:5.1f}/{our_m:2d}  {their_s:5.1f}/{our_m:2d}  {gap:+5.1f}    {winner}")

        gaps.append({
            "category": name,
            "key": key,
            "our_score": our_s,
            "their_score": their_s,
            "gap": gap,
            "max_score": our_m,
        })

    # Where we're losing
    losing = sorted([g for g in gaps if g["gap"] < 0], key=lambda x: x["gap"])
    winning = sorted([g for g in gaps if g["gap"] > 0], key=lambda x: x["gap"], reverse=True)

    if losing:
        print(f"\n  🔴 WHERE WE'RE BEHIND (Priority fix areas):")
        print(f"  {'─'*55}")
        for g in losing:
            deficit = abs(g["gap"])
            pct_behind = (deficit / g["max_score"]) * 100
            print(f"  • {g['category']}: {deficit:.1f} points behind ({pct_behind:.0f}% gap)")

            # Pull specific findings from competitor that we're missing
            their_ok = [f for f in their_cats.get(g["key"], {}).get("findings", []) if f.get("severity") == "OK"]
            our_issues = [f for f in our_cats.get(g["key"], {}).get("findings", []) if f.get("severity") in ["CRITICAL", "HIGH"]]
            for issue in our_issues[:2]:
                print(f"    → {issue['issue'][:80]}")
                if issue.get("fix"):
                    print(f"      Fix: {issue['fix'][:70]}")

    if winning:
        print(f"\n  ✅ WHERE WE'RE AHEAD (Maintain advantage):")
        print(f"  {'─'*55}")
        for g in winning:
            print(f"  • {g['category']}: +{g['gap']:.1f} points ahead")

    # Generate action plan
    print(f"\n  📋 PRIORITIZED ACTION PLAN TO CLOSE GAPS:")
    print(f"  {'─'*55}")

    actions = []
    for g in losing:
        our_findings = our_cats.get(g["key"], {}).get("findings", [])
        for f in our_findings:
            if f.get("fix") and f.get("severity") in ["CRITICAL", "HIGH"]:
                actions.append({
                    "priority": 1 if f["severity"] == "CRITICAL" else 2,
                    "category": g["category"],
                    "action": f["fix"],
                    "impact": abs(g["gap"]),
                })

    actions.sort(key=lambda x: (x["priority"], -x["impact"]))
    for i, a in enumerate(actions[:20], 1):
        icon = "🔴" if a["priority"] == 1 else "🟠"
        print(f"  {i:2d}. {icon} [{a['category']}] {a['action'][:75]}")

    # Save comparison report
    comparison = {
        "our_domain": our_domain,
        "competitor_domain": competitor_domain,
        "our_overall": {"score": our_score, "max": our_max, "pct": our_pct, "grade": ours.get("overall_grade")},
        "their_overall": {"score": their_score, "max": their_max, "pct": their_pct, "grade": theirs.get("overall_grade")},
        "gaps": gaps,
        "actions": actions,
        "losing_categories": [g["category"] for g in losing],
        "winning_categories": [g["category"] for g in winning],
    }

    report_path = REPORTS_DIR / f"compare_{our_domain.replace('.', '_')}_vs_{competitor_domain.replace('.', '_')}.json"
    report_path.write_text(json.dumps(comparison, indent=2, default=str))
    print(f"\n  Comparison saved: {report_path}")
    print(f"{'='*75}\n")

    return comparison


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO Agent Competitive Comparison")
    parser.add_argument("--our", required=True, help="Our domain")
    parser.add_argument("--competitor", required=True, help="Competitor domain")
    args = parser.parse_args()
    compare_audits(args.our, args.competitor)
