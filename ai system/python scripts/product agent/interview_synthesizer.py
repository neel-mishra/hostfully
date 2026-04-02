#!/usr/bin/env python3
"""
User Interview Synthesizer

Processes transcripts from advertiser or subscriber interviews and extracts
structured themes: JTBD, pain points, feature wishes, competitor mentions.

Usage:
  python interview_synthesizer.py --dir path/to/interviews/   # batch
  python interview_synthesizer.py --file path/to/interview.md  # single
  python interview_synthesizer.py --dry-run                     # preview
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

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
INTERVIEWS_DIR = WORKSPACE_ROOT / "docs" / "product_assets" / "interviews"
SUMMARIES_DIR = INTERVIEWS_DIR / "summaries"
OUTPUT_DIR = INTERVIEWS_DIR


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


def discover_interviews(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(
        f for f in directory.iterdir()
        if f.is_file() and f.suffix in (".md", ".txt") and not f.name.startswith("_") and "summary" not in f.name.lower()
    )


def analyze_interview(content: str, filename: str, api_key: str) -> str:
    prompt = f"""You are a user research analyst for Hostfully, the largest daily tech newsletter (7M+ subscribers).

Analyze this interview transcript and extract structured insights.

INTERVIEW ({filename}):
{content[:15000]}

Generate the summary in this EXACT format:

# Interview Summary: [Name] — [Date]

## Profile
- **Type:** Advertiser / Reader
- **Role:** [title]
- **Company:** [company]
- **Hostfully Usage:** [which newsletters, how long, frequency]

## Jobs to Be Done
- [JTBD 1 — what job are they hiring Hostfully for?]
- [JTBD 2]

## Pain Points
| Pain Point | Severity (1-5) | Quote |
|---|---|---|

## Delights
| What They Love | Quote |
|---|---|

## Feature Wishes
| Request | Urgency | Quote |
|---|---|---|

## Competitor Context
| Competitor/Alternative | Usage | Comparison to Hostfully |
|---|---|---|

## Key Quotes
1. "[most powerful quote for marketing]"
2. "[most insightful quote for product]"
3. "[quote about competitor/alternative]"

## Actionable Takeaways
1. For product: [specific action]
2. For sales/CS: [specific action]
3. For content: [specific action]

RULES:
- Extract exact quotes where possible
- Severity should reflect how much the pain point affects their Hostfully usage
- JTBD should be framed as "When [situation], I want [motivation], so I can [outcome]"
- Be specific in takeaways — not "improve the product" but "add self-serve reporting dashboard" """

    return claude_generate(prompt, api_key)


def generate_synthesis(summaries: list[str], api_key: str) -> str:
    combined = "\n\n---\n\n".join(s[:3000] for s in summaries)

    prompt = f"""You are synthesizing insights across {len(summaries)} user interviews for Hostfully newsletters.

INTERVIEW SUMMARIES:
{combined[:20000]}

Generate a cross-interview synthesis in this format:

# Interview Synthesis — {datetime.now().strftime('%Y-%m-%d')}

## Summary
- Interviews analyzed: {len(summaries)}

## Top Jobs to Be Done
| JTBD | Frequency | Type (Adv/Reader) | Representative Quote |
|---|---|---|---|

## Pain Point Themes
| Theme | Frequency | Avg Severity | Quote | Recommended Fix |
|---|---|---|---|---|

## Feature Requests (Ranked)
| Request | Frequency | Urgency | Requesting Segment |
|---|---|---|---|

## Competitive Landscape (From Interviews)
| Competitor | Mentions | Sentiment | Key Insight |
|---|---|---|---|

## Delight Themes (Protect These)
| Theme | Frequency | Quote |
|---|---|---|

## Recommendations
### For Product
1. [recommendation with evidence]
### For Marketing
1. [quotes to use in campaigns]
### For Sales
1. [talking points from interviews]"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="User Interview Synthesizer")
    parser.add_argument("--dir", type=str, help="Directory of interview files")
    parser.add_argument("--file", type=str, help="Single interview file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    interview_dir = Path(args.dir) if args.dir else INTERVIEWS_DIR
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

    if args.file:
        p = Path(args.file)
        if not p.exists():
            print(f"❌ File not found: {p}")
            sys.exit(1)
        print(f"  📋 Analyzing: {p.name}")
        if not args.dry_run:
            summary = analyze_interview(p.read_text(encoding="utf-8"), p.name, api_key)
            out = SUMMARIES_DIR / f"{p.stem}_summary.md"
            out.write_text(summary, encoding="utf-8")
            print(f"  ✅ Summary saved to {out}")
        return

    interviews = discover_interviews(interview_dir)
    if not interviews:
        print(f"  ℹ No interviews found in {interview_dir}")
        INTERVIEWS_DIR.mkdir(parents=True, exist_ok=True)
        return

    print(f"  Found {len(interviews)} interview(s)\n")

    if args.dry_run:
        for f in interviews:
            print(f"     - {f.name}")
        return

    summaries = []
    for f in interviews:
        print(f"  📋 Analyzing: {f.name}")
        content = f.read_text(encoding="utf-8")
        summary = analyze_interview(content, f.name, api_key)
        summaries.append(summary)
        out = SUMMARIES_DIR / f"{f.stem}_summary.md"
        out.write_text(summary, encoding="utf-8")
        print(f"     ✅ {out.name}")
        time.sleep(2)

    if len(summaries) >= 2:
        print("\n  🧠 Generating cross-interview synthesis...")
        synthesis = generate_synthesis(summaries, api_key)
        today = datetime.now().strftime("%Y-%m-%d")
        syn_path = OUTPUT_DIR / f"synthesis_{today}.md"
        syn_path.write_text(synthesis, encoding="utf-8")
        print(f"  ✅ Synthesis saved to {syn_path}")


if __name__ == "__main__":
    main()
