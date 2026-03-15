#!/usr/bin/env python3
"""
Competitive Battlecard Generator

Creates structured sales battlecards for TLDR's advertising sales team.
Compares TLDR against LinkedIn Ads, Google Ads, Meta Ads, Paved, Beehiiv,
and podcast sponsorships using internal positioning data and fresh research.

Usage:
  python battlecard_generator.py                          # generate all battlecards
  python battlecard_generator.py --competitor "LinkedIn Ads"  # single competitor
  python battlecard_generator.py --dry-run                # preview without writing
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

COMMANDS_DIR = WORKSPACE_ROOT / "commands"
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "sales_assets" / "battlecards"
CALL_ANALYSIS_DIR = WORKSPACE_ROOT / "docs" / "sales_assets" / "call_analysis"
COMPETITIVE_DATA_DIR = WORKSPACE_ROOT / "docs" / "competitor content tracker" / "paid ads creatives"

COMPETITORS = {
    "LinkedIn Ads": {
        "slug": "linkedin-ads",
        "type": "Platform",
        "research_urls": [
            "https://business.linkedin.com/marketing-solutions/ads",
            "https://www.linkedin.com/business/marketing/pricing",
        ],
    },
    "Google Ads": {
        "slug": "google-ads",
        "type": "Platform",
        "research_urls": [
            "https://ads.google.com",
        ],
    },
    "Meta Ads": {
        "slug": "meta-ads",
        "type": "Platform",
        "research_urls": [
            "https://www.facebook.com/business/ads",
        ],
    },
    "Paved": {
        "slug": "paved",
        "type": "Newsletter network",
        "research_urls": [
            "https://www.paved.com",
        ],
    },
    "Beehiiv": {
        "slug": "beehiiv",
        "type": "Newsletter platform",
        "research_urls": [
            "https://www.beehiiv.com/advertise",
        ],
    },
    "Podcast Sponsorships": {
        "slug": "podcast-sponsorships",
        "type": "Channel",
        "research_urls": [],
    },
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
                wait = min(60, 2 ** (attempt + 2))
                print(f"  ⚠ Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            print(f"  ⚠ Claude API error {resp.status_code}: {resp.text[:200]}")
            time.sleep(5)
        except Exception as e:
            print(f"  ⚠ Claude API exception: {e}")
            time.sleep(10)
    raise Exception("Max retries reached for Claude API")


# ---------------------------------------------------------------------------
# Context Loading
# ---------------------------------------------------------------------------

def load_context() -> dict[str, str]:
    context = {}
    files = {
        "competitors": "core/competitor_landscape.md",
        "business": "core/business_context.md",
        "icp": "core/ideal_customer_profile.md",
        "messaging": "identity/messaging_pillars.md",
    }
    for key, rel_path in files.items():
        full_path = COMMANDS_DIR / rel_path
        try:
            context[key] = full_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            context[key] = ""
    return context


def load_call_objections() -> str:
    """Load real objection data from call analysis if available."""
    insights_files = sorted(CALL_ANALYSIS_DIR.glob("insights_report_*.md"), reverse=True)
    if insights_files:
        try:
            return insights_files[0].read_text(encoding="utf-8")[:3000]
        except Exception:
            pass
    return ""


def load_competitive_ad_data() -> str:
    """Load recent competitive ad tracking data."""
    log_path = COMPETITIVE_DATA_DIR / "ad_creative_log.csv"
    if log_path.exists():
        try:
            content = log_path.read_text(encoding="utf-8")
            lines = content.strip().split("\n")
            if len(lines) > 1:
                return f"Recent competitor ad data ({len(lines)-1} entries):\n" + "\n".join(lines[:20])
        except Exception:
            pass
    return ""


# ---------------------------------------------------------------------------
# Battlecard Generation
# ---------------------------------------------------------------------------

def generate_battlecard(competitor_name: str, competitor_info: dict, api_key: str, context: dict, call_data: str, ad_data: str) -> str:
    prompt = f"""You are a competitive intelligence strategist for TLDR, the largest daily tech newsletter network (7M+ subscribers, 12 newsletters, 40-48% open rates). Create a comprehensive sales battlecard that AEs can use to win deals against {competitor_name}.

COMPETITOR: {competitor_name} ({competitor_info['type']})

