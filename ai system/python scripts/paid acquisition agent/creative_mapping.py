import os
import json
from datetime import datetime
from typing import Any, Dict, List


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AUDIENCE_ROOT = os.path.join(REPO_ROOT, "docs", "paid_acquisition", "audiences")
PAID_ASSETS_ROOT = os.path.join(REPO_ROOT, "docs", "paid_ads_assets")
SIGNALS_PATH = os.path.join(REPO_ROOT, "outputs", "training_data", "paid_ads", "signals", "signals_latest.jsonl")
WINNERS_ROOT = os.path.join(REPO_ROOT, "docs", "context_repository", "paid_ads", "winning_angles")

ANGLE_PRIOR_WEIGHT_HIST = 0.70
ANGLE_PRIOR_WEIGHT_MESSAGE_FIT = 0.30
DEFAULT_PLATFORM_FUNNEL = [
    ("meta", "prospecting"),
    ("meta", "retargeting"),
    ("google", "prospecting"),
    ("google", "retargeting"),
]


def _today_folder() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def _input_dir() -> str:
    return os.path.join(AUDIENCE_ROOT, _today_folder())


def _load_best_performing_linkedin_posts() -> List[Dict[str, str]]:
    """
    Placeholder: in a fuller implementation we would inspect analytics or
    curated lists of best-performing LinkedIn posts and map them by angle.
    Here we simply expose a couple of slots for manual linking.
    """
    return [
        {
            "angle": "drift_sunset_replacement",
            "url": "https://www.linkedin.com/feed/update/REPLACE_WITH_Hostfully_POST",
            "notes": "Narrative about Drift sunsetting and Hostfully as the modern inbound agent.",
        }
    ]


def _angle_tag(text: str) -> str:
    t = (text or "").lower()
    if any(k in t for k in ["automate", "save time", "manual", "workflow"]):
        return "ops_relief"
    if any(k in t for k in ["revenue", "profit", "roi", "bookings", "occupancy"]):
        return "roi_proof"
    if any(k in t for k in ["scale", "growth", "portfolio", "units"]):
        return "scale_story"
    if any(k in t for k in ["integration", "connect", "sync", "api"]):
        return "integration_power"
    if any(k in t for k in ["trusted", "rated", "customers", "case study"]):
        return "social_proof"
    return "general_value"


