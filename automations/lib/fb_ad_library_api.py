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

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

API_KEY = os.environ.get("SCRAPECREATORS_API_KEY", "")
BASE_URL = "https://api.scrapecreators.com/v1"


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
    data = api_get("facebook/adLibrary/search/companies", {"query": brand_name})
    results = data.get("data", data.get("searchResults", data.get("results", [])))
    print(json.dumps(results, indent=2))
    return results


def cmd_ads(platform_id, limit=50):
    data = api_get("facebook/adLibrary/company/ads", {
        "companyName": platform_id,
        "country": "US",
        "trim": "true",
    })
    ads = data.get("data", data.get("ads", data.get("results", [])))
    if limit and isinstance(ads, list):
        ads = ads[:limit]
    print(json.dumps(ads, indent=2))
    return ads


def cmd_full(brand_name, limit=30):
    """Pull all ads for a brand directly via the company ads endpoint."""
    data = api_get("facebook/adLibrary/company/ads", {
        "companyName": brand_name,
        "country": "US",
        "trim": "true",
    })
    ads = data.get("data", data.get("ads", data.get("results", [])))
    if isinstance(ads, list) and limit:
        ads = ads[:limit]

    print(json.dumps({
        "brand": brand_name,
        "ad_count": len(ads) if isinstance(ads, list) else 0,
        "ads": ads,
    }, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Meta Ad Library (ScrapeCreators) API CLI")
    parser.add_argument("command", choices=["search", "ads", "full"])
    parser.add_argument("--brand", help="Brand/company name to search")
    parser.add_argument("--platform-id", help="Meta platform ID")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args.brand)
    elif args.command == "ads":
        cmd_ads(args.platform_id, args.limit)
    elif args.command == "full":
        cmd_full(args.brand, args.limit)


if __name__ == "__main__":
    main()
