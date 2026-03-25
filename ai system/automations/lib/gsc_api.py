#!/usr/bin/env python3
"""
Google Search Console API wrapper for automations and scripts.

Uses the same credentials as search_ranking_agent.py and other GSC consumers:
  GSC_SITE_URL, GOOGLE_APPLICATION_CREDENTIALS (path to service account JSON)

Usage:
  python gsc_api.py search-analytics --start-date 2026-02-01 --end-date 2026-03-10
  python gsc_api.py search-analytics --start-date 2026-02-01 --end-date 2026-03-10 --dimensions page --limit 100
  python gsc_api.py sitemaps-list
  python gsc_api.py sitemap-urls
  python gsc_api.py sitemap-urls --sitemap https://tldr.tech/sitemap.xml
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from automation_runtime import (
    emit_run_event,
    is_duplicate_success,
    logical_period_idempotency_key,
    preflight_env,
)

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

GSC_SITE_URL = os.environ.get("GSC_SITE_URL", "").strip()
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip()


def _get_client():
    """Build Search Console API client. Returns (service, error_message)."""
    if not GSC_SITE_URL:
        return None, "GSC_SITE_URL not set in .env"
    if not GOOGLE_APPLICATION_CREDENTIALS or not os.path.isfile(GOOGLE_APPLICATION_CREDENTIALS):
        return None, "GOOGLE_APPLICATION_CREDENTIALS not set or file not found"
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
        creds = service_account.Credentials.from_service_account_file(
            GOOGLE_APPLICATION_CREDENTIALS, scopes=scopes
        )
        service = build("searchconsole", "v1", credentials=creds)
        return service, None
    except ImportError as e:
        return None, f"Missing dependency: {e}"
    except Exception as e:
        return None, str(e)


def cmd_search_analytics(start_date: str, end_date: str, dimensions: list, limit: int) -> None:
    service, err = _get_client()
    if err:
        print(json.dumps({"error": err, "source": "gsc_api"}), file=sys.stderr)
        sys.exit(1)
    try:
        request = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": dimensions,
            "rowLimit": min(limit, 25000),
        }
        response = service.searchanalytics().query(siteUrl=GSC_SITE_URL, body=request).execute()
        rows = []
        for row in response.get("rows", []):
            keys = row.get("keys", [])
            out = {
                "clicks": row.get("clicks", 0),
                "impressions": row.get("impressions", 0),
                "ctr": row.get("ctr", 0),
                "position": row.get("position", 0),
            }
            for i, dim in enumerate(dimensions):
                if i < len(keys):
                    out[dim] = keys[i]
            rows.append(out)
        print(json.dumps({"siteUrl": GSC_SITE_URL, "startDate": start_date, "endDate": end_date, "rows": rows}))
    except Exception as e:
        print(json.dumps({"error": str(e), "source": "gsc_api"}), file=sys.stderr)
        sys.exit(1)


def cmd_sitemaps_list() -> None:
    service, err = _get_client()
    if err:
        print(json.dumps({"error": err, "source": "gsc_api"}), file=sys.stderr)
        sys.exit(1)
    try:
        response = service.sitemaps().list(siteUrl=GSC_SITE_URL).execute()
        sitemaps = response.get("sitemap", [])
        out = [{"path": s.get("path"), "type": s.get("type"), "isSitemapsIndex": s.get("isSitemapsIndex")} for s in sitemaps]
        print(json.dumps({"siteUrl": GSC_SITE_URL, "sitemaps": out}))
    except Exception as e:
        print(json.dumps({"error": str(e), "source": "gsc_api"}), file=sys.stderr)
        sys.exit(1)


def _fetch_urls_from_sitemap_xml(url: str) -> list:
    """Fetch sitemap URL and parse <loc> URLs. Handles sitemap index (nested <sitemap><loc>)."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; GSC-automation)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        xml = resp.read().decode("utf-8", errors="ignore")
    # Sitemap index: <sitemap><loc>URL</loc></sitemap>
    sitemap_locs = re.findall(r"<sitemap>\s*<loc>\s*([^<]+)\s*</loc>", xml, re.I)
    if sitemap_locs:
        urls = []
        for child in sitemap_locs:
            urls.extend(_fetch_urls_from_sitemap_xml(child.strip()))
        return urls
    # URL set: <url><loc>URL</loc></url>
    return re.findall(r"<url>\s*<loc>\s*([^<]+)\s*</loc>", xml, re.I) or re.findall(r"<loc>\s*([^<]+)\s*</loc>", xml, re.I)


