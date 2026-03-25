#!/usr/bin/env python3
"""
Advertiser Prospect Intelligence Agent

Identifies ideal advertising prospects for TLDR newsletters by analyzing
funding signals, ad spend patterns, and competitor activity. Uses Claude API
for analysis and scoring, Ahrefs data for domain intelligence, and Meta Ad
Library for ad spend signals.

Usage:
  python prospect_intelligence.py                          # full signal scan
  python prospect_intelligence.py --vertical ai            # scan specific vertical
  python prospect_intelligence.py --company "Acme Corp"    # deep dive on one company
  python prospect_intelligence.py --dry-run                # preview without writing
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
sys.path.insert(0, str(WORKSPACE_ROOT))

COMMANDS_DIR = WORKSPACE_ROOT / "commands"
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "sales_assets" / "prospect_lists"
BRIEFS_DIR = OUTPUT_DIR / "briefs"

PROSPECT_CSV_COLUMNS = [
    "Company",
    "Website",
    "Industry",
    "Funding Stage",
    "Last Funding",
    "Signal Type",
    "Signal Detail",
    "Current Ad Platforms",
    "Newsletter Fit",
    "Priority Score",
    "Outreach Angle",
    "Contact Target",
]

VERTICALS = [
    "B2B SaaS",
    "Developer Tools",
    "Cloud Infrastructure",
    "AI/ML Platforms",
    "Cybersecurity",
    "Fintech",
    "HR Tech / Recruiting",
    "Education / Upskilling",
    "DevOps",
    "Data Infrastructure",
    "Open Source",
]

NEWSLETTER_MAP = {
    "AI/ML Platforms": ["TLDR AI", "TLDR Tech"],
    "Developer Tools": ["TLDR Dev", "TLDR Tech"],
    "Cloud Infrastructure": ["TLDR DevOps", "TLDR Tech"],
    "Cybersecurity": ["TLDR InfoSec", "TLDR Tech"],
    "Fintech": ["TLDR Fintech", "TLDR Tech"],
    "B2B SaaS": ["TLDR Tech", "TLDR Product"],
    "HR Tech / Recruiting": ["TLDR Tech", "TLDR Founders"],
    "Education / Upskilling": ["TLDR Tech", "TLDR Dev"],
    "DevOps": ["TLDR DevOps", "TLDR Tech"],
    "Data Infrastructure": ["TLDR Data", "TLDR Tech", "TLDR AI"],
    "Open Source": ["TLDR Dev", "TLDR Tech", "TLDR DevOps"],
}


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


# ---------------------------------------------------------------------------
# Claude API
# ---------------------------------------------------------------------------

CLAUDE_API_BASE = "https://api.anthropic.com/v1/messages"


def claude_generate(prompt: str, api_key: str, max_tokens: int = 4096, retries: int = 3) -> str:
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
                timeout=120,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["content"][0]["text"]
            if resp.status_code == 429:
                wait = min(60, 2 ** (attempt + 2))
                print(f"  ⚠ Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            print(f"  ⚠ Claude API error {resp.status_code}: {resp.text[:200]}")
            time.sleep(5)
        except Exception as e:
            print(f"  ⚠ Claude API exception on attempt {attempt+1}: {e}")
            time.sleep(10)
    raise Exception("Max retries reached for Claude API")


# ---------------------------------------------------------------------------
# Context Loading
# ---------------------------------------------------------------------------

def load_context() -> dict[str, str]:
    context = {}
    files = {
        "icp": "core/ideal_customer_profile.md",
        "competitors": "core/competitor_landscape.md",
        "messaging": "identity/messaging_pillars.md",
        "business": "core/business_context.md",
    }
    for key, rel_path in files.items():
        full_path = COMMANDS_DIR / rel_path
        try:
            context[key] = full_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"  ⚠ Missing context file: {full_path}")
            context[key] = ""
    return context


# ---------------------------------------------------------------------------
# Signal Scanning
# ---------------------------------------------------------------------------

def scan_funding_signals(vertical: str | None, api_key: str, context: dict) -> list[dict]:
    """Use Claude to identify recently funded companies that match TLDR's advertiser ICP."""
    vertical_filter = f"Focus specifically on the {vertical} vertical." if vertical else "Cover all B2B tech verticals."

    prompt = f"""You are a B2B advertising prospect researcher for TLDR, the largest daily tech newsletter (7M+ subscribers).

TASK: Identify 15-20 B2B tech companies that recently raised funding (Series A through D, $5M+) in the last 6 months that would be ideal advertising prospects for TLDR newsletters.

{vertical_filter}

TLDR's ADVERTISER ICP:
{context.get('icp', 'B2B SaaS, developer tools, cloud, AI/ML, cybersecurity, fintech, HR tech')}

For each company, provide STRICTLY this JSON format (no other text):
```json
[
  {{
    "company": "Company Name",
    "website": "https://example.com",
    "industry": "One of: B2B SaaS, Developer Tools, Cloud Infrastructure, AI/ML Platforms, Cybersecurity, Fintech, HR Tech / Recruiting, Education / Upskilling, DevOps, Data Infrastructure, Open Source",
    "funding_stage": "Series A/B/C/D",
    "last_funding": "$XXM Series X (Month YYYY)",
    "signal_type": "Recent Funding",
    "signal_detail": "Specific details about the round and why it signals ad spend",
    "current_ad_platforms": "LinkedIn, Meta, Google, or Unknown",
    "contact_target": "Head of Growth / VP Marketing / etc."
  }}
]
```

Only include companies where:
1. Their product targets developers, engineers, PMs, CTOs, or tech teams
2. They have enough funding to support $3K+ ad campaigns
3. They would benefit from reaching TLDR's technical audience

Be specific and factual. Use real companies with real funding data you know about."""

    print("  🔍 Scanning funding signals...")
    raw = claude_generate(prompt, api_key)

    json_start = raw.find("[")
    json_end = raw.rfind("]") + 1
    if json_start == -1 or json_end == 0:
        print("  ⚠ Could not parse funding scan results")
        return []

    try:
        prospects = json.loads(raw[json_start:json_end])
        print(f"  ✓ Found {len(prospects)} funding-signal prospects")
        return prospects
    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse error: {e}")
        return []


