#!/usr/bin/env python3
"""
Paid Ads Intelligence — MVP

Single script to pull Meta Ads + Google Ads performance and return:
- Portfolio-level summary (per platform): spend, leads/results, impressions, clicks, CTR, CPM, CPC, CPL, conversion rate
- Campaign-level breakdown: same metrics per campaign

Use this to confirm data accuracy before scaling. Output includes source citation for QA.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "automations" / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Load env and import agent modules
from dotenv import load_dotenv
load_dotenv(WORKSPACE_ROOT / ".env")

# Import only what we need from the main agent
from paid_ads_intelligence_agent import (
    pull_full_meta_data,
    build_lead_analysis,
    fetch_gads_account_summary,
    fetch_gads_campaigns,
)


def _gads_metric(row: dict, key_camel: str, key_snake: str = None) -> float:
    """Read a numeric metric from a Google Ads API row (metrics use camelCase)."""
    m = row.get("metrics") or {}
    val = m.get(key_camel) or (m.get(key_snake) if key_snake else None)
    if val is None:
        return 0.0
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0


def _gads_agg(rows: list, key_camel: str, key_snake: str = None) -> float:
    """Sum a metric across multiple GAQL rows (e.g. one per day)."""
    total = 0.0
    for r in rows:
        if r.get("error"):
            continue
        total += _gads_metric(r, key_camel, key_snake)
    return total


def _first_meta_account_row(raw: dict):
    """First row of account_summary.data. Handles data being list or dict (API variance)."""
    acct = (raw.get("account_summary") or {}) if isinstance(raw, dict) else {}
    if not isinstance(acct, dict) or "data" not in acct:
        return {}
    data = acct.get("data")
    if not data:
        return {}
    if isinstance(data, list):
        return data[0] if data else {}
    if isinstance(data, dict):
        vals = list(data.values())
        return vals[0] if vals else {}
    return {}


def build_meta_summary(raw: dict, analysis: dict, since: str, until: str) -> dict:
    """Build normalized portfolio + campaign summary for Meta Ads."""
    acct_row = _first_meta_account_row(raw)
    campaigns = raw.get("campaigns") or []
    campaign_results = {c["campaign_id"]: c for c in (analysis.get("campaign_results") or [])}

    # Portfolio — spend is always total amount spent (account-level or sum of all campaigns)
    spend = analysis.get("account_level_spend") or analysis.get("total_campaign_spend") or 0
    leads = analysis.get("total_leads") or 0
    impressions = int(float(acct_row.get("impressions") or 0))
    reach = int(float(acct_row.get("reach") or 0))
    clicks = int(float(acct_row.get("clicks") or 0))
    ctr = float(acct_row.get("ctr") or 0)
    cpc = float(acct_row.get("cpc") or 0)
    cpm = float(acct_row.get("cpm") or 0)
    cpl = round(spend / leads, 2) if leads else None
    conv_rate = round(100.0 * leads / clicks, 2) if clicks else None

    portfolio = {
        "spend": round(spend, 2),
        "leads": leads,
        "impressions": impressions,
        "reach": reach,
        "clicks": clicks,
        "ctr": round(ctr, 4),
        "cpc": round(cpc, 4),
        "cpm": round(cpm, 2),
        "cpl": cpl,
        "conversion_rate_pct": conv_rate,
    }

    # Campaigns — only include in-scope (had delivery in period); use objective-aligned results and primary objective
    campaign_list = []
    for camp in campaigns:
        cid = camp.get("id", "")
        res = campaign_results.get(cid)
        if not res:
            continue
        ci = camp.get("_campaign_insights") or {}
        if not isinstance(ci, dict):
            ci = {}
        spend_c = res.get("spend", 0)
        leads_c = res.get("leads", 0)
        imp_c = int(float(ci.get("impressions") or 0))
        clk_c = int(float(ci.get("clicks") or 0))
        ctr_c = float(ci.get("ctr") or 0)
        cpc_c = float(ci.get("cpc") or 0)
        cpm_c = float(ci.get("cpm") or 0)
        cpl_c = round(spend_c / leads_c, 2) if leads_c else None
        cvr_c = round(100.0 * leads_c / clk_c, 2) if clk_c else None
        campaign_list.append({
            "campaign_id": cid,
            "campaign_name": camp.get("name") or "Unknown",
            "spend": round(spend_c, 2),
            "leads": leads_c,
            "primary_objective": res.get("primary_objective_label", ""),
            "impressions": imp_c,
            "clicks": clk_c,
            "ctr": round(ctr_c, 4),
            "cpc": round(cpc_c, 4),
            "cpm": round(cpm_c, 2),
            "cpl": cpl_c,
            "conversion_rate_pct": cvr_c,
        })

    # Breakdown of total leads by allowed conversion actions (for QA)
    allowed_breakdown = analysis.get("allowed_lead_breakdown") or []
    campaign_leads_breakdown = analysis.get("campaign_leads_breakdown") or []

    return {
        "platform": "Meta Ads",
        "period": {"since": since, "until": until},
        "source": f"Meta Marketing API (Graph API), {since} to {until}",
        "portfolio": portfolio,
        "total_leads_breakdown": allowed_breakdown,
        "campaign_leads_breakdown": campaign_leads_breakdown,
        "campaigns": campaign_list,
    }


def build_google_summary(account_rows: list, campaign_rows: list, since: str, until: str) -> dict:
    """Build normalized portfolio + campaign summary for Google Ads."""
    # Portfolio: sum across all account rows (one per day)
    spend = _gads_agg(account_rows, "costMicros", "cost_micros") / 1_000_000
    impressions = int(_gads_agg(account_rows, "impressions"))
    clicks = int(_gads_agg(account_rows, "clicks"))
    conversions = _gads_agg(account_rows, "conversions")
    ctr = _gads_agg(account_rows, "ctr") / max(len(account_rows), 1)  # average
    cpc = _gads_agg(account_rows, "averageCpc", "average_cpc") / 1_000_000
    cpm = _gads_agg(account_rows, "averageCpm", "average_cpm") / 1_000_000
    cpl = round(spend / conversions, 2) if conversions else None
    conv_rate = round(100.0 * conversions / clicks, 2) if clicks else None

    # Skip error rows
    account_rows_ok = [r for r in account_rows if not r.get("error")]
    if account_rows_ok:
        ctr = _gads_agg(account_rows_ok, "ctr") / len(account_rows_ok)

    portfolio = {
        "spend": round(spend, 2),
        "leads": round(conversions, 2),
        "impressions": impressions,
        "clicks": clicks,
        "ctr": round(ctr, 4),
        "cpc": round(cpc, 4),
        "cpm": round(cpm, 2),
        "cpl": cpl,
        "conversion_rate_pct": conv_rate,
    }

    # Campaigns: group by campaign id and sum metrics
    by_campaign = {}
    for row in campaign_rows:
        if row.get("error"):
            continue
        camp = row.get("campaign") or {}
        cid = camp.get("id")
        if not cid:
            continue
        cid = str(cid)
        if cid not in by_campaign:
            by_campaign[cid] = {"id": cid, "name": camp.get("name") or "Unknown", "rows": []}
        by_campaign[cid]["rows"].append(row)

    campaign_list = []
    for cid, data in by_campaign.items():
        rows = data["rows"]
        spend_c = _gads_agg(rows, "costMicros", "cost_micros") / 1_000_000
        imp_c = int(_gads_agg(rows, "impressions"))
        clk_c = int(_gads_agg(rows, "clicks"))
        conv_c = _gads_agg(rows, "conversions")
        ctr_c = _gads_agg(rows, "ctr") / max(len(rows), 1)
        cpc_c = _gads_agg(rows, "averageCpc", "average_cpc") / 1_000_000
        cpm_c = _gads_agg(rows, "averageCpm", "average_cpm") / 1_000_000
        cpl_c = round(spend_c / conv_c, 2) if conv_c else None
        cvr_c = round(100.0 * conv_c / clk_c, 2) if clk_c else None
        campaign_list.append({
            "campaign_id": cid,
            "campaign_name": data["name"],
            "spend": round(spend_c, 2),
            "leads": round(conv_c, 2),
            "impressions": imp_c,
            "clicks": clk_c,
            "ctr": round(ctr_c, 4),
            "cpc": round(cpc_c, 4),
            "cpm": round(cpm_c, 2),
            "cpl": cpl_c,
            "conversion_rate_pct": cvr_c,
        })

    campaign_list.sort(key=lambda x: -x["spend"])

    return {
        "platform": "Google Ads",
        "period": {"since": since, "until": until},
        "source": f"Google Ads API (GAQL), {since} to {until}",
        "portfolio": portfolio,
        "campaigns": campaign_list,
    }


def run_mvp(since: str, until: str, output_dir: Path = None) -> dict:
    """Pull Meta + Google and return normalized portfolio + campaign summary."""
    output_dir = output_dir or (WORKSPACE_ROOT / "docs" / "paid ads intelligence" / "mvp")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "period": {"since": since, "until": until},
        "generated_at": datetime.now().isoformat(),
        "meta_ads": None,
        "google_ads": None,
        "errors": [],
    }

    # Meta Ads
    if os.environ.get("META_ACCESS_TOKEN") and os.environ.get("META_AD_ACCOUNT_ID"):
        print("\n📥 Meta Ads...")
        try:
            raw_meta = pull_full_meta_data(since, until)
            analysis = build_lead_analysis(raw_meta, raw_meta.get("optimization_map"))
            result["meta_ads"] = build_meta_summary(raw_meta, analysis, since, until)
            print(f"   Portfolio: ${result['meta_ads']['portfolio']['spend']:,.2f} spend, {result['meta_ads']['portfolio']['leads']} leads")
        except Exception as e:
            result["errors"].append(f"Meta Ads: {e}")
            print(f"   ❌ {e}")
    else:
        result["errors"].append("Meta Ads: credentials not set (META_ACCESS_TOKEN, META_AD_ACCOUNT_ID)")
        print("\n⚠️ Meta Ads: skip (no credentials)")

    # Google Ads
    if os.environ.get("GOOGLE_ADS_REFRESH_TOKEN") and os.environ.get("GOOGLE_ADS_CUSTOMER_ID"):
        print("\n📥 Google Ads...")
        try:
            account_rows = fetch_gads_account_summary(since, until)
            campaign_rows = fetch_gads_campaigns(since, until)
            if account_rows and account_rows[0].get("error"):
                result["errors"].append(f"Google Ads: {account_rows[0].get('error')}")
                print(f"   ❌ {account_rows[0].get('error')}")
            else:
                result["google_ads"] = build_google_summary(account_rows or [], campaign_rows or [], since, until)
                print(f"   Portfolio: ${result['google_ads']['portfolio']['spend']:,.2f} spend, {result['google_ads']['portfolio']['leads']} leads")
        except Exception as e:
            result["errors"].append(f"Google Ads: {e}")
            print(f"   ❌ {e}")
    else:
        result["errors"].append("Google Ads: credentials not set")
        print("\n⚠️ Google Ads: skip (no credentials)")

    # Write JSON
    out_path = output_dir / "paid_ads_mvp_output.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n💾 JSON: {out_path}")

    return result


def print_summary(data: dict) -> None:
    """Print human-readable portfolio + campaign summary."""
    since = data["period"]["since"]
    until = data["period"]["until"]
    print("\n" + "=" * 70)
    print(f"  PAID ADS INTELLIGENCE — MVP SUMMARY")
    print(f"  Period: {since} to {until}")
    print("=" * 70)

    for platform_key, label in [("meta_ads", "Meta Ads"), ("google_ads", "Google Ads")]:
        plat = data.get(platform_key)
        if not plat:
            continue
        print(f"\n### {label}")
        print(f"Source: {plat.get('source', 'N/A')}")
        p = plat.get("portfolio") or {}
        print(f"\n  Portfolio:")
        print(f"    Spend:        ${p.get('spend', 0):,.2f}")
        print(f"    Leads/Results: {p.get('leads', 0)}")
        print(f"    Impressions:  {p.get('impressions', 0):,}")
        print(f"    Clicks:       {p.get('clicks', 0):,}")
        print(f"    CTR:          {p.get('ctr', 0):.2%}" if isinstance(p.get('ctr'), (int, float)) else f"    CTR:          {p.get('ctr')}")
        print(f"    CPC:          ${p.get('cpc', 0):.4f}" if isinstance(p.get('cpc'), (int, float)) else f"    CPC:          {p.get('cpc')}")
        print(f"    CPM:          ${p.get('cpm', 0):.2f}" if isinstance(p.get('cpm'), (int, float)) else f"    CPM:          {p.get('cpm')}")
        print(f"    CPL:          ${p.get('cpl')}" if p.get('cpl') is not None else "    CPL:          N/A")
        print(f"    Conv. rate:   {p.get('conversion_rate_pct')}%" if p.get('conversion_rate_pct') is not None else "    Conv. rate:   N/A")

        if platform_key == "meta_ads":
            breakdown = plat.get("total_leads_breakdown") or []
            if breakdown:
                print(f"\n  Total leads breakdown (leads, qualified_meeting_booked, Website Complete Registration):")
                for item in breakdown:
                    print(f"    {item.get('label', item.get('action_type', '?'))}: {item.get('count', 0)}")
                total_from_breakdown = sum(item.get("count", 0) for item in breakdown)
                print(f"    — Total: {total_from_breakdown}")
            camp_breakdown = plat.get("campaign_leads_breakdown") or []
            if camp_breakdown:
                print(f"\n  Results by campaign (Lead | qualified_meeting_booked | Complete Reg | Total):")
                print(f"    {'Campaign':<48} {'Lead':>6} {'QMB':>6} {'Reg':>6} {'Total':>6}  Spend")
                print("    " + "-" * 90)
                for row in camp_breakdown:
                    if row.get("total", 0) == 0 and row.get("spend", 0) == 0:
                        continue
                    name = (row.get("campaign_name") or "")[:47]
                    print(f"    {name:<48} {row.get('lead', 0):>6} {row.get('qualified_meeting_booked', 0):>6} {row.get('complete_registration', 0):>6} {row.get('total', 0):>6}  ${row.get('spend', 0):,.2f}")
                shown = sum(1 for r in camp_breakdown if r.get("total", 0) > 0 or r.get("spend", 0) > 0)
                if shown < len(camp_breakdown):
                    print(f"    ... and {len(camp_breakdown) - shown} more campaigns with 0 results")

        campaigns = plat.get("campaigns") or []
        if not campaigns:
            continue
        print(f"\n  Campaigns (Results | Primary objective | Spend):")
        print(f"    {'Campaign':<42} {'Results':>8} {'Primary objective':<28} {'Spend':>12}")
        print("    " + "-" * 92)
        for c in campaigns[:20]:
            name = (c.get("campaign_name") or "")[:41]
            obj = (c.get("primary_objective") or "—")[:27]
            print(f"    {name:<42} {c.get('leads', 0):>8} {obj:<28} ${c.get('spend', 0):>11,.2f}")
        if len(campaigns) > 15:
            print(f"    ... and {len(campaigns) - 15} more")

    if data.get("errors"):
        print("\n⚠️ Errors:", data["errors"])
    print("\n" + "=" * 70)


if __name__ == "__main__":
    from datetime import datetime, timedelta
    since = "2026-01-01"
    until = "2026-01-31"
    if len(sys.argv) >= 3:
        since, until = sys.argv[1], sys.argv[2]
    elif len(sys.argv) == 1:
        # Default: last 30 days
        end = datetime.now()
        start = end - timedelta(days=30)
        since = start.strftime("%Y-%m-%d")
        until = end.strftime("%Y-%m-%d")
        print(f"Using last 30 days: {since} to {until}")

    result = run_mvp(since, until)
    print_summary(result)
