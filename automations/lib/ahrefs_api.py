#!/usr/bin/env python3
"""
Ahrefs REST API v3 wrapper for Cursor Automations.

Usage:
  python ahrefs_api.py organic-keywords --target tldr.tech --date 2026-03-10
  python ahrefs_api.py top-pages --target tldr.tech --date 2026-03-10
  python ahrefs_api.py metrics-history --target tldr.tech --date-from 2025-12-01
  python ahrefs_api.py organic-competitors --target tldr.tech --country us --date 2026-03-10
  python ahrefs_api.py domain-rating --target tldr.tech --date 2026-03-10
  python ahrefs_api.py paid-pages --target tldr.tech --date 2026-03-10
  python ahrefs_api.py keywords-overview --country us --keywords "newsletter advertising,tech newsletter"
  python ahrefs_api.py keywords-matching --country us --keywords "newsletter advertising"
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

BASE_URL = "https://api.ahrefs.com/v3"
API_KEY = os.environ.get("AHREFS_API_KEY", "")

DEFAULT_SELECT = {
    "organic-keywords": ["keyword", "volume", "position", "traffic", "difficulty", "url"],
    "top-pages": ["url", "traffic", "keywords", "top_keyword", "position"],
    "organic-competitors": ["domain", "common_keywords", "keywords", "traffic"],
    "paid-pages": ["url", "traffic", "keywords", "top_keyword"],
    "domain-rating": ["domain_rating", "ahrefs_rank"],
    "keywords-overview": ["keyword", "volume", "difficulty", "cpc"],
    "keywords-matching": ["keyword", "volume", "difficulty"],
}

ENDPOINT_MAP = {
    "organic-keywords": "/site-explorer/organic-keywords",
    "top-pages": "/site-explorer/top-pages",
    "metrics-history": "/site-explorer/metrics-history",
    "organic-competitors": "/site-explorer/organic-competitors",
    "domain-rating": "/site-explorer/domain-rating",
    "domain-rating-history": "/site-explorer/domain-rating-history",
    "paid-pages": "/site-explorer/paid-pages",
    "metrics": "/site-explorer/metrics",
    "keywords-overview": "/keywords-explorer/overview",
    "keywords-matching": "/keywords-explorer/matching-terms",
    "pages-by-traffic": "/site-explorer/pages-by-traffic",
    "backlinks-stats": "/site-explorer/backlinks-stats",
}


def call_ahrefs(endpoint, params):
    if not API_KEY:
        print(json.dumps({"error": "AHREFS_API_KEY not set"}))
        sys.exit(1)

    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}

    resp = requests.get(url, headers=headers, params=params, timeout=60)
    if resp.status_code != 200:
        print(json.dumps({"error": f"HTTP {resp.status_code}", "body": resp.text[:500]}))
        sys.exit(1)

    print(json.dumps(resp.json(), indent=2))


def main():
    parser = argparse.ArgumentParser(description="Ahrefs API v3 CLI")
    parser.add_argument("command", choices=list(ENDPOINT_MAP.keys()))
    parser.add_argument("--target", help="Target domain/URL")
    parser.add_argument("--date", help="Date YYYY-MM-DD")
    parser.add_argument("--date-from", help="Start date for history endpoints")
    parser.add_argument("--country", default="us")
    parser.add_argument("--keywords", help="Comma-separated keywords (for keywords-explorer)")
    parser.add_argument("--select", help="Comma-separated fields to select")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    endpoint = ENDPOINT_MAP[args.command]
    params = {"limit": args.limit, "output": "json"}

    if args.target:
        params["target"] = args.target
    if args.date:
        params["date"] = args.date
    if args.date_from:
        params["date_from"] = args.date_from
    if args.country:
        params["country"] = args.country

    select_fields = args.select.split(",") if args.select else DEFAULT_SELECT.get(args.command)
    if select_fields:
        params["select"] = ",".join(select_fields)

    if args.keywords:
        kw_list = [k.strip() for k in args.keywords.split(",")]
        if args.command in ("keywords-overview", "keywords-matching"):
            params["keywords"] = ",".join(kw_list)

    call_ahrefs(endpoint, params)


if __name__ == "__main__":
    main()
