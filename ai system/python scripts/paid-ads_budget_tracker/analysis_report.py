"""
Human-readable markdown summary: targets, current state, recommendations, artifact index.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from config import MonthContext, paths
from pacing_allocation import ChannelPacingSummary
from model_legend import MODEL_LEGEND_LINES


def _money(x: Any, currency: str = "USD") -> str:
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "—"
    try:
        v = float(x)
    except (TypeError, ValueError):
        return str(x)
    sym = "$" if currency.upper() == "USD" else f"{currency} "
    return f"{sym}{v:,.2f}"


def _esc(s: Any) -> str:
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return ""
    t = str(s).replace("|", "\\|").replace("\n", " ")
    return t[:500] + ("…" if len(str(s)) > 500 else "")


def write_analysis_markdown(
    path: Path,
    as_of: date,
    currency: str,
    month_ctx: MonthContext,
    playbook: pd.DataFrame,
    merged_all: pd.DataFrame,
    combined: Optional[pd.DataFrame],
    meta_df: pd.DataFrame,
    google_df: pd.DataFrame,
    meta_s: ChannelPacingSummary,
    google_s: ChannelPacingSummary,
    nonlive_merged: pd.DataFrame,
    warnings: List[str],
    artifacts: Dict[str, str],
    *,
    live_pull_succeeded: bool,
) -> Path:
    """
    Write a single markdown file covering: targets, live state, redistribution,
    channel pacing, per-campaign recommendations, checks, and output file index.
    """
    lines: List[str] = []

    lines.append(f"# Paid ads budget pacing — {as_of.isoformat()}")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- **Calendar month:** {month_ctx.month_start.isoformat()} → {month_ctx.month_end.isoformat()}")
    lines.append(f"- **As-of date:** {as_of.isoformat()}")
    lines.append(f"- **Currency:** {currency}")
    lines.append(
        f"- **Time math:** {month_ctx.days_elapsed} day(s) elapsed in month, "
        f"{month_ctx.days_remaining} day(s) remaining in month after as-of."
    )
    lines.append(
        f"- **Live data:** {'API pull (Meta + Google)' if live_pull_succeeded else 'CSV snapshot fallback (`campaign_snapshot_latest.csv` or env path)'}"
    )
    lines.append(f"- **Playbook file (only source of monthly targets):** `{paths.campaign_playbook}`")
    lines.append("")
    lines.append("## Model legend")
    lines.append("")
    for line in MODEL_LEGEND_LINES:
        lines.append(f"- {line}")
    lines.append("")

    # --- Original playbook targets (plan) ---
    lines.append("## Original targets (playbook)")
    lines.append("")
    pb = playbook.copy()
    if "monthly_budget" in pb.columns:
        pb["monthly_budget"] = pb["monthly_budget"].astype(float)
    by_plat = pb.groupby("platform")["monthly_budget"].sum() if "platform" in pb.columns else pd.Series()
    total_pb = float(pb["monthly_budget"].sum()) if not pb.empty else 0.0
    n_pb = len(pb)
    lines.append(
        f"The **portfolio total** below is **only** the sum of `monthly_budget` in that CSV "
        f"(**{n_pb}** row(s) → **{_money(total_pb, currency)}**). It is **not** read from slides, GTM docs, or a separate $60k figure."
    )
    lines.append("")
    lines.append(
        "> **If you expect March = $60,000** but see a lower number here, the playbook file is incomplete or amounts are wrong. "
        "Add every campaign row (with `ca-us_…`-style `campaign_id`s) and adjust `monthly_budget` until the file sums to $60,000."
    )
    lines.append("")
    lines.append("### By channel (rollup)")
    lines.append("")
    lines.append("| Channel | Planned monthly budget (playbook) |")
    lines.append("|---------|-------------------------------------|")
    for plat in ("meta", "google"):
        if plat in by_plat.index:
            lines.append(f"| {plat.upper()} | {_money(by_plat[plat], currency)} |")
    lines.append(f"| **Portfolio** | **{_money(total_pb, currency)}** |")
    lines.append("")
    lines.append("### By campaign (every playbook row)")
    lines.append("")
    lines.append(
        "**Matching:** `campaign_id` is matched to the live campaign name **case-insensitively** first; "
        "if missing, **canonical geo aliases** are used (e.g. playbook `uk-au_pms_*` ↔ platform `au-uk_pms_*`). "
        "Optional column `platform_campaign_name` in the snapshot CSV copies the UI name when it differs."
    )
    lines.append("")
    lines.append("| Playbook `campaign_id` | Playbook `campaign_name` | Channel | `monthly_budget` |")
    lines.append("|-------------------------|---------------------------|---------|-------------------|")
    for _, r in pb.iterrows():
        cid = _esc(r.get("campaign_id"))
        cname = _esc(r.get("campaign_name", ""))
        plat = _esc(str(r.get("platform", "")).lower())
        mb = _money(r.get("monthly_budget"), currency)
        lines.append(f"| {cid} | {cname} | {plat} | {mb} |")
    lines.append("")

    # Effective targets after redistribution (all playbook rows)
    if merged_all is not None and not merged_all.empty and "monthly_budget_effective" in merged_all.columns:
        lines.append("### Effective monthly target (after redistribution)")
        lines.append("")
        lines.append(
            "Playbook **effective** amounts include non-live dollars reallocated to live campaigns in-channel."
        )
        lines.append("")
        lines.append(
            "| Source | Playbook `campaign_id` | Playbook `campaign_name` | Platform name (Meta/Google) | Channel | Playbook | Redistribution | Effective | Live |"
        )
        lines.append("|--------|-------------------------|---------------------------|------------------------------|---------|----------|----------------|-----------|------|")
        for _, r in merged_all.iterrows():
            live = r.get("is_live", False)
            pcn = r.get("platform_campaign_name", "—")
            lines.append(
                f"| {_esc(r.get('source', 'playbook'))} | {_esc(r.get('campaign_id'))} | {_esc(r.get('campaign_name', ''))} | {_esc(pcn)} | {_esc(r.get('platform'))} | "
                f"{_money(r.get('monthly_budget_playbook'), currency)} | "
                f"{_money(r.get('redistribution_received'), currency)} | "
                f"{_money(r.get('monthly_budget_effective'), currency)} | "
                f"{'yes' if live else 'no'} |"
            )
        lines.append("")

    # --- Redistribution ---
    lines.append("## Redistribution (non-live playbook)")
    lines.append("")
    if nonlive_merged.empty:
        lines.append(
            "*All playbook campaigns in the snapshot matched as live, or no non-live rows — "
            "no in-channel redistribution of paused/missing campaigns.*"
        )
    else:
        lines.append(
            "Non-live campaigns do not spend in-platform. Their **playbook** monthly amounts "
            "are **pooled per channel** and added to **live** rows **in proportion to each live campaign’s playbook share**."
        )
        lines.append("")
        lines.append(
            "| Playbook `campaign_id` | Playbook `campaign_name` | Platform name (Meta/Google) | Channel | Playbook $ (not spending) |"
        )
        lines.append("|-------------------------|---------------------------|------------------------------|---------|-----------------------------|")
        for _, r in nonlive_merged.iterrows():
            pcn = r.get("platform_campaign_name", "—")
            lines.append(
                f"| {_esc(r.get('campaign_id'))} | {_esc(r.get('campaign_name', ''))} | {_esc(pcn)} | {_esc(r.get('platform'))} | "
                f"{_money(r.get('monthly_budget_playbook'), currency)} |"
            )
        lines.append("")
    lines.append("")

    # --- Portfolio & channel current state (summaries) ---
    lines.append("## Current state (pacing) — by channel")
    lines.append("")
    lines.append(
        "**Channel totals:** **Spend MTD** and **Σ daily budgets** include **every campaign** in the live pull for "
        "that platform (not only playbook rows). Monthly targets and per-campaign rows remain playbook-only. "
        "Forecast uses **spend MTD + Σ(daily budget) × days remaining** after as-of. "
        "**Pacing delta** = channel effective monthly target − forecast (positive = underspend vs target)."
    )
    lines.append("")

    def channel_block(name: str, df: pd.DataFrame, s: ChannelPacingSummary) -> None:
        lines.append(f"### {name}")
        lines.append("")
        if df.empty and s.monthly_budget_total <= 0 and s.spend_mtd_total <= 0:
            lines.append("*No live playbook campaigns in this channel; no spend in live pull.*")
            lines.append("")
            return
        lines.append(f"- **Effective monthly target (live):** {_money(s.monthly_budget_total, currency)}")
        lines.append(f"- **Spend MTD (all campaigns in channel):** {_money(s.spend_mtd_total, currency)}")
        lines.append(f"- **Sum of current daily budgets (all campaigns in channel):** {_money(s.sum_current_daily_budget, currency)}")
        lines.append(f"- **Forecast month-end spend:** {_money(s.forecast_month_spend, currency)}")
        lines.append(f"- **Pacing delta:** {_money(s.pacing_delta, currency)} (positive = underspend)")
        lines.append(f"- **Daily pacing pool (required Σ daily budget deltas):** {_money(s.daily_pool, currency)}")
        lines.append(f"- **Required daily run rate to hit plan:** {_money(s.required_daily_run_rate, currency)}")
        lines.append("")

    channel_block("Meta", meta_df, meta_s)
    channel_block("Google", google_df, google_s)

    # Portfolio roll-up
    B = meta_s.monthly_budget_total + google_s.monthly_budget_total
    S = meta_s.spend_mtd_total + google_s.spend_mtd_total
    F = meta_s.forecast_month_spend + google_s.forecast_month_spend
    cur_d = meta_s.sum_current_daily_budget + google_s.sum_current_daily_budget
    d_rem = max(meta_s.days_remaining, google_s.days_remaining)
    req = (B - S) / d_rem if d_rem > 0 else 0.0
    total_target = 0.0
    if not meta_df.empty:
        total_target += float(meta_df["recommended_daily_budget_capped"].sum())
    if not google_df.empty:
        total_target += float(google_df["recommended_daily_budget_capped"].sum())

    lines.append("### Portfolio (Meta + Google)")
    lines.append("")
    lines.append(f"- **Total effective monthly target:** {_money(B, currency)}")
    lines.append(f"- **Total spend MTD:** {_money(S, currency)}")
    lines.append(f"- **Total forecast month-end:** {_money(F, currency)}")
    lines.append(f"- **Total pacing delta (monthly − forecast):** {_money(B - F, currency)}")
    lines.append(f"- **Total current daily budgets (all campaigns in pull):** {_money(cur_d, currency)}")
    lines.append(f"- **Total recommended daily budgets (sum, after caps):** {_money(total_target, currency)}")
    lines.append(f"- **Portfolio required daily run rate (to hit plan):** {_money(req, currency)}")
    lines.append("")

    # --- Recommendations ---
    lines.append("## Recommendations (per campaign)")
    lines.append("")
    lines.append(
        "Apply **recommended daily budget** in each ad platform. **Delta** = recommended − current. "
        "Notes explain pool direction (underspend vs overspend) and performance weighting."
    )
    lines.append("")

    rec_cols = [
        "source",
        "campaign_id",
        "campaign_name",
        "platform_campaign_name",
        "platform",
        "is_live",
        "monthly_budget_playbook",
        "monthly_budget_effective",
        "current_daily_budget",
        "spend_mtd",
        "forecast_month_spend",
        "pacing_delta_campaign",
        "recommended_daily_budget_capped",
        "daily_budget_delta",
        "pct_budget_change",
        "allocation_share_pct",
        "ctr_mtd",
        "cvr_mtd",
        "cpl_mtd",
        "pipeline_amount",
        "closed_won_amount",
        "sql_count",
        "roi_priority_weight",
        "performance_bucket",
        "note",
    ]
    _rec_headers = {
        "source": "source",
        "campaign_id": "playbook_campaign_id",
        "campaign_name": "playbook_campaign_name",
        "platform_campaign_name": "platform_campaign_name",
        "platform": "channel",
        "is_live": "is_live",
        "monthly_budget_playbook": "monthly_budget_playbook",
        "monthly_budget_effective": "monthly_budget_effective",
        "current_daily_budget": "current_daily_budget",
        "spend_mtd": "spend_mtd",
        "forecast_month_spend": "forecast_month_spend",
        "pacing_delta_campaign": "pacing_delta_campaign",
        "recommended_daily_budget_capped": "recommended_daily_budget_capped",
        "daily_budget_delta": "daily_budget_delta",
        "pct_budget_change": "pct_budget_change",
        "allocation_share_pct": "allocation_share_pct",
        "ctr_mtd": "ctr_mtd",
        "cvr_mtd": "cvr_mtd",
        "cpl_mtd": "cpl_mtd",
        "pipeline_amount": "pipeline_amount",
        "closed_won_amount": "closed_won_amount",
        "sql_count": "sql_count",
        "roi_priority_weight": "roi_priority_weight",
        "performance_bucket": "performance_bucket",
        "note": "note",
    }
    if combined is not None and not combined.empty:
        sub = combined[[c for c in rec_cols if c in combined.columns]].copy()
        if not sub.empty:
            display_cols = [c for c in rec_cols if c in sub.columns]
            header_cells = [_rec_headers.get(c, c) for c in display_cols]
            lines.append("| " + " | ".join(header_cells) + " |")
            lines.append("| " + " | ".join(["---"] * len(display_cols)) + " |")
            for _, r in sub.iterrows():
                cells = []
                for c in display_cols:
                    v = r.get(c)
                    if c in ("current_daily_budget", "spend_mtd", "forecast_month_spend", "pacing_delta_campaign",
                             "monthly_budget_playbook", "monthly_budget_effective",
                             "recommended_daily_budget_capped", "daily_budget_delta",
                             "pipeline_amount", "closed_won_amount", "roi_priority_weight"):
                        cells.append(_money(v, currency) if pd.notna(v) and v != "" else "—")
                    elif c in ("sql_count",):
                        cells.append(f"{float(v):.2f}" if pd.notna(v) and v != "" else "—")
                    elif c in ("pct_budget_change", "allocation_share_pct", "ctr_mtd", "cvr_mtd"):
                        cells.append(f"{float(v):.2f}%" if pd.notna(v) and v != "" else "—")
                    elif c in ("cpl_mtd",):
                        cells.append(_money(v, currency) if pd.notna(v) and v != "" else "—")
                    elif c == "is_live":
                        cells.append("yes" if v else "no")
                    else:
                        cells.append(_esc(v))
                lines.append("| " + " | ".join(cells) + " |")
            lines.append("")
    else:
        lines.append("*No combined campaign table for this run.*")
        lines.append("")

    # --- Checks / warnings ---
    lines.append("## Checks & warnings")
    lines.append("")
    if warnings:
        for w in warnings:
            lines.append(f"- {w}")
    else:
        lines.append("- None reported.")
    lines.append("")

    # --- Output artifacts ---
    lines.append("## Output files (this run)")
    lines.append("")
    lines.append("| File | Purpose |")
    lines.append("|------|---------|")
    for label, rel in sorted(artifacts.items(), key=lambda x: x[0]):
        lines.append(f"| `{rel}` | {_esc(label)} |")
    lines.append("")
    lines.append("---")
    lines.append("*Generated by `paid-ads_budget_tracker` (`analysis_report.py`).*")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
