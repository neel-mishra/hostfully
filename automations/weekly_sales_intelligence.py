#!/usr/bin/env python3
"""
Weekly Sales Intelligence Package Generator

Uses Gemini API (fallback for Claude) to identify prospects, score them,
and produce the weekly intelligence package for TLDR's sales team.
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import google.generativeai as genai

WORKSPACE = Path(__file__).resolve().parent.parent
TODAY = datetime.now().strftime("%Y-%m-%d")
WEEK_OF = datetime.now().strftime("%B %d, %Y")
OUTPUT_DIR = WORKSPACE / "docs" / "sales_assets"
PROSPECT_DIR = OUTPUT_DIR / "prospect_lists"
BATTLECARD_DIR = OUTPUT_DIR / "battlecards"


def setup_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set")
        sys.exit(1)
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")


def gemini_generate(model, prompt, retries=3):
    for attempt in range(retries):
        try:
            resp = model.generate_content(prompt)
            return resp.text
        except Exception as e:
            print(f"  Gemini error (attempt {attempt+1}): {e}")
            time.sleep(2 ** (attempt + 1))
    return ""


def load_context():
    ctx = {}
    files = {
        "icp": "commands/core/ideal_customer_profile.md",
        "competitors": "commands/core/competitor_landscape.md",
        "business": "commands/core/business_context.md",
        "messaging": "commands/identity/messaging_pillars.md",
        "competitive_brief": "docs/competitor content tracker/competitive_brief_2026-03.md",
    }
    for key, rel in files.items():
        p = WORKSPACE / rel
        try:
            ctx[key] = p.read_text(encoding="utf-8")
        except FileNotFoundError:
            ctx[key] = ""
    return ctx


def identify_prospects(model, context):
    """Identify 15-20 high-potential advertising prospects."""
    prompt = f"""You are a B2B advertising prospect researcher for TLDR, the largest daily tech newsletter (7M+ subscribers, 12 newsletters, 40-48% open rates).

TASK: Identify 20 B2B tech companies that would be ideal advertising prospects for TLDR newsletters in March 2026. Focus on companies that:
- Are B2B SaaS, developer tools, AI/ML, cybersecurity, or fintech
- Have Series A+ funding (raised $5M+)
- Are likely running paid ads (Google, LinkedIn, Meta)
- Target tech professionals (developers, engineers, PMs, CTOs)
- Have a marketing team capable of running campaigns

TLDR'S ADVERTISER ICP:
{context.get('icp', '')[:3000]}

EXISTING ADVERTISERS TO EXCLUDE: AWS, Google Cloud, Anthropic, Shopify, Plaid, Bland AI, Delve, Kolena, Paragon

Return STRICTLY valid JSON array (no markdown fences, no extra text):
[
  {{
    "company": "Company Name",
    "website": "https://example.com",
    "industry": "B2B SaaS|Developer Tools|AI/ML Platforms|Cybersecurity|Fintech|Cloud Infrastructure|DevOps|Data Infrastructure|HR Tech|Open Source",
    "funding_stage": "Series A/B/C/D",
    "last_funding": "$XXM Series X (Month YYYY)",
    "signal_type": "Recent Funding|Active Ads|Competitor Newsletter Advertiser|New Product Launch",
    "signal_detail": "Why this company is a strong prospect right now",
    "current_ad_platforms": "LinkedIn, Meta, Google, etc.",
    "contact_target": "Head of Growth / VP Marketing / etc.",
    "estimated_ad_spend": "Low/Medium/High",
    "meta_ads_likely": true,
    "tech_audience_fit": "Strong/Medium/Weak"
  }}
]

Be specific. Use real companies with real funding data. Include a mix of well-known growth companies and emerging ones."""

    print("  Identifying prospects via Gemini...")
    raw = gemini_generate(model, prompt)

    json_start = raw.find("[")
    json_end = raw.rfind("]") + 1
    if json_start == -1 or json_end == 0:
        print(f"  Could not parse prospect results. Raw: {raw[:500]}")
        return []

    try:
        prospects = json.loads(raw[json_start:json_end])
        print(f"  Found {len(prospects)} prospects")
        return prospects
    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}")
        print(f"  Raw snippet: {raw[json_start:json_start+500]}")
        return []


def score_prospects(model, prospects, context):
    """Score and rank prospects."""
    summaries = "\n".join(
        f"- {p['company']} ({p.get('industry','?')}): {p.get('signal_detail','N/A')}"
        for p in prospects
    )
    prompt = f"""Score these advertising prospects for TLDR newsletters (7M+ tech subscribers).

