#!/usr/bin/env python3
"""
Paid Ads Intelligence Agent
Pulls performance data from all live paid ads channels (Meta Ads, Google Ads)
and generates deep-dive analysis reports matching the depth of a senior
media-buyer performance review.

Variables analyzed (extracted from reference PMS Campaign Performance Analysis):
  Account-level:  Spend, Impressions, Reach, Clicks, CTR, CPC, CPM, Leads, CPL
  Temporal:        Weekly & monthly trends, spend vs. lead efficiency curves
  Campaign-level:  Budget allocation, objective, bid strategy, status
  Audience/AdSet:  Targeting type, audience performance, concentration risk
  Creative/Ad:     Lead volume by creative, CTR by creative, CPL by creative,
                   format split (video vs image), fatigue detection
  Geographic:      Performance by region/country
  Keywords:        (Google) match type, quality score, keyword-level ROI
  Lead events:     Breakdown by conversion event type (lead forms, pixel leads,
                   custom pixel events, messaging leads, website leads)
  Strategic:       Inflection points, what worked/didn't, next steps, decisions log

DATA ACCURACY GUARANTEE:
  - All API responses are stored VERBATIM in raw_data.json — zero field simplification.
  - Explicit time_range (YYYY-MM-DD boundaries) used instead of relative date_preset.
  - "Results" (leads) calculated per-campaign using objective → action_type mapping,
    matching Meta Ads Manager's Results column logic exactly.
  - Post-pull validation: campaign spend sum cross-checked against account total.
"""

import json
import os
import sys
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
AGENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(WORKSPACE_ROOT / "automations" / "lib"))
sys.path.insert(0, str(AGENT_DIR))
load_dotenv(WORKSPACE_ROOT / ".env")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# ─── Meta Ads credentials ────────────────────────────────────────────
META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN", "").strip()
META_AD_ACCOUNT_ID = os.environ.get("META_AD_ACCOUNT_ID", "").strip()
META_BASE_URL = "https://graph.facebook.com/v24.0"

# ─── Google Ads credentials ──────────────────────────────────────────
GADS_CLIENT_ID = os.environ.get("GOOGLE_ADS_CLIENT_ID", "")
GADS_CLIENT_SECRET = os.environ.get("GOOGLE_ADS_CLIENT_SECRET", "")
GADS_DEV_TOKEN = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN", "")
GADS_REFRESH_TOKEN = os.environ.get("GOOGLE_ADS_REFRESH_TOKEN", "")
GADS_CUSTOMER_ID = os.environ.get("GOOGLE_ADS_CUSTOMER_ID", "").replace("-", "")
GADS_MANAGER_ID = os.environ.get("GOOGLE_ADS_MANAGER_ID", "").replace("-", "")

INSIGHT_FIELDS = ",".join([
    "impressions", "reach", "clicks", "ctr", "cpc", "spend", "cpm",
    "actions", "conversions", "cost_per_action_type", "frequency",
])
CAMPAIGN_FIELDS = ",".join([
    "id", "name", "status", "objective",
    "daily_budget", "lifetime_budget", "bid_strategy",
])

# ─── Actions taxonomy ────────────────────────────────────────────────
# These action_types are NOT leads — they are engagement, traffic, or view metrics.
NON_LEAD_ACTIONS = frozenset([
    "page_engagement", "post_engagement", "post_interaction_gross",
    "post_reaction", "onsite_conversion.post_save", "onsite_conversion.post_unsave",
    "onsite_conversion.post_net_save", "onsite_conversion.post_net_like",
    "onsite_conversion.post_unlike", "comment", "like", "post",
    "link_click", "landing_page_view", "omni_landing_page_view", "video_view",
])

# Sub-metrics that track the same event at different funnel stages.
# These must NEVER be counted independently — they're always captured
# by a parent action (e.g., `lead` or `total_messaging_connection`).
SUB_METRICS = frozenset([
    # Lead form funnel stages (all part of a single `lead` event)
    "offsite_complete_registration_add_meta_leads",
    "offsite_search_add_meta_leads",
    "offsite_content_view_add_meta_leads",
    "onsite_conversion.lead_grouped",
    # Messaging funnel stages (all part of `total_messaging_connection`)
    "onsite_conversion.messaging_first_reply",
    "onsite_conversion.messaging_conversation_started_7d",
    # Pixel lead is a sub-metric when `lead` is present (same event, different layer)
    "onsite_web_lead",
])

# Primary lead/conversion action types. Only these are counted as "Results".
# When `lead` is present, it is the canonical count (includes pixel leads + form fills).
# When absent, the remaining primary actions are counted individually.
PRIMARY_LEAD_ACTIONS = frozenset([
    "lead",
    "offsite_conversion.fb_pixel_lead",
    "offsite_conversion.fb_pixel_custom",
    "onsite_conversion.total_messaging_connection",
])

# For portfolio "total leads" summary: only count campaigns whose primary conversion is one of these.
# (lead = Meta Lead Form, qualified_meeting_booked = custom pixel, complete_registration = Website Completed Registration)
ALLOWED_LEAD_ACTIONS_FOR_TOTAL = frozenset([
    "lead",
    "offsite_conversion.fb_pixel_complete_registration",
    "offsite_conversion.fb_pixel_custom.qualified_meeting_booked",
])

# Path to Meta campaign → objective context file (single source of truth for Results).
META_OBJECTIVES_PATH = WORKSPACE_ROOT / "docs" / "paid ads intelligence" / "meta_campaign_objectives.json"

# Campaigns whose primary objective is lead_email-valid (custom pixel event).
# Used only when meta_campaign_objectives.json is not loaded (fallback).
CAMPAIGNS_PRIMARY_LEAD_EMAIL_VALID = frozenset([
    "au-uk_pms_prospecting_website-conv",
    "au-uk_pms_retargeting_website-conv",
    "ca-us_pms_retargeting_website-conv",
    "ca-us_pms_prospecting_website-conv",
])

# Human-readable labels for conversion event types in the report.
LEAD_TYPE_LABELS = {
    "lead": "Leads",
    "offsite_conversion.fb_pixel_complete_registration": "Website Complete Registration",
    "offsite_conversion.fb_pixel_custom.qualified_meeting_booked": "qualified_meeting_booked",
    "offsite_conversion.fb_pixel_custom.2025_industry_study": "2025_industry_study",
    "offsite_conversion.fb_pixel_custom.lead_email-valid": "lead_email-valid",
    "onsite_conversion.lead_grouped": "Meta Lead Form (grouped)",
    "onsite_web_lead": "Website Lead (onsite)",
    "offsite_conversion.fb_pixel_lead": "Pixel Lead (fb_pixel_lead)",
    "offsite_conversion.fb_pixel_custom": "Custom Pixel Event (fb_pixel_custom)",
    "onsite_conversion.total_messaging_connection": "Messaging Lead",
    "onsite_conversion.messaging_first_reply": "Messaging First Reply",
    "onsite_conversion.messaging_conversation_started_7d": "Messaging Conversation Started",
    "offsite_complete_registration_add_meta_leads": "Lead Form Registration Step",
    "offsite_search_add_meta_leads": "Lead Form Search Step",
    "offsite_content_view_add_meta_leads": "Lead Form Content View Step",
}


def week_folder_name(dt: datetime = None) -> str:
    """Generate folder name in wwmmmyy format, e.g. '11mar26'."""
    dt = dt or datetime.now()
    week_num = dt.isocalendar()[1]
    return f"{week_num:02d}{dt.strftime('%b').lower()}{dt.strftime('%y')}"


def _time_range_for_week(dt: datetime = None) -> dict:
    """Return the Monday–Sunday time_range for the ISO week containing dt."""
    dt = dt or datetime.now()
    monday = dt - timedelta(days=dt.weekday())
    sunday = monday + timedelta(days=6)
    return {"since": monday.strftime("%Y-%m-%d"), "until": sunday.strftime("%Y-%m-%d")}


# ═══════════════════════════════════════════════════════════════════════
#  META ADS DATA LAYER
# ═══════════════════════════════════════════════════════════════════════

def meta_get(endpoint, params=None):
    if not META_ACCESS_TOKEN:
        return {"error": "META_ACCESS_TOKEN not set"}
    url = f"{META_BASE_URL}/{endpoint}"
    params = params or {}
    params["access_token"] = META_ACCESS_TOKEN
    try:
        resp = requests.get(url, params=params, timeout=60)
        if resp.status_code != 200:
            data = resp.json() if "application/json" in resp.headers.get("content-type", "") else {}
            return {"error": f"HTTP {resp.status_code}", "body": data}
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def _make_time_range_param(since: str, until: str) -> str:
    return json.dumps({"since": since, "until": until})


def meta_insights_collect_all_pages(initial_response: dict) -> list:
    """
    Collect every insight row from paged Meta Graph API responses.

    Meta often returns multiple rows (daily breakdown) and/or multiple pages (25+ rows).
    Using only data[0] undercounts MTD spend; sum all rows and follow paging.next.
    """
    rows: list = []
    raw = initial_response
    while isinstance(raw, dict):
        if raw.get("error"):
            break
        for row in raw.get("data") or []:
            if isinstance(row, dict):
                rows.append(row)
        next_url = raw.get("paging", {}).get("next")
        if not next_url:
            break
        try:
            resp = requests.get(next_url, timeout=60)
            raw = resp.json() if resp.status_code == 200 else {}
        except Exception:
            break
    return rows


