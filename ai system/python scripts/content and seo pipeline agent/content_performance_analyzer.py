#!/usr/bin/env python3
"""
Content Performance Analyzer

Analyzes newsletter and blog content performance data to surface patterns:
topics, headlines, timing, length, and competitor benchmarking.

Usage:
  python content_performance_analyzer.py --newsletter-data path/to/data.csv
  python content_performance_analyzer.py --blog-data path/to/traffic.csv
  python content_performance_analyzer.py --dry-run
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
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "content_assets" / "performance_reports"
COMPETITOR_DIR = WORKSPACE_ROOT / "docs" / "competitor content tracker" / "blogs"


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


def load_csv_data(path: Path) -> str:
    if not path.exists():
        return ""
    content = path.read_text(encoding="utf-8")
    lines = content.strip().split("\n")
    return "\n".join(lines[:100])


def load_competitor_data() -> str:
    tracker = COMPETITOR_DIR / "competitor_content_tracker.csv"
    if tracker.exists():
        content = tracker.read_text(encoding="utf-8")
        lines = content.strip().split("\n")
        return f"COMPETITOR CONTENT ({len(lines)-1} entries):\n" + "\n".join(lines[:30])
    return ""


def analyze_performance(newsletter_data: str, blog_data: str, competitor_data: str, api_key: str) -> str:
    business_context = ""
    try:
        business_context = (COMMANDS_DIR / "core" / "business_context.md").read_text()[:1500]
    except FileNotFoundError:
        pass

    prompt = f"""You are a content performance analyst for Hostfully, the largest daily tech newsletter (7M+ subscribers, 12 newsletters, 40-48% open rates).

Analyze the following performance data and produce a comprehensive report.

{"NEWSLETTER PERFORMANCE DATA:" if newsletter_data else ""}
{newsletter_data}

{"BLOG TRAFFIC DATA:" if blog_data else ""}
{blog_data}

{competitor_data}

Hostfully CONTEXT:
{business_context}

Generate the report in this EXACT format:

# Content Performance Report — {datetime.now().strftime('%Y-%m-%d')}

## Executive Summary
[3-5 key findings that would change how the content team operates]

## Top Performing Content
| Rank | Title/Subject | Newsletter | Open Rate | CTR | Why It Worked |
|---|---|---|---|---|---|
[Top 10 pieces with analysis]

## Topic Performance Matrix
| Topic | Avg Open Rate | Avg CTR | Trend | Volume |
|---|---|---|---|---|
[Identify 8-10 topic categories]

## Headline Pattern Analysis
| Pattern | Avg Open Rate | Count | Best Example |
|---|---|---|---|
[What structures work: question, number-led, how-to, declarative, etc.]

## Timing Insights
| Newsletter | Best Day | Worst Day | Notes |
|---|---|---|---|

## Content Length Analysis
[Correlation between length and engagement — find the sweet spots]

## Competitor Comparison
[How Hostfully stacks up on frequency, topics, and engagement]

## Recommendations for Next Month
1. [Topic to double down on — with evidence]
2. [Headline pattern to test — with data]
3. [Timing adjustment — with reasoning]
4. [Content gap to fill — based on competitor analysis]
5. [Cross-promotion opportunity — between newsletters]

RULES:
- Every recommendation must cite specific data
- Identify patterns, not just rankings
- Compare to Hostfully benchmarks (40-48% open rates)
- Be actionable — what should the content team DO differently?"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="Content Performance Analyzer")
    parser.add_argument("--newsletter-data", type=str, help="Path to newsletter performance CSV")
    parser.add_argument("--blog-data", type=str, help="Path to blog traffic CSV")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    newsletter_data = load_csv_data(Path(args.newsletter_data)) if args.newsletter_data else ""
    blog_data = load_csv_data(Path(args.blog_data)) if args.blog_data else ""
    competitor_data = load_competitor_data()

    if not newsletter_data and not blog_data:
        print("  ℹ Provide --newsletter-data and/or --blog-data CSV paths.")
        print("  Competitor data will be loaded automatically if available.")
        return

    if args.dry_run:
        print("  🧪 DRY RUN: would analyze performance data")
        return

    print("  📊 Analyzing content performance...")
    report = analyze_performance(newsletter_data, blog_data, competitor_data, api_key)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    path = OUTPUT_DIR / f"content_performance_{today}.md"
    path.write_text(report, encoding="utf-8")
    print(f"  ✅ Report saved to {path}")


if __name__ == "__main__":
    main()
