#!/usr/bin/env python3
"""
Deal Risk Analysis from Notes

Analyzes CRM notes, email threads, and call summaries to assess deal health
for active advertising opportunities. Flags at-risk deals with specific
warning signals and recommended save actions.

Usage:
  python deal_risk_analyzer.py --dir path/to/deal-notes/   # analyze folder of notes
  python deal_risk_analyzer.py --file path/to/note.md       # single deal
  python deal_risk_analyzer.py --dry-run                     # preview
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
COMMANDS_DIR = WORKSPACE_ROOT / "commands"
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "sales_assets"


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


def discover_notes(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(
        f for f in directory.iterdir()
        if f.is_file() and f.suffix in (".md", ".txt") and not f.name.startswith("_")
    )


def analyze_deals(notes: list[tuple[str, str]], api_key: str) -> str:
    notes_text = "\n\n".join(
        f"--- DEAL: {name} ---\n{content[:4000]}" for name, content in notes
    )

    competitor_context = ""
    try:
        competitor_context = (COMMANDS_DIR / "core" / "competitor_landscape.md").read_text()[:2000]
    except FileNotFoundError:
        pass

    prompt = f"""You are a deal risk analyst for TLDR's advertising sales team (7M+ tech newsletter subscribers, 100% ad-supported).

Analyze these deal notes and assess the health of each opportunity.

DEAL NOTES ({len(notes)} deals):
{notes_text[:20000]}

COMPETITOR CONTEXT:
{competitor_context}

RISK SIGNAL CATEGORIES:
- Champion Risk: single-threaded, champion silent, role change
- Timing Risk: slipping timeline, "revisit next quarter"
- Budget Risk: unconfirmed budget, competing priorities, freeze
- Competition Risk: evaluating LinkedIn/Meta/Paved/etc.
- Decision Risk: committee involved, no clear decision-maker
- Engagement Risk: slower responses, shorter replies
- Fit Risk: audience mismatch, wrong newsletter

RISK LEVELS:
- On Track (Green): Active engagement, clear next steps, budget confirmed
- Needs Attention (Yellow): 1-2 warning signals
- At Risk (Red): 3+ warning signals
- Lost Likely (Black): Strong negative signals

Generate the report in this EXACT format:

# Deal Risk Analysis — {datetime.now().strftime('%Y-%m-%d')}

## Pipeline Summary
| Risk Level | Count | Deals |
|---|---|---|

## At-Risk Deals (Action Required)

[For each Red/Black deal:]
### {{Company}} — RED
- **Risk Signals:** [specific signals detected from notes]
- **Key Quote:** "[concerning quote]"
- **Save Actions:**
  1. [specific action]
  2. [specific action]
- **Escalation:** [who should get involved]

## Needs Attention Deals

[For each Yellow deal:]
### {{Company}} — YELLOW
- **Risk Signal:** [primary concern]
- **Recommended Action:** [one action]

## Healthy Deals (On Track)
| Company | Next Step | Confidence |
|---|---|---|

## Cross-Deal Patterns
[Any patterns across deals: common objections, competitor trends, timing issues]

RULES:
- Cite specific evidence from the notes for every risk signal
- Save actions must be concrete and specific to this deal
- Be honest about lost-likely deals — don't sugarcoat
- Cross-deal patterns help the sales team address systemic issues"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="Deal Risk Analysis from Notes")
    parser.add_argument("--dir", type=str, help="Directory of deal note files")
    parser.add_argument("--file", type=str, help="Single deal note file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    notes = []
    if args.file:
        p = Path(args.file)
        if p.exists():
            notes.append((p.stem, p.read_text(encoding="utf-8")))
    elif args.dir:
        for p in discover_notes(Path(args.dir)):
            notes.append((p.stem, p.read_text(encoding="utf-8")))
    else:
        print("Specify --dir or --file. Use --help for options.")
        return

    if not notes:
        print("  ℹ No deal notes found.")
        return

    print(f"  📋 Analyzing {len(notes)} deal(s)...")

    if args.dry_run:
        for name, _ in notes:
            print(f"     - {name}")
        return

    report = analyze_deals(notes, api_key)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    path = OUTPUT_DIR / f"deal_risk_{today}.md"
    path.write_text(report, encoding="utf-8")
    print(f"  ✅ Analysis saved to {path}")


if __name__ == "__main__":
    main()
