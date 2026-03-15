#!/usr/bin/env python3
"""
Feature Request Prioritizer

Aggregates feature requests from all customer-facing sources,
deduplicates, scores, and produces a ranked backlog.

Usage:
  python feature_request_prioritizer.py            # auto-load all sources
  python feature_request_prioritizer.py --dry-run  # preview
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "product_assets"

SOURCES = {
    "feedback": WORKSPACE_ROOT / "docs" / "advertiser_success" / "feedback_reports",
    "calls": WORKSPACE_ROOT / "docs" / "sales_assets" / "call_analysis",
    "support": WORKSPACE_ROOT / "docs" / "advertiser_success" / "health_reports",
    "battlecards": WORKSPACE_ROOT / "docs" / "sales_assets" / "battlecards",
    "interviews": WORKSPACE_ROOT / "docs" / "product_assets" / "interviews",
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


def load_latest(directory: Path, pattern: str) -> str:
    if not directory.exists():
        return ""
    files = sorted(directory.glob(pattern), reverse=True)
    if files:
        try:
            return files[0].read_text(encoding="utf-8")[:4000]
        except Exception:
            pass
    return ""


def gather_sources() -> dict[str, str]:
    gathered = {}
    for name, path in SOURCES.items():
        if name == "feedback":
            data = load_latest(path, "feedback_synthesis_*.md")
        elif name == "calls":
            data = load_latest(path, "insights_report_*.md")
        elif name == "support":
            data = load_latest(path, "support_analysis_*.md")
        elif name == "battlecards":
            bc_parts = []
            if path.exists():
                for f in sorted(path.glob("*_battlecard.md"))[:3]:
                    bc_parts.append(f.read_text(encoding="utf-8")[:1500])
            data = "\n".join(bc_parts)
        elif name == "interviews":
            data = load_latest(path, "synthesis_*.md")
        else:
            data = ""

        if data:
            gathered[name] = data
            print(f"  ✓ Loaded {name}")
    return gathered


def prioritize(sources: dict[str, str], api_key: str) -> str:
    source_text = "\n\n".join(
        f"--- {name.upper()} ---\n{content}" for name, content in sources.items()
    )

    prompt = f"""You are a product prioritization specialist for TLDR (7M+ tech newsletter subscribers, 100% ad-supported).

Aggregate feature requests from all these customer-facing sources, deduplicate, and score them.

SOURCES:
{source_text[:20000]}

SCORING FRAMEWORK (each dimension 1-10):
- Request Frequency (25%): How many distinct sources raised this?
- Revenue Impact (30%): Blocks enterprise deals? Prevents churn? Enables upsell?
- Strategic Alignment (25%): Core to TLDR's roadmap?
- Effort Inverse (20%): Quick win scores higher

Priority Score = weighted average.

Generate in this EXACT format:

# Feature Request Backlog — {datetime.now().strftime('%Y-%m-%d')}

## Summary
- Sources analyzed: {len(sources)} ({', '.join(sources.keys())})
- Unique requests identified: [count after dedup]

## Ranked Backlog

### #1: [Feature] — Score: [X]/10
- **Description:** [what it is]
- **Evidence:** [N] sources
  - [Source]: "[quote or signal]"
  - [Source]: "[quote or signal]"
- **Revenue Impact:** [estimate]
- **Effort:** [S/M/L/XL]

[Repeat for all features, ranked by score]

## Quick Wins (Score 7+, Effort S)
| Feature | Score | Top Signal |
|---|---|---|

## Strategic Bets (Score 7+, Effort L/XL)
| Feature | Score | Business Case |
|---|---|---|

## Declined / Deferred
| Feature | Score | Why Not Now |
|---|---|---|

RULES:
- Deduplicate: same request from multiple sources = higher frequency score
- Cite specific evidence for every feature
- Be honest about effort — don't underestimate
- "Declined" must have clear reasoning"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="Feature Request Prioritizer")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    print("  📥 Gathering feature request sources...")
    sources = gather_sources()

    if not sources:
        print("  ℹ No source data found. Run other agents first.")
        return

    if args.dry_run:
        print(f"  🧪 DRY RUN: would prioritize from {len(sources)} sources")
        return

    print("  🧠 Prioritizing feature requests...")
    backlog = prioritize(sources, api_key)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    path = OUTPUT_DIR / f"feature_backlog_{today}.md"
    path.write_text(backlog, encoding="utf-8")
    print(f"  ✅ Backlog saved to {path}")


if __name__ == "__main__":
    main()
