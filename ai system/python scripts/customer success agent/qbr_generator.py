#!/usr/bin/env python3
"""
Advertiser QBR (Quarterly Business Review) Generator

Auto-generates structured QBR documents using campaign performance data,
historical spend, and TLDR benchmarks. Outputs markdown QBR decks ready
for presentation.

Usage:
  python qbr_generator.py --advertiser "Anthropic"     # single QBR
  python qbr_generator.py --quarter Q1                  # batch all advertisers for Q1
  python qbr_generator.py --dry-run                     # preview
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
COMMANDS_DIR = WORKSPACE_ROOT / "commands"
DATA_DIR = WORKSPACE_ROOT / "data" / "advertiser_performance"
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "advertiser_success" / "qbr_decks"
COMPETITIVE_DIR = WORKSPACE_ROOT / "docs" / "competitor content tracker"


def _resolve_env_key(name: str) -> str | None:
    val = os.environ.get(name)
    if val:
        return val
    current = Path(__file__).resolve().parent
    while current != current.parent:
        env_file = current / ".env"
        if env_file.exists():
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(f"{name}="):
                        return line.split("=", 1)[1].strip().strip("'\"")
        current = current.parent
    return None


CLAUDE_API_BASE = "https://api.anthropic.com/v1/messages"


def claude_generate(prompt: str, api_key: str, max_tokens: int = 8192, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            resp = requests.post(
                CLAUDE_API_BASE,
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=180,
            )
            if resp.status_code == 200:
                return resp.json()["content"][0]["text"]
            if resp.status_code == 429:
                time.sleep(min(60, 2 ** (attempt + 2)))
                continue
            print(f"  ⚠ Claude API error {resp.status_code}")
            time.sleep(5)
        except Exception as e:
            print(f"  ⚠ Claude exception: {e}")
            time.sleep(10)
    raise Exception("Max retries reached")


def load_context() -> dict[str, str]:
    context = {}
    for key, path in {
        "business": "core/business_context.md",
        "messaging": "identity/messaging_pillars.md",
    }.items():
        try:
            context[key] = (COMMANDS_DIR / path).read_text()
        except FileNotFoundError:
            context[key] = ""
    return context


def load_campaign_data(advertiser: str | None = None) -> list[dict]:
    csvs = sorted(DATA_DIR.glob("campaign_performance_*.csv"), reverse=True)
    if not csvs:
        return []
    with open(csvs[0], "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if advertiser:
        rows = [r for r in rows if advertiser.lower() in r.get("advertiser_name", "").lower()]
    return rows


def load_health_data(advertiser: str | None = None) -> list[dict]:
    csvs = sorted(DATA_DIR.glob("advertiser_health_*.csv"), reverse=True)
    if not csvs:
        return []
    with open(csvs[0], "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if advertiser:
        rows = [r for r in rows if advertiser.lower() in r.get("advertiser_name", "").lower()]
    return rows


def get_unique_advertisers() -> list[str]:
    """Get list of all advertisers with campaign data."""
    campaigns = load_campaign_data()
    return sorted(set(r.get("advertiser_name", "") for r in campaigns if r.get("advertiser_name")))


def generate_qbr(advertiser: str, api_key: str, context: dict, quarter: str) -> str:
    campaigns = load_campaign_data(advertiser)
    health = load_health_data(advertiser)

    campaign_summary = ""
    if campaigns:
        campaign_summary = "CAMPAIGN DATA:\n"
        for c in campaigns[:20]:
            campaign_summary += (
                f"- {c.get('placement_date', 'N/A')} | {c.get('newsletter', 'N/A')} | "
                f"{c.get('placement_type', 'N/A')} | Clicks: {c.get('clicks', 'N/A')} | "
                f"CTR: {c.get('ctr', 'N/A')} | Spend: ${c.get('spend', 'N/A')}\n"
            )

    health_summary = ""
    if health:
        h = health[0]
        health_summary = (
            f"ACCOUNT HEALTH:\n"
            f"- LTV Spend: ${h.get('total_spend_ltv', 'N/A')}\n"
            f"- This Quarter: ${h.get('spend_this_quarter', 'N/A')}\n"
            f"- Last Quarter: ${h.get('spend_last_quarter', 'N/A')}\n"
            f"- Trend: {h.get('spend_trend', 'N/A')}\n"
            f"- Avg CTR: {h.get('avg_ctr', 'N/A')}\n"
            f"- Newsletters: {h.get('newsletters_used', 'N/A')}\n"
        )

    prompt = f"""You are a customer success strategist for TLDR, the largest daily tech newsletter (7M+ subscribers, 12 newsletters, 40-48% open rates).