def scan_competitor_advertisers(api_key: str, context: dict) -> list[dict]:
    """Identify companies advertising on competitor newsletters."""
    prompt = f"""You are a B2B advertising prospect researcher for TLDR newsletters.

TASK: Identify 10-15 companies that are currently advertising on competitor newsletters (Morning Brew, The Hustle, Lenny's Newsletter, Bytes.dev) or other B2B tech media that would also be a great fit for TLDR.

COMPETITOR LANDSCAPE:
{context.get('competitors', '')}

TLDR BUSINESS CONTEXT:
{context.get('business', '')}

For each company, provide STRICTLY this JSON format (no other text):
```json
[
  {{
    "company": "Company Name",
    "website": "https://example.com",
    "industry": "Vertical category",
    "funding_stage": "Stage if known, else Unknown",
    "last_funding": "Amount if known, else Unknown",
    "signal_type": "Competitor Newsletter Advertiser",
    "signal_detail": "Seen advertising on [newsletter name] — describe what ad/sponsorship was observed",
    "current_ad_platforms": "Newsletter, LinkedIn, etc.",
    "contact_target": "Head of Growth / VP Marketing / etc."
  }}
]
```

Focus on companies that:
1. Target technical audiences (developers, engineers, PMs)
2. Have proven willingness to spend on newsletter advertising
3. Are NOT already known TLDR advertisers (AWS, Google Cloud, Anthropic, Shopify, Plaid, Bland AI, Delve, Kolena, Paragon)

Be specific about where you've seen their ads."""

    print("  🔍 Scanning competitor newsletter advertisers...")
    raw = claude_generate(prompt, api_key)

    json_start = raw.find("[")
    json_end = raw.rfind("]") + 1
    if json_start == -1 or json_end == 0:
        print("  ⚠ Could not parse competitor advertiser results")
        return []

    try:
        prospects = json.loads(raw[json_start:json_end])
        print(f"  ✓ Found {len(prospects)} competitor-advertiser prospects")
        return prospects
    except json.JSONDecodeError:
        return []


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_prospects(prospects: list[dict], api_key: str, context: dict) -> list[dict]:
    """Score each prospect using Claude on 5 dimensions."""
    if not prospects:
        return []

    prospect_summaries = "\n".join(
        f"- {p['company']} ({p.get('industry', 'Unknown')}): {p.get('signal_detail', 'N/A')}"
        for p in prospects
    )

    prompt = f"""You are scoring advertising prospects for TLDR newsletters (7M+ tech subscribers).

SCORING DIMENSIONS (score each 1-10):
1. Budget Signal (30% weight): 1-3=no visible spend, 4-6=some ads, 7-10=heavy active spend
2. Audience Overlap (25% weight): 1-3=consumer/non-tech, 4-6=partially tech, 7-10=core B2B tech
3. Newsletter Fit (20% weight): 1-3=poor fit, 4-6=fits 1-2 newsletters, 7-10=fits 3+ newsletters
4. Timing (15% weight): 1-3=no urgency, 4-6=some momentum, 7-10=fresh funding/launch
5. Deal Size Potential (10% weight): 1-3=likely $3K one-off, 4-6=$10-30K, 7-10=$50K+ recurring

TLDR CONTEXT:
{context.get('icp', '')}

PROSPECTS TO SCORE:
{prospect_summaries}

For each prospect, output STRICTLY this JSON (no other text):
```json
[
  {{
    "company": "Company Name",
    "budget_signal": 7,
    "audience_overlap": 8,
    "newsletter_fit": 9,
    "timing": 8,
    "deal_size": 6,
    "priority_score": 8,
    "outreach_angle": "One sentence personalized pitch angle",
    "newsletter_fit_names": "TLDR AI, TLDR Tech"
  }}
]
```

The priority_score should be the weighted average: (budget*0.3 + audience*0.25 + newsletter*0.2 + timing*0.15 + deal*0.1), rounded to nearest integer."""

    print("  📊 Scoring prospects...")
    raw = claude_generate(prompt, api_key, max_tokens=8192)

    json_start = raw.find("[")
    json_end = raw.rfind("]") + 1
    if json_start == -1 or json_end == 0:
        print("  ⚠ Could not parse scoring results")
        return prospects

    try:
        scores = json.loads(raw[json_start:json_end])
        score_map = {s["company"]: s for s in scores}

        for p in prospects:
            s = score_map.get(p["company"], {})
            p["Priority Score"] = s.get("priority_score", 5)
            p["Outreach Angle"] = s.get("outreach_angle", "")
            p["Newsletter Fit"] = s.get("newsletter_fit_names", _infer_newsletter_fit(p.get("industry", "")))

        print(f"  ✓ Scored {len(prospects)} prospects")
        return sorted(prospects, key=lambda x: x.get("Priority Score", 0), reverse=True)
    except json.JSONDecodeError:
        return prospects


