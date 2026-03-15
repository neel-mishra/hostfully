#!/usr/bin/env python3
"""
Advertiser Feedback Synthesizer

Processes advertiser feedback from markdown files and generates structured
synthesis: praise themes, friction points, feature requests, competitor
switch triggers, and actionable recommendations.

Usage:
  python feedback_synthesizer.py                          # synthesize all feedback
  python feedback_synthesizer.py --dir path/to/feedback   # custom directory
  python feedback_synthesizer.py --dry-run                # preview
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
COMMANDS_DIR = WORKSPACE_ROOT / "commands"
FEEDBACK_DIR = WORKSPACE_ROOT / "docs" / "advertiser_success" / "feedback_reports" / "raw"
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "advertiser_success" / "feedback_reports"


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


def discover_feedback_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(
        f for f in directory.rglob("*.md")
        if f.is_file() and not f.name.startswith("_")
    )


def synthesize_feedback(files: list[Path], api_key: str) -> str:
    """Load all feedback files and run synthesis through Claude."""
    all_feedback = []
    for f in files:
        content = f.read_text(encoding="utf-8")
        all_feedback.append(f"--- FILE: {f.name} ---\n{content[:3000]}\n")

    combined = "\n".join(all_feedback)

    business_context = ""
    try:
        business_context = (COMMANDS_DIR / "core" / "business_context.md").read_text()[:1500]
    except FileNotFoundError:
        pass

    prompt = f"""You are an advertiser insights analyst for TLDR, the largest daily tech newsletter (7M+ subscribers).

Analyze the following advertiser feedback and produce a structured synthesis report.

FEEDBACK ({len(files)} sources):
{combined[:25000]}

TLDR CONTEXT:
{business_context}

Generate the report in this EXACT markdown format:

# Advertiser Feedback Synthesis — {datetime.now().strftime('%Y-%m-%d')}

## Summary
- Feedback sources analyzed: {len(files)}
- Advertisers represented: [count unique advertisers]
- Overall sentiment: [positive / mixed / negative]

## Praise Themes
| Theme | Frequency | Top Quote | Advertisers |
|---|---|---|---|
[Identify 4-6 themes of positive feedback]

## Friction Points
| Theme | Frequency | Severity (1-5) | Top Quote | Suggested Fix |
|---|---|---|---|---|
[Identify 4-6 themes of negative feedback]

## Feature Requests (Ranked)
| Request | Frequency | Revenue Weight | Feasibility | Requesting Advertisers |
|---|---|---|---|---|
[Rank by frequency * revenue impact]

## Competitor Switch Triggers
| Competitor | Trigger | Frequency | Risk Level |
|---|---|---|---|
[Any signals of advertisers considering alternatives]

## Sentiment Distribution
| Category | Count | % | Key Names |
|---|---|---|---|
| Promoters | ... | ... | ... |
| Passives | ... | ... | ... |
| Detractors | ... | ... | ... |

## Actionable Recommendations

### For CS Team
1. [action]
2. [action]

### For Sales Team
1. [action]
2. [action]

### For Product Team
1. [action]
2. [action]

### For Editorial/Content Team
1. [action]

RULES:
- Use actual quotes from the feedback where possible
- Be specific about which advertisers said what
- Rank everything by impact (frequency * revenue weight)
- Every friction point must have a suggested fix"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="Advertiser Feedback Synthesizer")
    parser.add_argument("--dir", type=str, help="Custom feedback directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    feedback_dir = Path(args.dir) if args.dir else FEEDBACK_DIR
    print(f"  📂 Scanning: {feedback_dir}")

    files = discover_feedback_files(feedback_dir)
    if not files:
        print(f"  ℹ No feedback files found in {feedback_dir}")
        print(f"  Add markdown feedback files and re-run.")

        FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
        return

    print(f"  Found {len(files)} feedback file(s)\n")

    if args.dry_run:
        print(f"  🧪 DRY RUN: would synthesize {len(files)} files")
        for f in files:
            print(f"     - {f.name}")
        return

    print("  🧠 Synthesizing feedback...")
    report = synthesize_feedback(files, api_key)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = OUTPUT_DIR / f"feedback_synthesis_{today}.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"  ✅ Synthesis saved to {report_path}")


if __name__ == "__main__":
    main()
