#!/usr/bin/env python3
"""
Advertiser Health & Renewal Risk Agent

Analyzes advertiser account data to flag churn risk and recommend
retention interventions. Scores each advertiser Green/Yellow/Red
across 5 dimensions and generates a prioritized action plan.

Usage:
  python advertiser_health.py                          # full health audit
  python advertiser_health.py --advertiser "Acme Corp" # single account
  python advertiser_health.py --dry-run                # preview
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
COMMANDS_DIR = WORKSPACE_ROOT / "commands"
DATA_DIR = WORKSPACE_ROOT / "data" / "advertiser_performance"
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "advertiser_success" / "health_reports"
CALL_ANALYSIS_DIR = WORKSPACE_ROOT / "docs" / "sales_assets" / "call_analysis"

HEALTH_CSV_COLUMNS = [
    "advertiser_name", "risk_level", "spend_trend", "days_to_renewal",
    "last_contact_days", "avg_ctr", "ctr_vs_benchmark", "primary_risk_factor",
    "recommended_action", "urgency",
]

TLDR_CTR_BENCHMARK = 0.02  # 2% average CTR across newsletters


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


def claude_generate(prompt: str, api_key: str, max_tokens: int = 4096, retries: int = 3) -> str:
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
                timeout=120,
            )
            if resp.status_code == 200:
                return resp.json()["content"][0]["text"]
            if resp.status_code == 429:
                time.sleep(min(60, 2 ** (attempt + 2)))
                continue
            print(f"  ⚠ Claude API error {resp.status_code}: {resp.text[:200]}")
            time.sleep(5)
        except Exception as e:
            print(f"  ⚠ Claude API exception: {e}")
            time.sleep(10)
    raise Exception("Max retries reached for Claude API")


def load_advertiser_data() -> list[dict]:
    """Load the most recent advertiser health CSV."""
    csvs = sorted(DATA_DIR.glob("advertiser_health_*.csv"), reverse=True)
    if not csvs:
        return []
    with open(csvs[0], "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_campaign_data() -> list[dict]:
    """Load the most recent campaign performance CSV."""
    csvs = sorted(DATA_DIR.glob("campaign_performance_*.csv"), reverse=True)
    if not csvs:
        return []
    with open(csvs[0], "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def score_advertiser(adv: dict) -> dict:
    """Score an advertiser on 5 dimensions and assign risk level."""
    today = datetime.now()
    scores = {}

    # Dimension 1: Spend Trend
    trend = adv.get("spend_trend", "stable").lower()
    q_this = float(adv.get("spend_this_quarter", 0) or 0)
    q_last = float(adv.get("spend_last_quarter", 0) or 0)
    if trend == "declining" or (q_last > 0 and q_this < q_last * 0.75):
        scores["spend"] = "Red"
    elif trend == "declining" or (q_last > 0 and q_this < q_last * 0.9):
        scores["spend"] = "Yellow"
    else:
        scores["spend"] = "Green"

    # Dimension 2: Campaign Performance
    avg_ctr = float(adv.get("avg_ctr", 0) or 0)
    if avg_ctr >= TLDR_CTR_BENCHMARK:
        scores["performance"] = "Green"
    elif avg_ctr >= TLDR_CTR_BENCHMARK * 0.7:
        scores["performance"] = "Yellow"
    else:
        scores["performance"] = "Red"

    # Dimension 3: Communication Recency
    last_contact = adv.get("last_contact_date", "")
    if last_contact:
        try:
            contact_date = datetime.strptime(last_contact, "%Y-%m-%d")
            days_since = (today - contact_date).days
        except ValueError:
            days_since = 999
    else:
        days_since = 999

    if days_since <= 14:
        scores["communication"] = "Green"
    elif days_since <= 30:
        scores["communication"] = "Yellow"
    else:
        scores["communication"] = "Red"

    # Dimension 4: Renewal Proximity
    renewal_date = adv.get("contract_renewal", "")
    if renewal_date:
        try:
            renewal = datetime.strptime(renewal_date, "%Y-%m-%d")
            days_to_renewal = (renewal - today).days
        except ValueError:
            days_to_renewal = 999
    else:
        days_to_renewal = 999

    if days_to_renewal > 60:
        scores["renewal"] = "Green"
    elif days_to_renewal > 30:
        scores["renewal"] = "Yellow"
    else:
        scores["renewal"] = "Red"

    # Dimension 5: Engagement Signals (NPS as proxy)
    nps = int(adv.get("nps_score", 8) or 8)
    if nps >= 8:
        scores["engagement"] = "Green"
    elif nps >= 6:
        scores["engagement"] = "Yellow"
    else:
        scores["engagement"] = "Red"

    # Overall risk level
    red_count = sum(1 for v in scores.values() if v == "Red")
    yellow_count = sum(1 for v in scores.values() if v == "Yellow")

    if red_count >= 3:
        overall = "Red"
    elif red_count >= 2 or yellow_count >= 3:
        overall = "Yellow"
    else:
        overall = "Green"

    # Primary risk factor
    risk_priority = ["spend", "performance", "communication", "renewal", "engagement"]
    primary_risk = "None"
    for dim in risk_priority:
        if scores[dim] == "Red":
            primary_risk = dim
            break
    if primary_risk == "None":
        for dim in risk_priority:
            if scores[dim] == "Yellow":
                primary_risk = dim
                break

    urgency = "critical" if overall == "Red" and days_to_renewal < 30 else (
        "high" if overall == "Red" else ("medium" if overall == "Yellow" else "low")
    )

    ctr_benchmark = "above" if avg_ctr >= TLDR_CTR_BENCHMARK else (
        "at" if avg_ctr >= TLDR_CTR_BENCHMARK * 0.7 else "below"
    )

    return {
        "advertiser_name": adv.get("advertiser_name", "Unknown"),
        "risk_level": overall,
        "spend_trend": trend,
        "days_to_renewal": days_to_renewal if days_to_renewal < 999 else "N/A",
        "last_contact_days": days_since if days_since < 999 else "N/A",
        "avg_ctr": f"{avg_ctr:.3f}" if avg_ctr else "N/A",
        "ctr_vs_benchmark": ctr_benchmark,
        "primary_risk_factor": primary_risk,
        "urgency": urgency,
        "dimension_scores": scores,
        "raw_data": adv,
    }


def generate_interventions(scored_accounts: list[dict], api_key: str) -> list[dict]:
    """Use Claude to generate specific interventions for at-risk accounts."""
    at_risk = [a for a in scored_accounts if a["risk_level"] in ("Red", "Yellow")]
    if not at_risk:
        for a in scored_accounts:
            a["recommended_action"] = "Monitor — no immediate action needed"
        return scored_accounts

    context = ""
    try:
        context = (COMMANDS_DIR / "core" / "business_context.md").read_text()[:2000]
    except FileNotFoundError:
        pass

    summaries = "\n".join(
        f"- {a['advertiser_name']}: risk={a['risk_level']}, factor={a['primary_risk_factor']}, "
        f"spend_trend={a['spend_trend']}, days_to_renewal={a['days_to_renewal']}, "
        f"last_contact={a['last_contact_days']} days ago, CTR={a['avg_ctr']}"
        for a in at_risk
    )

    prompt = f"""You are a customer success strategist for TLDR newsletters (7M+ tech subscribers).

