#!/usr/bin/env python3
"""
Centralized preflight checker for automation dependencies.

Checks:
- required env vars per automation
- key workspace path readability/writability

Usage:
  python preflight_automations.py
  python preflight_automations.py --automation 4
  python preflight_automations.py --strict
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

from automation_runtime import WORKSPACE_ROOT, emit_run_event, resolve_docs_path

load_dotenv(WORKSPACE_ROOT / ".env")

AUTOMATION_REQUIREMENTS = {
    "1": {
        "name": "Daily Content Pipeline Orchestrator",
        "env": ["AHREFS_API_KEY", "GSHEETS_CLIENT_EMAIL", "GSHEETS_PRIVATE_KEY"],
        "paths": [
            "docs/competitor content tracker/blogs",
            "docs/analytics_reports",
        ],
    },
    "2": {
        "name": "Weekly Content Execution + Repurposing Chain",
        "env": ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"],
        "paths": [
            "docs/blogs",
            "docs/content_assets/repurposed",
        ],
    },
    "3": {
        "name": "Monthly Competitive Ad Intelligence",
        "env": ["SCRAPECREATORS_API_KEY", "META_ACCESS_TOKEN"],
        "paths": ["docs/competitor content tracker/paid ads creatives"],
    },
    "4": {
        "name": "Weekly Ad Performance Dashboard",
        "env": [
            "META_ACCESS_TOKEN",
            "GOOGLE_ADS_CLIENT_ID",
            "GOOGLE_ADS_CLIENT_SECRET",
            "GOOGLE_ADS_DEVELOPER_TOKEN",
            "GOOGLE_ADS_REFRESH_TOKEN",
            "GOOGLE_ADS_CUSTOMER_ID",
            "GSHEETS_CLIENT_EMAIL",
            "GSHEETS_PRIVATE_KEY",
        ],
        "paths": ["docs/analytics_reports"],
    },
    "5": {
        "name": "Weekly SEO Intelligence Report",
        "env": ["AHREFS_API_KEY", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"],
        "paths": ["docs/analytics_reports", "docs/competitor content tracker/blogs"],
    },
    "6": {
        "name": "Bi-Weekly Advertiser Health Monitor",
        "env": ["META_ACCESS_TOKEN", "GOOGLE_ADS_CLIENT_ID", "ANTHROPIC_API_KEY"],
        "paths": ["data/advertiser_performance", "docs/advertiser_success/health_reports"],
    },
    "7": {
        "name": "Weekly Sales Intelligence Package",
        "env": ["AHREFS_API_KEY", "SCRAPECREATORS_API_KEY", "ANTHROPIC_API_KEY"],
        "paths": ["docs/sales_assets/prospect_lists", "docs/sales_assets/battlecards"],
    },
    "8": {
        "name": "Weekly CRO + Landing Page Audit",
        "env": ["AHREFS_API_KEY", "GEMINI_API_KEY"],
        "paths": ["docs/cro_reports", "docs/paid_ads_assets"],
    },
    "9": {
        "name": "Monthly GTM Execution Commander",
        "env": ["META_ACCESS_TOKEN", "GOOGLE_ADS_CLIENT_ID", "AHREFS_API_KEY"],
        "paths": ["docs/GTM playbook", "docs/competitor content tracker/blogs"],
    },
    "10": {
        "name": "Monthly Competitor Convergence Report",
        "env": ["SCRAPECREATORS_API_KEY", "AHREFS_API_KEY"],
        "paths": ["docs/competitor content tracker", "docs/paid_ads_assets"],
    },
}


def check_env(names: list[str]) -> list[str]:
    return [n for n in names if not os.environ.get(n, "").strip()]


def check_paths(paths: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for rel in paths:
        p = resolve_docs_path(rel) if rel.startswith("docs/") else (WORKSPACE_ROOT / rel)
        if p.exists():
            if p.is_dir() and os.access(p, os.W_OK):
                out[rel] = "ok"
            elif p.is_file() and os.access(p, os.R_OK):
                out[rel] = "ok"
            else:
                out[rel] = "exists_but_no_access"
        else:
            out[rel] = "missing"
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Preflight checker for all automations")
    parser.add_argument("--automation", help="Automation number 1-10 (optional)")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any missing env/path")
    parser.add_argument("--no-write-report", action="store_true", help="Do not write preflight report artifact")
    args = parser.parse_args()

    ids = [args.automation] if args.automation else sorted(AUTOMATION_REQUIREMENTS.keys(), key=lambda x: int(x))
    report = []
    strict_fail = False

    emit_run_event("preflight_automations", "started", details={"automation": args.automation or "all", "strict": args.strict})

    for aid in ids:
        req = AUTOMATION_REQUIREMENTS.get(aid)
        if not req:
            report.append({"automation": aid, "error": "unknown_automation_id"})
            strict_fail = True
            continue
        missing_env = check_env(req["env"])
        path_status = check_paths(req["paths"])
        any_bad_path = any(v != "ok" for v in path_status.values())
        ok = (not missing_env) and (not any_bad_path)
        if (missing_env or any_bad_path) and args.strict:
            strict_fail = True
        report.append(
            {
                "automation_id": aid,
                "automation_name": req["name"],
                "ok": ok,
                "missing_env": missing_env,
                "path_status": path_status,
            }
        )

    payload = {"workspace_root": str(WORKSPACE_ROOT), "results": report}
    print(json.dumps(payload, indent=2))

    if not args.no_write_report:
        out_dir = WORKSPACE_ROOT / "outputs" / "automation_runs"
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dated = out_dir / f"preflight_{ts}.json"
        latest = out_dir / "latest_preflight.json"
        dated.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        latest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    emit_run_event("preflight_automations", "success" if not strict_fail else "failed", details={"strict_fail": strict_fail})
    if strict_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