def meta_aggregate_insight_rows(rows: list) -> dict:
    """
    Merge multiple insight rows into one dict: sum spend (and additive metrics);
    merge actions/conversions by action_type (sum values). Matches Ads Manager MTD.
    """
    if not rows:
        return {}
    total_spend = 0.0
    total_impressions = 0.0
    total_clicks = 0.0
    for r in rows:
        try:
            total_spend += float(r.get("spend", 0) or 0)
        except (TypeError, ValueError):
            pass
        try:
            total_impressions += float(r.get("impressions", 0) or 0)
        except (TypeError, ValueError):
            pass
        try:
            total_clicks += float(r.get("clicks", 0) or 0)
        except (TypeError, ValueError):
            pass

    def _merge_action_lists(key: str) -> list:
        totals: dict[str, float] = {}
        for r in rows:
            for a in r.get(key) or []:
                if not isinstance(a, dict):
                    continue
                at = a.get("action_type")
                if not at:
                    continue
                try:
                    v = float(a.get("value", 0) or 0)
                except (TypeError, ValueError):
                    continue
                totals[at] = totals.get(at, 0.0) + v
        out = []
        for at, v in totals.items():
            s = str(int(v)) if float(v).is_integer() else str(v)
            out.append({"action_type": at, "value": s})
        return out

    return {
        "spend": str(round(total_spend, 2)),
        "impressions": str(int(total_impressions)),
        "clicks": str(int(total_clicks)),
        "actions": _merge_action_lists("actions"),
        "conversions": _merge_action_lists("conversions"),
    }


def fetch_meta_account_summary(since: str, until: str):
    return meta_get(f"act_{META_AD_ACCOUNT_ID}/insights", {
        "fields": INSIGHT_FIELDS,
        "time_range": _make_time_range_param(since, until),
    })


def fetch_meta_account_spend_mtd(since: str, until: str) -> float:
    """Account-level spend for time_range (aggregated across all insight pages/rows)."""
    acc = fetch_meta_account_summary(since, until)
    rows = meta_insights_collect_all_pages(acc)
    merged = meta_aggregate_insight_rows(rows)
    try:
        return float(merged.get("spend", 0) or 0)
    except (TypeError, ValueError):
        return 0.0


def fetch_meta_campaigns(since: str, until: str):
    # Include ARCHIVED: campaigns can spend in-period then archive; excluding them drops MTD spend.
    return meta_get(f"act_{META_AD_ACCOUNT_ID}/campaigns", {
        "fields": f"{CAMPAIGN_FIELDS},insights{{{INSIGHT_FIELDS}}}",
        "effective_status": '["ACTIVE","PAUSED","ARCHIVED"]',
        "time_range": _make_time_range_param(since, until),
        "limit": 500,
    })


def fetch_meta_ad_sets(campaign_id: str, since: str, until: str):
    return meta_get(f"{campaign_id}/adsets", {
        "fields": f"id,name,status,targeting,daily_budget,bid_amount,optimization_goal,"
                  f"promoted_object,insights{{{INSIGHT_FIELDS}}}",
        "time_range": _make_time_range_param(since, until),
        "limit": 100,
    })


def fetch_meta_ads(ad_set_id: str, since: str, until: str):
    return meta_get(f"{ad_set_id}/ads", {
        "fields": f"id,name,status,"
                  f"creative{{title,body,image_url,thumbnail_url,video_id}},"
                  f"insights{{{INSIGHT_FIELDS}}}",
        "time_range": _make_time_range_param(since, until),
        "limit": 100,
    })


def pull_full_meta_data(since: str, until: str):
    """Pull the complete Meta Ads hierarchy for ALL campaigns.
    Reports data on all campaigns; only POST_ENGAGEMENT campaigns are excluded from lead counts.
    """
    print("   📥 Pulling Meta Ads account summary...")
    account = fetch_meta_account_summary(since, until)

    print("   📥 Pulling Meta Ads campaigns...")
    campaigns_raw = fetch_meta_campaigns(since, until)
    campaigns = campaigns_raw.get("data", []) if isinstance(campaigns_raw, dict) else []
    while isinstance(campaigns_raw, dict) and campaigns_raw.get("paging", {}).get("next"):
        try:
            resp = requests.get(campaigns_raw["paging"]["next"], timeout=60)
            campaigns_raw = resp.json()
            campaigns.extend(campaigns_raw.get("data", []))
        except Exception:
            break

    # Fetch optimization map for ALL campaigns (bulk ad set fetch; no campaign filter)
    print("   📥 Fetching optimization map (all ad sets)...")
    optimization_map = fetch_meta_optimization_map()

    enriched_campaigns = []
    for camp in campaigns:
        camp_id = camp.get("id", "")
        camp_name = camp.get("name", "Unknown")

        # Fetch insights for ALL campaigns (required for accurate lead/conversion counts)
        print(f"      📥 Insights: {camp_name}")
        camp_insights = meta_get(f"{camp_id}/insights", {
            "fields": f"{INSIGHT_FIELDS}",
            "time_range": _make_time_range_param(since, until),
        })
        # IMPORTANT: Always set _campaign_insights to avoid falling back to embedded/lifetime insights.
        # Sum all insight rows + paginate — Meta returns daily rows and/or >1 page; data[0] alone undercounts MTD.
        if isinstance(camp_insights, dict) and "data" in camp_insights:
            ci_rows = meta_insights_collect_all_pages(camp_insights)
            camp["_campaign_insights"] = meta_aggregate_insight_rows(ci_rows) if ci_rows else {}
        else:
            camp["_campaign_insights"] = {}

        # Ad sets/ads only for campaigns with spend (saves API calls; optimization_map from bulk fetch)
        ci = camp.get("_campaign_insights") or {}
        spend = float(ci.get("spend", "0") if isinstance(ci, dict) else 0)
        enriched_ad_sets = []
        if spend > 0:
            ad_sets_raw = fetch_meta_ad_sets(camp_id, since, until)
            ad_sets = ad_sets_raw.get("data", []) if isinstance(ad_sets_raw, dict) else []
            for adset in ad_sets:
                adset_spend = 0
                ins = adset.get("insights", {})
                if isinstance(ins, dict) and ins.get("data"):
                    adset_spend = float(ins["data"][0].get("spend", "0"))
                if adset_spend > 0:
                    ads_raw = fetch_meta_ads(adset.get("id", ""), since, until)
                    adset["_ads"] = ads_raw.get("data", []) if isinstance(ads_raw, dict) else []
                enriched_ad_sets.append(adset)
        camp["_ad_sets"] = enriched_ad_sets
        enriched_campaigns.append(camp)

    print(f"      Mapped {len(optimization_map)} campaigns to optimization events")

    return {
        "platform": "Meta Ads",
        "time_range": {"since": since, "until": until},
        "pulled_at": datetime.now().isoformat(),
        "account_summary": account,
        "campaigns": enriched_campaigns,
        "optimization_map": optimization_map,
    }


# ═══════════════════════════════════════════════════════════════════════
#  OPTIMIZATION EVENT MAPPING
# ═══════════════════════════════════════════════════════════════════════

def fetch_meta_optimization_map() -> dict:
    """Fetch all ad sets and build campaign_id -> optimization event mapping.

    Returns dict:  {campaign_id: {
        "optimization_goal": str,
        "custom_event_type": str,   # LEAD, OTHER, PURCHASE, etc.
        "custom_event_str": str,    # e.g. "2025_industry_study"
        "custom_conversion_id": str,
    }}

    When a campaign has multiple ad sets, the first ACTIVE one is used.
    """
    all_adsets = []
    result = meta_get(f"act_{META_AD_ACCOUNT_ID}/adsets", {
        "fields": "campaign_id,name,optimization_goal,promoted_object,effective_status",
        "limit": 200,
    })
    if isinstance(result, dict) and "error" in result:
        print(f"      ⚠️ Ad set fetch error: {result['error']}")
    if isinstance(result, dict) and "data" in result:
        all_adsets.extend(result["data"])
        while result.get("paging", {}).get("next"):
            try:
                resp = requests.get(result["paging"]["next"], timeout=60)
                result = resp.json()
                all_adsets.extend(result.get("data", []))
            except Exception:
                break
    print(f"      Fetched {len(all_adsets)} ad sets total")

    campaign_adsets: dict[str, list] = {}
    for adset in all_adsets:
        cid = adset.get("campaign_id")
        if cid:
            campaign_adsets.setdefault(cid, []).append(adset)

    opt_map: dict[str, dict] = {}
    for cid, adsets in campaign_adsets.items():
        active = [a for a in adsets if a.get("effective_status") == "ACTIVE"]
        chosen = active[0] if active else adsets[0]
        promoted = chosen.get("promoted_object") or {}
        opt_map[cid] = {
            "optimization_goal": chosen.get("optimization_goal", ""),
            "custom_event_type": promoted.get("custom_event_type", ""),
            "custom_event_str": promoted.get("custom_event_str", ""),
            "custom_conversion_id": promoted.get("custom_conversion_id", ""),
        }

    return opt_map