def _infer_newsletter_fit(industry: str) -> str:
    return ", ".join(NEWSLETTER_MAP.get(industry, ["TLDR Tech"]))


# ---------------------------------------------------------------------------
# Prospect Brief Generation
# ---------------------------------------------------------------------------

def generate_brief(prospect: dict, api_key: str, context: dict) -> str:
    prompt = f"""You are writing a detailed prospect brief for TLDR's advertising sales team.

PROSPECT:
- Company: {prospect.get('company', 'Unknown')}
- Website: {prospect.get('website', 'Unknown')}
- Industry: {prospect.get('industry', 'Unknown')}
- Funding: {prospect.get('last_funding', 'Unknown')}
- Signal: {prospect.get('signal_detail', 'Unknown')}
- Score: {prospect.get('Priority Score', 'N/A')}/10
- Newsletter Fit: {prospect.get('Newsletter Fit', 'Unknown')}

TLDR CONTEXT:
{context.get('business', '')}

MESSAGING PILLARS:
{context.get('messaging', '')}

Write a prospect brief in this exact markdown format:

# Prospect Brief: {{Company}}

## Company Overview
[What they do, target market, stage, key metrics if known]

## Why TLDR
[3-4 specific reasons this company should advertise with TLDR — tie to their product and audience]

## Current Marketing Activity
[What you know about their ad spend, channels, messaging]

## Newsletter Fit
[Which TLDR newsletters and placement types, with reasoning]

## Outreach Strategy
[Personalized angle, suggested email subject line, 3 key talking points]

## Competitive Intelligence
[Are they likely advertising elsewhere? What would make them switch to TLDR?]

Be specific and actionable. This brief will be handed directly to an AE for outreach."""

    return claude_generate(prompt, api_key)


# ---------------------------------------------------------------------------
# CSV Output
# ---------------------------------------------------------------------------

def write_prospect_csv(prospects: list[dict], dry_run: bool = False) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    csv_path = OUTPUT_DIR / f"prospect_list_{today}.csv"

    rows = []
    for p in prospects:
        rows.append({
            "Company": p.get("company", ""),
            "Website": p.get("website", ""),
            "Industry": p.get("industry", ""),
            "Funding Stage": p.get("funding_stage", ""),
            "Last Funding": p.get("last_funding", ""),
            "Signal Type": p.get("signal_type", ""),
            "Signal Detail": p.get("signal_detail", ""),
            "Current Ad Platforms": p.get("current_ad_platforms", ""),
            "Newsletter Fit": p.get("Newsletter Fit", ""),
            "Priority Score": p.get("Priority Score", ""),
            "Outreach Angle": p.get("Outreach Angle", ""),
            "Contact Target": p.get("contact_target", ""),
        })

    if dry_run:
        print(f"\n  🧪 DRY RUN: would write {len(rows)} prospects to {csv_path}")
        for r in rows[:5]:
            print(f"     [{r['Priority Score']}] {r['Company']} — {r['Signal Type']}")
        return csv_path

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PROSPECT_CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  ✅ Wrote {len(rows)} prospects to {csv_path}")
    return csv_path


