#!/usr/bin/env python3
"""
Meta Marketing API wrapper for Cursor Automations.

Usage:
  python meta_ads_api.py account-summary --date-preset last_30d
  python meta_ads_api.py campaigns --date-preset last_7d
  python meta_ads_api.py campaign-performance --id 12345 --date-preset last_7d
  python meta_ads_api.py ad-sets --campaign-id 12345 --date-preset last_7d
  python meta_ads_api.py ads --ad-set-id 12345 --date-preset last_7d
  python meta_ads_api.py results-summary --date-preset last_7d
  python meta_ads_api.py results-summary --date-preset last_7d --include-post-engagement
  python meta_ads_api.py results-summary --date-preset last_7d
  python meta_ads_api.py results-summary --since 2026-03-07 --until 2026-03-13
  python meta_ads_api.py results-summary --date-preset last_7d [--all-campaigns] [--include-post-engagement]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN", "").strip()
AD_ACCOUNT_ID = os.environ.get("META_AD_ACCOUNT_ID", "").strip()
BASE_URL = "https://graph.facebook.com/v23.0"

INSIGHT_FIELDS = "impressions,reach,clicks,ctr,cpc,spend,actions,cost_per_action_type"
CAMPAIGN_FIELDS = "id,name,status,objective,daily_budget,lifetime_budget,bid_strategy"


def meta_get(endpoint, params=None):
    if not ACCESS_TOKEN:
        print(json.dumps({"error": "META_ACCESS_TOKEN not set"}))
        sys.exit(1)

    url = f"{BASE_URL}/{endpoint}"
    params = params or {}
    params["access_token"] = ACCESS_TOKEN

    resp = requests.get(url, params=params, timeout=60)
    if resp.status_code != 200:
        data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        if "date_preset" in str(params):
            return meta_get_with_time_range(endpoint, params)
        print(json.dumps({"error": f"HTTP {resp.status_code}", "body": data}))
        sys.exit(1)

    return resp.json()


def meta_get_with_time_range(endpoint, params):
    """Retry with explicit time_range if date_preset fails."""
    new_params = {k: v for k, v in params.items() if k != "date_preset"}
    now = datetime.now()
    past = now - timedelta(days=30)
    new_params["time_range"] = json.dumps({
        "since": past.strftime("%Y-%m-%d"),
        "until": now.strftime("%Y-%m-%d"),
    })
    resp = requests.get(f"{BASE_URL}/{endpoint}", params=new_params, timeout=60)
    if resp.status_code != 200:
        print(json.dumps({"error": f"HTTP {resp.status_code} (retry)", "body": resp.text[:500]}))
        sys.exit(1)
    return resp.json()


def cmd_account_summary(date_preset):
    data = meta_get(f"act_{AD_ACCOUNT_ID}/insights", {
        "fields": INSIGHT_FIELDS,
        "date_preset": date_preset,
    })
    print(json.dumps(data, indent=2))


def cmd_campaigns(date_preset):
    data = meta_get(f"act_{AD_ACCOUNT_ID}/campaigns", {
        "fields": f"{CAMPAIGN_FIELDS},insights{{spend,impressions,clicks,ctr,cpc,actions}}",
        "effective_status": '["ACTIVE","PAUSED"]',
        "date_preset": date_preset,
        "limit": 50,
    })
    print(json.dumps(data, indent=2))


def cmd_campaign_performance(campaign_id, date_preset):
    data = meta_get(f"{campaign_id}/insights", {
        "fields": INSIGHT_FIELDS,
        "date_preset": date_preset,
    })
    print(json.dumps(data, indent=2))


def cmd_ad_sets(campaign_id, date_preset):
    data = meta_get(f"{campaign_id}/adsets", {
        "fields": "id,name,status,targeting,daily_budget,bid_amount,insights{spend,impressions,clicks,ctr,cpc}",
        "date_preset": date_preset,
        "limit": 50,
    })
    print(json.dumps(data, indent=2))


def cmd_ads(ad_set_id, date_preset):
    data = meta_get(f"{ad_set_id}/ads", {
        "fields": "id,name,status,creative{title,body,image_url,thumbnail_url},insights{spend,impressions,clicks,ctr,cpc}",
        "date_preset": date_preset,
        "limit": 50,
    })
    print(json.dumps(data, indent=2))


# Action types we treat as "results" (exclude clicks, views, etc.)
RESULT_ACTION_TYPES = {
    "lead",
    "complete_registration",
    "omni_complete_registration",
    "post_engagement",
    "post_reaction",
    "post_interaction_gross",
    "offsite_complete_registration_add_meta_leads",
    "offsite_conversion.fb_pixel_lead",
    "offsite_conversion.fb_pixel_complete_registration",
    "offsite_conversion.fb_pixel_custom",
    "onsite_conversion.lead_grouped",
    "onsite_conversion.post_net_like",
    "onsite_conversion.post_net_save",
    "onsite_conversion.post_save",
    "onsite_conversion.post_unlike",
    "onsite_web_lead",
    "onsite_conversion.messaging_conversation_started_7d",
    "onsite_conversion.messaging_first_reply",
    "onsite_conversion.total_messaging_connection",
    "onsite_conversion.messaging_block",
}
# Additional: any action_type containing these is included as a result
RESULT_ACTION_SUBSTRINGS = ("conversion", "lead", "registration", "engagement", "qualified", "meeting")

# Map API action_type to Meta Ads Manager UI-style result label
ACTION_TYPE_TO_LABEL = {
    "lead": "lead_email-valid",
    "offsite_conversion.fb_pixel_lead": "lead_email-valid",
    "onsite_conversion.lead_grouped": "lead_email-valid",
    "onsite_web_lead": "lead_email-valid",
    "offsite_complete_registration_add_meta_leads": "lead_email-valid",
    "complete_registration": "complete_registration",
    "omni_complete_registration": "complete_registration",
    "offsite_conversion.fb_pixel_complete_registration": "complete_registration",
    "post_engagement": "Post engagements",
    "post_reaction": "Post engagements",
    "post_interaction_gross": "Post engagements",
    "onsite_conversion.post_net_like": "Post engagements",
    "onsite_conversion.post_net_save": "Post engagements",
    "onsite_conversion.post_save": "Post engagements",
    "onsite_conversion.post_unlike": "Post engagements",
    "offsite_conversion.fb_pixel_custom": "custom_conversion",
}

# Labels we exclude by default (everything else = "lead generation" per user)
POST_ENGAGEMENT_LABELS = {"Post engagements", "page engagement"}


def _is_result_action(action_type):
    if action_type in RESULT_ACTION_TYPES:
        return True
    return any(s in action_type.lower() for s in RESULT_ACTION_SUBSTRINGS)


def _label_for_action_type(action_type):
    if action_type in ACTION_TYPE_TO_LABEL:
        return ACTION_TYPE_TO_LABEL[action_type]
    at_lower = action_type.lower()
    if "qualified" in at_lower and "meeting" in at_lower:
        return "qualified_meeting_booked"
    if "qualified" in at_lower or "meeting" in at_lower:
        return "qualified_meeting_booked"
    return action_type.replace("_", " ").replace(".", " ").strip()


def _date_range_for_preset(preset):
    """Return (since, until) for date_preset so we always use explicit time_range in API calls."""
    today = datetime.now().date()
    if preset == "last_7d":
        until = today - timedelta(days=1)  # yesterday = end of last full period
        since = until - timedelta(days=6)
    elif preset == "last_14d":
        until = today - timedelta(days=1)
        since = until - timedelta(days=13)
    elif preset == "last_30d":
        until = today - timedelta(days=1)
        since = until - timedelta(days=29)
    else:
        return None, None
    return since.strftime("%Y-%m-%d"), until.strftime("%Y-%m-%d")


def cmd_results_summary(
    date_preset,
    lead_campaigns_only=False,
    had_delivery_only=True,
    include_post_engagement=False,
    since=None,
    until=None,
):
    """Match Meta Ads Manager: campaigns with delivery in date range, one result per campaign (primary conversion), then sum.
    Uses explicit time_range so insights are for that period only. Default: had_delivery_only=True.
    Primary result = the conversion action with the highest value for that campaign (what the UI shows in Results column)."""
    # Always use explicit since/until so API returns insights for that period only
    if since and until:
        pass
    else:
        since, until = _date_range_for_preset(date_preset)
        if not since:
            since, until = None, None
    params = {
        "fields": f"id,name,objective,insights{{actions,spend}}",
        "effective_status": '["ACTIVE","PAUSED"]',
        "limit": 200,
    }
    if since and until:
        params["time_range"] = json.dumps({"since": since, "until": until})
    else:
        params["date_preset"] = date_preset
    data = meta_get(f"act_{AD_ACCOUNT_ID}/campaigns", params)
    campaigns = data.get("data") or []
    if lead_campaigns_only:
        campaigns = [c for c in campaigns if c.get("objective") == "OUTCOME_LEADS"]
    if had_delivery_only:
        def has_delivery(c):
            insights = (c.get("insights") or {}).get("data") or []
            for row in insights:
                try:
                    if float(row.get("spend") or 0) > 0:
                        return True
                except (TypeError, ValueError):
                    pass
            return False
        campaigns = [c for c in campaigns if has_delivery(c)]
    # When a campaign has multiple conversion types, prefer the one that matches UI "Results" (lead/meeting over generic custom)
    PREFERRED_LABELS = {"qualified_meeting_booked", "lead_email-valid", "complete_registration"}

    # One result per campaign: primary conversion
    by_label = {}
    campaign_detail = []
    for camp in campaigns:
        insights = (camp.get("insights") or {}).get("data") or []
        candidates = []  # (label, value)
        for row in insights:
            for action in row.get("actions") or []:
                at = action.get("action_type")
                if not at or not _is_result_action(at):
                    continue
                label = _label_for_action_type(at)
                if not include_post_engagement and label in POST_ENGAGEMENT_LABELS:
                    continue
                try:
                    val = int(action.get("value", 0))
                except (TypeError, ValueError):
                    continue
                if val > 0:
                    candidates.append((label, val))
        if not candidates:
            continue
        preferred = [(l, v) for l, v in candidates if l in PREFERRED_LABELS]
        if preferred:
            primary_label, primary_value = max(preferred, key=lambda x: x[1])
        else:
            primary_label, primary_value = max(candidates, key=lambda x: x[1])
        by_label[primary_label] = by_label.get(primary_label, 0) + primary_value
        campaign_detail.append({
            "campaign_name": camp.get("name", camp.get("id")),
            "result_type": primary_label,
            "result_value": primary_value,
        })
    parts = [f"{v:,} {k}" for k, v in sorted(by_label.items(), key=lambda x: -x[1]) if v]
    one_line = ", ".join(parts) if parts else "0"
    total_all = sum(by_label.values())
    total_lead = sum(v for k, v in by_label.items() if k not in POST_ENGAGEMENT_LABELS)
    if include_post_engagement:
        scope = "campaigns with delivery"
    else:
        scope = "lead results only (excl. post engagement)"
    out = {
        "date_range": f"{since} to {until}" if (since and until) else date_preset,
        "since": since,
        "until": until,
        "campaign_count": len(campaigns),
        "campaigns_with_results": len(campaign_detail),
        "results_by_conversion_action": by_label,
        "total_results": total_lead if not include_post_engagement else total_all,
        "total_results_all_types": total_all,
        "results_summary_line": f"Results ({scope}): {one_line}",
        "one_row_total": total_lead if not include_post_engagement else total_all,
        "campaign_detail": campaign_detail,
    }
    print(json.dumps(out, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Meta Marketing API CLI")
    parser.add_argument("command", choices=[
        "account-summary", "campaigns", "campaign-performance", "ad-sets", "ads", "results-summary"
    ])
    parser.add_argument("--date-preset", default="last_30d")
    parser.add_argument("--lead-campaigns-only", action="store_true", help="For results-summary: only OUTCOME_LEADS campaigns")
    parser.add_argument("--all-campaigns", action="store_true", dest="all_campaigns", help="For results-summary: include campaigns with no delivery (default is had-delivery only)")
    parser.add_argument("--include-post-engagement", action="store_true", help="For results-summary: include Post engagements in the sum (default is lead results only)")
    parser.add_argument("--since", help="For results-summary: start date YYYY-MM-DD (use with --until)")
    parser.add_argument("--until", help="For results-summary: end date YYYY-MM-DD (use with --since)")
    parser.add_argument("--id", help="Campaign ID (for campaign-performance)")
    parser.add_argument("--campaign-id", help="Campaign ID (for ad-sets)")
    parser.add_argument("--ad-set-id", help="Ad Set ID (for ads)")
    args = parser.parse_args()

    if args.command == "account-summary":
        cmd_account_summary(args.date_preset)
    elif args.command == "campaigns":
        cmd_campaigns(args.date_preset)
    elif args.command == "campaign-performance":
        cmd_campaign_performance(args.id, args.date_preset)
    elif args.command == "ad-sets":
        cmd_ad_sets(args.campaign_id, args.date_preset)
    elif args.command == "ads":
        cmd_ads(args.ad_set_id, args.date_preset)
    elif args.command == "results-summary":
        cmd_results_summary(
            args.date_preset,
            lead_campaigns_only=args.lead_campaigns_only,
            had_delivery_only=not getattr(args, "all_campaigns", False),
            include_post_engagement=args.include_post_engagement,
            since=args.since,
            until=args.until,
        )


if __name__ == "__main__":
    main()