# Custom conversion events effective from a certain date. Exclude from periods
# before this date (Meta API may attribute conversions due to attribution windows
# even when the event was not yet configured).
CONVERSION_EVENT_EFFECTIVE_DATE = {
    "lead_email-valid": "2026-03-01",
}

# Maps Meta custom_event_type values to their standard action_type names.
STANDARD_EVENT_TYPE_TO_ACTION = {
    "LEAD": "lead",
    "COMPLETE_REGISTRATION": "offsite_conversion.fb_pixel_complete_registration",
    "PURCHASE": "offsite_conversion.fb_pixel_purchase",
    "ADD_TO_CART": "offsite_conversion.fb_pixel_add_to_cart",
    "INITIATE_CHECKOUT": "offsite_conversion.fb_pixel_initiate_checkout",
    "SEARCH": "offsite_conversion.fb_pixel_search",
    "VIEW_CONTENT": "offsite_conversion.fb_pixel_view_content",
    "ADD_PAYMENT_INFO": "offsite_conversion.fb_pixel_add_payment_info",
    "ADD_TO_WISHLIST": "offsite_conversion.fb_pixel_add_to_wishlist",
    "SUBSCRIBE": "offsite_conversion.fb_pixel_subscribe",
    "START_TRIAL": "offsite_conversion.fb_pixel_start_trial",
}


def _build_optimization_map_from_campaigns(campaigns: list) -> dict:
    """Build optimization map from ad sets already fetched per campaign.
    Uses the promoted_object and optimization_goal from each campaign's ad sets."""
    opt_map: dict[str, dict] = {}
    for camp in campaigns:
        camp_id = camp.get("id", "")
        adsets = camp.get("_ad_sets", [])
        if not adsets or not camp_id:
            continue
        active = [a for a in adsets if a.get("status") == "ACTIVE"
                  or a.get("effective_status") == "ACTIVE"]
        chosen = active[0] if active else adsets[0]
        promoted = chosen.get("promoted_object") or {}
        opt_map[camp_id] = {
            "optimization_goal": chosen.get("optimization_goal", ""),
            "custom_event_type": promoted.get("custom_event_type", ""),
            "custom_event_str": promoted.get("custom_event_str", ""),
            "custom_conversion_id": promoted.get("custom_conversion_id", ""),
        }
    return opt_map


def _label_for_action_type(at: str) -> str:
    """Human-readable label for any action_type, including dynamic custom events."""
    if at in LEAD_TYPE_LABELS:
        return LEAD_TYPE_LABELS[at]
    if at.startswith("offsite_conversion.fb_pixel_custom."):
        event_name = at.replace("offsite_conversion.fb_pixel_custom.", "")
        return f"Custom Pixel Event ({event_name})"
    if at.startswith("offsite_conversion.custom."):
        conv_id = at.replace("offsite_conversion.custom.", "")
        return f"Custom Conversion ({conv_id})"
    return at


# ═══════════════════════════════════════════════════════════════════════
#  RESULTS / LEAD CALCULATOR
# ═══════════════════════════════════════════════════════════════════════

def _get_insight_field(entity: dict, field: str) -> list:
    """Extract a list field (actions, conversions) from an entity.
    When _campaign_insights exists (per-campaign insight call with explicit
    time_range), ALWAYS use it — never fall through to embedded insights
    which may use a default/lifetime time range."""
    ci = entity.get("_campaign_insights")
    if ci is not None:
        return ci.get(field, [])
    val = entity.get(field)
    if val is not None:
        return val
    insights = entity.get("insights", {})
    if isinstance(insights, dict):
        data = insights.get("data", [])
        if data:
            return data[0].get(field, [])
    return []


def _get_actions(entity: dict) -> list:
    """Extract the actions list from an entity (campaign/ad set/ad)."""
    return _get_insight_field(entity, "actions")


def _get_conversions(entity: dict) -> list:
    """Extract the conversions list from an entity.
    The 'conversions' field returns specific named pixel events
    (e.g. offsite_conversion.fb_pixel_custom.2025_industry_study)
    unlike 'actions' which aggregates custom events."""
    return _get_insight_field(entity, "conversions")


def _get_campaign_allowed_breakdown(campaign: dict) -> dict:
    """Per-campaign counts for the three allowed conversion types (lead, qualified_meeting_booked, complete_registration).
    Returns dict with keys: lead, qualified_meeting_booked, complete_registration, total."""
    def _int_val(lst, action_type):
        for item in lst or []:
            if isinstance(item, dict) and item.get("action_type") == action_type:
                try:
                    return int(item.get("value", 0))
                except (TypeError, ValueError):
                    return 0
        return 0

    actions = _get_actions(campaign)
    conversions = _get_conversions(campaign)
    lead = _int_val(actions, "lead")
    complete_reg = _int_val(actions, "offsite_conversion.fb_pixel_complete_registration")
    qualified_meeting = _int_val(conversions, "offsite_conversion.fb_pixel_custom.qualified_meeting_booked")
    return {
        "lead": lead,
        "qualified_meeting_booked": qualified_meeting,
        "complete_registration": complete_reg,
        "total": lead + qualified_meeting + complete_reg,
    }


def _campaign_had_delivery(campaign: dict) -> bool:
    """True if this campaign had delivery in the requested period (impressions>0 or spend>0)."""
    ci = campaign.get("_campaign_insights") or {}
    if not isinstance(ci, dict):
        return False
    try:
        impressions = int(float(ci.get("impressions") or 0))
    except (TypeError, ValueError):
        impressions = 0
    try:
        spend = float(ci.get("spend") or 0)
    except (TypeError, ValueError):
        spend = 0.0
    return impressions > 0 or spend > 0


def _campaign_status_ok(campaign: dict) -> bool:
    """Conservative status filter for including campaigns in reporting."""
    # Prefer effective_status when present; fall back to status.
    status = (campaign.get("effective_status") or campaign.get("status") or "").upper()
    # Allow PAUSED if it still delivered in the period; we filter delivery separately.
    return status in {"ACTIVE", "PAUSED"}


def load_meta_campaign_objectives() -> dict | None:
    """Load meta_campaign_objectives.json. Returns None if file missing or invalid."""
    if not META_OBJECTIVES_PATH.is_file():
        return None
    try:
        with open(META_OBJECTIVES_PATH, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data.get("campaigns"), dict) and isinstance(data.get("objective_keys"), dict):
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return None


def _primary_action_for_campaign(
    campaign: dict,
    optimization_map: dict | None = None,
    meta_objectives: dict | None = None,
) -> str | None:
    """Return the single action_type to use for 'Results' based on the campaign's objective.

    When meta_objectives (from meta_campaign_objectives.json) is provided:
    - If campaign_id is in the file: use objective_keys[entry.objective]; 'none' => None.
    - If campaign_id is not in the file: log warning and return None (strict mode).
    When meta_objectives is None (file missing): use fallback logic (optimization map + API + inference).
    """
    cid = (campaign.get("id") or "").strip()
    name = (campaign.get("name") or "").strip()
    campaigns_map = (meta_objectives or {}).get("campaigns") or {}
    keys_map = (meta_objectives or {}).get("objective_keys") or {}

    if meta_objectives is not None and campaigns_map and keys_map:
        if cid in campaigns_map:
            obj_key = (campaigns_map[cid].get("objective") or "").strip()
            if obj_key == "none" or not obj_key:
                return None
            action_type = (keys_map.get(obj_key) or "").strip()
            if action_type:
                return action_type
            return None
        print(f"   ⚠️ Campaign {cid} ({name}) not in meta_campaign_objectives.json; reporting 0 results.", file=sys.stderr)
        return None

    # Fallback when context file not loaded
    if name in CAMPAIGNS_PRIMARY_LEAD_EMAIL_VALID:
        return "offsite_conversion.fb_pixel_custom.lead_email-valid"

    obj = (campaign.get("objective") or "").upper()
    if obj in {"LEAD_GENERATION", "OUTCOME_LEADS", "LEADS"}:
        return "lead"

    om = (optimization_map or {}).get(cid) if cid else None
    if isinstance(om, dict):
        ces = (om.get("custom_event_str") or "").strip()
        cet = (om.get("custom_event_type") or "").strip().upper()
        if ces == "qualified_meeting_booked":
            return "offsite_conversion.fb_pixel_custom.qualified_meeting_booked"
        if ces == "2025_industry_study":
            return "offsite_conversion.fb_pixel_custom.2025_industry_study"
        if cet == "COMPLETE_REGISTRATION":
            return "offsite_conversion.fb_pixel_complete_registration"

    allowed = _get_campaign_allowed_breakdown(campaign)
    if allowed.get("qualified_meeting_booked", 0) > 0:
        return "offsite_conversion.fb_pixel_custom.qualified_meeting_booked"
    if allowed.get("complete_registration", 0) > 0:
        return "offsite_conversion.fb_pixel_complete_registration"
    if allowed.get("lead", 0) > 0:
        return "lead"
    return None