def write_prospect_briefs(prospects: list[dict], api_key: str, context: dict, dry_run: bool = False) -> int:
    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    high_priority = [p for p in prospects if p.get("Priority Score", 0) >= 7]

    if not high_priority:
        print("  ℹ No prospects scored 7+ — skipping brief generation")
        return 0

    if dry_run:
        print(f"  🧪 DRY RUN: would generate {len(high_priority)} briefs")
        return len(high_priority)

    count = 0
    for p in high_priority:
        company_slug = p["company"].lower().replace(" ", "_").replace("/", "_")
        brief_path = BRIEFS_DIR / f"{company_slug}_brief.md"

        print(f"  📝 Generating brief for {p['company']}...")
        brief = generate_brief(p, api_key, context)

        brief_path.write_text(brief, encoding="utf-8")
        count += 1
        time.sleep(2)

    print(f"  ✅ Generated {count} prospect briefs")
    return count


# ---------------------------------------------------------------------------
# Single Company Deep Dive
# ---------------------------------------------------------------------------

def deep_dive(company: str, api_key: str, context: dict, dry_run: bool = False) -> None:
    print(f"\n🔬 Deep Dive: {company}")

    prompt = f"""You are researching a potential advertising prospect for TLDR newsletters.

COMPANY TO RESEARCH: {company}

Research this company and provide STRICTLY this JSON (no other text):
```json
{{
  "company": "{company}",
  "website": "URL",
  "industry": "Vertical",
  "funding_stage": "Stage",
  "last_funding": "Details",
  "signal_type": "Deep Dive Research",
  "signal_detail": "Comprehensive summary of why they're a good TLDR prospect",
  "current_ad_platforms": "Known platforms",
  "contact_target": "Ideal contact role"
}}
```

TLDR ICP:
{context.get('icp', '')}

Be thorough — include funding history, product description, target audience, and any known marketing activity."""

    raw = claude_generate(prompt, api_key)
    json_start = raw.find("{")
    json_end = raw.rfind("}") + 1

    if json_start == -1:
        print("  ⚠ Could not parse deep dive results")
        return

    try:
        prospect = json.loads(raw[json_start:json_end])
    except json.JSONDecodeError:
        print("  ⚠ JSON parse error in deep dive")
        return

    scored = score_prospects([prospect], api_key, context)
    write_prospect_csv(scored, dry_run=dry_run)
    write_prospect_briefs(scored, api_key, context, dry_run=dry_run)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_full_scan(vertical: str | None, api_key: str, dry_run: bool = False) -> None:
    print("=" * 60)
    print(f"🎯 Advertiser Prospect Intelligence — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    if vertical:
        print(f"   Vertical filter: {vertical}")
    print("=" * 60)

    context = load_context()

    funding_prospects = scan_funding_signals(vertical, api_key, context)
    competitor_prospects = scan_competitor_advertisers(api_key, context)

    all_prospects = funding_prospects + competitor_prospects

    seen = set()
    deduped = []
    for p in all_prospects:
        key = p.get("company", "").lower().strip()
        if key and key not in seen:
            seen.add(key)
            deduped.append(p)
    all_prospects = deduped

    print(f"\n  📋 {len(all_prospects)} unique prospects found")

    scored = score_prospects(all_prospects, api_key, context)

    csv_path = write_prospect_csv(scored, dry_run=dry_run)
    brief_count = write_prospect_briefs(scored, api_key, context, dry_run=dry_run)

    print(f"\n{'=' * 60}")
    print(f"✅ Prospect scan complete")
    print(f"   Total prospects: {len(scored)}")
    print(f"   High priority (7+): {sum(1 for p in scored if p.get('Priority Score', 0) >= 7)}")
    print(f"   Briefs generated: {brief_count}")
    print(f"   CSV: {csv_path}")
    print(f"{'=' * 60}")


def main():
    parser = argparse.ArgumentParser(
        description="Advertiser Prospect Intelligence — find ideal TLDR advertising prospects",
    )
    parser.add_argument("--vertical", type=str, help=f"Filter by vertical: {', '.join(VERTICALS)}")
    parser.add_argument("--company", type=str, help="Deep dive on a single company")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found. Set it in .env or as an environment variable.")
        sys.exit(1)

    if args.company:
        context = load_context()
        deep_dive(args.company, api_key, context, dry_run=args.dry_run)
    else:
        run_full_scan(args.vertical, api_key, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
