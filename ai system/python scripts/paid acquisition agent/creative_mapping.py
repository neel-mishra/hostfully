import os
from datetime import datetime
from typing import Dict, List


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AUDIENCE_ROOT = os.path.join(REPO_ROOT, "docs", "paid_acquisition", "audiences")
PAID_ASSETS_ROOT = os.path.join(REPO_ROOT, "docs", "paid_ads_assets")


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
            "url": "https://www.linkedin.com/feed/update/REPLACE_WITH_TLDR_POST",
            "notes": "Narrative about Drift sunsetting and TLDR as the modern inbound agent.",
        }
    ]


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