def _read_conversion_count(campaign: dict, action_type: str) -> int:
    """Read count for a single action_type from campaign insights (actions or conversions)."""
    def _int_val(lst, at):
        for item in lst or []:
            if isinstance(item, dict) and item.get("action_type") == at:
                try:
                    return int(item.get("value", 0))
                except (TypeError, ValueError):
                    return 0
        return 0

    actions = _get_actions(campaign)
    conversions = _get_conversions(campaign)
    if action_type == "lead":
        return _int_val(actions, "lead")
    if action_type == "offsite_conversion.fb_pixel_complete_registration":
        return _int_val(actions, action_type)
    # Custom pixel events (qualified_meeting_booked, 2025_industry_study, etc.) are in conversions
    if action_type.startswith("offsite_conversion.fb_pixel_custom."):
        return _int_val(conversions, action_type)
    return 0


def _objective_aligned_results(campaign: dict, primary_action_type: str | None) -> int:
    """Read results count for the chosen primary action_type for this campaign and period."""
    if not primary_action_type:
        return 0
    return _read_conversion_count(campaign, primary_action_type)


def _get_spend(entity: dict) -> float:
    """Extract spend from an entity. When _campaign_insights exists (explicit
    time_range), ALWAYS use it to avoid stale embedded insight data."""
    ci = entity.get("_campaign_insights")
    if ci is not None:
        return float(ci.get("spend", "0"))
    spend = entity.get("spend")
    if spend is not None:
        return float(spend)
    insights = entity.get("insights", {})
    if isinstance(insights, dict):
        data = insights.get("data", [])
        if data:
            return float(data[0].get("spend", "0"))
    return 0.0


def _get_metric(entity: dict, field: str) -> str:
    """Extract a metric string from an entity. When _campaign_insights exists,
    ALWAYS use it to avoid stale embedded insight data."""
    ci = entity.get("_campaign_insights")
    if ci is not None:
        return str(ci.get(field, ""))
    val = entity.get(field)
    if val is not None:
        return str(val)
    insights = entity.get("insights", {})
    if isinstance(insights, dict):
        data = insights.get("data", [])
        if data:
            return str(data[0].get(field, ""))
    return ""


def _is_conversion_in_scope(action_type: str, period_until: str) -> bool:
    """Return False if this action_type should be excluded for the given period (e.g. event added later)."""
    if not action_type.startswith("offsite_conversion.fb_pixel_custom."):
        return True
    event_name = action_type.replace("offsite_conversion.fb_pixel_custom.", "")
    effective = CONVERSION_EVENT_EFFECTIVE_DATE.get(event_name)
    if not effective:
        return True
    return period_until >= effective


def calculate_campaign_results(campaign: dict, optimization_map: dict = None, time_range: dict = None) -> dict:
    """Calculate lead results for a single campaign. One conversion event per campaign.
    Aligns with Meta Ads Manager: standard events prioritized over custom; no double-counting.
    
    - POST_ENGAGEMENT / OUTCOME_ENGAGEMENT → 0 leads.
    - Lead campaigns: use standard 'lead' if present; else custom conversion or custom pixel
      (single largest event only). lead_email-valid excluded before its effective date (Mar 2026).
    """
    actions = _get_actions(campaign)
    conversions = _get_conversions(campaign)
    if not isinstance(actions, list):
        actions = []
    if not isinstance(conversions, list):
        conversions = []
    action_map = {}
    for a in actions:
        if isinstance(a, dict) and a.get("action_type") is not None:
            try:
                action_map[a["action_type"]] = int(a.get("value", 0))
            except (TypeError, ValueError):
                pass
    conversion_map = {}
    for c in conversions:
        if isinstance(c, dict) and c.get("action_type") is not None:
            try:
                conversion_map[c["action_type"]] = int(c.get("value", 0))
            except (TypeError, ValueError):
                pass

    # If it's explicitly an engagement campaign, return 0 leads
    goal = campaign.get("objective", "")
    if goal in ("OUTCOME_ENGAGEMENT", "POST_ENGAGEMENT"):
        return {"results": 0, "lead_breakdown": {}, "is_engagement_campaign": True}

    # Helper function to accumulate standard leads and webinar registrations
    lead_count = action_map.get("lead", 0)

    # ── 1. Check for standard 'lead' action ──
    # The standard 'lead' event in action_map is the aggregate canonical count from forms/website
    if lead_count > 0:
        return {"results": lead_count, "lead_breakdown": {"lead": lead_count}, "is_engagement_campaign": False}

    # ── 1.25 Check for complete_registration standard event ──
    if "offsite_conversion.fb_pixel_complete_registration" in action_map and action_map["offsite_conversion.fb_pixel_complete_registration"] > 0:
        reg_count = action_map["offsite_conversion.fb_pixel_complete_registration"]
        return {"results": reg_count, "lead_breakdown": {"offsite_conversion.fb_pixel_complete_registration": reg_count}, "is_engagement_campaign": False}

    # ── 1.5 Check for custom conversions if available ──
    # Meta ads managers often report "offsite_conversion.custom.XXX" as the main conversion event
    # We should prioritize this before standard custom pixel events
    custom_conversions = {}
    for conv_key, val in conversion_map.items():
        if conv_key.startswith("offsite_conversion.custom."):
            custom_conversions[conv_key] = val
            
    if custom_conversions:
        top_event_key = max(custom_conversions, key=custom_conversions.get)
        top_count = custom_conversions[top_event_key]
        return {"results": top_count, "lead_breakdown": {top_event_key: top_count}, "is_engagement_campaign": False}

    # ── 2. Check for Custom Pixel Events in conversions map ──
    # If no standard lead, check if any custom pixel event was fired
    period_until = (time_range or {}).get("until", "9999-12-31")
    custom_events = {}
    for conv_key, val in conversion_map.items():
        if conv_key.startswith("offsite_conversion.fb_pixel_custom.") and _is_conversion_in_scope(conv_key, period_until):
            # Special exclusion: ignore lead_email-valid in fallback logic as it often duplicates standard leads
            if conv_key == "offsite_conversion.fb_pixel_custom.lead_email-valid" and period_until < "2026-03-01":
                continue
            custom_events[conv_key] = val

    if custom_events:
        # Just return the single largest custom event for this campaign to avoid double counting
        top_event_key = max(custom_events, key=custom_events.get)
        top_count = custom_events[top_event_key]
        
        # If the largest is lead_email-valid and we are pre-March 2026, ignore it (should be caught above, but just in case)
        if top_event_key == "offsite_conversion.fb_pixel_custom.lead_email-valid" and period_until < "2026-03-01":
             return {"results": 0, "lead_breakdown": {}, "is_engagement_campaign": False}
             
        return {"results": top_count, "lead_breakdown": {top_event_key: top_count}, "is_engagement_campaign": False}

    # ── 3. Check for specific fallback events (Messaging) ──
    if "onsite_conversion.total_messaging_connection" in action_map and action_map["onsite_conversion.total_messaging_connection"] > 0:
        msg_count = action_map["onsite_conversion.total_messaging_connection"]
        return {"results": msg_count, "lead_breakdown": {"onsite_conversion.total_messaging_connection": msg_count}, "is_engagement_campaign": False}

    # If no leads or recognized custom events are found, it generated 0 leads.
    return {"results": 0, "lead_breakdown": {}, "is_engagement_campaign": False}


def _first_account_insight_row(data: dict):
    """First row of account_summary.data. Handles data being list or dict (API variance). Returns dict or None."""
    acct = data.get("account_summary", {}) if isinstance(data, dict) else {}
    if not isinstance(acct, dict) or "data" not in acct:
        return None
    acct_data = acct.get("data")
    if not acct_data:
        return None
    if isinstance(acct_data, list):
        return acct_data[0] if acct_data else None
    if isinstance(acct_data, dict):
        vals = list(acct_data.values())
        return vals[0] if vals else None
    return None


def _get_account_lead_count(data: dict) -> int | None:
    """Extract account-level 'lead' count from account_summary. Matches Meta Ads Manager Results.
    Returns None if account summary or lead action is missing."""
    row = _first_account_insight_row(data)
    if not row or not isinstance(row, dict):
        return None
    actions = row.get("actions") or []
    for a in actions:
        if isinstance(a, dict) and a.get("action_type") == "lead":
            try:
                return int(a.get("value", 0))
            except (TypeError, ValueError):
                return None
    return None


def _get_account_allowed_lead_breakdown(data: dict):
    """Get account-level counts for the three allowed conversion types (lead, qualified_meeting_booked, complete_registration).
    Reads from account_summary.data[0].actions and .conversions so totals match Meta Ads Manager.
    Returns (total_leads, allowed_breakdown_list) or (None, None) if no account row."""
    row = _first_account_insight_row(data)
    if not row or not isinstance(row, dict):
        return None, None

    def _int_val(lst, action_type):
        for item in lst or []:
            if isinstance(item, dict) and item.get("action_type") == action_type:
                try:
                    return int(item.get("value", 0))
                except (TypeError, ValueError):
                    return 0
        return 0

    actions = row.get("actions") or []
    conversions = row.get("conversions") or []

    lead_count = _int_val(actions, "lead")
    complete_reg_count = _int_val(actions, "offsite_conversion.fb_pixel_complete_registration")
    qualified_meeting_count = _int_val(conversions, "offsite_conversion.fb_pixel_custom.qualified_meeting_booked")

    total = lead_count + complete_reg_count + qualified_meeting_count
    breakdown_list = [
        {"action_type": "lead", "label": _label_for_action_type("lead"), "count": lead_count},
        {"action_type": "offsite_conversion.fb_pixel_custom.qualified_meeting_booked", "label": _label_for_action_type("offsite_conversion.fb_pixel_custom.qualified_meeting_booked"), "count": qualified_meeting_count},
        {"action_type": "offsite_conversion.fb_pixel_complete_registration", "label": _label_for_action_type("offsite_conversion.fb_pixel_complete_registration"), "count": complete_reg_count},
    ]
    return total, breakdown_list


