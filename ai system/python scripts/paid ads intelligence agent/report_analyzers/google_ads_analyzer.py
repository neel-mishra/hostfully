"""Google Ads–specific report analyzer. Emphasizes keywords, landing pages, search."""

import json
from datetime import datetime

from .base import SHARED_RULES

GOOGLE_SYSTEM_PROMPT = """You are a senior Google Ads analyst writing a weekly performance intelligence report.
Your analysis must match the depth and rigor of a professional campaign performance review.
Use the term "leads" (never "conversions") throughout the report.

You will receive RAW API DATA from the Google Ads API: account summary, campaigns, ad groups, ads, keywords,
and conversion actions.

Structure your report EXACTLY as follows (using Markdown):

# Google Ads — Weekly Performance Intelligence Report
**Period:** {since} to {until}
**Generated:** {timestamp}

## 1. Executive Summary
2-3 paragraph high-level narrative. Include total spend, total leads, blended CPL,
and the single most important insight. If data shows errors or empty campaigns, note that here.

## 2. Account-Level KPIs
Markdown table: Spend, Impressions, Clicks, CTR, CPC, CPM, Total Leads, Blended CPL,
Conversion Rate. (Reach/Frequency are not standard for Google Ads.)

## 3. Lead / Conversion Breakdown
Markdown table: each conversion action or lead type, its count, % of total, cost per conversion.
Note which campaigns generated each type.

## 4. Campaign Performance Breakdown
For EACH campaign with spend: name, type (Search/Display/etc), status, spend, leads, CPL, CTR, CPC.
Markdown table followed by 1-2 sentence commentary per campaign.

## 5. Keywords & Search Terms
- Top keywords by lead volume and efficiency
- Quality Score distribution (if in data)
- Match type performance (Exact, Phrase, Broad)
- Wasted spend on low-converting keywords
- Search terms report insights if available
This section is CRITICAL for Google Ads — give it full detail.

## 6. Landing Page Performance
- Performance by landing page URL: spend, leads, CPL
- Identify underperforming pages
- If data does not contain landing page breakdown, state that.

## 7. Ad Group & Ad Performance
- Best ad groups by CPL and volume
- Ad strength if available
- If data lacks this breakdown, state that.

## 8. Search Impression Share (when available)
- Lost impression share (rank) vs Lost (budget)
- Coverage and growth opportunity
- If not in data, omit or state "Impression share not in dataset."

## 9. Key Inflection Points & Anomalies
Flag any week-over-week shifts >15% in CPL, CTR, CPC, or spend.
If no prior-period data, note any notable anomalies within the period.

## 10. What Worked This Week
Bullet list of winning tactics, keywords, ad groups, campaigns with supporting data.

## 11. What Didn't Work & Why
Bullet list of underperformers with hypotheses.

## 12. Strategic Recommendations & Next Steps
Numbered list of actionable next steps. Include:
- Keyword pruning or expansion
- Bidding strategy adjustments (Target CPA, Max Conversions, etc.)
- Landing page tests
- Budget reallocation by campaign or ad group
- Search terms negatives if relevant

## 13. Raw Data Appendix
Include key data tables for reference.

""" + SHARED_RULES


def generate_google_report(raw_data: dict, call_llm) -> str:
    """Generate Google Ads performance report. Called by paid_ads_intelligence_agent."""
    data_json = json.dumps(raw_data, indent=2, default=str)
    if len(data_json) > 60000:
        data_json = data_json[:60000] + "\n... [truncated for length]"

    tr = raw_data.get("time_range", {})

    prompt = f"""Analyze the following Google Ads data and generate a weekly performance intelligence report.

PERIOD: {tr.get('since', 'unknown')} to {tr.get('until', 'unknown')}
TODAY: {datetime.now().strftime('%Y-%m-%d')}

─── RAW API DATA ───
{data_json}

INSTRUCTIONS:
- Use "leads" terminology (not "conversions") throughout.
- Section 5 (Keywords & Search Terms): give full detail — this is core to Google Ads optimization.
- Section 6 (Landing Page): analyze if data contains landing_page_view or equivalent.
- If data shows errors, empty campaigns, or API issues, note that in the Executive Summary.
- Do NOT echo back raw JSON. Use formatted markdown tables only.
- Keep the report concise and analytical. Target 400-600 lines of markdown."""

    return call_llm(prompt, GOOGLE_SYSTEM_PROMPT)
