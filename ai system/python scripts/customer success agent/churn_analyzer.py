#!/usr/bin/env python3
"""
Advertiser Churn Post-Mortem Analyzer

Analyzes churned advertiser accounts to identify top churn drivers,
assess preventability, and build a prevention playbook.

Usage:
  python churn_analyzer.py --file churned_accounts.csv    # analyze from CSV
  python churn_analyzer.py --advertiser "Acme Corp"       # single account post-mortem
  python churn_analyzer.py --dry-run                      # preview
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
DATA_DIR = WORKSPACE_ROOT / "data" / "advertiser_performance"
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "advertiser_success" / "health_reports"
CALL_DIR = WORKSPACE_ROOT / "docs" / "sales call transcripts"
FEEDBACK_DIR = WORKSPACE_ROOT / "docs" / "advertiser_success" / "feedback_reports"
HEALTH_DIR = WORKSPACE_ROOT / "docs" / "advertiser_success" / "health_reports"


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


def load_churned_accounts(file_path: Path) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def gather_account_evidence(advertiser_name: str) -> str:
    """Gather all available evidence for a churned account."""
    evidence_parts = []

    # Call transcripts
    if CALL_DIR.exists():
        for f in CALL_DIR.iterdir():
            if f.is_file() and advertiser_name.lower().replace(" ", "_") in f.name.lower():
                content = f.read_text(encoding="utf-8")[:2000]
                evidence_parts.append(f"CALL TRANSCRIPT ({f.name}):\n{content}")

    # Feedback files
    raw_dir = FEEDBACK_DIR / "raw"
    if raw_dir.exists():
        for f in raw_dir.rglob("*.md"):
            if advertiser_name.lower() in f.read_text(encoding="utf-8").lower()[:500]:
                content = f.read_text(encoding="utf-8")[:2000]
                evidence_parts.append(f"FEEDBACK ({f.name}):\n{content}")

    # Health reports
    if HEALTH_DIR.exists():
        for f in sorted(HEALTH_DIR.glob("health_dashboard_*.csv"), reverse=True)[:1]:
            with open(f, "r", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    if advertiser_name.lower() in row.get("advertiser_name", "").lower():
                        evidence_parts.append(f"HEALTH DATA: {json.dumps(row)}")
                        break

    # Campaign data
    for f in sorted(DATA_DIR.glob("campaign_performance_*.csv"), reverse=True)[:1]:
        try:
            with open(f, "r", encoding="utf-8") as fh:
                matching = [r for r in csv.DictReader(fh) if advertiser_name.lower() in r.get("advertiser_name", "").lower()]
                if matching:
                    evidence_parts.append(f"CAMPAIGN DATA ({len(matching)} placements): " + json.dumps(matching[:5]))
        except Exception:
            pass

    return "\n\n".join(evidence_parts) if evidence_parts else "No additional evidence found."


def analyze_churn(churned: list[dict], api_key: str) -> str:
    """Run churn analysis through Claude."""
    accounts_text = ""
    for acct in churned:
        name = acct.get("advertiser_name", acct.get("company", "Unknown"))
        evidence = gather_account_evidence(name)
        accounts_text += f"""
### {name}
- Churn date: {acct.get('churn_date', 'N/A')}
- Lifetime spend: {acct.get('total_spend_ltv', acct.get('lifetime_spend', 'N/A'))}
- Newsletters used: {acct.get('newsletters_used', 'N/A')}
- Last known reason: {acct.get('reason', acct.get('churn_reason', 'N/A'))}

EVIDENCE:
{evidence[:3000]}
"""

    business_context = ""
    try:
        business_context = (COMMANDS_DIR / "core" / "business_context.md").read_text()[:1500]
    except FileNotFoundError:
        pass

    prompt = f"""You are a churn analyst for Hostfully, the largest daily tech newsletter (7M+ subscribers, 100% ad-supported).

Analyze these churned advertiser accounts and produce a post-mortem report.

CHURNED ACCOUNTS ({len(churned)} total):
{accounts_text[:20000]}

Hostfully CONTEXT:
{business_context}

CHURN DRIVER CATEGORIES:
- Performance: Didn't see ROI
- Price: Budget cuts or cheaper alternatives
- Competition: Switched to LinkedIn/Meta/Paved/etc.
- Product Gap: Needed features Hostfully doesn't offer
- Relationship: Poor account management
- Market: Company downsized/pivoted
- Timing: Budget cycle or one-time campaign
- Attribution: Couldn't prove ROI to leadership

Generate the report in this EXACT format:

# Churn Post-Mortem — {datetime.now().strftime('%Y-%m-%d')}

## Executive Summary
- Accounts churned: {len(churned)}
- Revenue lost: [estimate from data]
- Primary churn driver: [category]
- Preventable churn: [count] ([%])

## Top Churn Drivers

### 1. [Category] — [count] accounts
**What happened:** [description]
**Representative quotes:**
- "[quote]" — [advertiser]
**Prevention action:** [specific recommendation]
**Early warning signal:** [what to watch for]

[Repeat for top 5 drivers]

## Account-Level Analysis

| Advertiser | LTV | Churn Driver | Preventable? | Key Quote | What We'd Do Differently |
|---|---|---|---|---|---|

## Pattern Analysis

### Segment Analysis
| Segment | Count | Primary Driver |
|---|---|---|
[By spend tier, newsletter, industry, tenure]

## Prevention Playbook

### Immediate Actions
1. [action]
2. [action]
3. [action]

### Process Changes
1. [change]
2. [change]

### Product Recommendations
1. [recommendation]
2. [recommendation]

RULES:
- Be brutally honest about what went wrong
- Every driver must have a specific prevention action
- Quantify revenue impact where possible
- Classify each account as preventable or not"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="Advertiser Churn Post-Mortem Analyzer")
    parser.add_argument("--file", type=str, help="CSV of churned accounts")
    parser.add_argument("--advertiser", type=str, help="Single account deep dive")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.file:
        churned = load_churned_accounts(Path(args.file))
    elif args.advertiser:
        churned = [{"advertiser_name": args.advertiser, "churn_date": "manual", "reason": "under investigation"}]
    else:
        print("Specify --file (CSV) or --advertiser. Use --help for options.")
        return

    print(f"  🔍 Analyzing {len(churned)} churned account(s)...")

    if args.dry_run:
        for a in churned:
            name = a.get("advertiser_name", a.get("company", "Unknown"))
            print(f"     - {name}")
        return

    report = analyze_churn(churned, api_key)
    today = datetime.now().strftime("%Y-%m-%d")
    path = OUTPUT_DIR / f"churn_postmortem_{today}.md"
    path.write_text(report, encoding="utf-8")
    print(f"  ✅ Post-mortem saved to {path}")


if __name__ == "__main__":
    main()