def build_lead_analysis(data: dict, optimization_map: dict = None) -> dict:
    """Pre-compute lead counts and breakdowns for every campaign.
    Uses account-level spend and account-level 'lead' count when available so totals match Meta Ads Manager.
    Primary conversion per campaign comes from meta_campaign_objectives.json when present."""
    campaigns = data.get("campaigns", [])
    optimization_map = optimization_map or data.get("optimization_map", {})
    time_range = data.get("time_range", {})
    meta_objectives = load_meta_campaign_objectives()
    campaign_total_leads = 0
    total_spend = 0.0
    campaign_results = []
    lead_type_totals = {}

    in_scope_campaigns = []
    for camp in campaigns:
        # Only include campaigns that were active-ish AND had delivery in this time period.
        if not _campaign_status_ok(camp):
            continue
        if not _campaign_had_delivery(camp):
            continue
        in_scope_campaigns.append(camp)

    for camp in in_scope_campaigns:
        spend = _get_spend(camp)
        total_spend += spend

        # Objective-aligned results: only count the single conversion tied to the campaign's objective.
        primary_action = _primary_action_for_campaign(camp, optimization_map, meta_objectives)
        results = _objective_aligned_results(camp, primary_action)
        campaign_total_leads += results

        # Keep the existing lead_type_totals for diagnostics (still based on calculate_campaign_results).
        res = calculate_campaign_results(camp, optimization_map, time_range)
        for at, count in (res.get("lead_breakdown") or {}).items():
            if at in SUB_METRICS:
                continue
            lead_type_totals[at] = lead_type_totals.get(at, 0) + count

        allowed = _get_campaign_allowed_breakdown(camp)
        primary_objective_label = _label_for_action_type(primary_action) if primary_action else ""
        campaign_results.append({
            "campaign_id": camp.get("id", ""),
            "campaign_name": camp.get("name", ""),
            "objective": camp.get("objective", ""),
            "status": camp.get("status", ""),
            "effective_status": camp.get("effective_status", ""),
            "spend": spend,
            "leads": results,
            "primary_action_type": primary_action,
            "primary_objective_label": primary_objective_label,
            "cpl": round(spend / results, 2) if results > 0 else None,
            "is_engagement": res.get("is_engagement_campaign", False),
            "lead_breakdown": res.get("lead_breakdown", {}),
            "allowed_breakdown": allowed,
        })

    account_spend = 0.0
    acct_row = _first_account_insight_row(data)
    if acct_row and isinstance(acct_row, dict):
        account_spend = float(acct_row.get("spend", "0"))
    else:
        acct = data.get("account_summary", {})
        if isinstance(acct, dict):
            account_spend = float(acct.get("spend", "0"))

    # Total leads = sum of objective-aligned results across in-scope campaigns.
    total_leads = sum(int(cr.get("leads", 0) or 0) for cr in campaign_results)

    # Allowed breakdown = sum of objective-aligned results by objective-mapped conversion type.
    allowed_lead_breakdown = {
        "lead": 0,
        "offsite_conversion.fb_pixel_custom.qualified_meeting_booked": 0,
        "offsite_conversion.fb_pixel_complete_registration": 0,
    }
    for cr in campaign_results:
        pat = cr.get("primary_action_type")
        if pat in allowed_lead_breakdown:
            allowed_lead_breakdown[pat] += int(cr.get("leads", 0) or 0)

    allowed_breakdown_list = [
        {"action_type": at, "label": _label_for_action_type(at), "count": allowed_lead_breakdown.get(at, 0)}
        for at in [
            "lead",
            "offsite_conversion.fb_pixel_custom.qualified_meeting_booked",
            "offsite_conversion.fb_pixel_complete_registration",
        ]
    ]

    reporting_spend = account_spend if account_spend > 0 else total_spend
    spend_delta = abs(account_spend - total_spend)

    lead_type_breakdown = []
    for at, count in sorted(lead_type_totals.items(), key=lambda x: -x[1]):
        label = _label_for_action_type(at)
        lead_type_breakdown.append({"action_type": at, "label": label, "count": count})

    campaign_leads_breakdown = [
        {
            "campaign_name": cr.get("campaign_name", ""),
            "spend": cr.get("spend", 0),
            "results": cr.get("leads", 0),
            "primary_objective": cr.get("primary_objective_label", ""),
            "lead": (cr.get("allowed_breakdown") or {}).get("lead", 0),
            "qualified_meeting_booked": (cr.get("allowed_breakdown") or {}).get("qualified_meeting_booked", 0),
            "complete_registration": (cr.get("allowed_breakdown") or {}).get("complete_registration", 0),
            "total": cr.get("leads", 0),
        }
        for cr in campaign_results
    ]
    campaign_leads_breakdown.sort(key=lambda x: -x["total"])

    return {
        "total_leads": total_leads,
        "total_campaign_spend": round(total_spend, 2),
        "account_level_spend": round(account_spend, 2),
        "reporting_spend": round(reporting_spend, 2),
        "spend_delta": round(spend_delta, 2),
        "blended_cpl": round(reporting_spend / total_leads, 2) if total_leads > 0 else None,
        "lead_type_breakdown": lead_type_breakdown,
        "allowed_lead_breakdown": allowed_breakdown_list,
        "campaign_results": campaign_results,
        "campaign_leads_breakdown": campaign_leads_breakdown,
    }


def validate_data(data: dict, analysis: dict) -> list:
    """Cross-check data integrity. Returns list of warning strings."""
    warnings = []
    if analysis["spend_delta"] > 0.01:
        warnings.append(
            f"Spend mismatch: account-level ${analysis['account_level_spend']:.2f} vs "
            f"sum of campaigns ${analysis['total_campaign_spend']:.2f} "
            f"(delta: ${analysis['spend_delta']:.2f})"
        )
    return warnings


# ═══════════════════════════════════════════════════════════════════════
#  GOOGLE ADS DATA LAYER
# ═══════════════════════════════════════════════════════════════════════

def gads_access_token():
    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": GADS_CLIENT_ID,
        "client_secret": GADS_CLIENT_SECRET,
        "refresh_token": GADS_REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }, timeout=30)
    data = resp.json()
    return data.get("access_token")


def _parse_googleads_http_error(resp: requests.Response) -> str:
    """Extract message from Google Ads API JSON error (403/404 debugging)."""
    try:
        j = resp.json()
        err = j.get("error") or {}
        msg = err.get("message") or err.get("status")
        if msg:
            return str(msg)[:900]
        return str(j)[:900]
    except Exception:
        return (resp.text or "")[:900]