TLDR'S COMPETITIVE POSITIONING:
{context.get('competitors', '')}

TLDR BUSINESS CONTEXT:
{context.get('business', '')}

TLDR MESSAGING PILLARS:
{context.get('messaging', '')}

TLDR ADVERTISER ICP:
{context.get('icp', '')[:2000]}

{"REAL OBJECTION DATA FROM SALES CALLS:" if call_data else ""}
{call_data}

{"COMPETITOR AD TRACKING DATA:" if ad_data else ""}
{ad_data}

Generate a battlecard in this EXACT markdown format:

# Battlecard: TLDR vs. {competitor_name}

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Competitor Type:** {competitor_info['type']}

---

## 1. Competitor Overview
[2-3 sentences: what they are, their core pitch to advertisers, typical customer, pricing model and rough CPCs/CPMs]

## 2. Their Strengths (Be Honest)
[3-5 bullet points — what they genuinely do well. AEs lose credibility trashing competitors.]

## 3. Their Weaknesses (Where TLDR Wins)
[4-6 bullet points — specific, evidence-backed. Each weakness maps to a TLDR advantage.]

## 4. Head-to-Head Comparison

| Dimension | {competitor_name} | TLDR |
|---|---|---|
| Audience Quality | ... | ... |
| Audience Size (Tech) | ... | ... |
| CPC Range | ... | ... |
| Attribution / Tracking | ... | ... |
| Ad Format | ... | ... |
| Ad Density / Competition | ... | ... |
| Creative Support | ... | ... |
| Minimum Spend | ... | ... |
| Best For | ... | ... |

## 5. Common Objections + Rebuttals

| Objection | Rebuttal | Proof Point |
|---|---|---|
[5-8 rows. Rebuttals must be conversational — how an AE would actually say it. Proof points from TLDR case studies: Delve ($1M pipeline, 52x ROI), Plaid ($382K pipeline, 20x ROI), Redact (50% lower CPC than LinkedIn), MLOps Community (higher quality than Meta)]