Generate a Quarterly Business Review (QBR) document for this advertiser.

ADVERTISER: {advertiser}
QUARTER: {quarter} {datetime.now().year}

{campaign_summary}

{health_summary}

TLDR CONTEXT:
{context.get('business', '')[:2000]}

TLDR BENCHMARKS:
- Average open rate: 40-48% across newsletters
- Average CTR: 1.5-3% depending on newsletter and placement
- Benchmark CPC: $2-5 (vs LinkedIn $8-15, Google $20-50)
- Case studies: Delve ($1M pipeline, 52x ROI), Plaid ($382K pipeline, 20x ROI), Redact (50% lower CPC than LinkedIn)

Generate a complete QBR in this markdown format:

# Quarterly Business Review: {advertiser}
**Quarter:** {quarter} {datetime.now().year}
**Prepared:** {datetime.now().strftime('%Y-%m-%d')}

---

## Executive Summary
[3-4 bullet points for the CMO who will skim this]

## Campaign Performance

### Overview
| Metric | This Quarter | Last Quarter | Delta | TLDR Benchmark |
|---|---|---|---|---|
[Fill with real data where available, reasonable estimates where not]

### Campaign Detail
[Per-placement breakdown if data available]

## Audience Engagement
[Open rates, click distribution, audience composition relevant to their product]

## ROI Analysis
[CPC comparison to industry, estimated value, efficiency metrics]

## Strategic Recommendations
[3-5 specific, actionable recommendations for next quarter]

## Proposed Next Quarter Plan
| Month | Newsletter | Placement | Goal |
|---|---|---|---|

---

RULES:
- Lead with wins, even if modest
- Be honest about underperformance but pair with a fix
- Recommendations must be specific (not "try new creative" but "test testimonial-style ad in TLDR AI")
- Always end with forward motion"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="Advertiser QBR Generator")
    parser.add_argument("--advertiser", type=str, help="Generate QBR for specific advertiser")
    parser.add_argument("--quarter", type=str, default="Q1", help="Quarter (Q1/Q2/Q3/Q4)")
    parser.add_argument("--batch", action="store_true", help="Generate QBRs for all advertisers")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    context = load_context()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.batch:
        advertisers = get_unique_advertisers()
        if not advertisers:
            print("  ℹ No advertiser campaign data found.")
            return
        print(f"  Generating QBRs for {len(advertisers)} advertisers...")
        for adv in advertisers:
            slug = adv.lower().replace(" ", "_")
            path = OUTPUT_DIR / f"qbr_{slug}_{datetime.now().year}_{args.quarter}.md"
            print(f"  📊 {adv}...")
            if not args.dry_run:
                content = generate_qbr(adv, api_key, context, args.quarter)
                path.write_text(content, encoding="utf-8")
            print(f"     ✅ {path.name}")
            time.sleep(3)
    elif args.advertiser:
        slug = args.advertiser.lower().replace(" ", "_")
        path = OUTPUT_DIR / f"qbr_{slug}_{datetime.now().year}_{args.quarter}.md"
        print(f"  📊 Generating QBR for {args.advertiser}...")
        if not args.dry_run:
            content = generate_qbr(args.advertiser, api_key, context, args.quarter)
            path.write_text(content, encoding="utf-8")
        print(f"  ✅ Saved to {path}")
    else:
        print("Specify --advertiser or --batch. Use --help for options.")


if __name__ == "__main__":
    main()
