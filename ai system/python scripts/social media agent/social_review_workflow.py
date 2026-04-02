import json
import os
from typing import Dict, List

from social_agent_contracts import SocialBatch, SocialDraft, save_scheduler_exports  # type: ignore


def _load_batch(path: str) -> SocialBatch:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    drafts = [SocialDraft(**d) for d in raw.get("drafts", [])]
    return SocialBatch(
        batch_id=raw["batch_id"],
        generated_at=raw["generated_at"],
        mode=raw["mode"],
        input_mode=raw["input_mode"],
        strictness=raw["strictness"],
        channels=raw["channels"],
        people=raw["people"],
        plan_notes=raw.get("plan_notes", ""),
        source_refs=raw.get("source_refs", []),
        drafts=drafts,
    )


def apply_approvals(batch_json_path: str, approvals: Dict[str, str]) -> Dict[str, str]:
    """
    approvals format: {draft_id: "approved"|"rejected"|"draft"}
    """
    batch = _load_batch(batch_json_path)
    for draft in batch.drafts:
        new_state = approvals.get(draft.draft_id)
        if new_state in {"approved", "rejected", "draft"}:
            draft.approval_state = new_state  # type: ignore[assignment]

    with open(batch_json_path, "w", encoding="utf-8") as f:
        json.dump(batch.to_dict(), f, indent=2, ensure_ascii=False)

    out_dir = os.path.dirname(batch_json_path)
    return save_scheduler_exports(batch, out_dir)


def approvals_from_list(approved_ids: List[str], rejected_ids: List[str]) -> Dict[str, str]:
    approvals: Dict[str, str] = {}
    for draft_id in approved_ids:
        approvals[draft_id] = "approved"
    for draft_id in rejected_ids:
        approvals[draft_id] = "rejected"
    return approvals

