from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import re

from campaign_name_match import (
    best_match_against_candidates,
    canonical_campaign_match_key,
    exact_match_key,
)
from config import allocation_config


def _normalize_utm_campaign(v: object) -> str:
    s = str(v or "").strip()
    if not s or s.lower() == "brand":
        return ""
    # CRM naming issue: placeholders / numeric IDs represent PMAX opportunities.
    if s.lower() in {"{campaign_name}", "campaign_name"}:
        return "__PMAX_PLACEHOLDER__"
    if re.fullmatch(r"\d{4,}", s):
        return "__PMAX_PLACEHOLDER__"
    # HubSpot exports often suffix adset variants like " - 1".
    if " - " in s and s.rsplit(" - ", 1)[-1].isdigit():
        s = s.rsplit(" - ", 1)[0].strip()
    return s


def _parse_pipeline_report(path: str | Path) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=0, header=None)

    # Export header row is fixed in this report format.
    stage = raw.iloc[:, 1]
    utm_campaign = raw.iloc[:, 11]
    amount = raw.iloc[:, 13]
    lead_source = raw.iloc[:, 12]
    utm_source = raw.iloc[:, 10]

    df = pd.DataFrame(
        {
            "stage": stage,
            "utm_campaign": utm_campaign,
            "amount": amount,
            "lead_source": lead_source,
            "utm_source": utm_source,
        }
    )
    df["stage"] = df["stage"].ffill()
    df["utm_campaign"] = df["utm_campaign"].map(_normalize_utm_campaign)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df = df[df["utm_campaign"] != ""].copy()

    def platform_from_source(v: object) -> str:
        s = str(v or "").strip().lower()
        if "meta" in s or s in {"fb", "ig", "facebook"}:
            return "meta"
        if "google" in s:
            return "google"
        return ""

    df["platform"] = df["utm_source"].map(platform_from_source)
    df = df[df["platform"] != ""].copy()

    stage_norm = df["stage"].astype(str).str.lower().str.strip()
    closed_won = stage_norm.str.contains("closed won", na=False)
    # Include all funnel stages requested by user.
    stage_mask = stage_norm.str.contains(
        "pre-qualification|needs analysis|proposal|negotiation|verbal agreement|closed won|closed lost",
        na=False,
    )
    df["closed_won_amount"] = df["amount"].where(closed_won, 0.0)
    df["pipeline_amount"] = df["amount"].where(stage_mask, 0.0)
    df["sql_count"] = stage_mask.astype(float)

    g = (
        df.groupby(["platform", "utm_campaign"], dropna=False)[
            ["pipeline_amount", "closed_won_amount", "sql_count"]
        ]
        .sum()
        .reset_index()
    )
    # Closed won should dominate prioritization. This is used as allocation weight.
    g["roi_priority_weight"] = g["pipeline_amount"] + 2.0 * g["closed_won_amount"]
    g["_key_exact"] = g["utm_campaign"].map(exact_match_key)
    g["_key_canon"] = g["utm_campaign"].map(canonical_campaign_match_key)
    return g


def attach_pipeline_roi(merged_live: pd.DataFrame, report_path: Optional[str | Path]) -> pd.DataFrame:
    if merged_live is None or merged_live.empty or not report_path:
        out = merged_live.copy()
        if "roi_priority_weight" not in out.columns:
            out["roi_priority_weight"] = 0.0
            out["pipeline_amount"] = 0.0
            out["closed_won_amount"] = 0.0
            out["sql_count"] = 0.0
        return out

    parsed = _parse_pipeline_report(report_path)
    out = merged_live.copy()
    out["_pb_exact"] = out["campaign_id"].map(exact_match_key)
    out["_pb_canon"] = out["campaign_id"].map(canonical_campaign_match_key)
    out["_pl_exact"] = out["platform_campaign_name"].map(exact_match_key)
    out["_pl_canon"] = out["platform_campaign_name"].map(canonical_campaign_match_key)

    out["pipeline_amount"] = 0.0
    out["closed_won_amount"] = 0.0
    out["roi_priority_weight"] = 0.0
    out["sql_count"] = 0.0

    for idx, r in out.iterrows():
        plat = str(r.get("platform", "")).lower()
        sub = parsed[(parsed["platform"] == plat) & (parsed["utm_campaign"] != "__PMAX_PLACEHOLDER__")]
        if sub.empty:
            continue
        candidates = sub["utm_campaign"].astype(str).tolist()
        target = str(r.get("platform_campaign_name") or r.get("campaign_id") or "")
        mr = best_match_against_candidates(
            target,
            candidates,
            min_score=float(allocation_config.match_min_score),
            exact_weight=float(allocation_config.match_weight_exact),
            canonical_weight=float(allocation_config.match_weight_canonical),
            fuzzy_weight=float(allocation_config.match_weight_fuzzy),
        )
        if not mr.matched_name:
            continue
        hit = sub[sub["utm_campaign"].astype(str) == mr.matched_name]
        out.at[idx, "pipeline_amount"] = float(hit["pipeline_amount"].sum())
        out.at[idx, "closed_won_amount"] = float(hit["closed_won_amount"].sum())
        out.at[idx, "roi_priority_weight"] = float(hit["roi_priority_weight"].sum())
        out.at[idx, "sql_count"] = float(hit["sql_count"].sum())

    # Distribute unresolved PMAX placeholder opportunities across Google PMAX rows.
    pmax = parsed[
        (parsed["platform"] == "google") & (parsed["utm_campaign"] == "__PMAX_PLACEHOLDER__")
    ]
    if not pmax.empty:
        p_pipeline = float(pmax["pipeline_amount"].sum())
        p_closed = float(pmax["closed_won_amount"].sum())
        p_roi = float(pmax["roi_priority_weight"].sum())
        p_sql = float(pmax["sql_count"].sum())
        gmask = (out["platform"].astype(str).str.lower() == "google") & (
            out["campaign_id"].astype(str).str.lower().str.contains("pmax")
            | out["platform_campaign_name"].astype(str).str.lower().str.contains("pmax")
        )
        gsub = out.loc[gmask]
        if not gsub.empty and p_roi > 0:
            spend = pd.to_numeric(gsub["spend_mtd"], errors="coerce").fillna(0.0)
            if float(spend.sum()) > 0:
                share = spend / float(spend.sum())
            else:
                cur = pd.to_numeric(gsub["current_daily_budget"], errors="coerce").fillna(0.0)
                if float(cur.sum()) > 0:
                    share = cur / float(cur.sum())
                else:
                    share = pd.Series(1.0 / len(gsub), index=gsub.index)
            out.loc[gsub.index, "pipeline_amount"] += share * p_pipeline
            out.loc[gsub.index, "closed_won_amount"] += share * p_closed
            out.loc[gsub.index, "roi_priority_weight"] += share * p_roi
            out.loc[gsub.index, "sql_count"] += share * p_sql

    return out.drop(columns=["_pb_exact", "_pb_canon", "_pl_exact", "_pl_canon"], errors="ignore")