SCORING (1-10):
1. Budget Signal (30%): ad spend evidence
2. Audience Overlap (25%): how well their target matches TLDR readers
3. Newsletter Fit (20%): how many TLDR newsletters they could advertise in
4. Timing (15%): urgency signals (funding, launch, growth phase)
5. Deal Size Potential (10%): likely spend ($3K one-off vs $50K+ recurring)

PROSPECTS:
{summaries}

TLDR NEWSLETTER PORTFOLIO:
- TLDR Tech (1.6M subs), TLDR AI (725K), TLDR Dev (375K), TLDR InfoSec (340K), TLDR DevOps (250K)
- Also: TLDR Product, TLDR Marketing, TLDR Founders, TLDR Crypto, TLDR Design, TLDR Data, TLDR Fintech

Return STRICTLY valid JSON array (no markdown fences):
[
  {{
    "company": "Company Name",
    "budget_signal": 7,
    "audience_overlap": 8,
    "newsletter_fit": 9,
    "timing": 8,
    "deal_size": 6,
    "priority_score": 8,
    "outreach_angle": "One sentence personalized pitch angle",
    "best_newsletters": "TLDR AI, TLDR Tech",
    "tier": "hot|medium|watch"
  }}
]

Tier: hot = score 7+, medium = score 5-6, watch = score 4 or below.
priority_score = weighted average rounded to nearest int."""

    print("  Scoring prospects...")
    raw = gemini_generate(model, prompt)

    json_start = raw.find("[")
    json_end = raw.rfind("]") + 1
    if json_start == -1:
        return prospects

    try:
        scores = json.loads(raw[json_start:json_end])
        score_map = {s["company"]: s for s in scores}

        for p in prospects:
            s = score_map.get(p["company"], {})
            p["priority_score"] = s.get("priority_score", 5)
            p["outreach_angle"] = s.get("outreach_angle", "")
            p["best_newsletters"] = s.get("best_newsletters", "TLDR Tech")
            p["tier"] = s.get("tier", "medium")
            p["budget_signal"] = s.get("budget_signal", 5)
            p["audience_overlap"] = s.get("audience_overlap", 5)
            p["newsletter_fit"] = s.get("newsletter_fit", 5)
            p["timing"] = s.get("timing", 5)
            p["deal_size"] = s.get("deal_size", 5)

        return sorted(prospects, key=lambda x: x.get("priority_score", 0), reverse=True)
    except json.JSONDecodeError:
        return prospects


def generate_deep_dives(model, top_prospects, context):
    """Generate deep dives for top 3 prospects."""
    dives = []
    for p in top_prospects[:3]:
        prompt = f"""Write a detailed prospect deep dive for TLDR's sales team about {p['company']}.

PROSPECT DATA:
- Company: {p['company']}
- Website: {p.get('website', 'N/A')}
- Industry: {p.get('industry', 'N/A')}
- Funding: {p.get('last_funding', 'N/A')}
- Signal: {p.get('signal_detail', 'N/A')}
- Priority Score: {p.get('priority_score', 'N/A')}/10
- Best TLDR Newsletters: {p.get('best_newsletters', 'N/A')}

TLDR CONTEXT:
{context.get('business', '')[:2000]}

Write in this format (no markdown fences around the whole thing):

### {p['company']} ({p.get('website', '')})

**Industry:** {p.get('industry', 'N/A')} | **Funding:** {p.get('last_funding', 'N/A')} | **Score:** {p.get('priority_score', 'N/A')}/10

**Company Overview:** [2-3 sentences about what they do, target market, key metrics]

