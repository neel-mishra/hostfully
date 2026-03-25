#!/usr/bin/env python3
"""
Google Ads API wrapper for Cursor Automations.

Usage:
  python google_ads_api.py account-summary --date-range LAST_30_DAYS
  python google_ads_api.py campaigns --date-range LAST_7_DAYS
  python google_ads_api.py campaign-performance --id 12345 --date-range LAST_7_DAYS
  python google_ads_api.py keywords --campaign-id 12345 --date-range LAST_7_DAYS
  python google_ads_api.py conversions
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv
from automation_runtime import (
    emit_run_event,
    is_duplicate_success,
    logical_period_idempotency_key,
    preflight_env,
)

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

CLIENT_ID = os.environ.get("GOOGLE_ADS_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("GOOGLE_ADS_CLIENT_SECRET", "")
DEV_TOKEN = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN", "")
REFRESH_TOKEN = os.environ.get("GOOGLE_ADS_REFRESH_TOKEN", "")
CUSTOMER_ID = os.environ.get("GOOGLE_ADS_CUSTOMER_ID", "").replace("-", "")
MANAGER_ID = os.environ.get("GOOGLE_ADS_MANAGER_ID", "").replace("-", "")

GAQL_URL = f"https://googleads.googleapis.com/v18/customers/{CUSTOMER_ID}/googleAds:searchStream"


def get_access_token():
    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }, timeout=30)
    data = resp.json()
    if "access_token" not in data:
        print(json.dumps({"error": "Token refresh failed", "detail": data}))
        sys.exit(1)
    return data["access_token"]


def parse_date_range(range_str):
    today = datetime.now()
    ranges = {
        "LAST_7_DAYS": (today - timedelta(days=7), today - timedelta(days=1)),
        "LAST_14_DAYS": (today - timedelta(days=14), today - timedelta(days=1)),
        "LAST_30_DAYS": (today - timedelta(days=30), today - timedelta(days=1)),
        "LAST_90_DAYS": (today - timedelta(days=90), today - timedelta(days=1)),
        "THIS_MONTH": (today.replace(day=1), today),
        "LAST_MONTH": (
            (today.replace(day=1) - timedelta(days=1)).replace(day=1),
            today.replace(day=1) - timedelta(days=1),
        ),
    }
    if range_str in ranges:
        start, end = ranges[range_str]
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
    if ":" in range_str:
        parts = range_str.split(":")
        return parts[0], parts[1]
    return (today - timedelta(days=30)).strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")


def gaql_query(query):
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "developer-token": DEV_TOKEN,
        "Content-Type": "application/json",
    }
    if MANAGER_ID:
        headers["login-customer-id"] = MANAGER_ID

    resp = requests.post(GAQL_URL, headers=headers, json={"query": query}, timeout=60)
    if resp.status_code != 200:
        print(json.dumps({"error": f"HTTP {resp.status_code}", "body": resp.text[:1000]}))
        sys.exit(1)

    results = resp.json()
    all_rows = []
    for batch in results if isinstance(results, list) else [results]:
        for row in batch.get("results", []):
            all_rows.append(row)
    return all_rows


def cmd_account_summary(date_range):
    start, end = parse_date_range(date_range)
    rows = gaql_query(f"""
        SELECT metrics.impressions, metrics.clicks, metrics.ctr,
               metrics.average_cpc, metrics.cost_micros, metrics.conversions,
               metrics.cost_per_conversion
        FROM customer
        WHERE segments.date BETWEEN '{start}' AND '{end}'
    """)
    print(json.dumps(rows, indent=2))


def cmd_campaigns(date_range):
    start, end = parse_date_range(date_range)
    rows = gaql_query(f"""
        SELECT campaign.id, campaign.name, campaign.status,
               campaign.advertising_channel_type,
               metrics.impressions, metrics.clicks, metrics.ctr,
               metrics.average_cpc, metrics.cost_micros, metrics.conversions
        FROM campaign
        WHERE segments.date BETWEEN '{start}' AND '{end}'
          AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
        LIMIT 50
    """)
    print(json.dumps(rows, indent=2))


def cmd_campaign_performance(campaign_id, date_range):
    start, end = parse_date_range(date_range)
    rows = gaql_query(f"""
        SELECT campaign.id, campaign.name,
               metrics.impressions, metrics.clicks, metrics.ctr,
               metrics.average_cpc, metrics.cost_micros, metrics.conversions,
               metrics.cost_per_conversion, metrics.search_impression_share
        FROM campaign
        WHERE campaign.id = {campaign_id}
          AND segments.date BETWEEN '{start}' AND '{end}'
    """)
    print(json.dumps(rows, indent=2))


def cmd_keywords(campaign_id, date_range):
    start, end = parse_date_range(date_range)
    rows = gaql_query(f"""
        SELECT ad_group_criterion.keyword.text,
               ad_group_criterion.keyword.match_type,
               ad_group_criterion.quality_info.quality_score,
               metrics.impressions, metrics.clicks, metrics.ctr,
               metrics.average_cpc, metrics.cost_micros, metrics.conversions
        FROM keyword_view
        WHERE campaign.id = {campaign_id}
          AND segments.date BETWEEN '{start}' AND '{end}'
        ORDER BY metrics.impressions DESC
        LIMIT 50
    """)
    print(json.dumps(rows, indent=2))


def cmd_conversions():
    rows = gaql_query("""
        SELECT conversion_action.id, conversion_action.name,
               conversion_action.type, conversion_action.status,
               metrics.conversions, metrics.all_conversions
        FROM conversion_action
        ORDER BY metrics.conversions DESC
        LIMIT 50
    """)
    print(json.dumps(rows, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Google Ads API CLI")
    parser.add_argument("command", choices=[
        "account-summary", "campaigns", "campaign-performance", "keywords", "conversions"
    ])
    parser.add_argument("--date-range", default="LAST_30_DAYS")
    parser.add_argument("--id", help="Campaign ID")
    parser.add_argument("--campaign-id", help="Campaign ID (for keywords)")
    parser.add_argument("--idempotency-key", help="Optional idempotency key")
    parser.add_argument("--idempotency-granularity", choices=["day", "week", "month"], default="week")
    parser.add_argument("--allow-duplicate-run", action="store_true")
    args = parser.parse_args()

    idempotency_key = args.idempotency_key or logical_period_idempotency_key(
        "google_ads_api",
        granularity=args.idempotency_granularity,
        suffix=f"{args.command}:{args.date_range}:{args.id or args.campaign_id or ''}",
    )
    if (not args.allow_duplicate_run) and is_duplicate_success(idempotency_key):
        print(json.dumps({"status": "skipped", "reason": "idempotent_success", "idempotency_key": idempotency_key}))
        emit_run_event("google_ads_api", "skipped", step=args.command, idempotency_key=idempotency_key)
        return

    missing = preflight_env([
        "GOOGLE_ADS_CLIENT_ID",
        "GOOGLE_ADS_CLIENT_SECRET",
        "GOOGLE_ADS_DEVELOPER_TOKEN",
        "GOOGLE_ADS_REFRESH_TOKEN",
        "GOOGLE_ADS_CUSTOMER_ID",
    ])
    if missing:
        print(json.dumps({"error": "missing_env", "missing": missing}))
        emit_run_event("google_ads_api", "failed", step=args.command, idempotency_key=idempotency_key, details={"missing_env": missing})
        sys.exit(1)

    emit_run_event("google_ads_api", "started", step=args.command, idempotency_key=idempotency_key)

    if args.command == "account-summary":
        cmd_account_summary(args.date_range)
    elif args.command == "campaigns":
        cmd_campaigns(args.date_range)
    elif args.command == "campaign-performance":
        cmd_campaign_performance(args.id, args.date_range)
    elif args.command == "keywords":
        cmd_keywords(args.campaign_id, args.date_range)
    elif args.command == "conversions":
        cmd_conversions()
    emit_run_event("google_ads_api", "success", step=args.command, idempotency_key=idempotency_key)


if __name__ == "__main__":
    main()
