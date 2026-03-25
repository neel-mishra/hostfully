from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from loaders import empty_daily_performance_frame


def normalize_google_rows(raw_rows: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Normalize rows returned from the google_ads_mcp server into the shared
    daily_performance schema.

    This function does not call the MCP server directly; it only converts
    already-fetched records into the canonical shape.
    """
    if not raw_rows:
        return empty_daily_performance_frame()

    records: List[Dict[str, Any]] = []
    for row in raw_rows:
        records.append(
            {
                "date": row.get("date") or row.get("segments_date"),
                "platform": "google",
                "ad_account_id": row.get("customer_id"),
                "platform_campaign_id": row.get("campaign_id"),
                "campaign_name_raw": row.get("campaign_name"),
                "status_actual": row.get("campaign_status"),
                "spend": float(row.get("spend", 0.0) or row.get("metrics_cost_micros", 0.0)) / (
                    1_000_000 if "metrics_cost_micros" in row else 1.0
                ),
                "impressions": int(row.get("impressions", 0) or row.get("metrics_impressions", 0) or 0),
                "clicks": int(row.get("clicks", 0) or row.get("metrics_clicks", 0) or 0),
                "leads": int(row.get("leads", 0) or row.get("conversions", 0) or row.get("metrics_conversions", 0) or 0),
                "revenue": float(row.get("revenue", 0.0) or 0.0),
            }
        )

    return pd.DataFrame.from_records(records)