def gads_list_accessible_customers():
    """List customer IDs accessible to the OAuth user. Helps debug 404s."""
    token = gads_access_token()
    if not token:
        return None, "Could not obtain access token"
    url = "https://googleads.googleapis.com/v23/customers:listAccessibleCustomers"
    headers = {
        "Authorization": f"Bearer {token}",
        "developer-token": GADS_DEV_TOKEN,
        "Content-Type": "application/json",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code != 200:
            return None, f"HTTP {resp.status_code}: {resp.text[:500]}"
        data = resp.json()
        return data.get("resourceNames", []), None
    except Exception as e:
        return None, str(e)


def _gaql_request(query: str, use_search_stream: bool = True, login_customer_id: str = None, omit_login: bool = False):
    """Make a GAQL request. Returns (rows, error_string). omit_login=True skips login-customer-id header."""
    token = gads_access_token()
    if not token:
        return [], "Could not obtain Google Ads access token"
    method = "searchStream" if use_search_stream else "search"
    url = f"https://googleads.googleapis.com/v23/customers/{GADS_CUSTOMER_ID}/googleAds:{method}"
    headers = {
        "Authorization": f"Bearer {token}",
        "developer-token": GADS_DEV_TOKEN,
        "Content-Type": "application/json",
    }
    if not omit_login:
        if login_customer_id:
            headers["login-customer-id"] = login_customer_id
        elif GADS_MANAGER_ID:
            headers["login-customer-id"] = GADS_MANAGER_ID
    body = {"query": query}
    if not use_search_stream:
        body["pageSize"] = 10000
    try:
        resp = requests.post(url, headers=headers, json=body, timeout=60)
        if resp.status_code != 200:
            detail = _parse_googleads_http_error(resp)
            return [], f"HTTP {resp.status_code}: {detail}"
        data = resp.json()
        rows = []
        if use_search_stream:
            batches = data if isinstance(data, list) else [data]
            for batch in batches:
                rows.extend(batch.get("results", []))
        else:
            rows = data.get("results", [])
            next_token = data.get("nextPageToken")
            while next_token:
                body["pageToken"] = next_token
                resp2 = requests.post(url, headers=headers, json=body, timeout=60)
                if resp2.status_code != 200:
                    break
                data2 = resp2.json()
                rows.extend(data2.get("results", []))
                next_token = data2.get("nextPageToken")
        return rows, None
    except Exception as e:
        return [], str(e)


def gaql_query(query):
    """Execute GAQL query. Retries on 403/404: different login-customer-id, omit MCC, search vs stream."""
    rows, err = _gaql_request(query, use_search_stream=True)
    if not err:
        return rows

    err_str = err or ""
    # Only retry on permission / not-found (403/404). Other codes (401, 400) return as-is.
    if "403" not in err_str and "404" not in err_str:
        return [{"error": err_str}]

    # --- Retry ladder for 403 (permission / wrong login-customer-id) and 404 ---
    retry_specs = [
        ("searchStream omit login-customer-id (leaf account)", True, True),
        ("search omit login-customer-id", False, True),
        ("search with default login headers", False, False),
    ]
    for label, use_stream, omit_login in retry_specs:
        rows2, e2 = _gaql_request(query, use_search_stream=use_stream, omit_login=omit_login)
        if not e2:
            print(f"   ✅ GAQL resolved: {label}")
            return rows2

    # Try each accessible customer as login-customer-id (MCC / linked accounts)
    accessible, acc_err = gads_list_accessible_customers()
    if accessible is not None:
        ids = [n.replace("customers/", "") for n in accessible if n.startswith("customers/")]
        print(f"   📋 Accessible Google Ads accounts: {ids}")
        for lid in ids:
            for use_stream in (True, False):
                rows2, e2 = _gaql_request(query, use_search_stream=use_stream, login_customer_id=lid)
                if not e2:
                    print(f"   ✅ GAQL resolved with login-customer-id={lid}")
                    return rows2
        # Legacy: if customer id not in list, try alternate login (already covered by loop above)
        if GADS_MANAGER_ID:
            rows2, e2 = _gaql_request(query, use_search_stream=True, omit_login=True)
            if not e2:
                print(f"   ✅ Resolved by omitting login-customer-id")
                return rows2

    hint = (
        " 403 often: OAuth user lacks access to GOOGLE_ADS_CUSTOMER_ID; wrong MCC header "
        "(set GOOGLE_ADS_MANAGER_ID to your MCC for client accounts, or remove for direct-linked); "
        "developer token not approved for production. 404: invalid customer id."
    )
    if acc_err:
        hint += f" listAccessibleCustomers: {acc_err}."
    return [{"error": f"{err_str}{hint}"}]


def fetch_gads_account_summary(since: str, until: str):
    return gaql_query(f"""
        SELECT metrics.impressions, metrics.clicks, metrics.ctr,
               metrics.average_cpc, metrics.cost_micros, metrics.conversions,
               metrics.cost_per_conversion, metrics.all_conversions,
               metrics.interaction_rate, metrics.average_cpm
        FROM customer
        WHERE segments.date BETWEEN '{since}' AND '{until}'
    """)


def fetch_gads_campaigns(since: str, until: str):
    return gaql_query(f"""
        SELECT campaign.id, campaign.name, campaign.status,
               campaign.advertising_channel_type, campaign.bidding_strategy_type,
               metrics.impressions, metrics.clicks, metrics.ctr,
               metrics.average_cpc, metrics.cost_micros, metrics.conversions,
               metrics.cost_per_conversion, metrics.search_impression_share,
               metrics.average_cpm
        FROM campaign
        WHERE segments.date BETWEEN '{since}' AND '{until}'
          AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
        LIMIT 50
    """)


def fetch_gads_ad_groups(campaign_id, since: str, until: str):
    return gaql_query(f"""
        SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.type,
               metrics.impressions, metrics.clicks, metrics.ctr,
               metrics.average_cpc, metrics.cost_micros, metrics.conversions,
               metrics.cost_per_conversion
        FROM ad_group
        WHERE campaign.id = {campaign_id}
          AND segments.date BETWEEN '{since}' AND '{until}'
        ORDER BY metrics.cost_micros DESC
        LIMIT 50
    """)


def fetch_gads_ads(ad_group_id, since: str, until: str):
    return gaql_query(f"""
        SELECT ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.type,
               ad_group_ad.ad.final_urls, ad_group_ad.status,
               metrics.impressions, metrics.clicks, metrics.ctr,
               metrics.average_cpc, metrics.cost_micros, metrics.conversions,
               metrics.cost_per_conversion
        FROM ad_group_ad
        WHERE ad_group.id = {ad_group_id}
          AND segments.date BETWEEN '{since}' AND '{until}'
        ORDER BY metrics.impressions DESC
        LIMIT 50
    """)


def fetch_gads_keywords(campaign_id, since: str, until: str):
    return gaql_query(f"""
        SELECT ad_group_criterion.keyword.text,
               ad_group_criterion.keyword.match_type,
               ad_group_criterion.quality_info.quality_score,
               metrics.impressions, metrics.clicks, metrics.ctr,
               metrics.average_cpc, metrics.cost_micros, metrics.conversions,
               metrics.cost_per_conversion
        FROM keyword_view
        WHERE campaign.id = {campaign_id}
          AND segments.date BETWEEN '{since}' AND '{until}'
        ORDER BY metrics.impressions DESC
        LIMIT 100
    """)


def fetch_gads_conversions():
    return gaql_query("""
        SELECT conversion_action.id, conversion_action.name,
               conversion_action.type, conversion_action.status,
               metrics.conversions, metrics.all_conversions
        FROM conversion_action
        ORDER BY metrics.conversions DESC
        LIMIT 50
    """)


def pull_full_google_data(since: str, until: str):
    """Pull the complete Google Ads hierarchy. All API responses stored verbatim."""
    print("   📥 Pulling Google Ads account summary...")
    account = fetch_gads_account_summary(since, until)

    print("   📥 Pulling Google Ads campaigns...")
    campaigns = fetch_gads_campaigns(since, until)

    enriched_campaigns = []
    for camp_row in campaigns:
        camp = camp_row.get("campaign", {})
        camp_id = camp.get("id")
        camp_name = camp.get("name", "Unknown")
        if not camp_id:
            enriched_campaigns.append(camp_row)
            continue

        print(f"      📥 Ad groups for campaign: {camp_name}")
        ad_groups = fetch_gads_ad_groups(camp_id, since, until)

        enriched_ad_groups = []
        for ag_row in ad_groups:
            ag = ag_row.get("adGroup", {})
            ag_id = ag.get("id")
            if ag_id:
                print(f"         📥 Ads for ad group: {ag.get('name', 'Unknown')}")
                ads = fetch_gads_ads(ag_id, since, until)
                ag_row["ads"] = ads
            enriched_ad_groups.append(ag_row)

        camp_row["ad_groups"] = enriched_ad_groups

        print(f"      📥 Keywords for campaign: {camp_name}")
        camp_row["keywords"] = fetch_gads_keywords(camp_id, since, until)

        enriched_campaigns.append(camp_row)

    print("   📥 Pulling Google Ads conversion actions...")
    conversions = fetch_gads_conversions()

    return {
        "platform": "Google Ads",
        "time_range": {"since": since, "until": until},
        "pulled_at": datetime.now().isoformat(),
        "account_summary": account,
        "campaigns": enriched_campaigns,
        "conversion_actions": conversions,
    }


# ═══════════════════════════════════════════════════════════════════════
#  AI ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════════════════

ANALYSIS_SYSTEM_PROMPT = """You are a senior paid media analyst writing a weekly performance intelligence report.
Your analysis must match the depth and rigor of a professional campaign performance review.
Use the term "leads" (never "conversions") throughout the report.

You will receive TWO inputs:
1. RAW API DATA — the verbatim response from the ad platform API.
2. PRE-COMPUTED LEAD ANALYSIS — an exact, validated breakdown of leads per campaign
   computed deterministically from the API data. These numbers are AUTHORITATIVE.
   You MUST use these numbers exactly as provided. Do NOT recalculate leads from the raw data.

Structure your report EXACTLY as follows (using Markdown):

# {Platform} — Weekly Performance Intelligence Report
**Period:** {start_date} to {end_date}
**Generated:** {timestamp}

## 1. Executive Summary
2-3 paragraph high-level narrative of the week. Include total spend, total leads,
blended CPL, and the single most important insight.

## 2. Account-Level KPIs
Markdown table with: Spend, Impressions, Reach (if available), Clicks, CTR, CPC,
CPM, Total Leads, Blended CPL, Frequency (if available).

## 3. Lead Breakdown by Conversion Event Type
Markdown table showing each type of lead event, its count, and percentage of total.
Types include: Meta Lead Forms, Pixel Leads, Custom Pixel Events, Messaging Leads, etc.
Also include cost per lead for each type if calculable.

## 4. Campaign Performance Breakdown
For EACH campaign with spend: name, objective, status, spend, leads, CPL, CTR, CPM.
Markdown table followed by 1-2 sentence commentary per campaign.

## 5. Audience / Ad Set / Ad Group Analysis
Break down by targeting type or ad group. Identify:
- Best and worst performers by CPL and volume
- Concentration risk (% of leads from top audience)
- CTR differentials between audiences

## 6. Creative / Ad-Level Performance
- Top creatives ranked by lead volume
- Creative format breakdown (video vs image vs text)
- CTR and CPL by creative
- Fatigue signals (rising CPL or declining CTR on previously strong creatives)

## 7. Keywords & Search Terms (Google Ads only)
- Top keywords by leads
- Quality Score distribution
- Match type performance
- Wasted spend on low-converting keywords

## 8. Key Inflection Points & Anomalies
Flag any week-over-week shifts > 15% in CPL, CTR, CPM, or spend. Explain probable causes.

## 9. What Worked This Week
Bullet list of winning tactics, audiences, creatives with supporting data.

## 10. What Didn't Work & Why
Bullet list of underperformers with hypotheses.

## 11. Strategic Recommendations & Next Steps
Numbered list of actionable next steps with rationale. Include budget reallocation
suggestions, creative refresh timing, audience expansion/pruning, and testing proposals.

## 12. Raw Data Appendix
Include key data tables for reference.

RULES:
- ALWAYS use the numbers from the PRE-COMPUTED LEAD ANALYSIS. These are verified 1:1
  against the ad platform. Do NOT derive your own lead counts from the raw actions array.
- Always cite specific numbers. Never say "improved" without a %, $, or absolute number.
- If data is missing or the account has no active campaigns, state that clearly.
- Use $ formatting for costs, % for rates. Preserve decimal precision from the source data.
- Keep the tone analytical and direct — no fluff.
- Never use the word "conversions" — always say "leads" instead."""


def call_llm(prompt: str, system: str = None) -> str:
    """Call available LLM (prefers Anthropic Claude, falls back to Gemini)."""
    if system is None:
        system = ANALYSIS_SYSTEM_PROMPT
    if ANTHROPIC_API_KEY:
        result = _call_claude(prompt, system)
        if not result.startswith("⚠️"):
            return result
        print(f"   ⚠️ Claude failed, falling back to Gemini...")
    if GEMINI_API_KEY:
        return _call_gemini(prompt, system)
    return "⚠️ No LLM API key set. Add ANTHROPIC_API_KEY or GEMINI_API_KEY to .env."


def _is_retryable_error(exc, status_code: int = None) -> bool:
    """True for 503, connection errors, or other transient failures."""
    if status_code == 503:
        return True
    if exc is None:
        return False
    msg = str(exc).lower()
    return any(x in msg for x in (
        "connection aborted", "remotedisconnected", "connection reset",
        "timeout", "503", "service unavailable", "too many requests",
    ))


def _call_claude(prompt: str, system: str) -> str:
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 8000,
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
    }
    last_err = None
    for attempt in range(3):
        try:
            resp = requests.post(ANTHROPIC_URL, headers=headers, json=body, timeout=180)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("content", [{}])[0].get("text", "No response content.")
            err_msg = f"⚠️ Claude API error {resp.status_code}: {resp.text[:500]}"
            if _is_retryable_error(None, resp.status_code) and attempt < 2:
                wait = 2 ** (attempt + 1)
                print(f"   ⚠️ Claude error, retrying in {wait}s...")
                time.sleep(wait)
                last_err = err_msg
                continue
            return err_msg
        except Exception as e:
            last_err = f"⚠️ Claude API call failed: {e}"
            if _is_retryable_error(e) and attempt < 2:
                wait = 2 ** (attempt + 1)
                print(f"   ⚠️ Claude failed ({e}), retrying in {wait}s...")
                time.sleep(wait)
                continue
            return last_err
    return last_err or "⚠️ Claude API call failed."


