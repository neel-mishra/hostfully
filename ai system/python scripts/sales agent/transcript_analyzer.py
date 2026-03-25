#!/usr/bin/env python3
"""
Sales Call Transcript Analyzer

Processes advertiser sales call transcripts and extracts structured intelligence:
objections, competitor mentions, budget signals, deal stage, and key quotes.
Supports markdown, plain text, and JSON (Gong/Fireflies) formats.

Usage:
  python transcript_analyzer.py                            # batch analyze all transcripts
  python transcript_analyzer.py --file path/to/call.md     # analyze single transcript
  python transcript_analyzer.py --dry-run                  # preview without writing
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
sys.path.insert(0, str(WORKSPACE_ROOT))

COMMANDS_DIR = WORKSPACE_ROOT / "commands"
TRANSCRIPTS_DIR = WORKSPACE_ROOT / "docs" / "sales call transcripts"
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "sales_assets" / "call_analysis"
CALLS_DIR = OUTPUT_DIR / "calls"

EXTRACTION_CSV_COLUMNS = [
    "call_date",
    "advertiser",
    "contact",
    "contact_role",
    "call_type",
    "deal_stage",
    "primary_objection",
    "competitors_mentioned",
    "budget_signal",
    "next_step",
    "risk_level",
    "key_quote",
]


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


# ---------------------------------------------------------------------------
# Claude API
# ---------------------------------------------------------------------------

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
                wait = min(60, 2 ** (attempt + 2))
                print(f"  ⚠ Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            print(f"  ⚠ Claude API error {resp.status_code}: {resp.text[:200]}")
            time.sleep(5)
        except Exception as e:
            print(f"  ⚠ Claude API exception: {e}")
            time.sleep(10)
    raise Exception("Max retries reached for Claude API")


# ---------------------------------------------------------------------------
# Context Loading
# ---------------------------------------------------------------------------

def load_context() -> dict[str, str]:
    context = {}
    files = {
        "competitors": "core/competitor_landscape.md",
        "icp": "core/ideal_customer_profile.md",
        "messaging": "identity/messaging_pillars.md",
    }
    for key, rel_path in files.items():
        full_path = COMMANDS_DIR / rel_path
        try:
            context[key] = full_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            context[key] = ""
    return context


# ---------------------------------------------------------------------------
# Transcript Loading
# ---------------------------------------------------------------------------

def discover_transcripts(directory: Path) -> list[Path]:
    extensions = {".md", ".txt", ".json"}
    files = []
    if not directory.exists():
        print(f"  ⚠ Transcript directory not found: {directory}")
        return files
    for f in sorted(directory.iterdir()):
        if f.is_file() and f.suffix in extensions and not f.name.startswith("_"):
            files.append(f)
    return files


def load_transcript(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        try:
            data = json.loads(raw)
            if isinstance(data, dict) and "transcript" in data:
                lines = []
                for entry in data["transcript"]:
                    speaker = entry.get("speaker", "Unknown")
                    text = entry.get("text", "")
                    ts = entry.get("timestamp", "")
                    prefix = f"[{ts}] " if ts else ""
                    lines.append(f"{prefix}{speaker}: {text}")
                return "\n".join(lines)
        except json.JSONDecodeError:
            pass
    return raw


# ---------------------------------------------------------------------------
# Single Call Analysis
# ---------------------------------------------------------------------------

def analyze_call(transcript_text: str, filename: str, api_key: str, context: dict) -> dict:
    """Analyze a single call transcript and return structured extraction."""
    prompt = f"""You are a sales intelligence analyst for TLDR, the largest daily tech newsletter (7M+ subscribers). Analyze this advertiser sales call transcript and extract structured intelligence.

TRANSCRIPT (filename: {filename}):
---
{transcript_text[:15000]}
---

COMPETITOR CONTEXT (for generating rebuttals):
{context.get('competitors', '')[:3000]}

EXTRACT the following and return STRICTLY as JSON (no other text):

