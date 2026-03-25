import os
import math
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SOCIAL_DIR = os.path.join(REPO_ROOT, "docs", "social media")


def _week_folder_for_today(date: datetime) -> str:
    month_name = date.strftime("%B")
    first_day = date.replace(day=1)
    while first_day.weekday() != 0:
        first_day = first_day.replace(day=first_day.day + 1)
    if date < first_day:
        week_num = 1
    else:
        delta = date - first_day
        week_num = (delta.days // 7) + 1
    if week_num > 4:
        week_num = 4
    return f"{month_name} Week {week_num}"


def _day_prefix(day_name: str) -> str:
    mapping = {
        "Monday": "1. Monday",
        "Tuesday": "2. Tuesday",
        "Wednesday": "3. Wednesday",
        "Thursday": "4. Thursday",
        "Friday": "5. Friday",
        "Saturday": "6. Saturday",
        "Sunday": "7. Sunday",
    }
    return mapping.get(day_name, day_name)


@dataclass
class DraftInfo:
    person_id: str
    file_path: str
    copy: str


def _collect_today_drafts(date: datetime) -> List[DraftInfo]:
    """Scan docs/social media/<Month Week N>/*/<Day>/draft_*.md for today's drafts."""
    week_folder = _week_folder_for_today(date)
    day_folder = _day_prefix(date.strftime("%A"))
    base_week_dir = os.path.join(SOCIAL_DIR, week_folder)
    if not os.path.isdir(base_week_dir):
        return []

    drafts: List[DraftInfo] = []
    for person_id in os.listdir(base_week_dir):
        person_dir = os.path.join(base_week_dir, person_id, day_folder)
        if not os.path.isdir(person_dir):
            continue
        for name in os.listdir(person_dir):
            if not name.startswith("draft_") or not name.endswith(".md"):
                continue
            path = os.path.join(person_dir, name)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Strip off frontmatter if present.
            if content.lstrip().startswith("---"):
                parts = content.split("---", 2)
                if len(parts) == 3:
                    content = parts[2]
            drafts.append(DraftInfo(person_id=person_id, file_path=path, copy=content.strip()))
    return drafts


def _tokenise(text: str) -> List[str]:
    # Simple whitespace + punctuation splitting; good enough for similarity checks.
    cleaned = "".join(ch.lower() if ch.isalnum() or ch.isspace() else " " for ch in text)
    return [t for t in cleaned.split() if t]


def _cosine_similarity(a: str, b: str) -> float:
    a_tokens = _tokenise(a)
    b_tokens = _tokenise(b)
    if not a_tokens or not b_tokens:
        return 0.0
    a_counts = Counter(a_tokens)
    b_counts = Counter(b_tokens)
    all_keys = set(a_counts) | set(b_counts)
    dot = sum(a_counts[k] * b_counts[k] for k in all_keys)
    norm_a = math.sqrt(sum(v * v for v in a_counts.values()))
    norm_b = math.sqrt(sum(v * v for v in b_counts.values()))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


def _pairwise_similarities(drafts: List[DraftInfo]) -> List[Tuple[DraftInfo, DraftInfo, float]]:
    results: List[Tuple[DraftInfo, DraftInfo, float]] = []
    for i in range(len(drafts)):
        for j in range(i + 1, len(drafts)):
            a = drafts[i]
            b = drafts[j]
            if a.person_id == b.person_id:
                # Uniqueness gate is about cross-person duplication.
                continue
            score = _cosine_similarity(a.copy, b.copy)
            results.append((a, b, score))
    # Sort by descending similarity.
    results.sort(key=lambda t: t[2], reverse=True)
    return results


def _write_collision_report(
    date: datetime,
    collisions: List[Tuple[DraftInfo, DraftInfo, float]],
    threshold: float,
) -> None:
    qa_dir = os.path.join(SOCIAL_DIR, "_qa")
    os.makedirs(qa_dir, exist_ok=True)
    slug = date.strftime("%Y-%m-%d")
    path = os.path.join(qa_dir, f"uniqueness_report_{slug}.md")

    lines: List[str] = []
    lines.append(f"# Uniqueness Report for {slug}")
    lines.append("")
    lines.append(f"- Hard similarity threshold: {threshold:.2f}")
    lines.append(f"- Total cross-person pairs checked: {len(collisions)}")
    lines.append("")
    lines.append("| Person A | File A | Person B | File B | Similarity |")
    lines.append("|----------|--------|----------|--------|------------|")

    for a, b, score in collisions:
        lines.append(
            f"| {a.person_id} | `{os.path.basename(a.file_path)}` | "
            f"{b.person_id} | `{os.path.basename(b.file_path)}` | {score:.2f} |"
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def run_uniqueness_gate(threshold: float = 0.75) -> None:
    """
    Compute pairwise similarity across all drafts for today's date and
    emit a collision report under docs/social media/_qa/.

    This is intentionally read-only w.r.t. drafts; it does not delete or
    modify posts, it simply surfaces collisions for human review or
    downstream regenerations.
    """
    today = datetime.now()
    drafts = _collect_today_drafts(today)
    if not drafts:
        return

    sims = _pairwise_similarities(drafts)
    _write_collision_report(today, sims, threshold=threshold)


if __name__ == "__main__":
    run_uniqueness_gate()

