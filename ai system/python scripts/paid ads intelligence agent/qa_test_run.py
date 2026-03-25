#!/usr/bin/env python3
"""
QA test run: 3 periods, summary stats only. No full report.
Run: python qa_test_run.py
"""
import sys
import os

# Suppress verbose print during data pull
class Quiet:
    def write(self, x): pass
    def flush(self): pass

sys.stdout, sys.stderr = Quiet(), Quiet()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paid_ads_intelligence_agent import (
    pull_full_meta_data,
    build_lead_analysis,
    META_ACCESS_TOKEN,
    META_AD_ACCOUNT_ID,
)

# Restore stdout for summary output only
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

PERIODS = [
    ("2026-03-03", "2026-03-09", "Mar 3–9, 2026"),
    ("2026-02-24", "2026-03-02", "Feb 24 – Mar 2, 2026"),
    ("2026-02-17", "2026-02-23", "Feb 17–23, 2026"),
]

if not META_ACCESS_TOKEN or not META_AD_ACCOUNT_ID:
    print("Meta Ads credentials not set. Check .env")
    sys.exit(1)

for since, until, label in PERIODS:
    _save, _err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = Quiet(), Quiet()
    raw = pull_full_meta_data(since, until)
    analysis = build_lead_analysis(raw, raw.get("optimization_map", {}))
    sys.stdout, sys.stderr = _save, _err

    print("=" * 64)
    print(f"  PERIOD: {label}")
    print(f"  Date range: {since} to {until}")
    print("=" * 64)
    print(f"  Account spend:     ${analysis['account_level_spend']:,.2f}")
    print(f"  Campaign spend:    ${analysis['total_campaign_spend']:,.2f}")
    print(f"  Spend delta:      ${analysis['spend_delta']:,.2f}")
    print(f"  Total leads:      {analysis['total_leads']}")
    print(f"  Blended CPL:      ${analysis['blended_cpl'] or 'N/A'}")
    print()
    print("  Campaigns with spend:")
    for c in analysis["campaign_results"]:
        if c["spend"] > 0:
            cpl = f"${c['cpl']:,.2f}" if c["cpl"] else "N/A"
            print(f"    {c['campaign_name'][:50]:<50}  spend=${c['spend']:,.2f}  leads={c['leads']}  cpl={cpl}")
    print()
