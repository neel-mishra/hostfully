"""
Pull live Meta + Google campaign budgets and MTD performance for the budget tracker.

Uses the same API stack as `paid_ads_intelligence_agent.py` (Graph API + Google Ads GAQL),
which aligns with what the Meta MCP and `google_ads_mcp` server use under the hood.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from campaign_name_match import canonical_campaign_match_key, exact_match_key
from config import load_env_files, workspace_root


def platform_channel_totals(live_full: pd.DataFrame, platform: str) -> tuple[float, float]:
    """
    Sum spend_mtd and current_daily_budget for that platform in the raw live pull.

    - **Spend MTD**: sum of all rows (includes paused campaigns that spent earlier in the month).
    - **Daily budget (pacing Σ)**: sum intended for ``F = S + b_sum * d_rem`` — only **live**
      campaigns (Meta: ACTIVE; Google: ENABLED), **deduped** so we do not double-count:
      - **Google**: multiple campaigns can reference the same ``campaign_budget`` resource; we
        count each budget resource once.
      - **Meta**: duplicate ``platform_campaign_id`` rows (e.g. pagination quirks) are counted once.
    """
    if live_full is None or live_full.empty or "platform" not in live_full.columns:
        return 0.0, 0.0
    plat = str(platform).lower()
    m = live_full["platform"].astype(str).str.lower() == plat
    sub = live_full.loc[m]
    if sub.empty:
        return 0.0, 0.0
    spend = float(sub["spend_mtd"].sum())

    daily_sub = sub
    if "is_live" in daily_sub.columns:
        daily_sub = daily_sub[daily_sub["is_live"].fillna(False).astype(bool)]
    if daily_sub.empty or "current_daily_budget" not in daily_sub.columns:
        return spend, 0.0

    if plat == "google" and "campaign_budget_id" in daily_sub.columns:
        ids = daily_sub["campaign_budget_id"].astype(str).str.strip()
        nonempty = ids != ""
        if nonempty.any():
            tmp = daily_sub.loc[nonempty].drop_duplicates(subset=["campaign_budget_id"], keep="first")
            daily = float(tmp["current_daily_budget"].sum())
        elif "platform_campaign_id" in daily_sub.columns:
            tmp = daily_sub.drop_duplicates(subset=["platform_campaign_id"], keep="first")
            daily = float(tmp["current_daily_budget"].sum())
        else:
            daily = float(daily_sub["current_daily_budget"].sum())
    elif plat == "meta" and "platform_campaign_id" in daily_sub.columns:
        tmp = daily_sub.drop_duplicates(subset=["platform_campaign_id"], keep="first")
        daily = float(tmp["current_daily_budget"].sum())
    else:
        daily = float(daily_sub["current_daily_budget"].sum())
    return spend, daily


def _agent_dir() -> Path:
    return workspace_root() / "ai system" / "python scripts" / "paid ads intelligence agent"


def _ensure_agent_importable() -> None:
    root = workspace_root()
    agent = _agent_dir()
    for p in (root, agent, root / "automations" / "lib"):
        s = str(p)
        if s not in sys.path:
            sys.path.insert(0, s)
    load_env_files()


def _month_bounds(as_of: date) -> tuple[str, str]:
    start = as_of.replace(day=1)
    return start.isoformat(), as_of.isoformat()


def _meta_leads_from_insight(ins: Optional[dict]) -> float:
    if not ins or not isinstance(ins, dict):
        return 0.0
    for a in ins.get("actions") or []:
        if isinstance(a, dict) and a.get("action_type") == "lead":
            try:
                return float(a.get("value", 0))
            except (TypeError, ValueError):
                return 0.0
    try:
        return float(ins.get("conversions", 0) or 0)
    except (TypeError, ValueError):
        return 0.0


def _meta_float(ins: Optional[dict], key: str) -> float:
    if not ins or not isinstance(ins, dict):
        return 0.0
    try:
        return float(ins.get(key, 0) or 0)
    except (TypeError, ValueError):
        return 0.0


def _meta_is_live(camp: dict) -> bool:
    st = (camp.get("status") or "").upper()
    eff = (camp.get("effective_status") or camp.get("effectiveStatus") or "").upper()
    return st == "ACTIVE" or eff == "ACTIVE"


def fetch_meta_snapshot_rows(since: str, until: str) -> List[Dict[str, Any]]:
    _ensure_agent_importable()
    import paid_ads_intelligence_agent as pa  # noqa: WPS433

    if not pa.META_ACCESS_TOKEN or not pa.META_AD_ACCOUNT_ID:
        raise RuntimeError(
            "Meta not configured: set META_ACCESS_TOKEN and META_AD_ACCOUNT_ID in .env"
        )

    raw = pa.fetch_meta_campaigns(since, until)
    camps = raw.get("data", []) if isinstance(raw, dict) else []
    while isinstance(raw, dict) and raw.get("paging", {}).get("next"):
        try:
            import requests

            r = requests.get(raw["paging"]["next"], timeout=60)
            raw = r.json()
            camps.extend(raw.get("data", []))
        except Exception:
            break

    rows: List[Dict[str, Any]] = []
    for camp in camps:
        cid = str(camp.get("id", ""))
        name = (camp.get("name") or "").strip()
        camp_insights = pa.meta_get(
            f"{cid}/insights",
            {
                "fields": pa.INSIGHT_FIELDS,
                "time_range": pa._make_time_range_param(since, until),
            },
        )
        # Sum all rows + follow paging — Meta often returns daily breakdown and/or paginated data;
        # using only data[0] undercounts March MTD vs Ads Manager.
        ci_rows = pa.meta_insights_collect_all_pages(camp_insights)
        ins: dict = pa.meta_aggregate_insight_rows(ci_rows) if ci_rows else {}

        spend = 0.0
        try:
            spend = float(ins.get("spend", 0) or 0)
        except (TypeError, ValueError):
            pass

        daily_raw = camp.get("daily_budget")
        daily = 0.0
        if daily_raw is not None:
            try:
                daily = float(daily_raw) / 100.0  # Meta uses cents
            except (TypeError, ValueError):
                daily = 0.0

        rows.append(
            {
                "campaign_id": name,
                "platform": "meta",
                "platform_campaign_id": cid,
                "current_daily_budget": daily,
                "spend_mtd": spend,
                "leads_mtd": _meta_leads_from_insight(ins),
                "clicks_mtd": _meta_float(ins, "clicks"),
                "impressions_mtd": _meta_float(ins, "impressions"),
                "is_live": _meta_is_live(camp),
            }
        )
    return rows


def _gaql_first_error(rows: List[dict]) -> Optional[str]:
    """If GAQL returned only an error payload, surface it (otherwise silent empty pull)."""
    if not rows:
        return None
    if len(rows) == 1 and isinstance(rows[0], dict) and rows[0].get("error"):
        return str(rows[0]["error"])
    return None


def _agg_google_metrics(
    rows: List[dict],
) -> tuple[Dict[str, float], Dict[str, float], Dict[str, float], Dict[str, float]]:
    spend: Dict[str, float] = {}
    conv: Dict[str, float] = {}
    clicks: Dict[str, float] = {}
    impressions: Dict[str, float] = {}
    for r in rows:
        if not isinstance(r, dict) or "error" in r:
            continue
        camp = r.get("campaign") or {}
        met = r.get("metrics") or {}
        cid = str(camp.get("id", ""))
        micros = met.get("costMicros") or met.get("cost_micros") or 0
        try:
            spend[cid] = spend.get(cid, 0.0) + float(micros) / 1_000_000.0
        except (TypeError, ValueError):
            pass
        try:
            conv[cid] = conv.get(cid, 0.0) + float(met.get("conversions", 0) or 0)
        except (TypeError, ValueError):
            pass
        try:
            clicks[cid] = clicks.get(cid, 0.0) + float(met.get("clicks", 0) or 0)
        except (TypeError, ValueError):
            pass
        try:
            impressions[cid] = impressions.get(cid, 0.0) + float(met.get("impressions", 0) or 0)
        except (TypeError, ValueError):
            pass
    return spend, conv, clicks, impressions


def fetch_google_snapshot_rows(since: str, until: str) -> List[Dict[str, Any]]:
    _ensure_agent_importable()
    import paid_ads_intelligence_agent as pa  # noqa: WPS433

    if not pa.GADS_CUSTOMER_ID or not pa.GADS_DEV_TOKEN:
        raise RuntimeError(
            "Google Ads not configured: set GOOGLE_ADS_CUSTOMER_ID, GOOGLE_ADS_DEVELOPER_TOKEN, "
            "and OAuth vars in .env (same as google_ads_mcp / intelligence agent)"
        )

    spend_q = f"""
        SELECT campaign.id, campaign.name, campaign.status,
               metrics.cost_micros, metrics.conversions, metrics.clicks, metrics.impressions
        FROM campaign
        WHERE segments.date BETWEEN '{since}' AND '{until}'
          AND campaign.status != 'REMOVED'
    """
    spend_rows = pa.gaql_query(spend_q)
    err = _gaql_first_error(spend_rows if isinstance(spend_rows, list) else [])
    if err:
        raise RuntimeError(f"Google Ads GAQL (spend): {err}")
    spend_by_id, conv_by_id, clicks_by_id, imps_by_id = _agg_google_metrics(spend_rows)

    budget_q = """
        SELECT campaign.id, campaign.name, campaign.status,
               campaign_budget.id, campaign_budget.amount_micros, campaign_budget.period
        FROM campaign
        WHERE campaign.status != 'REMOVED'
    """
    budget_rows = pa.gaql_query(budget_q)
    err_b = _gaql_first_error(budget_rows if isinstance(budget_rows, list) else [])
    if err_b:
        raise RuntimeError(f"Google Ads GAQL (budgets): {err_b}")
    daily_by_id: Dict[str, float] = {}
    budget_id_by_cid: Dict[str, str] = {}
    name_by_id: Dict[str, str] = {}
    status_by_id: Dict[str, str] = {}
    for r in budget_rows:
        if not isinstance(r, dict) or "error" in r:
            continue
        camp = r.get("campaign") or {}
        cb = r.get("campaignBudget") or r.get("campaign_budget") or {}
        cid = str(camp.get("id", ""))
        bid = cb.get("id")
        if bid is None or bid == "":
            budget_id_by_cid[cid] = ""
        else:
            try:
                budget_id_by_cid[cid] = str(int(float(bid)))
            except (TypeError, ValueError):
                budget_id_by_cid[cid] = str(bid).strip()
        name_by_id[cid] = str(camp.get("name", "") or "")
        status_by_id[cid] = str(camp.get("status", "") or "")
        micros = cb.get("amountMicros") or cb.get("amount_micros") or 0
        period = str(cb.get("period") or "").upper()
        try:
            amt = float(micros) / 1_000_000.0
        except (TypeError, ValueError):
            amt = 0.0
        # DAILY budget is already per day; TOTAL uses lifetime — approximate daily as amt/30 for pacing only if needed
        if "DAILY" in period or not period:
            daily_by_id[cid] = amt
        else:
            daily_by_id[cid] = amt / 30.0 if amt else 0.0

    rows: List[Dict[str, Any]] = []
    all_ids = set(spend_by_id.keys()) | set(daily_by_id.keys())
    for cid in sorted(all_ids, key=lambda x: int(x) if x.isdigit() else 0):
        name = name_by_id.get(cid, "")
        st = (status_by_id.get(cid) or "").upper()
        is_live = st == "ENABLED"
        rows.append(
            {
                "campaign_id": name,
                "platform": "google",
                "platform_campaign_id": cid,
                "campaign_budget_id": budget_id_by_cid.get(cid, ""),
                "current_daily_budget": daily_by_id.get(cid, 0.0),
                "spend_mtd": spend_by_id.get(cid, 0.0),
                "leads_mtd": conv_by_id.get(cid, 0.0),
                "clicks_mtd": clicks_by_id.get(cid, 0.0),
                "impressions_mtd": imps_by_id.get(cid, 0.0),
                "is_live": is_live,
            }
        )
    return rows


def build_live_snapshot_dataframe(as_of: date) -> pd.DataFrame:
    since, until = _month_bounds(as_of)
    parts: List[pd.DataFrame] = []
    errors: List[str] = []

    try:
        parts.append(pd.DataFrame(fetch_meta_snapshot_rows(since, until)))
    except Exception as e:
        errors.append(f"Meta: {e}")

    try:
        parts.append(pd.DataFrame(fetch_google_snapshot_rows(since, until)))
    except Exception as e:
        errors.append(f"Google: {e}")

    if not parts:
        raise RuntimeError("Live fetch failed for all platforms: " + "; ".join(errors))

    df = pd.concat(parts, ignore_index=True)
    if errors:
        df.attrs["fetch_warnings"] = errors

    # Reconcile Meta account-level MTD vs sum of campaign rows (same API, same time_range)
    try:
        _ensure_agent_importable()
        import paid_ads_intelligence_agent as pa  # noqa: WPS433

        since, until = _month_bounds(as_of)
        if pa.META_ACCESS_TOKEN and pa.META_AD_ACCOUNT_ID:
            acct_spend = pa.fetch_meta_account_spend_mtd(since, until)
            df.attrs["meta_account_spend_mtd"] = round(acct_spend, 2)
            meta_mask = df["platform"].astype(str).str.lower() == "meta" if "platform" in df.columns else None
            if meta_mask is not None and meta_mask.any():
                row_sum = float(df.loc[meta_mask, "spend_mtd"].sum())
                df.attrs["meta_campaign_rows_spend_sum"] = round(row_sum, 2)
                delta = abs(acct_spend - row_sum)
                tol = max(2.0, 0.005 * max(acct_spend, 1.0))
                if delta > tol:
                    msg = (
                        f"Meta spend reconcile: account-level MTD ${acct_spend:,.2f} vs sum of "
                        f"campaign rows ${row_sum:,.2f} (Δ ${delta:,.2f}). "
                        "Usually missing campaigns (pagination), deleted IDs, or account vs campaign attribution."
                    )
                    warns = list(df.attrs.get("fetch_warnings") or [])
                    warns.append(msg)
                    df.attrs["fetch_warnings"] = warns
    except Exception:
        pass

    return df


def build_snapshot_from_playbook_and_live(
    playbook: pd.DataFrame,
    live: pd.DataFrame,
    id_col: str = "campaign_id",
) -> pd.DataFrame:
    """
    One row per playbook campaign. Match live API by platform + normalised name == playbook id_col.
    Missing API match → not live, zeros (redistribution applies downstream).
    """
    if playbook.empty:
        return pd.DataFrame(
            columns=[
                id_col,
                "platform",
                "platform_campaign_id",
                "platform_campaign_name",
                "current_daily_budget",
                "spend_mtd",
                "leads_mtd",
                "clicks_mtd",
                "impressions_mtd",
                "is_live",
            ]
        )

    live = live.copy() if not live.empty else pd.DataFrame()
    if not live.empty:
        live["_key_exact"] = live["campaign_id"].map(exact_match_key)
        live["_key_canon"] = live["campaign_id"].map(canonical_campaign_match_key)

    rows: List[Dict[str, Any]] = []
    for _, pr in playbook.iterrows():
        plat = str(pr.get("platform", "")).lower()
        p_exact = exact_match_key(pr.get(id_col))
        p_canon = canonical_campaign_match_key(str(pr.get(id_col) or ""))
        sub = pd.DataFrame()
        if not live.empty and "platform" in live.columns:
            base = live[live["platform"] == plat]
            # 1) Exact name match (case-insensitive)
            sub = base[base["_key_exact"] == p_exact]
            # 2) Canonical geo alias match (e.g. uk-au_* ↔ au-uk_*)
            if sub.empty:
                sub = base[base["_key_canon"] == p_canon]
        if sub.empty:
            rows.append(
                {
                    id_col: pr[id_col],
                    "platform": plat,
                    "platform_campaign_id": "",
                    "platform_campaign_name": "",
                    "current_daily_budget": 0.0,
                    "spend_mtd": 0.0,
                    "leads_mtd": 0.0,
                    "clicks_mtd": 0.0,
                    "impressions_mtd": 0.0,
                    "is_live": False,
                }
            )
        else:
            r = sub.iloc[0].to_dict()
            # Live fetch uses Meta/Google campaign *name* as `campaign_id`; keep explicit column for reports
            live_name = str(r.get("campaign_id") or "").strip()
            rows.append(
                {
                    id_col: pr[id_col],
                    "platform": plat,
                    "platform_campaign_id": str(r.get("platform_campaign_id", "") or ""),
                    "platform_campaign_name": live_name,
                    "current_daily_budget": float(r.get("current_daily_budget") or 0),
                    "spend_mtd": float(r.get("spend_mtd") or 0),
                    "leads_mtd": float(r.get("leads_mtd") or 0),
                    "clicks_mtd": float(r.get("clicks_mtd") or 0),
                    "impressions_mtd": float(r.get("impressions_mtd") or 0),
                    "is_live": bool(r.get("is_live", False)),
                }
            )

    out = pd.DataFrame(rows)
    out = out.rename(columns={id_col: "campaign_id"})
    return out