def _load_signal_angle_priors() -> Dict[str, float]:
    if not os.path.exists(SIGNALS_PATH):
        return {}
    scores: Dict[str, List[float]] = {}
    with open(SIGNALS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            tag = _angle_tag(str(row.get("entity_text", "")))
            score = float(row.get("blended_score") or 0.0)
            scores.setdefault(tag, []).append(score)
    out: Dict[str, float] = {}
    for k, vals in scores.items():
        out[k] = sum(vals) / max(len(vals), 1)
    return out


def _message_fit_priors() -> Dict[str, float]:
    return {
        "ops_relief": 0.85,
        "roi_proof": 0.90,
        "scale_story": 0.80,
        "integration_power": 0.75,
        "social_proof": 0.70,
        "general_value": 0.60,
    }


def _write_angle_priors_json(ranked: List[Dict[str, Any]]) -> None:
    """Shared artifact for search_ads_agent / social_ads_agent retrieval."""
    os.makedirs(WINNERS_ROOT, exist_ok=True)
    path = os.path.join(WINNERS_ROOT, "angle_priors_mar2026_onward.json")
    plat_top: Dict[str, List[str]] = {}
    for plat, funnel in DEFAULT_PLATFORM_FUNNEL:
        key = f"{plat}_{funnel}"
        plat_top[key] = [r["angle_family"] for r in ranked[:5]] if ranked else ["general_value"]
    payload = {
        "generated_at_utc": datetime.utcnow().isoformat() + "Z",
        "angle_prior_weight_hist": ANGLE_PRIOR_WEIGHT_HIST,
        "angle_prior_weight_message_fit": ANGLE_PRIOR_WEIGHT_MESSAGE_FIT,
        "ranked_families": ranked,
        "platform_top5_angle_families": plat_top,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def _rank_angle_families() -> List[Dict[str, float]]:
    hist = _load_signal_angle_priors()
    fit = _message_fit_priors()
    all_tags = sorted(set(hist.keys()) | set(fit.keys()))
    ranked: List[Dict[str, float]] = []
    for tag in all_tags:
        h = float(hist.get(tag, 0.0))
        m = float(fit.get(tag, 0.0))
        score = ANGLE_PRIOR_WEIGHT_HIST * h + ANGLE_PRIOR_WEIGHT_MESSAGE_FIT * m
        ranked.append({"angle_family": tag, "hist_score": h, "message_fit_score": m, "combined_score": score})
    ranked.sort(key=lambda x: x["combined_score"], reverse=True)
    return ranked


def _write_creative_mapping() -> None:
    out_dir = _input_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "creative_mapping.md")

    linkedin_posts = _load_best_performing_linkedin_posts()

    lines: List[str] = []
    lines.append("# Creative Mapping for This Audience Pack")
    lines.append("")
    lines.append(f"- Generated at (UTC): {datetime.utcnow().isoformat()}")
    lines.append("")
    lines.append("## LinkedIn")
    lines.append("")
    lines.append("## Weighted Angle Family Priors")
    lines.append("")
    lines.append(
        f"Scoring: {ANGLE_PRIOR_WEIGHT_HIST:.2f} * historical_signals + {ANGLE_PRIOR_WEIGHT_MESSAGE_FIT:.2f} * messaging_fit"
    )
    lines.append("")
    lines.append("| Rank | Angle Family | Hist Score | Message Fit | Combined |")
    lines.append("|------|--------------|------------|-------------|----------|")
    ranked = _rank_angle_families()
    _write_angle_priors_json(ranked)
    for i, r in enumerate(ranked, start=1):
        lines.append(
            f"| {i} | {r['angle_family']} | {r['hist_score']:.3f} | {r['message_fit_score']:.3f} | {r['combined_score']:.3f} |"
        )
    lines.append("")
    lines.append(
        f"- Machine-readable priors also written to `{os.path.join(WINNERS_ROOT, 'angle_priors_mar2026_onward.json')}`."
    )
    lines.append("")
    lines.append("### Platform x Funnel Recommended Top-3")
    lines.append("")
    for plat, funnel in DEFAULT_PLATFORM_FUNNEL:
        top = ", ".join([r["angle_family"] for r in ranked[:3]]) if ranked else "general_value"
        lines.append(f"- **{plat} / {funnel}**: {top}")
    lines.append("")
    lines.append("Use high-performing thought-leadership posts as Sponsored Content:")
    lines.append("")
    lines.append("| Angle | Post URL | Notes |")
    lines.append("|-------|----------|-------|")
    for post in linkedin_posts:
        lines.append(
            f"| {post['angle']} | {post['url']} | {post['notes']} |"
        )

    lines.append("")
    lines.append("## Meta (Facebook/Instagram)")
    lines.append("")
    lines.append(
        "- All videos should be 9:16, mobile-first, with a strong visual hook in the first 3 seconds."
    )
    lines.append(
        "- Use creative briefs under `docs/paid_ads_assets/meta/.../creative-briefs/` for actual production."
    )
    lines.append("")
    lines.append("## YouTube")
    lines.append("")
    lines.append(
        "- Use 16:9 product explainers and cut 5–15s bumper variants for pre-roll."
    )
    lines.append(
        "- Reference existing explainers and campaign structures under `docs/paid_ads_assets/google/` and related folders."
    )
    lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def run_creative_mapping() -> None:
    _write_creative_mapping()


if __name__ == "__main__":
    run_creative_mapping()

