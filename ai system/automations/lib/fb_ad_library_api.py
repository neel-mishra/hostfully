#!/usr/bin/env python3
"""
Meta Ad Library (ScrapeCreators) API wrapper for Cursor Automations.

Usage:
  python fb_ad_library_api.py search --brand "Morning Brew"
  python fb_ad_library_api.py ads --platform-id 12345 --limit 50
  python fb_ad_library_api.py full --brand "Morning Brew" --limit 30
"""

import argparse
import json
import os
import sys
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

API_KEY = os.environ.get("SCRAPECREATORS_API_KEY", "")
BASE_URL = "https://api.scrapecreators.com/v2"


def api_get(endpoint, params=None):
    if not API_KEY:
        print(json.dumps({"error": "SCRAPECREATORS_API_KEY not set"}))
        sys.exit(1)

    resp = requests.get(
        f"{BASE_URL}/{endpoint}",
        headers={"x-api-key": API_KEY},
        params=params or {},
        timeout=60,
    )
    if resp.status_code != 200:
        print(json.dumps({"error": f"HTTP {resp.status_code}", "body": resp.text[:500]}))
        sys.exit(1)
    return resp.json()


def cmd_search(brand_name):
    data = api_get("meta-ad-library/search-page", {"query": brand_name})
    results = data.get("data", data.get("results", []))
    print(json.dumps(results, indent=2))
    return results


def cmd_ads(platform_id, limit=50):
    data = api_get("meta-ad-library/ads", {"platform_id": platform_id, "limit": limit})
    ads = data.get("data", data.get("ads", data.get("results", [])))
    print(json.dumps(ads, indent=2))
    return ads


def cmd_full(brand_name, limit=30):
    """Search for brand, then pull ads for the first result."""
    search_data = api_get("meta-ad-library/search-page", {"query": brand_name})
    pages = search_data.get("data", search_data.get("results", []))

    if not pages:
        print(json.dumps({"brand": brand_name, "platform_id": None, "ads": [], "message": "No pages found"}))
        return

    page = pages[0]
    platform_id = page.get("id") or page.get("page_id") or page.get("platform_id", "")
    page_name = page.get("name", brand_name)

    if not platform_id:
        print(json.dumps({"brand": brand_name, "platform_id": None, "ads": [], "message": "No platform ID found"}))
        return

    ads_data = api_get("meta-ad-library/ads", {"platform_id": platform_id, "limit": limit})
    ads = ads_data.get("data", ads_data.get("ads", ads_data.get("results", [])))

    print(json.dumps({
        "brand": brand_name,
        "page_name": page_name,
        "platform_id": platform_id,
        "ad_count": len(ads),
        "ads": ads,
    }, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Meta Ad Library (ScrapeCreators) API CLI")
    parser.add_argument("command", choices=["search", "ads", "full"])
    parser.add_argument("--brand", help="Brand/company name to search")
    parser.add_argument("--platform-id", help="Meta platform ID")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--idempotency-key", help="Optional idempotency key")
    parser.add_argument("--idempotency-granularity", choices=["day", "week", "month"], default="week")
    parser.add_argument("--allow-duplicate-run", action="store_true")
    args = parser.parse_args()

    idempotency_key = args.idempotency_key or logical_period_idempotency_key(
        "fb_ad_library_api",
        granularity=args.idempotency_granularity,
        suffix=f"{args.command}:{args.brand or args.platform_id or ''}:{args.limit}",
    )
    if (not args.allow_duplicate_run) and is_duplicate_success(idempotency_key):
        print(json.dumps({"status": "skipped", "reason": "idempotent_success", "idempotency_key": idempotency_key}))
        emit_run_event("fb_ad_library_api", "skipped", step=args.command, idempotency_key=idempotency_key)
        return

    missing = preflight_env(["SCRAPECREATORS_API_KEY"])
    if missing:
        print(json.dumps({"error": "missing_env", "missing": missing}))
        emit_run_event("fb_ad_library_api", "failed", step=args.command, idempotency_key=idempotency_key, details={"missing_env": missing})
        sys.exit(1)

    emit_run_event("fb_ad_library_api", "started", step=args.command, idempotency_key=idempotency_key)

    if args.command == "search":
        cmd_search(args.brand)
    elif args.command == "ads":
        cmd_ads(args.platform_id, args.limit)
    elif args.command == "full":
        cmd_full(args.brand, args.limit)
    emit_run_event("fb_ad_library_api", "success", step=args.command, idempotency_key=idempotency_key)


if __name__ == "__main__":
    main()