**Why TLDR Fits:**
- [Reason 1 tied to their product/audience]
- [Reason 2 tied to TLDR's reach]
- [Reason 3 tied to timing/opportunity]

**Current Marketing Activity:** [What's known about their ad spend, channels, content strategy]

**Recommended Newsletter Placements:** {p.get('best_newsletters', 'TLDR Tech')}

**Suggested Contact:** {p.get('contact_target', 'VP Marketing / Head of Growth')}

**Outreach Template:**
Subject: [Personalized subject line]
Body: [3-4 sentence email draft]

Keep it actionable and specific."""

        print(f"  Generating deep dive: {p['company']}...")
        dive = gemini_generate(model, prompt)
        dives.append(dive)
        time.sleep(1)
    return dives


def generate_battlecard_summary(model, context):
    """Generate a battlecard summary section."""
    prompt = f"""You are a competitive intelligence strategist for TLDR newsletters.

Based on this competitive landscape and recent intelligence, provide a battlecard update summary.

COMPETITOR LANDSCAPE:
{context.get('competitors', '')[:3000]}

RECENT COMPETITIVE BRIEF:
{context.get('competitive_brief', '')[:3000]}

Write a concise battlecard update summary covering:

## Battlecard Updates — Week of {WEEK_OF}

### Key Changes This Week
[3-4 bullet points on what's changed in the competitive landscape]

### Competitive Talking Points
| Competitor | Key Talking Point | Proof Point |
|---|---|---|
[One row for each of: LinkedIn Ads, Google Ads, Meta Ads, Paved, Beehiiv, Podcast Sponsorships]

### Quick Objection Handlers
| Objection | Response |
|---|---|
[5 most common objections with 1-2 sentence conversational rebuttals]

Keep it concise and actionable for AEs."""

    print("  Generating battlecard summary...")
    return gemini_generate(model, prompt)


def generate_market_signals(model, prospects):
    """Generate market signals section."""
    companies = ", ".join(p["company"] for p in prospects[:15])
    prompt = f"""Based on these B2B tech companies that are potential TLDR advertising prospects, identify market signals.

COMPANIES ANALYZED: {companies}

Write a market signals section:

## Market Signals — Week of {WEEK_OF}

### Companies Increasing Ad Spend
[3-5 companies that appear to be ramping up marketing/advertising, with brief evidence]

### New Market Entrants
[2-3 newer companies (Series A/B) entering the advertising space for the first time]

### Companies That May Have Reduced Spend
[2-3 companies that may be pulling back, with reasoning]

### Emerging Trends
[3-4 brief bullet points on trends in B2B tech advertising relevant to TLDR's sales team]

Be specific and tie signals to actionable sales opportunities."""

    print("  Generating market signals...")
    return gemini_generate(model, prompt)


def compile_package(prospects, deep_dives, battlecard_summary, market_signals):
    """Compile the full sales intelligence package."""
    hot = [p for p in prospects if p.get("tier") == "hot"][:5]
    medium = [p for p in prospects if p.get("tier") == "medium"][:10]

    def prospect_table(items):
        rows = []
        for p in items:
            rows.append(
                f"| {p.get('company','')} | {p.get('website','')} | {p.get('industry','')} | "
                f"{p.get('last_funding','')} | {p.get('meta_ads_likely','N/A')} | "
                f"{p.get('estimated_ad_spend','N/A')} | {p.get('priority_score','')}/10 | "
                f"{p.get('outreach_angle','')} |"
            )
        return "\n".join(rows)

    package = f"""# TLDR Sales Intelligence Package
## Week of {WEEK_OF}

**Generated:** {TODAY}
**Data Sources:** Gemini AI analysis, TLDR business context, competitive intelligence tracker
**Note:** Ahrefs domain data unavailable this week (API key not configured). Meta Ad Library (ScrapeCreators) returned 404. Prospect signals derived from AI-powered funding/ad spend analysis and internal competitive data.

---

## Tier 1: Hot Prospects (Score 7+)

These companies have active ad signals, recent funding, and strong tech audience fit.

| Company | Website | Industry | Funding | Meta Ads | Paid Spend | Fit Score | Outreach Angle |
|---|---|---|---|---|---|---|---|
{prospect_table(hot)}

---

## Tier 2: Medium Prospects (Score 5-6)

Companies with one or two positive signals worth monitoring or pursuing with a longer timeline.

| Company | Website | Industry | Funding | Meta Ads | Paid Spend | Fit Score | Outreach Angle |
|---|---|---|---|---|---|---|---|
{prospect_table(medium)}

---

## Top 3 Prospect Deep Dives

{"---".join(deep_dives)}

---

{battlecard_summary}

---

{market_signals}

---

## Methodology & Limitations

- **Prospect identification:** Gemini AI analysis of B2B tech companies matching TLDR's advertiser ICP (B2B SaaS, developer tools, AI/ML, cybersecurity, fintech; Series A+ funding; active marketing teams)
- **Scoring model:** 5-dimension weighted scoring (Budget Signal 30%, Audience Overlap 25%, Newsletter Fit 20%, Timing 15%, Deal Size Potential 10%)
- **Limitations this week:**
  - Ahrefs API key not configured — no domain rating, organic/paid traffic, or paid page data
  - ScrapeCreators (Meta Ad Library) API returned 404 — no live Meta ad activity verification
  - Anthropic API credits depleted — used Gemini as fallback LLM
- **Recommendations for next week:**
  - Configure AHREFS_API_KEY secret for domain intelligence
  - Verify ScrapeCreators API endpoint/key for Meta ad data
  - Top up Anthropic API credits for Claude-based analysis

---

*Generated by TLDR Sales Intelligence Automation — {TODAY}*
"""
    return package


def save_prospect_csv(prospects):
    """Save prospects to CSV."""
    import csv
    PROSPECT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = PROSPECT_DIR / f"prospect_list_{TODAY}.csv"
    fields = [
        "company", "website", "industry", "funding_stage", "last_funding",
        "signal_type", "signal_detail", "current_ad_platforms", "best_newsletters",
        "priority_score", "outreach_angle", "contact_target", "tier",
        "estimated_ad_spend", "meta_ads_likely", "tech_audience_fit",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(prospects)
    print(f"  Saved prospect CSV: {csv_path}")
    return csv_path


def main():
    print("=" * 60)
    print(f"TLDR Weekly Sales Intelligence — {WEEK_OF}")
    print("=" * 60)

    model = setup_gemini()
    context = load_context()

    # Step 1: Identify prospects
    print("\n[1/5] Identifying prospects...")
    prospects = identify_prospects(model, context)
    if not prospects:
        print("  No prospects identified. Exiting.")
        sys.exit(1)

    # Step 2: Score prospects
    print("\n[2/5] Scoring and ranking prospects...")
    scored = score_prospects(model, prospects, context)

    # Step 3: Deep dives on top 3
    hot = [p for p in scored if p.get("tier") == "hot"]
    print(f"\n[3/5] Generating deep dives for top {min(3, len(hot))} prospects...")
    deep_dives = generate_deep_dives(model, hot if hot else scored[:3], context)

    # Step 4: Battlecard summary
    print("\n[4/5] Generating battlecard updates...")
    battlecard_summary = generate_battlecard_summary(model, context)

    # Step 5: Market signals
    print("\n[5/5] Generating market signals...")
    market_signals = generate_market_signals(model, scored)

    # Compile package
    print("\n  Compiling final package...")
    package = compile_package(scored, deep_dives, battlecard_summary, market_signals)

    # Save outputs
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PROSPECT_DIR.mkdir(parents=True, exist_ok=True)

    report_path = OUTPUT_DIR / f"weekly_intelligence_{TODAY}.md"
    report_path.write_text(package, encoding="utf-8")
    print(f"  Saved report: {report_path}")

    csv_path = save_prospect_csv(scored)

    print(f"\n{'=' * 60}")
    print(f"Sales Intelligence Package complete")
    print(f"  Report: {report_path}")
    print(f"  CSV: {csv_path}")
    print(f"  Total prospects: {len(scored)}")
    print(f"  Hot (7+): {sum(1 for p in scored if p.get('tier') == 'hot')}")
    print(f"  Medium (5-6): {sum(1 for p in scored if p.get('tier') == 'medium')}")
    print(f"{'=' * 60}")

    return str(report_path), str(csv_path), package, scored


if __name__ == "__main__":
    report_path, csv_path, package, scored = main()