def cmd_sitemap_urls(sitemap_url: str | None) -> None:
    """Output JSON array of URLs. If sitemap_url not given, use GSC sitemaps list or default."""
    if sitemap_url:
        urls = _fetch_urls_from_sitemap_xml(sitemap_url)
        print(json.dumps({"source": "sitemap_url", "url": sitemap_url, "urls": urls}))
        return
    service, err = _get_client()
    if err:
        # Fallback: derive default sitemap from GSC_SITE_URL
        if GSC_SITE_URL:
            base = GSC_SITE_URL.rstrip("/")
            default_sitemap = f"{base}/sitemap.xml"
            urls = _fetch_urls_from_sitemap_xml(default_sitemap)
            print(json.dumps({"source": "default_sitemap", "url": default_sitemap, "urls": urls}))
            return
        print(json.dumps({"error": err, "source": "gsc_api"}), file=sys.stderr)
        sys.exit(1)
    try:
        response = service.sitemaps().list(siteUrl=GSC_SITE_URL).execute()
        sitemaps = response.get("sitemap", [])
        if not sitemaps:
            print(json.dumps({"siteUrl": GSC_SITE_URL, "urls": [], "note": "No sitemaps in GSC"}))
            return
        all_urls = []
        for s in sitemaps[:5]:  # limit to first 5 to avoid huge fetch
            path = s.get("path")
            if not path:
                continue
            all_urls.extend(_fetch_urls_from_sitemap_xml(path))
        all_urls = list(dict.fromkeys(all_urls))
        print(json.dumps({"siteUrl": GSC_SITE_URL, "source": "gsc_sitemaps_list", "urls": all_urls}))
    except Exception as e:
        if GSC_SITE_URL:
            base = GSC_SITE_URL.rstrip("/")
            default_sitemap = f"{base}/sitemap.xml"
            urls = _fetch_urls_from_sitemap_xml(default_sitemap)
            print(json.dumps({"source": "fallback_sitemap", "url": default_sitemap, "urls": urls}))
            return
        print(json.dumps({"error": str(e), "source": "gsc_api"}), file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Google Search Console API wrapper")
    sub = parser.add_subparsers(dest="command", required=True)

    # search-analytics
    p_sa = sub.add_parser("search-analytics", help="Query search analytics (query, page, date)")
    p_sa.add_argument("--start-date", required=True, help="Start date YYYY-MM-DD")
    p_sa.add_argument("--end-date", required=True, help="End date YYYY-MM-DD")
    p_sa.add_argument("--dimensions", default="query,page", help="Comma-separated: query, page, date")
    p_sa.add_argument("--limit", type=int, default=500, help="Row limit (max 25000)")

    # sitemaps-list
    sub.add_parser("sitemaps-list", help="List sitemaps for the property")

    # sitemap-urls
    p_su = sub.add_parser("sitemap-urls", help="Get URL list from sitemap(s)")
    p_su.add_argument("--sitemap", default=None, help="Sitemap URL (optional; else use GSC list or default)")
    parser.add_argument("--idempotency-key", help="Optional idempotency key")
    parser.add_argument("--idempotency-granularity", choices=["day", "week", "month"], default="day")
    parser.add_argument("--allow-duplicate-run", action="store_true")

    args = parser.parse_args()

    idempotency_key = args.idempotency_key or logical_period_idempotency_key(
        "gsc_api",
        granularity=args.idempotency_granularity,
        suffix=f"{args.command}:{getattr(args, 'start_date', '')}:{getattr(args, 'end_date', '')}:{getattr(args, 'sitemap', '')}",
    )
    if (not args.allow_duplicate_run) and is_duplicate_success(idempotency_key):
        print(json.dumps({"status": "skipped", "reason": "idempotent_success", "idempotency_key": idempotency_key}))
        emit_run_event("gsc_api", "skipped", step=args.command, idempotency_key=idempotency_key)
        return

    # only require credentials when calling search analytics or explicit GSC sitemap list
    if args.command in {"search-analytics", "sitemaps-list"}:
        missing = preflight_env(["GSC_SITE_URL", "GOOGLE_APPLICATION_CREDENTIALS"])
        if missing:
            print(json.dumps({"error": "missing_env", "missing": missing}))
            emit_run_event("gsc_api", "failed", step=args.command, idempotency_key=idempotency_key, details={"missing_env": missing})
            sys.exit(1)

    emit_run_event("gsc_api", "started", step=args.command, idempotency_key=idempotency_key)

    if args.command == "search-analytics":
        dims = [d.strip() for d in args.dimensions.split(",") if d.strip()]
        cmd_search_analytics(args.start_date, args.end_date, dims, args.limit)
    elif args.command == "sitemaps-list":
        cmd_sitemaps_list()
    elif args.command == "sitemap-urls":
        cmd_sitemap_urls(args.sitemap)
    else:
        parser.print_help()
        sys.exit(1)
    emit_run_event("gsc_api", "success", step=args.command, idempotency_key=idempotency_key)


if __name__ == "__main__":
    main()