For each at-risk advertiser account below, recommend a specific intervention action in one concise sentence.

CONTEXT:
{context}

AT-RISK ACCOUNTS:
{summaries}

Return STRICTLY as JSON (no other text):
```json
[{{"advertiser_name": "...", "recommended_action": "One sentence intervention"}}]
```"""

    try:
        raw = claude_generate(prompt, api_key)
    except Exception:
        for a in scored_accounts:
            a["recommended_action"] = "Review account manually (Claude unavailable)"
        return scored_accounts

    json_start = raw.find("[")
    json_end = raw.rfind("]") + 1
    if json_start == -1:
        for a in scored_accounts:
            if "recommended_action" not in a:
                a["recommended_action"] = "Monitor — no immediate action needed"
        return scored_accounts

    try:
        interventions = json.loads(raw[json_start:json_end])
        action_map = {i["advertiser_name"]: i["recommended_action"] for i in interventions}
        for a in scored_accounts:
            a["recommended_action"] = action_map.get(a["advertiser_name"], "Monitor — no immediate action needed")
    except (json.JSONDecodeError, KeyError):
        for a in scored_accounts:
            if "recommended_action" not in a:
                a["recommended_action"] = "Review account manually"

    return scored_accounts


def write_health_csv(accounts: list[dict], dry_run: bool = False) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    csv_path = OUTPUT_DIR / f"health_dashboard_{today}.csv"

    if dry_run:
        print(f"  🧪 DRY RUN: would write {len(accounts)} accounts to {csv_path}")
        return csv_path

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEALTH_CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(accounts)

    print(f"  ✅ Health dashboard saved to {csv_path}")
    return csv_path


def write_action_plan(accounts: list[dict], dry_run: bool = False) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = OUTPUT_DIR / f"action_plan_{today}.md"

    green = [a for a in accounts if a["risk_level"] == "Green"]
    yellow = [a for a in accounts if a["risk_level"] == "Yellow"]
    red = [a for a in accounts if a["risk_level"] == "Red"]

    red_section = ""
    for a in red:
        red_section += f"""
