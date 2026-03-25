from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from loaders import empty_daily_performance_frame


def normalize_meta_insights(raw_rows: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Normalize rows returned from the meta-ads MCP server into the shared
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
                "date": row.get("date_start") or row.get("date"),
                "platform": "meta",
                "ad_account_id": row.get("account_id"),
                "platform_campaign_id": row.get("campaign_id"),
                "campaign_name_raw": row.get("campaign_name"),
                "status_actual": row.get("status") or row.get("campaign_effective_status"),
                "spend": float(row.get("spend", 0.0) or 0.0),
                "impressions": int(row.get("impressions", 0) or 0),
                "clicks": int(row.get("clicks", 0) or 0),
                "leads": int(row.get("leads", 0) or row.get("actions_lead", 0) or 0),
                "revenue": float(row.get("revenue", 0.0) or 0.0),
            }
        )

    return pd.DataFrame.from_records(records)

