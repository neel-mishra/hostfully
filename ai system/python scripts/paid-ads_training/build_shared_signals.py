from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def _norm_str(v: object) -> str:
    return str(v or "").strip()


def _confidence_class(impr: float, clicks: float, results: float) -> str:
    if impr >= 5000 and clicks >= 100 and results >= 5:
        return "high"
    if impr >= 2000 and clicks >= 40 and results >= 2:
        return "medium"
    if impr >= 1000 and clicks >= 20 and results >= 1:
        return "low"
    return "insufficient"


def _base_fields(df: pd.DataFrame, platform: str, entity_type: str) -> pd.DataFrame:
    out = df.copy()
    out["platform"] = platform
    out["entity_type"] = entity_type
    out["grain"] = "monthly"
    out["date_start"] = pd.to_datetime(out.get("date_start"), errors="coerce")
    out["date_stop"] = pd.to_datetime(out.get("date_stop"), errors="coerce")
    out["fatigue_flag"] = False
    out["volatility_flag"] = False
    return out


def build_meta_signals(meta_csv: Path) -> pd.DataFrame:
    m = pd.read_csv(meta_csv)
    if m.empty:
        return pd.DataFrame()
    out = _base_fields(m, platform="meta", entity_type="meta_ad")
    out["entity_id"] = out.get("ad_id", "").map(_norm_str)
    out["entity_text"] = out.get("body", "").map(_norm_str)
    out["impressions"] = pd.to_numeric(out.get("impressions", 0.0), errors="coerce").fillna(0.0)
    out["clicks"] = pd.to_numeric(out.get("clicks", 0.0), errors="coerce").fillna(0.0)
    out["spend"] = pd.to_numeric(out.get("spend", 0.0), errors="coerce").fillna(0.0)
    out["results_or_conversions"] = pd.to_numeric(out.get("results", 0.0), errors="coerce").fillna(0.0)
    out["ctr"] = pd.to_numeric(out.get("ctr", 0.0), errors="coerce").fillna(0.0)
    out["campaign_name"] = out.get("campaign_name", "").map(_norm_str)
    out["confidence_class"] = out.apply(
        lambda r: _confidence_class(float(r["impressions"]), float(r["clicks"]), float(r["results_or_conversions"])),
        axis=1,
    )
    keep = [
        "platform",
        "entity_type",
        "entity_id",
        "entity_text",
        "campaign_name",
        "date_start",
        "date_stop",
        "grain",
        "impressions",
        "clicks",
        "spend",
        "results_or_conversions",
        "ctr",
        "roi_priority_weight",
        "roi_norm",
        "perf_signal",
        "blended_score",
        "confidence_class",
        "fatigue_flag",
        "volatility_flag",
    ]
    return out[keep].copy()


def build_google_signals(google_csv: Path) -> pd.DataFrame:
    g = pd.read_csv(google_csv)
    if g.empty:
        return pd.DataFrame()
    out = _base_fields(g, platform="google", entity_type="google_asset")
    out["entity_id"] = out.get("asset.id", "").map(_norm_str)
    out["entity_text"] = out.get("asset.textAsset.text", "").map(_norm_str)
    out["impressions"] = pd.to_numeric(out.get("metrics.impressions", 0.0), errors="coerce").fillna(0.0)
    out["clicks"] = pd.to_numeric(out.get("metrics.clicks", 0.0), errors="coerce").fillna(0.0)
    out["spend"] = 0.0
    out["results_or_conversions"] = pd.to_numeric(out.get("metrics.conversions", 0.0), errors="coerce").fillna(0.0)
    out["ctr"] = pd.to_numeric(out.get("metrics.ctr", 0.0), errors="coerce").fillna(0.0)
    out["campaign_name"] = out.get("campaign.name", "").map(_norm_str)
    out["confidence_class"] = out.apply(
        lambda r: _confidence_class(float(r["impressions"]), float(r["clicks"]), float(r["results_or_conversions"])),
        axis=1,
    )
    keep = [
        "platform",
        "entity_type",
        "entity_id",
        "entity_text",
        "campaign_name",
        "date_start",
        "date_stop",
        "grain",
        "impressions",
        "clicks",
        "spend",
        "results_or_conversions",
        "ctr",
        "roi_priority_weight",
        "roi_norm",
        "perf_signal",
        "blended_score",
        "confidence_class",
        "fatigue_flag",
        "volatility_flag",
    ]
    return out[keep].copy()


def _write_jsonl(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in df.to_dict(orient="records"):
            for k in ("date_start", "date_stop"):
                if isinstance(r.get(k), pd.Timestamp):
                    r[k] = r[k].date().isoformat()
                elif pd.isna(r.get(k)):
                    r[k] = None
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--meta_scored_csv", required=True)
    p.add_argument("--google_scored_csv", required=True)
    p.add_argument("--out_dir", default="outputs/training_data/paid_ads/signals")
    args = p.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = build_meta_signals(Path(args.meta_scored_csv))
    google = build_google_signals(Path(args.google_scored_csv))
    combined = pd.concat([d for d in (meta, google) if not d.empty], ignore_index=True) if (not meta.empty or not google.empty) else pd.DataFrame()

    if not meta.empty:
        meta_path = out_dir / "platform=meta" / "grain=monthly" / "entity_type=meta_ad" / "signals.parquet"
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        meta.to_parquet(meta_path, index=False)
        _write_jsonl(meta, out_dir / "meta_monthly_signals.jsonl")
    if not google.empty:
        google_path = out_dir / "platform=google" / "grain=monthly" / "entity_type=google_asset" / "signals.parquet"
        google_path.parent.mkdir(parents=True, exist_ok=True)
        google.to_parquet(google_path, index=False)
        _write_jsonl(google, out_dir / "google_monthly_signals.jsonl")
    if not combined.empty:
        combined.to_parquet(out_dir / "signals_latest.parquet", index=False)
        _write_jsonl(combined, out_dir / "signals_latest.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

