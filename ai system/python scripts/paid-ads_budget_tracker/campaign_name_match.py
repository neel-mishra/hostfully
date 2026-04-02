"""
Match playbook `campaign_id` to live platform campaign names when naming differs
but refers to the same entity (e.g. Meta: `au-uk_pms_*` vs playbook `uk-au_pms_*`).
"""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
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


@dataclass(frozen=True)
class MatchResult:
    matched_name: str
    match_type: str
    match_score: float


def fuzzy_similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return float(SequenceMatcher(None, exact_match_key(a), exact_match_key(b)).ratio())


def best_match_against_candidates(
    target: str,
    candidates: list[str],
    *,
    min_score: float = 0.75,
    exact_weight: float = 1.0,
    canonical_weight: float = 0.9,
    fuzzy_weight: float = 0.7,
) -> MatchResult:
    t_exact = exact_match_key(target)
    t_canon = canonical_campaign_match_key(target)
    # exact first
    for c in candidates:
        if exact_match_key(c) == t_exact:
            return MatchResult(matched_name=c, match_type="exact", match_score=exact_weight)
    # canonical fallback
    for c in candidates:
        if canonical_campaign_match_key(c) == t_canon:
            return MatchResult(matched_name=c, match_type="canonical", match_score=canonical_weight)
    # fuzzy last resort
    best_name = ""
    best = 0.0
    for c in candidates:
        s = fuzzy_similarity(target, c)
        if s > best:
            best = s
            best_name = c
    weighted = best * fuzzy_weight
    if best_name and weighted >= min_score:
        return MatchResult(matched_name=best_name, match_type="fuzzy", match_score=weighted)
    return MatchResult(matched_name="", match_type="none", match_score=0.0)


if __name__ == "__main__":
    a = canonical_campaign_match_key("uk-au_pms_prospecting_website-conv")
    b = canonical_campaign_match_key("au-uk_pms_prospecting_website-conv")
    assert a == b, (a, b)
    assert canonical_campaign_match_key("UK+AU_pms_x") == canonical_campaign_match_key("au-uk_pms_x")
    print("campaign_name_match OK")
