#!/usr/bin/env python3
"""
Competitive Feature Matrix Generator

Researches competitor platforms and builds feature-by-feature comparison
matrices against TLDR's advertising capabilities.

Usage:
  python competitive_feature_matrix.py                          # full matrix
  python competitive_feature_matrix.py --competitor "LinkedIn"  # single competitor
  python competitive_feature_matrix.py --dry-run                # preview
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
COMMANDS_DIR = WORKSPACE_ROOT / "commands"
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "product_assets"
BATTLECARD_DIR = WORKSPACE_ROOT / "docs" / "sales_assets" / "battlecards"

COMPETITORS = ["LinkedIn Ads", "Google Ads", "Meta Ads", "Paved", "Beehiiv", "Podcast Sponsorships"]


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
            time.sleep(5)
        except Exception as e:
            print(f"  ⚠ Claude exception: {e}")
            time.sleep(10)
    raise Exception("Max retries reached")


def load_battlecard_context() -> str:
    parts = []
    if BATTLECARD_DIR.exists():
        for f in sorted(BATTLECARD_DIR.glob("*_battlecard.md"))[:4]:
            parts.append(f.read_text(encoding="utf-8")[:2000])
    return "\n\n".join(parts)


def generate_matrix(competitors: list[str], api_key: str) -> str:
    business_context = ""
    try:
        business_context = (COMMANDS_DIR / "core" / "business_context.md").read_text()[:2000]
    except FileNotFoundError:
        pass

    competitor_context = ""
    try:
        competitor_context = (COMMANDS_DIR / "core" / "competitor_landscape.md").read_text()[:2000]
    except FileNotFoundError:
        pass

    battlecard_data = load_battlecard_context()
    comp_list = ", ".join(competitors)

    prompt = f"""You are a competitive product analyst for TLDR, the largest daily tech newsletter (7M+ subscribers, 12 newsletters, 40-48% open rates).

Build a detailed feature comparison matrix: TLDR vs {comp_list}.

TLDR CONTEXT:
{business_context}

COMPETITOR CONTEXT:
{competitor_context}

{"BATTLECARD DATA:" if battlecard_data else ""}
{battlecard_data[:5000]}

TLDR'S CURRENT CAPABILITIES:
- 12 newsletters segmented by tech vertical
- 3 ad placement types: Primary (top), Secondary (middle), Quick Links (bottom)
- Managed service only (no self-serve yet)
- TLDR team writes ad copy
- Dedicated CSM per advertiser
- UTM tracking, click reporting, performance reports included
- 40-48% open rates, 1.5-3% CTR
- Min spend ~$1,500-3,000 per placement
- Max 3 advertisers per newsletter per day

FEATURE DIMENSIONS TO COMPARE:
1. Targeting Capabilities
2. Ad Formats
3. Creative & Copy Support
4. Reporting & Attribution
5. Buying & Pricing Model
6. Account Management

Generate in this EXACT format:

# Competitive Feature Matrix — {datetime.now().strftime('%Y-%m-%d')}

## Quick View

| Feature | TLDR | {' | '.join(competitors)} |
|---|---|{'---|' * len(competitors)}
[Use ✅ / ❌ / Partial for each cell. 20+ rows covering all dimensions.]

## Detailed: Targeting Capabilities
| Capability | TLDR | {' | '.join(competitors)} |
|---|---|{'---|' * len(competitors)}
[8-10 rows]

## Detailed: Ad Formats
| Format | TLDR | {' | '.join(competitors)} |
|---|---|{'---|' * len(competitors)}

## Detailed: Creative & Copy
| Feature | TLDR | {' | '.join(competitors)} |
|---|---|{'---|' * len(competitors)}

## Detailed: Reporting & Attribution
| Feature | TLDR | {' | '.join(competitors)} |
|---|---|{'---|' * len(competitors)}

## Detailed: Buying & Pricing
| Feature | TLDR | {' | '.join(competitors)} |
|---|---|{'---|' * len(competitors)}

## Detailed: Account Management
| Feature | TLDR | {' | '.join(competitors)} |
|---|---|{'---|' * len(competitors)}

## TLDR's Unique Advantages
[Features only TLDR offers]

## Critical Gaps
| Gap | Who Has It | Priority | Impact on Deals |
|---|---|---|---|
[Ranked by deal impact]

## Roadmap Recommendations
1. [feature to build — based on gap analysis + evidence]
2. [feature to build]
3. [feature to build]

RULES:
- Be accurate — don't guess if uncertain, mark as "Unknown"
- TLDR's unique advantages (CSM, copywriting, low ad density) should be prominent
- Gaps should be honest — don't hide weaknesses
- Roadmap recs should be prioritized by deal impact"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="Competitive Feature Matrix Generator")
    parser.add_argument("--competitor", type=str, help="Single competitor to compare")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    comps = [args.competitor] if args.competitor else COMPETITORS

    print(f"  🏗️ Building feature matrix: TLDR vs {', '.join(comps)}")

    if args.dry_run:
        print("  🧪 DRY RUN: would generate matrix")
        return

    matrix = generate_matrix(comps, api_key)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    path = OUTPUT_DIR / f"competitive_feature_matrix_{today}.md"
    path.write_text(matrix, encoding="utf-8")
    print(f"  ✅ Matrix saved to {path}")


if __name__ == "__main__":
    main()