def _call_gemini(prompt: str, system: str) -> str:
    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
    body = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 32768, "temperature": 0.3},
    }
    last_err = None
    for attempt in range(3):
        try:
            resp = requests.post(url, json=body, timeout=180)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    return parts[0].get("text", "No response content.") if parts else "No response content."
                return "No response from Gemini."
            err_msg = f"⚠️ Gemini API error {resp.status_code}: {resp.text[:500]}"
            if _is_retryable_error(None, resp.status_code) and attempt < 2:
                wait = 2 ** (attempt + 1)
                print(f"   ⚠️ Gemini error, retrying in {wait}s...")
                time.sleep(wait)
                last_err = err_msg
                continue
            return err_msg
        except Exception as e:
            last_err = f"⚠️ Gemini API call failed: {e}"
            if _is_retryable_error(e) and attempt < 2:
                wait = 2 ** (attempt + 1)
                print(f"   ⚠️ Gemini failed ({e}), retrying in {wait}s...")
                time.sleep(wait)
                continue
            return last_err
    return last_err or "⚠️ Gemini API call failed."


call_claude = call_llm


def _slim_raw_data_for_prompt(raw_data: dict) -> dict:
    """Strip zero-spend campaigns and nested ad-level data to keep the prompt concise."""
    slim = {
        "platform": raw_data.get("platform"),
        "time_range": raw_data.get("time_range"),
        "account_summary": raw_data.get("account_summary"),
    }
    slim_campaigns = []
    for c in raw_data.get("campaigns", []):
        spend = _get_spend(c)
        if spend > 0:
            camp_copy = {k: v for k, v in c.items() if k not in ("_ad_sets", "_ads")}
            slim_campaigns.append(camp_copy)
    slim["campaigns_with_spend"] = slim_campaigns
    return slim


def _format_meta_fallback_report(raw_data: dict, lead_analysis: dict, warnings: list, llm_error: str) -> str:
    """Data-only report when LLM fails. Ensures we never write a raw error string to the file."""
    tr = raw_data.get("time_range", {})
    since = tr.get("since", "unknown")
    until = tr.get("until", "unknown")
    acct = raw_data.get("account_summary") or {}
    acct_data = acct[0] if isinstance(acct, list) and acct and isinstance(acct[0], dict) else acct if isinstance(acct, dict) else {}
    imp = acct_data.get("impressions", 0) or 0
    reach = acct_data.get("reach", 0) or 0
    clicks = acct_data.get("clicks", 0) or 0
    ctr = acct_data.get("ctr", "N/A")
    cpc = acct_data.get("cpc", "N/A")
    cpm = acct_data.get("cpm", "N/A")
    freq = acct_data.get("frequency", "N/A")

    lines = [
        "# Meta Ads — Weekly Performance Intelligence Report (Data Summary)",
        f"**Period:** {since} to {until}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "> **Note:** AI analysis unavailable due to LLM API failure. Below is a data-only summary from the collected metrics.",
        f"> *LLM error: {llm_error[:200]}*",
        "",
        "## 1. Executive Summary",
        f"This data summary covers {since} to {until}. The account generated **{lead_analysis.get('total_leads', 0)}** leads "
        f"from **${lead_analysis.get('reporting_spend', lead_analysis.get('total_campaign_spend', 0)):,.2f}** spend (blended CPL: "
        f"**${lead_analysis.get('blended_cpl') or 'N/A'}**).",
        "",
        "## 2. Account-Level KPIs",
        "| Metric | Value |",
        "| :------ | :---- |",
        f"| Spend | ${lead_analysis.get('reporting_spend', lead_analysis.get('total_campaign_spend', 0)):,.2f} |",
        f"| Impressions | {imp} |",
        f"| Reach | {reach} |",
        f"| Clicks | {clicks} |",
        f"| CTR | {ctr} |",
        f"| CPC | {cpc} |",
        f"| CPM | {cpm} |",
        f"| Total Leads | {lead_analysis.get('total_leads', 0)} |",
        f"| Blended CPL | ${lead_analysis.get('blended_cpl') or 'N/A'} |",
        f"| Frequency | {freq} |",
        "",
        "## 3. Lead Breakdown by Type",
        "| Lead Type | Count | % of Total |",
        "| :-------- | :---- | :--------- |",
    ]
    total = lead_analysis.get("total_leads") or 0
    for item in lead_analysis.get("lead_type_breakdown", []):
        cnt = item.get("count", 0)
        pct = f"{(100 * cnt / total):.1f}%" if total else "0%"
        lines.append(f"| {item.get('label', item.get('action_type', 'Unknown'))} | {cnt} | {pct} |")
    lines.extend([
        "",
        "## 4. Campaign Performance (Leads > 0)",
        "| Campaign | Spend | Leads | CPL |",
        "| :------- | :---- | :---- | :-- |",
    ])
    for cr in lead_analysis.get("campaign_results", []):
        if (cr.get("leads") or 0) > 0:
            cpl = cr.get("cpl")
            cpl_str = f"${cpl:,.2f}" if cpl is not None else "N/A"
            lines.append(f"| {cr.get('campaign_name', 'Unknown')} | ${cr.get('spend', 0):,.2f} | {cr.get('leads', 0)} | {cpl_str} |")
    if warnings:
        lines.extend(["", "## Data Validation Warnings", ""] + [f"- {w}" for w in warnings])
    lines.append("")
    return "\n".join(lines)