```json
{{
  "metadata": {{
    "advertiser": "Company name of the prospect/advertiser",
    "contact_name": "Name of the prospect contact",
    "contact_role": "Their job title/role",
    "call_date": "YYYY-MM-DD if mentioned or inferable from filename, else unknown",
    "call_type": "discovery / pitch / renewal / qbr / check-in / objection-handling",
    "estimated_duration": "Duration if mentioned, else unknown"
  }},
  "deal_stage": "early_discovery / qualified_interest / evaluation / negotiation / verbal_commit / at_risk",
  "objections": [
    {{
      "quote": "Exact or close paraphrase of the objection",
      "category": "price_budget / attribution / audience_fit / format_creative / timing / competition / internal",
      "severity": "low / medium / high",
      "suggested_rebuttal": "How TLDR should respond, referencing proof points"
    }}
  ],
  "competitor_mentions": [
    {{
      "competitor": "Name of competing channel (LinkedIn Ads, Google Ads, Meta Ads, Paved, Beehiiv, etc.)",
      "context": "positive / negative / currently_using / leaving / comparing",
      "quote": "What was said about them"
    }}
  ],
  "budget_signals": [
    "Each budget-related insight as a string"
  ],
  "feature_requests": [
    "Each product/service request as a string"
  ],
  "key_quotes": [
    "The 3-5 most important quotes from the call"
  ],
  "risk_level": "low / medium / high",
  "recommended_next_steps": [
    "Specific follow-up action 1",
    "Specific follow-up action 2",
    "Specific follow-up action 3"
  ],
  "summary": "2-3 sentence summary of the call"
}}
```

Be thorough. Extract every objection and competitor mention. If something is ambiguous, note that in the quote."""

    raw = claude_generate(prompt, api_key)

    json_start = raw.find("{")
    json_end = raw.rfind("}") + 1
    if json_start == -1:
        print(f"  ⚠ Could not parse analysis for {filename}")
        return {}

    try:
        return json.loads(raw[json_start:json_end])
    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse error for {filename}: {e}")
        return {}


# ---------------------------------------------------------------------------
# Output: Per-Call Analysis
# ---------------------------------------------------------------------------

def write_call_analysis(analysis: dict, filename: str, dry_run: bool = False) -> Path | None:
    if not analysis:
        return None

    CALLS_DIR.mkdir(parents=True, exist_ok=True)

    meta = analysis.get("metadata", {})
    advertiser = meta.get("advertiser", "unknown")
    call_date = meta.get("call_date", "unknown")
    slug = f"{call_date}_{advertiser.lower().replace(' ', '_')}"
    output_path = CALLS_DIR / f"{slug}_analysis.md"

    objection_rows = ""
    for i, obj in enumerate(analysis.get("objections", []), 1):
        objection_rows += f"| {i} | {obj.get('quote', '')} | {obj.get('category', '')} | {obj.get('severity', '')} | {obj.get('suggested_rebuttal', '')} |\n"

    competitor_rows = ""
    for cm in analysis.get("competitor_mentions", []):
        competitor_rows += f"| {cm.get('competitor', '')} | {cm.get('context', '')} | {cm.get('quote', '')} |\n"

    budget_bullets = "\n".join(f"- {b}" for b in analysis.get("budget_signals", []))
    feature_bullets = "\n".join(f"- {f}" for f in analysis.get("feature_requests", []))
    quote_list = "\n".join(f'{i}. "{q}"' for i, q in enumerate(analysis.get("key_quotes", []), 1))
    next_steps = "\n".join(f"{i}. {s}" for i, s in enumerate(analysis.get("recommended_next_steps", []), 1))

    content = f"""# Call Analysis: {advertiser} — {call_date}

## Metadata
- **Advertiser:** {advertiser}
- **Contact:** {meta.get('contact_name', 'Unknown')} ({meta.get('contact_role', 'Unknown')})
- **Call Type:** {meta.get('call_type', 'Unknown')}
- **Deal Stage:** {analysis.get('deal_stage', 'Unknown')}
- **Risk Level:** {analysis.get('risk_level', 'Unknown')}

## Summary
{analysis.get('summary', 'N/A')}

## Objections
| # | Quote | Category | Severity | Suggested Rebuttal |
|---|---|---|---|---|
{objection_rows}
## Competitor Mentions
| Competitor | Context | Quote |
|---|---|---|
{competitor_rows}
## Budget Signals
{budget_bullets if budget_bullets else '- No budget signals detected'}

## Feature Requests / Feedback
{feature_bullets if feature_bullets else '- No feature requests detected'}

## Key Quotes
{quote_list if quote_list else 'No key quotes extracted'}