### {a['advertiser_name']} — RISK: {a['primary_risk_factor']}
- **Spend Trend:** {a['spend_trend']}
- **Renewal:** {a['days_to_renewal']} days
- **Last Contact:** {a['last_contact_days']} days ago
- **CTR vs Benchmark:** {a['ctr_vs_benchmark']}
- **Recommended Action:** {a.get('recommended_action', 'Review manually')}
"""

    yellow_rows = "\n".join(
        f"| {a['advertiser_name']} | {a['primary_risk_factor']} | {a['days_to_renewal']} | {a.get('recommended_action', 'Monitor')} |"
        for a in yellow
    )

    green_rows = "\n".join(
        f"| {a['advertiser_name']} | {a.get('raw_data', {}).get('spend_this_quarter', 'N/A')} | {a.get('raw_data', {}).get('newsletters_used', 'N/A')} | Explore additional newsletters |"
        for a in green[:10]
    )

    content = f"""# Advertiser Health Action Plan — {today}

## Summary
- Total accounts analyzed: {len(accounts)}
- Green: {len(green)} ({len(green)/max(len(accounts),1)*100:.0f}%)
- Yellow: {len(yellow)} ({len(yellow)/max(len(accounts),1)*100:.0f}%)
- Red: {len(red)} ({len(red)/max(len(accounts),1)*100:.0f}%)

## Critical Actions (Red Accounts)
{red_section if red_section else "No Red accounts — all clear."}

## Watch List (Yellow Accounts)

| Advertiser | Risk Factor | Days to Renewal | Action |
|---|---|---|---|
{yellow_rows if yellow_rows else "| — | — | — | — |"}

## Healthy Accounts — Expansion Opportunities

| Advertiser | Current Spend | Newsletters Used | Expansion Suggestion |
|---|---|---|---|
{green_rows if green_rows else "| — | — | — | — |"}
"""

    if dry_run:
        print(f"  🧪 DRY RUN: would write action plan to {report_path}")
        return report_path

    report_path.write_text(content, encoding="utf-8")
    print(f"  ✅ Action plan saved to {report_path}")
    return report_path


def main():
    parser = argparse.ArgumentParser(description="Advertiser Health & Renewal Risk Agent")
    parser.add_argument("--advertiser", type=str, help="Analyze a single advertiser")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    print("=" * 60)
    print(f"🏥 Advertiser Health Audit — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    advertisers = load_advertiser_data()
    if not advertisers:
        print(f"  ℹ No advertiser data found in {DATA_DIR}")
        print(f"  Add advertiser_health_YYYY-MM.csv files or connect the MCP.")
        return

    if args.advertiser:
        advertisers = [a for a in advertisers if args.advertiser.lower() in a.get("advertiser_name", "").lower()]
        if not advertisers:
            print(f"  ❌ No advertiser matching '{args.advertiser}' found")
            return

    print(f"  Analyzing {len(advertisers)} accounts...\n")

    scored = [score_advertiser(a) for a in advertisers]
    scored = generate_interventions(scored, api_key)

    write_health_csv(scored, dry_run=args.dry_run)
    write_action_plan(scored, dry_run=args.dry_run)

    red = sum(1 for a in scored if a["risk_level"] == "Red")
    yellow = sum(1 for a in scored if a["risk_level"] == "Yellow")
    print(f"\n{'=' * 60}")
    print(f"✅ Audit complete: {len(scored)} accounts")
    print(f"   🔴 Red: {red}  🟡 Yellow: {yellow}  🟢 Green: {len(scored) - red - yellow}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