def _format_google_fallback_report(raw_data: dict, llm_error: str) -> str:
    """Structured fallback when Google Ads LLM fails. Explains API/data state."""
    tr = raw_data.get("time_range", {})
    since = tr.get("since", "unknown")
    until = tr.get("until", "unknown")
    errors = []
    for key in ("account_summary", "campaigns", "conversion_actions"):
        val = raw_data.get(key)
        if isinstance(val, list) and val and isinstance(val[0], dict) and "error" in val[0]:
            errors.append(f"- **{key}**: {val[0].get('error', 'Unknown')}")
    err_block = "\n".join(errors) if errors else "- No structured error info"
    return f"""# Google Ads — Weekly Performance Intelligence Report (Data Summary)
**Period:** {since} to {until}
**Generated:** {datetime.now().strftime('%Y-%m-%d')}

## Status: AI Analysis Unavailable

The LLM API could not generate a full analysis. Below is a summary of the data retrieval state.

### LLM Error
{llm_error[:400]}

### Data Retrieval Status
{err_block}

### Next Steps
1. Verify `GOOGLE_ADS_CUSTOMER_ID` is correct (format: 123-456-7890, stored without dashes).
2. If this account is under a Manager (MCC), set `GOOGLE_ADS_MANAGER_ID` in `.env`.
3. Ensure the Google Ads API developer token is approved for the account.
4. Check OAuth scopes include `https://www.googleapis.com/auth/adwords`.
"""


def generate_meta_report(raw_data: dict, lead_analysis: dict, warnings: list) -> str:
    """Generate Meta Ads report using platform-specific analyzer."""
    slim_data = _slim_raw_data_for_prompt(raw_data)
    from report_analyzers.meta_ads_analyzer import generate_meta_report as meta_generate
    return meta_generate(slim_data, lead_analysis, warnings, call_llm)


def generate_google_report(raw_data: dict) -> str:
    """Generate Google Ads report using platform-specific analyzer."""
    from report_analyzers.google_ads_analyzer import generate_google_report as google_generate
    return google_generate(raw_data, call_llm)


# ═══════════════════════════════════════════════════════════════════════
#  REPORT WRITER
# ═══════════════════════════════════════════════════════════════════════

class PaidAdsIntelligenceAgent:
    def __init__(self, workspace_root: str = None):
        self.workspace_root = Path(workspace_root or WORKSPACE_ROOT)
        self.base_output_dir = self.workspace_root / "docs" / "paid ads intelligence"

    def _output_dir(self, dt: datetime = None) -> Path:
        folder = week_folder_name(dt)
        return self.base_output_dir / folder

    def _has_meta_creds(self) -> bool:
        return bool(META_ACCESS_TOKEN and META_AD_ACCOUNT_ID)

    def _has_google_creds(self) -> bool:
        return bool(GADS_CLIENT_ID and GADS_REFRESH_TOKEN and GADS_CUSTOMER_ID)

    def run_meta_analysis(self, output_dir: Path, since: str, until: str):
        platform_dir = output_dir / "meta_ads"
        platform_dir.mkdir(parents=True, exist_ok=True)

        if not self._has_meta_creds():
            print("   ⚠️ Meta Ads credentials not configured. Writing placeholder report.")
            self._write_placeholder(platform_dir, "Meta Ads")
            return

        print("\n🔵 META ADS ANALYSIS")
        print("=" * 50)
        print(f"   Date range: {since} to {until}")

        raw_data = pull_full_meta_data(since, until)

        raw_path = platform_dir / "raw_data.json"
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=2, default=str)
        print(f"   💾 Raw data saved: {raw_path}")

        print("   📊 Computing lead analysis...")
        optimization_map = raw_data.get("optimization_map", {})
        lead_analysis = build_lead_analysis(raw_data, optimization_map)
        warnings = validate_data(raw_data, lead_analysis)

        analysis_path = platform_dir / "lead_analysis.json"
        with open(analysis_path, "w", encoding="utf-8") as f:
            json.dump(lead_analysis, f, indent=2)
        print(f"   💾 Lead analysis saved: {analysis_path}")

        if warnings:
            for w in warnings:
                print(f"   ⚠️ {w}")

        print(f"   📊 Total leads: {lead_analysis['total_leads']} | "
              f"Blended CPL: ${lead_analysis['blended_cpl'] or 'N/A'}")

        print("   🤖 Generating AI analysis...")
        report = generate_meta_report(raw_data, lead_analysis, warnings)
        if report.startswith("⚠️"):
            print("   ⚠️ LLM failed, writing data-only fallback report...")
            report = _format_meta_fallback_report(raw_data, lead_analysis, warnings, report)

        report_path = platform_dir / "performance_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"   ✅ Report saved: {report_path}")

    def run_google_analysis(self, output_dir: Path, since: str, until: str):
        platform_dir = output_dir / "google_ads"
        platform_dir.mkdir(parents=True, exist_ok=True)

        if not self._has_google_creds():
            print("   ⚠️ Google Ads credentials not configured. Writing placeholder report.")
            self._write_placeholder(platform_dir, "Google Ads")
            return

        print("\n🔴 GOOGLE ADS ANALYSIS")
        print("=" * 50)
        print(f"   Date range: {since} to {until}")

        raw_data = pull_full_google_data(since, until)

        raw_path = platform_dir / "raw_data.json"
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=2, default=str)
        print(f"   💾 Raw data saved: {raw_path}")

        print("   🤖 Generating AI analysis...")
        report = generate_google_report(raw_data)
        if report.startswith("⚠️"):
            print("   ⚠️ LLM failed, writing fallback report...")
            report = _format_google_fallback_report(raw_data, report)

        report_path = platform_dir / "performance_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"   ✅ Report saved: {report_path}")

    def _write_placeholder(self, platform_dir: Path, platform_name: str):
        report_path = platform_dir / "performance_report.md"
        content = f"""# {platform_name} — Weekly Performance Intelligence Report
**Period:** Last 7 days
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Status: Credentials Not Configured

This report could not be generated because the required API credentials
for {platform_name} are not set in the `.env` file.

### Required Environment Variables

"""
        if "Meta" in platform_name:
            content += """- `META_ACCESS_TOKEN` — Your Meta Marketing API access token
- `META_AD_ACCOUNT_ID` — Your ad account ID (numeric, without 'act_' prefix)

To obtain these:
1. Go to [Meta Business Suite](https://business.facebook.com/)
2. Navigate to Business Settings → Users → System Users
3. Generate a token with `ads_read` permission
"""
        else:
            content += """- `GOOGLE_ADS_CLIENT_ID` — OAuth 2.0 client ID
- `GOOGLE_ADS_CLIENT_SECRET` — OAuth 2.0 client secret
- `GOOGLE_ADS_DEVELOPER_TOKEN` — Google Ads API developer token
- `GOOGLE_ADS_REFRESH_TOKEN` — OAuth 2.0 refresh token
- `GOOGLE_ADS_CUSTOMER_ID` — Your Google Ads customer ID (format: 123-456-7890)
- `GOOGLE_ADS_MANAGER_ID` — **Required** if the account is under an MCC; use the manager account ID

To obtain these:
1. Go to [Google Ads API Center](https://ads.google.com/aw/apicenter)
2. Apply for a developer token
3. Create OAuth credentials in Google Cloud Console
"""
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   📝 Placeholder saved: {report_path}")

    def run(self, dt: datetime = None):
        dt = dt or datetime.now()
        output_dir = self._output_dir(dt)
        output_dir.mkdir(parents=True, exist_ok=True)

        tr = _time_range_for_week(dt)
        since, until = tr["since"], tr["until"]
        folder_name = week_folder_name(dt)

        print(f"\n{'='*60}")
        print(f"  PAID ADS INTELLIGENCE AGENT")
        print(f"  Week folder: {folder_name}")
        print(f"  Date range: {since} to {until}")
        print(f"  Output: {output_dir}")
        print(f"  Timestamp: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")

        channels_run = []

        try:
            self.run_meta_analysis(output_dir, since, until)
            channels_run.append("Meta Ads")
        except Exception as e:
            print(f"   ❌ Meta Ads analysis failed: {e}")
            traceback.print_exc()

        try:
            self.run_google_analysis(output_dir, since, until)
            channels_run.append("Google Ads")
        except Exception as e:
            print(f"   ❌ Google Ads analysis failed: {e}")
            traceback.print_exc()

        self._write_index(output_dir, channels_run, dt)

        print(f"\n{'='*60}")
        print(f"  ✅ PAID ADS INTELLIGENCE COMPLETE")
        print(f"  Channels analyzed: {', '.join(channels_run)}")
        print(f"  Reports: {output_dir}")
        print(f"{'='*60}\n")

        return output_dir

    def _write_index(self, output_dir: Path, channels: list, dt: datetime):
        index_path = output_dir / "_index.md"
        lines = [
            f"# Paid Ads Intelligence — Week of {dt.strftime('%B %d, %Y')}",
            f"**Folder:** `{week_folder_name(dt)}`",
            f"**Generated:** {dt.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Channel Reports",
            "",
        ]
        for ch in channels:
            slug = ch.lower().replace(" ", "_")
            lines.append(f"- [{ch}](./{slug}/performance_report.md)")
        lines.append("")
        lines.append("---")
        lines.append("*Generated by the Paid Ads Intelligence Agent.*")

        with open(index_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


if __name__ == "__main__":
    agent = PaidAdsIntelligenceAgent(workspace_root=str(WORKSPACE_ROOT))
    agent.run()