## Recommended Next Steps
{next_steps if next_steps else 'No next steps generated'}
"""

    if dry_run:
        print(f"  🧪 DRY RUN: would write analysis to {output_path}")
        return output_path

    output_path.write_text(content, encoding="utf-8")
    return output_path


# ---------------------------------------------------------------------------
# Output: Aggregate Report
# ---------------------------------------------------------------------------

def generate_aggregate_report(analyses: list[dict], dry_run: bool = False) -> Path | None:
    if not analyses:
        return None

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = OUTPUT_DIR / f"insights_report_{today}.md"

    all_objections: dict[str, list] = {}
    all_competitors: dict[str, list] = {}
    all_stages: dict[str, list] = {}
    all_features: dict[str, int] = {}
    all_budget_signals = []

    for a in analyses:
        meta = a.get("metadata", {})
        advertiser = meta.get("advertiser", "Unknown")

        for obj in a.get("objections", []):
            cat = obj.get("category", "unknown")
            all_objections.setdefault(cat, []).append({
                "advertiser": advertiser,
                "quote": obj.get("quote", ""),
                "severity": obj.get("severity", ""),
                "rebuttal": obj.get("suggested_rebuttal", ""),
            })

        for cm in a.get("competitor_mentions", []):
            comp = cm.get("competitor", "Unknown")
            all_competitors.setdefault(comp, []).append({
                "advertiser": advertiser,
                "context": cm.get("context", ""),
                "quote": cm.get("quote", ""),
            })

        stage = a.get("deal_stage", "unknown")
        all_stages.setdefault(stage, []).append(advertiser)

        for fr in a.get("feature_requests", []):
            all_features[fr] = all_features.get(fr, 0) + 1

        all_budget_signals.extend(a.get("budget_signals", []))

    objection_table = ""
    sorted_objections = sorted(all_objections.items(), key=lambda x: len(x[1]), reverse=True)
    for rank, (cat, objs) in enumerate(sorted_objections, 1):
        example = objs[0]["quote"] if objs else ""
        rebuttal = objs[0]["rebuttal"] if objs else ""
        objection_table += f"| {rank} | {cat} | {len(objs)} | {example[:80]} | {rebuttal[:80]} |\n"

    competitor_table = ""
    sorted_comps = sorted(all_competitors.items(), key=lambda x: len(x[1]), reverse=True)
    for comp, mentions in sorted_comps:
        contexts = [m["context"] for m in mentions]
        sentiment = max(set(contexts), key=contexts.count) if contexts else "neutral"
        key_insight = mentions[0]["quote"][:80] if mentions else ""
        competitor_table += f"| {comp} | {len(mentions)} | {sentiment} | {key_insight} |\n"

    stage_table = ""
    for stage, names in sorted(all_stages.items()):
        stage_table += f"| {stage} | {len(names)} | {', '.join(names[:5])} |\n"

    feature_table = ""
    for fr, count in sorted(all_features.items(), key=lambda x: x[1], reverse=True)[:10]:
        feature_table += f"| {fr[:60]} | {count} |\n"

    dates = []
    for a in analyses:
        d = a.get("metadata", {}).get("call_date", "")
        if d and d != "unknown":
            dates.append(d)

    content = f"""# Sales Call Insights Report — {today}

## Summary
- **Calls analyzed:** {len(analyses)}
- **Date range:** {min(dates) if dates else 'N/A'} to {max(dates) if dates else 'N/A'}

## Top Objections (by frequency)
| Rank | Category | Count | Example Quote | Recommended Response |
|---|---|---|---|---|
{objection_table}
## Competitor Landscape (from calls)
| Competitor | Mentions | Primary Sentiment | Key Insight |
|---|---|---|---|
{competitor_table}
## Budget Intelligence
{chr(10).join(f'- {b}' for b in all_budget_signals[:10]) if all_budget_signals else '- No budget signals captured'}

