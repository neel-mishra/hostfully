from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd


DEFAULT_START = date(2026, 3, 1)


@dataclass(frozen=True)
class SalesforceInputs:
    leads_path: Path
    opps_path: Path
    start_date: date = DEFAULT_START


def _read_salesforce_report_xlsx(path: Path, *, header_markers: set[str], max_scan_rows: int = 80) -> pd.DataFrame:
    """
    Salesforce exports in this repo often include a preamble (title, filters) before the real header row.
    This reader scans the top rows for a row containing known header markers, then re-reads with that
    row as the header.
    """
    raw = pd.read_excel(path, sheet_name=0, header=None)
    scan_n = min(max_scan_rows, len(raw))

    header_row_idx: Optional[int] = None
    for i in range(scan_n):
        row_vals = [str(v).strip() for v in raw.iloc[i].tolist()]
        row_set = {v for v in row_vals if v and v.lower() != "nan"}
        if not row_set:
            continue
        hit = {m for m in header_markers if m in row_set}
        if len(hit) >= max(2, min(4, len(header_markers))):
            header_row_idx = i
            break

    if header_row_idx is None:
        # Fall back to pandas' default behavior (first row is header), useful for "clean" exports.
        return pd.read_excel(path, sheet_name=0)

    df = pd.read_excel(path, sheet_name=0, header=header_row_idx)
    # Drop rows that are entirely empty.
    df = df.dropna(how="all").copy()
    return df


def _to_date(s: object) -> Optional[date]:
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return None
    ts = pd.to_datetime(s, errors="coerce")
    if pd.isna(ts):
        return None
    return ts.date()


def _norm_str(v: object) -> str:
    return str(v or "").strip()


def _normalize_utm_campaign(v: object) -> str:
    """
    Mirror the pacing model’s campaign normalization rules:
    - strip whitespace
    - treat placeholders / numeric ids as PMAX placeholder
    - remove HubSpot-style suffixes like " - 1"
    """
    s = _norm_str(v)
    if not s or s.lower() == "brand":
        return ""
    if s.lower() in {"{campaign_name}", "campaign_name"}:
        return "__PMAX_PLACEHOLDER__"
    if s.isdigit() and len(s) >= 4:
        return "__PMAX_PLACEHOLDER__"
    if " - " in s and s.rsplit(" - ", 1)[-1].isdigit():
        s = s.rsplit(" - ", 1)[0].strip()
    return s


def _require_cols(df: pd.DataFrame, cols: Iterable[str], *, label: str) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"{label} missing required columns: {missing}")


def load_leads(path: Path, *, start: date) -> pd.DataFrame:
    df = _read_salesforce_report_xlsx(
        path,
        header_markers={"First Name", "Lead Status", "UTM Source", "UTM Campaign", "Campaign Create Date"},
    )

    # Attempt common column names; Salesforce exports vary.
    created_col = next(
        (c for c in df.columns if str(c).strip().lower() in {"created_date", "createddate", "created", "campaign create date", "create date"}),
        None,
    )
    if created_col is None:
        raise ValueError("Leads export missing a create date column (expected Create Date / Campaign Create Date)")
    df["_created_date"] = df[created_col].map(_to_date)
    df = df[df["_created_date"].notna()].copy()
    df = df[df["_created_date"] >= start].copy()

    # UTM columns are authoritative for joins.
    rename_map = {
        "UTM Source": "utm_source",
        "UTM Medium": "utm_medium",
        "UTM Campaign": "utm_campaign",
        "UTM Content": "utm_content",
        "Lead Status": "lead_status",
        "FB click ID": "fbclid",
        "Google Click ID": "gclid",
    }
    for src, dst in rename_map.items():
        if src in df.columns and dst not in df.columns:
            df = df.rename(columns={src: dst})

    for c in ("utm_source", "utm_medium", "utm_campaign", "utm_content", "lead_status", "gclid", "fbclid"):
        if c in df.columns:
            df[c] = df[c].map(_norm_str)

    if "utm_campaign" in df.columns:
        df["utm_campaign_norm"] = df["utm_campaign"].map(_normalize_utm_campaign)
    return df


