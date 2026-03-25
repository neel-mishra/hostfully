#!/usr/bin/env python3
"""
Support Ticket Pattern Analyzer

Processes advertiser support tickets to identify recurring patterns,
systemic problems, and product gaps.

Usage:
  python support_ticket_analyzer.py --file tickets.csv       # from CSV
  python support_ticket_analyzer.py --dir path/to/tickets/    # from markdown files
  python support_ticket_analyzer.py --dry-run                  # preview
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
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "advertiser_success" / "health_reports"
TICKETS_DIR = WORKSPACE_ROOT / "docs" / "advertiser_success" / "support_tickets"


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


def load_tickets_csv(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return "".join(lines[:200])


def load_tickets_dir(directory: Path) -> str:
    parts = []
    for f in sorted(directory.iterdir()):
        if f.is_file() and f.suffix in (".md", ".txt") and not f.name.startswith("_"):
            parts.append(f"--- TICKET: {f.name} ---\n{f.read_text(encoding='utf-8')[:1500]}")
    return "\n\n".join(parts[:50])


def analyze_tickets(ticket_data: str, api_key: str) -> str:
    prompt = f"""You are a support intelligence analyst for TLDR, the largest daily tech newsletter (7M+ subscribers, 100% ad-supported).

Analyze these advertiser support tickets and identify patterns.

TICKET DATA:
{ticket_data[:20000]}

CATEGORIES TO USE:
- Reporting/Analytics
- Creative/Copy
- Scheduling/Availability
- Billing/Invoicing
- Performance
- Technical
- Onboarding
- Account Management

Generate the report in this EXACT format:

# Support Ticket Pattern Analysis — {datetime.now().strftime('%Y-%m-%d')}

## Summary
- Tickets analyzed: [count]
- Top category: [category] ([count] tickets)
- Most affected advertiser: [name] ([count] tickets)

## Volume by Category
| Category | Count | % of Total | Severity |
|---|---|---|---|

## Top Patterns

### Pattern 1: [Description] — [count] tickets
- **Root Cause:** [underlying issue]
- **Affected Advertisers:** [list]
- **Impact:** [churn risk / revenue impact / satisfaction impact]
- **Fix:** [specific recommendation]

### Pattern 2: [Description] — [count] tickets
- **Root Cause:** [underlying issue]
- **Affected Advertisers:** [list]
- **Impact:** [impact]
- **Fix:** [recommendation]

[Top 5 patterns]

## Repeat Ticket Advertisers
| Advertiser | Ticket Count | Categories | Churn Risk |
|---|---|---|---|

## Recommendations

### For Product/Engineering
1. [fix that eliminates the top ticket driver]
2. [fix]

### For CS Process
1. [process improvement]
2. [improvement]

### For Onboarding
1. [reduce onboarding friction]

RULES:
- Group similar tickets into patterns — don't list individual tickets
- Root causes should be systemic, not per-ticket
- Fixes should be actionable and specific
- Flag advertisers with 3+ tickets as churn risk"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="Support Ticket Pattern Analyzer")
    parser.add_argument("--file", type=str, help="Path to tickets CSV")
    parser.add_argument("--dir", type=str, help="Directory of ticket markdown files")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    if args.file:
        ticket_data = load_tickets_csv(Path(args.file))
    elif args.dir:
        ticket_data = load_tickets_dir(Path(args.dir))
    else:
        default_dir = TICKETS_DIR
        if default_dir.exists() and any(default_dir.iterdir()):
            ticket_data = load_tickets_dir(default_dir)
        else:
            print("Specify --file or --dir. Use --help for options.")
            print(f"  Or add tickets to {TICKETS_DIR}")
            TICKETS_DIR.mkdir(parents=True, exist_ok=True)
            return

    if args.dry_run:
        print("  🧪 DRY RUN: would analyze support tickets")
        return

    print("  🎫 Analyzing support ticket patterns...")
    report = analyze_tickets(ticket_data, api_key)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    path = OUTPUT_DIR / f"support_analysis_{today}.md"
    path.write_text(report, encoding="utf-8")
    print(f"  ✅ Analysis saved to {path}")


if __name__ == "__main__":
    main()
