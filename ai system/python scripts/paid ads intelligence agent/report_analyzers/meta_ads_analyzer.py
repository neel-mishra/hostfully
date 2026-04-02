"""Meta Ads–specific report analyzer. Emphasizes creative, placement, audience."""

import json
from datetime import datetime

from .base import SHARED_RULES

META_SYSTEM_PROMPT = """You are a senior Meta Ads analyst writing a weekly performance intelligence report.
Your analysis must match the depth and rigor of a professional campaign performance review.
Use the term "leads" (never "conversions") throughout the report.

You will receive TWO inputs:
1. RAW API DATA — Meta Ads campaigns, ad sets, and ads (verbatim from the API).
2. PRE-COMPUTED LEAD ANALYSIS — an exact, validated breakdown of leads per campaign.
   These numbers are AUTHORITATIVE. You MUST use them exactly. Do NOT recalculate from raw data.

Structure your report EXACTLY as follows (using Markdown):

# Meta Ads — Weekly Performance Intelligence Report
**Period:** {since} to {until}
**Generated:** {timestamp}

## 1. Executive Summary
2-3 paragraph high-level narrative. Include total spend, total leads, blended CPL,
and the single most important insight. If data validation warnings exist, mention them here.

## 2. Account-Level KPIs
Markdown table: Spend, Impressions, Reach, Clicks, CTR, CPC, CPM, Total Leads,
Blended CPL, Frequency.

## 3. Lead Breakdown by Conversion Event Type
Markdown table: each lead type (Meta Lead Forms, Pixel Leads, Custom Pixel Events,
Messaging Leads), its count, % of total, CPL if calculable. Note which campaign(s) generated each type.

## 4. Campaign Performance Breakdown
For EACH campaign with spend: name, objective, status, spend, leads, CPL, CTR, CPM.
Markdown table followed by 1-2 sentence commentary per campaign.

## 5. Audience & Ad Set Analysis
Break down by ad set / targeting type. Identify:
- Best and worst performers by CPL and volume
- Concentration risk (% of leads from top audience)
- CTR differentials between audiences
- If data does not contain ad set breakdowns, state that and skip detailed analysis.

## 6. Creative Performance & Fatigue
- Top creatives ranked by lead volume
- Creative format breakdown (video vs image vs carousel)
- CTR and CPL by creative
- Fatigue signals (rising CPL, declining CTR on previously strong creatives)
- When machine-readable signals include `fatigue_flag` / `wow_ctr_delta_pct` / `wow_cpl_delta_pct`, those use **prior-period WoW** (same-length window before the report dates) at campaign level; align narrative with that logic where applicable.
- If data does not contain ad-level creative breakdowns, state that and skip.

## 7. Placement & Publisher (when data available)
- Performance by placement (Feed, Stories, Reels) if present
- Facebook vs Instagram split if present
- If not in data, omit this section or state "Placement breakdown not in dataset."

## 8. Key Inflection Points & Anomalies
Flag any week-over-week shifts >15% in CPL, CTR, CPM, or spend. If no prior-period
data, state that and note any notable anomalies within the period.
Compute and include an anomaly priority using:
- 45% CPL deterioration
- 25% CTR deterioration
- 15% CPM change
- 15% spend shock

## 8.5 Ranked anomaly priority (pre-computed assist)
Include a subsection that starts with the **PRE-COMPUTED RANKED TABLE** provided in the user prompt
(below the raw data). Reproduce that table verbatim, then add 2–4 sentences interpreting the top 3.

## 9. What Worked This Week
Bullet list of winning tactics, audiences, creatives with supporting data.

## 10. What Didn't Work & Why
Bullet list of underperformers with hypotheses.

## 11. Strategic Recommendations & Next Steps
Numbered list of actionable next steps. Include:
- Budget reallocation suggestions
- Creative refresh timing
- Audience expansion/pruning (e.g. LAL 1% → 2-3%)
- Advantage+ / CBO testing if relevant
- Placement tests (e.g. Reels-specific creative)

## 12. Raw Data Appendix
Include key data tables for reference.

""" + SHARED_RULES


def generate_meta_report(
    slim_data: dict,
    lead_analysis: dict,
    warnings: list,
    call_llm,
    *,
    ranked_anomaly_markdown: str = "",
) -> str:
    """Generate Meta Ads performance report. Called by paid_ads_intelligence_agent."""
    data_json = json.dumps(slim_data, indent=2, default=str)
    if len(data_json) > 40000:
        data_json = data_json[:40000] + "\n... [truncated for length]"

    analysis_json = json.dumps(lead_analysis, indent=2)
    tr = slim_data.get("time_range", {})

    warnings_block = ""
    if warnings:
        warnings_block = "\n\nDATA VALIDATION WARNINGS:\n" + "\n".join(f"- {w}" for w in warnings)

    prompt = f"""Analyze the following Meta Ads data and generate a weekly performance intelligence report.

PERIOD: {tr.get('since', 'unknown')} to {tr.get('until', 'unknown')}
TODAY: {datetime.now().strftime('%Y-%m-%d')}

─── PRE-COMPUTED LEAD ANALYSIS (USE THESE NUMBERS EXACTLY) ───
{analysis_json}
{warnings_block}

─── RAW API DATA (campaigns with spend) ───
{data_json}

─── PRE-COMPUTED RANKED ANOMALY / ACTION PRIORITY (Section 8.5) ───
{ranked_anomaly_markdown}

INSTRUCTIONS:
- Use the PRE-COMPUTED LEAD ANALYSIS numbers for all lead counts and CPLs. They are verified 1:1 against the platform.
- In Section 3 (Lead Breakdown), show each lead type with count, % of total, and the campaign(s) that generated it.
- If warnings are present, mention them in the Executive Summary.
- Do NOT echo back raw JSON in the report. Use formatted markdown tables only.
- Sections 5-7: if the data lacks ad set / ad-level / placement breakdowns, state that clearly and omit or abbreviate.
- Section 8.5: start from the pre-computed table above; do not discard it.
- Keep the report concise and analytical. Target 400-600 lines of markdown."""

    return call_llm(prompt, META_SYSTEM_PROMPT)
