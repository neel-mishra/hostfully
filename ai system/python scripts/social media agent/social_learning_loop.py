import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List

import google.generativeai as genai
from dotenv import load_dotenv


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SOCIAL_DIR = os.path.join(REPO_ROOT, "docs", "social media")
RUNS_DIR = os.path.join(SOCIAL_DIR, "_runs")
LEARNING_DIR = os.path.join(SOCIAL_DIR, "_learning")


def _load_model() -> Any:
    load_dotenv(os.path.join(REPO_ROOT, ".env"))
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def _iter_run_files() -> List[str]:
    files: List[str] = []
    if not os.path.isdir(RUNS_DIR):
        return files
    for root, _, names in os.walk(RUNS_DIR):
        for name in names:
            if name.startswith("social_") and name.endswith(".json"):
                files.append(os.path.join(root, name))
    files.sort(key=os.path.getmtime, reverse=True)
    return files


def _load_recent_batches(days: int = 7) -> List[Dict[str, Any]]:
    since = datetime.now() - timedelta(days=days)
    out: List[Dict[str, Any]] = []
    for path in _iter_run_files():
        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        if mtime < since:
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                out.append(json.load(f))
        except Exception:
            continue
    return out


def append_feedback(batch_id: str, draft_id: str, verdict: str, notes: str) -> str:
    os.makedirs(LEARNING_DIR, exist_ok=True)
    path = os.path.join(LEARNING_DIR, "feedback_log.jsonl")
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "batch_id": batch_id,
        "draft_id": draft_id,
        "verdict": verdict,
        "notes": notes,
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return path


def _load_feedback_index() -> Dict[str, Dict[str, str]]:
    path = os.path.join(LEARNING_DIR, "feedback_log.jsonl")
    index: Dict[str, Dict[str, str]] = {}
    if not os.path.exists(path):
        return index
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
            except Exception:
                continue
            key = f"{row.get('batch_id')}::{row.get('draft_id')}"
            index[key] = {"verdict": str(row.get("verdict", "")), "notes": str(row.get("notes", ""))}
    return index


def build_weekly_retrospective(days: int = 7) -> str:
    batches = _load_recent_batches(days=days)
    feedback_index = _load_feedback_index()
    model = _load_model()

    samples: List[Dict[str, Any]] = []
    for batch in batches:
        for draft in batch.get("drafts", []):
            key = f"{batch.get('batch_id')}::{draft.get('draft_id')}"
            fb = feedback_index.get(key, {})
            samples.append(
                {
                    "batch_id": batch.get("batch_id"),
                    "draft_id": draft.get("draft_id"),
                    "channel": draft.get("channel"),
                    "person_id": draft.get("person_id"),
                    "angle": draft.get("angle"),
                    "confidence": draft.get("confidence_score"),
                    "quality_scores": draft.get("quality_scores", {}),
                    "flags": draft.get("compliance_flags", []),
                    "approval_state": draft.get("approval_state", "draft"),
                    "feedback_verdict": fb.get("verdict", ""),
                    "feedback_notes": fb.get("notes", ""),
                }
            )

    prompt = f"""
You are creating a weekly social agent retrospective.
Given this JSON sample, produce markdown with:
- Top performing angle/hook patterns
- Lowest-quality patterns
- Recurring compliance or uniqueness issues
- 5 concrete changes for next week

JSON:
{json.dumps(samples[:200], ensure_ascii=False)}
"""
    response = model.generate_content(prompt)
    os.makedirs(LEARNING_DIR, exist_ok=True)
    out_path = os.path.join(LEARNING_DIR, f"weekly_retrospective_{datetime.now().strftime('%Y-%m-%d')}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# Weekly Social Agent Retrospective\n\n")
        f.write(response.text or "No data available.\n")
    return out_path


if __name__ == "__main__":
    print(build_weekly_retrospective())