## 6. Killer Questions
[5-7 questions AEs should ask to expose {competitor_name}'s weakness. Write as actual questions with brief context.]

## 7. Win Scenarios
[3-4 deal profiles where TLDR consistently beats {competitor_name}]

## 8. Loss Scenarios
[2-3 situations where we might lose — and what to do about it. Honesty builds trust.]

## 9. Proof Points & Case Studies
[Relevant TLDR case studies and metrics. Match proof points to this specific competitor.]

## 10. Talk Track
[60-second pitch an AE can use when {competitor_name} comes up. Written in first person, conversational tone. Start with acknowledgment, pivot to TLDR's advantage.]

---

RULES:
- Every claim needs a source or proof point
- Rebuttals must sound like a human AE talking, not marketing copy
- Killer questions must be genuinely tough for {competitor_name}
- Be honest about loss scenarios
- Keep the talk track under 150 words"""

    return claude_generate(prompt, api_key, max_tokens=8192)


# ---------------------------------------------------------------------------
# Quick Reference & Index
# ---------------------------------------------------------------------------

def generate_quick_reference(api_key: str, context: dict) -> str:
    prompt = f"""Create a single-page quick reference card for TLDR's sales team. For EACH competitor below, provide the #1 objection an AE will face and the best 2-sentence rebuttal.

COMPETITORS:
1. LinkedIn Ads
2. Google Ads
3. Meta Ads
4. Paved
5. Beehiiv
6. Podcast Sponsorships

TLDR CONTEXT:
{context.get('competitors', '')[:3000]}

PROOF POINTS:
- Delve: $1M pipeline, 52x ROI
- Plaid: $382K pipeline, 20x ROI
- Redact: 50% lower CPC than LinkedIn
- MLOps Community: Higher quality attendees than Meta

Format as markdown:

# Quick Reference: Competitive Rebuttals

**Updated:** {datetime.now().strftime('%Y-%m-%d')}

| Competitor | Top Objection | Rebuttal |
|---|---|---|
[One row per competitor. Rebuttals must be conversational.]

## One-Line Positioning Against Each

| Competitor | TLDR's Advantage in One Sentence |
|---|---|
[One row per competitor.]"""

    return claude_generate(prompt, api_key, max_tokens=4096)


def generate_index(generated_cards: list[tuple[str, str, Path]]) -> str:
    rows = ""
    for name, comp_type, path in generated_cards:
        rows += f"| [{name}]({path.name}) | {comp_type} | {datetime.now().strftime('%Y-%m-%d')} |\n"

    return f"""# Battlecard Index

**Last Full Refresh:** {datetime.now().strftime('%Y-%m-%d')}

| Competitor | Type | Last Updated |
|---|---|---|
{rows}
## Quick Links

- [Quick Reference Card](quick_reference.md) — One-page cheat sheet for mid-call use
- [Call Insights Report](../call_analysis/) — Real objection data from sales calls
- [Competitive Ad Tracker](../../competitor%20creative%20tracker/paid%20ads%20creatives/) — What competitors' own ads look like

## Refresh Schedule

- **Quarterly:** Full suite refresh (after competitive tracker audits)
- **On-demand:** Single competitor dive (after lost deal or competitive threat)
- **After call analysis:** Update objection sections with real-world data
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_full_suite(api_key: str, dry_run: bool = False) -> None:
    print("=" * 60)
    print(f"⚔️  Competitive Battlecard Generator — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Generating battlecards for {len(COMPETITORS)} competitors")
    print("=" * 60)

    context = load_context()
    call_data = load_call_objections()
    ad_data = load_competitive_ad_data()

    if call_data:
        print("  📞 Loaded real objection data from call analysis")
    if ad_data:
        print("  📊 Loaded competitive ad tracking data")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generated = []

    for name, info in COMPETITORS.items():
        print(f"\n  ⚔️  Generating: {name}...")
        card_path = OUTPUT_DIR / f"{info['slug']}_battlecard.md"

        if dry_run:
            print(f"  🧪 DRY RUN: would write {card_path}")
            generated.append((name, info["type"], card_path))
            continue

        content = generate_battlecard(name, info, api_key, context, call_data, ad_data)
        card_path.write_text(content, encoding="utf-8")
        generated.append((name, info["type"], card_path))
        print(f"  ✅ Saved: {card_path.name}")
        time.sleep(3)

    print("\n  📋 Generating quick reference card...")
    if not dry_run:
        qr_content = generate_quick_reference(api_key, context)
        qr_path = OUTPUT_DIR / "quick_reference.md"
        qr_path.write_text(qr_content, encoding="utf-8")
        print(f"  ✅ Saved: {qr_path.name}")

    index_content = generate_index(generated)
    index_path = OUTPUT_DIR / "_index.md"
    if not dry_run:
        index_path.write_text(index_content, encoding="utf-8")
        print(f"  ✅ Saved: {index_path.name}")

    print(f"\n{'=' * 60}")
    print(f"✅ Battlecard generation complete")
    print(f"   Cards generated: {len(generated)}")
    print(f"   Output: {OUTPUT_DIR}")
    print(f"{'=' * 60}")


def run_single(competitor_name: str, api_key: str, dry_run: bool = False) -> None:
    if competitor_name not in COMPETITORS:
        print(f"❌ Unknown competitor: {competitor_name}")
        print(f"   Valid options: {', '.join(COMPETITORS.keys())}")
        sys.exit(1)

    info = COMPETITORS[competitor_name]
    print(f"\n⚔️  Deep Dive Battlecard: {competitor_name}")

    context = load_context()
    call_data = load_call_objections()
    ad_data = load_competitive_ad_data()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    card_path = OUTPUT_DIR / f"{info['slug']}_battlecard.md"

    if dry_run:
        print(f"  🧪 DRY RUN: would write {card_path}")
        return

    content = generate_battlecard(competitor_name, info, api_key, context, call_data, ad_data)
    card_path.write_text(content, encoding="utf-8")
    print(f"  ✅ Saved: {card_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Competitive Battlecard Generator — arm AEs to win against every competitor",
    )
    parser.add_argument("--competitor", type=str, help=f"Single competitor: {', '.join(COMPETITORS.keys())}")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found. Set it in .env or as an environment variable.")
        sys.exit(1)

    if args.competitor:
        run_single(args.competitor, api_key, dry_run=args.dry_run)
    else:
        run_full_suite(api_key, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