def load_opps(path: Path, *, start: date) -> pd.DataFrame:
    df = _read_salesforce_report_xlsx(
        path,
        header_markers={"Stage  ↑", "Stage", "UTM Source", "UTM Campaign", "Created Date", "Amount"},
    )

    rename_map = {
        "UTM Source": "utm_source",
        "UTM Campaign": "utm_campaign",
        "Created Date": "created_date",
        "Close Date": "close_date",
        "Amount": "amount",
        "Stage": "stage",
        "Stage  ↑": "stage",
    }
    for src, dst in rename_map.items():
        if src in df.columns and dst not in df.columns:
            df = df.rename(columns={src: dst})

    created_col = next((c for c in df.columns if str(c).strip().lower() in {"created_date", "createddate", "created"}), None)
    if created_col is None:
        raise ValueError("Opportunities export missing a created date column (expected Created Date)")
    stage_col = next((c for c in df.columns if str(c).strip().lower() in {"stage", "stagename"}), None)
    amount_col = next((c for c in df.columns if str(c).strip().lower() in {"amount"}), None)
    if stage_col is None or amount_col is None:
        raise ValueError("Opportunities export missing stage and/or amount")

    df["_created_date"] = df[created_col].map(_to_date)
    df = df[df["_created_date"].notna()].copy()
    df = df[df["_created_date"] >= start].copy()

    df[stage_col] = df[stage_col].map(_norm_str)
    df["_amount"] = pd.to_numeric(df[amount_col], errors="coerce").fillna(0.0)

    # UTM columns (authoritative keys)
    for c in ("utm_source", "utm_campaign"):
        if c in df.columns:
            df[c] = df[c].map(_norm_str)
    if "utm_campaign" in df.columns:
        df["utm_campaign_norm"] = df["utm_campaign"].map(_normalize_utm_campaign)

    # Closed-won inference (fallback if there is no closed_won_amount column)
    stage_norm = df[stage_col].astype(str).str.lower().str.strip()
    df["_is_closed_won"] = stage_norm.str.contains("closed won", na=False)
    df["_closed_won_amount"] = df["_amount"].where(df["_is_closed_won"], 0.0)

    # Default pipeline mask (mirrors pacing report’s intent: include later-funnel stages + closed)
    df["_is_pipeline_stage"] = stage_norm.str.contains(
        "pre-qualification|needs analysis|proposal|negotiation|verbal agreement|closed won|closed lost",
        na=False,
    )
    df["_pipeline_amount"] = df["_amount"].where(df["_is_pipeline_stage"], 0.0)

    return df


def compute_roi_weights(opps: pd.DataFrame) -> pd.DataFrame:
    _require_cols(opps, ["utm_source", "utm_campaign_norm", "_pipeline_amount", "_closed_won_amount"], label="opps")
    # Normalize utm_source to platform keys used elsewhere in the repo.
    def _platform(v: object) -> str:
        s = _norm_str(v).lower()
        if not s:
            return ""
        if "meta" in s or s in {"fb", "ig", "facebook", "instagram", "meta ads"}:
            return "meta"
        if "google" in s:
            return "google"
        return s

    out = opps.copy()
    out["utm_source"] = out["utm_source"].map(_platform)
    out = out[out["utm_source"].isin({"meta", "google"})].copy()
    g = (
        out.groupby(["utm_source", "utm_campaign_norm"], dropna=False)[["_pipeline_amount", "_closed_won_amount"]]
        .sum()
        .reset_index()
    )
    g = g.rename(columns={"_pipeline_amount": "pipeline_amount", "_closed_won_amount": "closed_won_amount"})
    g["roi_priority_weight"] = g["pipeline_amount"] + 2.0 * g["closed_won_amount"]
    return g


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--leads", required=True, help="Path to Salesforce Leads/Contacts export (XLSX)")
    p.add_argument("--opps", required=True, help="Path to Salesforce Opportunities export (XLSX)")
    p.add_argument("--start", default=str(DEFAULT_START), help="Start date (YYYY-MM-DD). Default: 2026-03-01")
    p.add_argument("--out_dir", default="outputs/training_data/paid_ads/salesforce/tables", help="Output directory")
    args = p.parse_args()

    start = pd.to_datetime(args.start).date()
    leads_path = Path(args.leads)
    opps_path = Path(args.opps)

    leads = load_leads(leads_path, start=start)
    opps = load_opps(opps_path, start=start)
    roi = compute_roi_weights(opps)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    leads.to_csv(out_dir / "leads_mar2026_onward.csv", index=False)
    opps.to_csv(out_dir / "opps_mar2026_onward.csv", index=False)
    roi.to_csv(out_dir / "roi_weights_by_utm_campaign.csv", index=False)

    print(f"Wrote: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

