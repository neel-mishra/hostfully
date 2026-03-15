#!/usr/bin/env python3
"""
Sprint Planning from Customer Signals

Synthesizes advertiser feedback, call insights, engagement data, and
competitive intelligence to produce evidence-based sprint recommendations.

Usage:
  python sprint_planner.py                    # auto-load all signal sources
  python sprint_planner.py --dry-run          # preview
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
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "product_assets" / "sprint_plans"

SIGNAL_SOURCES = {
    "feedback": WORKSPACE_ROOT / "docs" / "advertiser_success" / "feedback_reports",
    "call_analysis": WORKSPACE_ROOT / "docs" / "sales_assets" / "call_analysis",
    "behavior": WORKSPACE_ROOT / "docs" / "product_assets" / "behavior_reports",
    "battlecards": WORKSPACE_ROOT / "docs" / "sales_assets" / "battlecards",
    "competitive": WORKSPACE_ROOT / "docs" / "competitor content tracker",
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


def load_latest_report(directory: Path, pattern: str = "*.md") -> str:
    if not directory.exists():
        return ""
    files = sorted(directory.glob(pattern), reverse=True)
    if files:
        try:
            return files[0].read_text(encoding="utf-8")[:4000]
        except Exception:
            pass
    return ""


def gather_signals() -> dict[str, str]:
    signals = {}

    # Feedback synthesis
    feedback = load_latest_report(SIGNAL_SOURCES["feedback"], "feedback_synthesis_*.md")
    if feedback:
        signals["feedback"] = feedback
        print("  ✓ Loaded feedback synthesis")

    # Call analysis insights
    call = load_latest_report(SIGNAL_SOURCES["call_analysis"], "insights_report_*.md")
    if call:
        signals["calls"] = call
        print("  ✓ Loaded call analysis insights")

    # Engagement behavior
    behavior = load_latest_report(SIGNAL_SOURCES["behavior"], "engagement_audit_*.md")
    if behavior:
        signals["behavior"] = behavior
        print("  ✓ Loaded engagement behavior audit")

    # Battlecard competitive gaps
    bc_dir = SIGNAL_SOURCES["battlecards"]
    if bc_dir.exists():
        bc_texts = []
        for f in sorted(bc_dir.glob("*_battlecard.md"))[:3]:
            bc_texts.append(f.read_text(encoding="utf-8")[:1500])
        if bc_texts:
            signals["competitive"] = "\n\n".join(bc_texts)
            print("  ✓ Loaded competitive battlecards")

    return signals


def generate_sprint_plan(signals: dict[str, str], api_key: str) -> str:
    business_context = ""
    try:
        business_context = (COMMANDS_DIR / "core" / "business_context.md").read_text()[:1500]
    except FileNotFoundError:
        pass

    signal_text = ""
    for source, content in signals.items():
        signal_text += f"\n--- {source.upper()} SIGNALS ---\n{content}\n"

    prompt = f"""You are a product strategist for TLDR, the largest daily tech newsletter (7M+ subscribers, 100% ad-supported).

Synthesize the following customer signals to produce evidence-based sprint recommendations.

TLDR CONTEXT:
{business_context}

SIGNALS FROM MULTIPLE SOURCES:
{signal_text[:20000]}

PRIORITIZATION FRAMEWORK:
- Request Frequency (30%): How many distinct sources raised this?
- Revenue Impact (30%): Size of accounts + churn prevention + upsell potential
- Roadmap Alignment (20%): Does it fit TLDR's strategic direction?
- Effort (20%): Inverse of complexity (quick wins score higher)

Priority Score = weighted average, 1-10.

Generate the sprint recommendation in this EXACT format:

# Sprint Recommendations — {datetime.now().strftime('%Y-%m-%d')}

## Summary
- Signals analyzed from: [list sources]
- Features identified: [count]
- Top recommendation: [feature name]

## Prioritized Feature List

### Priority 1: [Feature Name] — Score: [X]/10
- **What:** [1-2 sentence description]
- **Evidence:**
  - [Source 1]: [specific signal]
  - [Source 2]: [specific signal]
- **Revenue Impact:** [estimate]
- **Effort:** [S / M / L / XL]
- **Spec Notes:** [key requirements]

### Priority 2: [Feature Name] — Score: [X]/10
...

[Top 5 features with full detail]

## Quick Wins (High Impact, Low Effort)
| Feature | Score | Effort | Top Signal |
|---|---|---|---|

## Strategic Bets (High Impact, High Effort)
| Feature | Score | Effort | Business Case |
|---|---|---|---|

## Evidence Map
| Signal Source | Features Surfaced | Key Insight |
|---|---|---|

## What NOT to Build
[Features requested but don't align with strategy, with reasoning]

RULES:
- Every recommendation must cite specific evidence from the signals
- Deduplicate features that appear across multiple sources (combine evidence)
- Be specific about effort estimates
- "What NOT to Build" prevents wasted cycles on low-value requests"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="Sprint Planning from Customer Signals")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    print("=" * 60)
    print(f"🏗️  Sprint Planner — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    print("\n  📥 Gathering signals...")
    signals = gather_signals()

    if not signals:
        print("  ℹ No signal data found. Run other agents first:")
        print("     - feedback_synthesizer.py")
        print("     - transcript_analyzer.py")
        print("     - engagement_behavior.py")
        print("     - battlecard_generator.py")
        return

    if args.dry_run:
        print(f"  🧪 DRY RUN: would synthesize {len(signals)} signal sources")
        return

    print("\n  🧠 Generating sprint recommendations...")
    plan = generate_sprint_plan(signals, api_key)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    path = OUTPUT_DIR / f"sprint_rec_{today}.md"
    path.write_text(plan, encoding="utf-8")

    print(f"\n  ✅ Sprint plan saved to {path}")


if __name__ == "__main__":
    main()
