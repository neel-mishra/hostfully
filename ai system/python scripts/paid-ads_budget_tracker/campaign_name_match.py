"""
Match playbook `campaign_id` to live platform campaign names when naming differs
but refers to the same entity (e.g. Meta: `au-uk_pms_*` vs playbook `uk-au_pms_*`).
"""

from __future__ import annotations

from typing import Final

# Region/geo token variants → canonical segment (order-agnostic UK/AU).
# Extend here if new geo aliases appear in accounts.
_UK_AU_VARIANTS: Final[tuple[tuple[str, str], ...]] = (
    ("au-uk", "uk-au"),
    ("au+uk", "uk-au"),
    ("uk+au", "uk-au"),
)


def canonical_campaign_match_key(name: str) -> str:
    """
    Lowercase + normalize known geo aliases so `uk-au_*` and `au-uk_*` collide.

    Matching order: prefer exact string match in callers first; use this key as fallback.
    """
    s = (name or "").strip().lower()
    if not s:
        return ""
    for variant, canonical in _UK_AU_VARIANTS:
        s = s.replace(variant, canonical)
    return s


def exact_match_key(name: str) -> str:
    """Case-insensitive exact key (strip only)."""
    return str(name or "").strip().lower()


if __name__ == "__main__":
    a = canonical_campaign_match_key("uk-au_pms_prospecting_website-conv")
    b = canonical_campaign_match_key("au-uk_pms_prospecting_website-conv")
    assert a == b, (a, b)
    assert canonical_campaign_match_key("UK+AU_pms_x") == canonical_campaign_match_key("au-uk_pms_x")
    print("campaign_name_match OK")
