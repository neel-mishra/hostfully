#!/usr/bin/env python3
"""
Newsletter Engagement Behavior Audit Agent

Analyzes subscriber engagement data to identify signup-to-value paths,
drop-off points, retention correlations, power user behaviors, and
churned reader patterns.

Usage:
  python engagement_behavior.py --data path/to/engagement.csv
  python engagement_behavior.py --dry-run
"""

import argparse
import csv
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
COMMANDS_DIR = WORKSPACE_ROOT / "commands"
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "product_assets" / "behavior_reports"


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


def load_csv_preview(path: Path, max_rows: int = 100) -> str:
    if not path.exists():
        return ""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return "".join(lines[:max_rows + 1])


def analyze_engagement(data_preview: str, api_key: str) -> str:
    business_context = ""
    try:
        business_context = (COMMANDS_DIR / "core" / "business_context.md").read_text()[:1500]
    except FileNotFoundError:
        pass

    prompt = f"""You are a behavioral analytics specialist for TLDR, the largest daily tech newsletter (7M+ subscribers, 12 newsletters).

Analyze this subscriber engagement data and produce a comprehensive behavior audit.

ENGAGEMENT DATA (sample):
{data_preview[:15000]}

TLDR CONTEXT:
{business_context}

TLDR BENCHMARKS:
- Open rates: 40-48% across newsletters
- 12 newsletters covering Tech, AI, Dev, InfoSec, DevOps, Product, Marketing, Founders, Crypto, Design, Data, Fintech

Generate the audit in this EXACT format:

# Newsletter Engagement Behavior Audit — {datetime.now().strftime('%Y-%m-%d')}

## Executive Summary
[3-5 key behavioral insights that should change editorial/growth strategy]

## Signup → First Value Moment
- Median editions to first click: [N]
- First-edition open rate: [%]
- Content types in first edition that predict retention: [topics]
- Recommendation: [what to optimize in onboarding]

## Retention Curve
| Editions Received | % Still Opening | Drop-Off Rate |
|---|---|---|
| 1 | ... | ... |
| 5 | ... | ... |
| 10 | ... | ... |
| 25 | ... | ... |
| 50 | ... | ... |

Critical drop-off window: editions [X] to [Y]

## What Predicts Retention
| Factor | Impact on 90-Day Retention | Confidence |
|---|---|---|
[Identify 5-8 factors from the data]

## Power User Profile
- Open rate: [%]+
- Click rate: [%]+
- Newsletters subscribed: [avg]
- Behavioral signature: [pattern]

## Churned Reader Profile
- Median lifespan: [editions]
- Common exit point: edition [N]
- Behavioral signature: [pattern]

## Cohort Analysis
| Signup Period | 30-Day Retention | 90-Day Retention | Notes |
|---|---|---|---|
[If data supports cohort grouping]

## Recommendations

### For Editorial
1. [content rec based on engagement data]
2. [content rec]

### For Growth
1. [acquisition/onboarding rec]
2. [retention rec]

### For Product
1. [feature/personalization rec]

RULES:
- Base every finding on patterns visible in the data
- Where data is insufficient, note the limitation and suggest what data to collect
- Quantify impact wherever possible
- Distinguish correlation from causation"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="Newsletter Engagement Behavior Audit")
    parser.add_argument("--data", type=str, required=True, help="Path to engagement data CSV")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"❌ File not found: {data_path}")
        sys.exit(1)

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    print(f"  📊 Loading engagement data: {data_path.name}")
    data_preview = load_csv_preview(data_path)

    if args.dry_run:
        print("  🧪 DRY RUN: would analyze engagement data")
        return

    print("  🧠 Analyzing engagement patterns...")
    report = analyze_engagement(data_preview, api_key)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    path = OUTPUT_DIR / f"engagement_audit_{today}.md"
    path.write_text(report, encoding="utf-8")
    print(f"  ✅ Audit saved to {path}")


if __name__ == "__main__":
    main()
