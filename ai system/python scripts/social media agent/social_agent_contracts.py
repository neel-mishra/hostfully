import csv
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SOCIAL_DIR = os.path.join(REPO_ROOT, "docs", "social media")

Channel = Literal["linkedin", "x", "instagram"]
Strictness = Literal["strict", "balanced", "experimental"]
GenerationMode = Literal["daily", "weekly", "campaign"]
InputMode = Literal["brief_only", "asset_repurpose", "performance_led"]
ApprovalState = Literal["draft", "approved", "rejected"]


@dataclass
class SocialDraft:
    draft_id: str
    person_id: str
    person_name: str
    channel: Channel
    objective: str
    angle: str
    hook_type: str
    target_persona: str
    cta: str
    copy: str
    rationale: str
    compliance_flags: List[str] = field(default_factory=list)
    quality_scores: Dict[str, float] = field(default_factory=dict)
    confidence_score: float = 0.0
    approval_state: ApprovalState = "draft"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SocialBatch:
    batch_id: str
    generated_at: str
    mode: GenerationMode
    input_mode: InputMode
    strictness: Strictness
    channels: List[Channel]
    people: List[str]
    plan_notes: str
    source_refs: List[str]
    drafts: List[SocialDraft]

    def to_dict(self) -> Dict[str, Any]:
        out = asdict(self)
        out["drafts"] = [d.to_dict() for d in self.drafts]
        return out


def _week_folder_for(date: datetime) -> str:
    month_name = date.strftime("%B")
    first_day = date.replace(day=1)
    while first_day.weekday() != 0:
        first_day = first_day.replace(day=first_day.day + 1)
    if date < first_day:
        week_num = 1
    else:
        week_num = ((date - first_day).days // 7) + 1
    return f"{month_name} Week {min(week_num, 4)}"


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


def build_batch_output_dir(mode: GenerationMode, run_time: Optional[datetime] = None) -> str:
    now = run_time or datetime.now()
    base = os.path.join(SOCIAL_DIR, "_runs", mode, _week_folder_for(now), _day_prefix(now.strftime("%A")))
    os.makedirs(base, exist_ok=True)
    return base


def save_batch_json(batch: SocialBatch, output_dir: str) -> str:
    path = os.path.join(output_dir, f"{batch.batch_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(batch.to_dict(), f, indent=2, ensure_ascii=False)
    return path


def save_scheduler_exports(batch: SocialBatch, output_dir: str) -> Dict[str, str]:
    json_path = os.path.join(output_dir, f"{batch.batch_id}_scheduler.json")
    csv_path = os.path.join(output_dir, f"{batch.batch_id}_scheduler.csv")

    approved = [d for d in batch.drafts if d.approval_state == "approved"]

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            [
                {
                    "draft_id": d.draft_id,
                    "person_id": d.person_id,
                    "channel": d.channel,
                    "copy": d.copy,
                    "cta": d.cta,
                    "objective": d.objective,
                }
                for d in approved
            ],
            f,
            indent=2,
            ensure_ascii=False,
        )

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["draft_id", "person_id", "channel", "objective", "cta", "copy"]
        )
        writer.writeheader()
        for d in approved:
            writer.writerow(
                {
                    "draft_id": d.draft_id,
                    "person_id": d.person_id,
                    "channel": d.channel,
                    "objective": d.objective,
                    "cta": d.cta,
                    "copy": d.copy,
                }
            )
    return {"json": json_path, "csv": csv_path}


def save_review_pack(batch: SocialBatch, output_dir: str) -> str:
    path = os.path.join(output_dir, f"{batch.batch_id}_review.md")
    lines: List[str] = []
    lines.append(f"# Social Review Pack - {batch.batch_id}")
    lines.append("")
    lines.append(f"- Generated at: {batch.generated_at}")
    lines.append(f"- Mode: {batch.mode}")
    lines.append(f"- Input mode: {batch.input_mode}")
    lines.append(f"- Strictness: {batch.strictness}")
    lines.append(f"- Channels: {', '.join(batch.channels)}")
    lines.append("")
    lines.append("## Draft Index")
    lines.append("")
    lines.append("| Draft ID | Person | Channel | Objective | Confidence | Approval |")
    lines.append("|----------|--------|---------|-----------|------------|----------|")
    for draft in batch.drafts:
        lines.append(
            f"| {draft.draft_id} | {draft.person_name} | {draft.channel} | {draft.objective} | "
            f"{draft.confidence_score:.2f} | {draft.approval_state} |"
        )
    lines.append("")
    lines.append("## Drafts")
    lines.append("")
    for draft in batch.drafts:
        lines.append(f"### {draft.draft_id} - {draft.person_name} ({draft.channel})")
        lines.append(f"- Angle: {draft.angle}")
        lines.append(f"- Hook type: {draft.hook_type}")
        lines.append(f"- Target persona: {draft.target_persona}")
        lines.append(f"- CTA: {draft.cta}")
        lines.append(f"- Rationale: {draft.rationale}")
        lines.append(f"- Compliance flags: {', '.join(draft.compliance_flags) if draft.compliance_flags else 'none'}")
        lines.append(f"- Quality: {json.dumps(draft.quality_scores)}")
        lines.append("")
        lines.append(draft.copy)
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).strip() + "\n")
    return path