## Deal Pipeline Health
| Stage | Count | Advertisers |
|---|---|---|
{stage_table}
## Feature Requests (aggregated)
| Request | Frequency |
|---|---|
{feature_table}
## Actionable Recommendations
1. Address the top objection category ("{sorted_objections[0][0] if sorted_objections else 'N/A'}") by preparing standardized proof points
2. Build competitive responses for {sorted_comps[0][0] if sorted_comps else 'top competitor'} — mentioned {len(sorted_comps[0][1]) if sorted_comps else 0} times
3. Prioritize follow-ups for accounts in "evaluation" and "negotiation" stages
4. Share top feature requests with product team for roadmap consideration
5. Update battlecards with real objection language captured from these calls
"""

    if dry_run:
        print(f"  🧪 DRY RUN: would write report to {report_path}")
        return report_path

    report_path.write_text(content, encoding="utf-8")
    print(f"  ✅ Insights report saved to {report_path}")
    return report_path


# ---------------------------------------------------------------------------
# Output: Extraction CSV
# ---------------------------------------------------------------------------

def write_extraction_csv(analyses: list[dict], dry_run: bool = False) -> Path | None:
    if not analyses:
        return None

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    csv_path = OUTPUT_DIR / f"call_extraction_{today}.csv"

    rows = []
    for a in analyses:
        meta = a.get("metadata", {})
        objections = a.get("objections", [])
        competitors = a.get("competitor_mentions", [])
        budget = a.get("budget_signals", [])
        quotes = a.get("key_quotes", [])
        next_steps = a.get("recommended_next_steps", [])

        rows.append({
            "call_date": meta.get("call_date", ""),
            "advertiser": meta.get("advertiser", ""),
            "contact": meta.get("contact_name", ""),
            "contact_role": meta.get("contact_role", ""),
            "call_type": meta.get("call_type", ""),
            "deal_stage": a.get("deal_stage", ""),
            "primary_objection": objections[0].get("category", "") if objections else "",
            "competitors_mentioned": ", ".join(set(c.get("competitor", "") for c in competitors)),
            "budget_signal": budget[0] if budget else "",
            "next_step": next_steps[0] if next_steps else "",
            "risk_level": a.get("risk_level", ""),
            "key_quote": quotes[0] if quotes else "",
        })

    if dry_run:
        print(f"  🧪 DRY RUN: would write {len(rows)} rows to {csv_path}")
        return csv_path

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EXTRACTION_CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  ✅ Extraction CSV saved to {csv_path}")
    return csv_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_batch(dry_run: bool = False) -> None:
    print("=" * 60)
    print(f"📞 Sales Call Transcript Analyzer — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    context = load_context()
    transcripts = discover_transcripts(TRANSCRIPTS_DIR)

    if not transcripts:
        print(f"  ℹ No transcripts found in {TRANSCRIPTS_DIR}")
        print("  Add .md, .txt, or .json transcripts to this folder and re-run.")
        return

    print(f"  Found {len(transcripts)} transcript(s)\n")

    analyses = []
    for path in transcripts:
        print(f"  📄 Analyzing: {path.name}")
        text = load_transcript(path)
        analysis = analyze_call(text, path.name, api_key, context)

        if analysis:
            analyses.append(analysis)
            write_call_analysis(analysis, path.name, dry_run=dry_run)
            meta = analysis.get("metadata", {})
            print(f"     → {meta.get('advertiser', '?')} | Stage: {analysis.get('deal_stage', '?')} | Risk: {analysis.get('risk_level', '?')}")
        else:
            print(f"     ⚠ No data extracted from {path.name}")

        time.sleep(2)

    generate_aggregate_report(analyses, dry_run=dry_run)
    write_extraction_csv(analyses, dry_run=dry_run)

    print(f"\n{'=' * 60}")
    print(f"✅ Analysis complete: {len(analyses)}/{len(transcripts)} calls processed")
    print(f"   Output: {OUTPUT_DIR}")
    print(f"{'=' * 60}")


def run_single(file_path: str, dry_run: bool = False) -> None:
    path = Path(file_path)
    if not path.exists():
        print(f"❌ File not found: {path}")
        sys.exit(1)

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    context = load_context()
    print(f"\n📄 Analyzing: {path.name}")

    text = load_transcript(path)
    analysis = analyze_call(text, path.name, api_key, context)

    if analysis:
        output = write_call_analysis(analysis, path.name, dry_run=dry_run)
        meta = analysis.get("metadata", {})
        print(f"\n{'=' * 60}")
        print(f"✅ Analysis: {meta.get('advertiser', '?')}")
        print(f"   Deal Stage: {analysis.get('deal_stage', '?')}")
        print(f"   Risk: {analysis.get('risk_level', '?')}")
        print(f"   Objections: {len(analysis.get('objections', []))}")
        print(f"   Competitors: {', '.join(set(c.get('competitor', '') for c in analysis.get('competitor_mentions', [])))}")
        if output:
            print(f"   Output: {output}")
        print(f"{'=' * 60}")
    else:
        print("  ⚠ No data could be extracted")


def main():
    parser = argparse.ArgumentParser(
        description="Sales Call Transcript Analyzer — extract intelligence from advertiser calls",
    )
    parser.add_argument("--file", type=str, help="Analyze a single transcript file")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    args = parser.parse_args()

    if args.file:
        run_single(args.file, dry_run=args.dry_run)
    else:
        run_batch(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
