import json
import os
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple

import google.generativeai as genai
from dotenv import load_dotenv

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

from social_agent_contracts import (  # type: ignore
    Channel,
    GenerationMode,
    InputMode,
    SocialBatch,
    SocialDraft,
    Strictness,
    build_batch_output_dir,
    save_batch_json,
    save_review_pack,
    save_scheduler_exports,
)
from uniqueness_gate import evaluate_draft_collisions  # type: ignore


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
AGENTS_DIR = os.path.join(REPO_ROOT, "ai system", "agents")
SOCIAL_DIR = os.path.join(REPO_ROOT, "docs", "social media")
COMMANDS_DIR = os.path.join(REPO_ROOT, "commands")
ROSTER_PATH = os.path.join(AGENTS_DIR, "social", "roster.yaml")


def _load_model() -> Any:
    load_dotenv(os.path.join(REPO_ROOT, ".env"))
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def _load_roster() -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required for roster parsing")
    with open(ROSTER_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _read_if_exists(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _load_identity_context() -> str:
    paths = [
        os.path.join(COMMANDS_DIR, "identity", "messaging_pillars.md"),
        os.path.join(COMMANDS_DIR, "identity", "brand_voice_matrix.md"),
        os.path.join(COMMANDS_DIR, "identity", "style_guides.md"),
        os.path.join(COMMANDS_DIR, "core", "ideal_customer_profile.md"),
    ]
    parts = []
    for path in paths:
        content = _read_if_exists(path)
        if content:
            parts.append(f"=== {os.path.basename(path)} ===\n{content}\n")
    return "\n".join(parts)


def _load_input_context(input_mode: InputMode) -> Tuple[str, List[str]]:
    refs: List[str] = []
    if input_mode == "brief_only":
        brief_dir = os.path.join(SOCIAL_DIR, "_briefs")
        today = datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(brief_dir, f"daily_brief_{today}.md")
        content = _read_if_exists(path)
        if content:
            refs.append(path)
            return content, refs
        return "No brief file found for today. Use evergreen business priorities.", refs

    if input_mode == "asset_repurpose":
        blogs_dir = os.path.join(REPO_ROOT, "docs", "blogs")
        if not os.path.isdir(blogs_dir):
            return "No blog assets found.", refs
        candidates: List[str] = []
        for root, _, files in os.walk(blogs_dir):
            for filename in files:
                if filename.endswith(".md"):
                    candidates.append(os.path.join(root, filename))
        candidates.sort(key=os.path.getmtime, reverse=True)
        top = candidates[:3]
        chunks = []
        for path in top:
            refs.append(path)
            chunks.append(f"## {os.path.basename(path)}\n{_read_if_exists(path)[:4000]}")
        return "\n\n".join(chunks) if chunks else "No repurposable assets found.", refs

    perf_path = os.path.join(SOCIAL_DIR, "_analytics", "top_posts_last_30_days.md")
    content = _read_if_exists(perf_path)
    if content:
        refs.append(perf_path)
        return content, refs
    return "No performance summary file found. Use quality-first assumptions.", refs


def _strictness_rule(strictness: Strictness) -> str:
    if strictness == "strict":
        return "Stay very close to known voice patterns. Avoid novel stylistic structures."
    if strictness == "experimental":
        return "Stay on-brand but actively test unconventional hooks, structure, and angles."
    return "Stay mostly on-brand while allowing moderate experimentation."


def _channel_rule(channel: Channel) -> str:
    if channel == "linkedin":
        return "Use 5-14 lines, professional insight tone, and a comment-oriented CTA."
    if channel == "x":
        return "Write as a short thread-style post under 280 chars per unit. Keep it punchy."
    return "Write Instagram-caption style with concise punchy lines and one clear CTA."


def _quality_score(copy: str) -> Dict[str, float]:
    words = [w for w in copy.split() if w.strip()]
    line_count = len([l for l in copy.splitlines() if l.strip()])
    has_cta = 1.0 if "?" in copy or "comment" in copy.lower() or "dm" in copy.lower() else 0.5
    specificity = 1.0 if any(ch.isdigit() for ch in copy) else 0.6
    clarity = 1.0 if 30 <= len(words) <= 220 else 0.6
    novelty = 0.8 if any(k in copy.lower() for k in ["unpopular", "counter", "mistake", "learned"]) else 0.6
    brand_alignment = 0.9 if "hostfully" in copy.lower() else 0.7
    return {
        "clarity": round(clarity, 2),
        "specificity": round(specificity, 2),
        "novelty": round(novelty, 2),
        "brand_alignment": round(brand_alignment, 2),
        "cta_fit": round(has_cta, 2),
        "line_count": float(line_count),
    }


def _compliance_flags(copy: str, banned_topics: List[str], hard_rules: List[str]) -> List[str]:
    flags: List[str] = []
    low = copy.lower()
    for topic in banned_topics:
        if topic and topic.lower() in low:
            flags.append(f"banned_topic:{topic}")
    risk_terms = ["guarantee", "always", "never fail", "100%"]
    for t in risk_terms:
        if t in low:
            flags.append(f"claim_risk:{t}")
    if hard_rules and len(copy) < 40:
        flags.append("quality:too_short")
    return flags


def _make_draft(
    model: Any,
    person: Dict[str, Any],
    channel: Channel,
    input_context: str,
    identity_context: str,
    strictness: Strictness,
) -> Dict[str, Any]:
    person_id = person.get("id", "unknown")
    tone_memory_path = os.path.join(SOCIAL_DIR, "_voice", f"{person_id}_tone.md")
    tone_memory = _read_if_exists(tone_memory_path)
    constraints = person.get("constraints", {}) or {}
    banned_topics = constraints.get("topics_to_avoid", []) or []
    hard_rules = constraints.get("hard_rules", []) or []
    prompt = f"""
You are writing a social post for {person.get("name")} ({person.get("role")}).
Channel: {channel}
Strictness behavior: {_strictness_rule(strictness)}
Channel behavior: {_channel_rule(channel)}

Identity context:
{identity_context}

Input context:
{input_context}

Voice memory:
{tone_memory}

Constraints:
- Primary audience: {person.get("primary_audience", [])}
- Content pillars: {person.get("content_pillars", [])}
- Topics to avoid: {banned_topics}
- Hard rules: {hard_rules}

Return JSON only:
{{
  "objective":"string",
  "angle":"string",
  "hook_type":"string",
  "target_persona":"string",
  "cta":"string",
  "copy":"string",
  "rationale":"string"
}}
"""
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    try:
        return json.loads(response.text or "{}")
    except Exception:
        return {
            "objective": "thought leadership",
            "angle": "tactical insight",
            "hook_type": "tactical",
            "target_persona": "GTM leaders",
            "cta": "Comment if this matches your experience.",
            "copy": "Most teams confuse activity with traction.\n\nIf your pipeline is flat, inspect message-to-market fit first.\n\nAt Hostfully, we see momentum when teams systemize distribution, not just creation.\n\nWhat is your biggest bottleneck this quarter?",
            "rationale": "Fallback used due to parse failure.",
        }


def run_social_agent(
    mode: GenerationMode = "daily",
    input_mode: InputMode = "brief_only",
    strictness: Strictness = "balanced",
    channels: List[Channel] | None = None,
    approved_draft_ids: List[str] | None = None,
) -> Dict[str, Any]:
    channels = channels or ["linkedin"]
    approved_draft_ids = approved_draft_ids or []
    model = _load_model()
    roster = _load_roster()
    identity = _load_identity_context()
    input_context, source_refs = _load_input_context(input_mode=input_mode)
    output_dir = build_batch_output_dir(mode=mode)
    people = roster.get("people", [])
    if not isinstance(people, list):
        raise ValueError("Invalid roster format")

    run_time = datetime.now()
    draft_items: List[SocialDraft] = []
    repeats: Dict[str, int] = {}
    for person in people:
        for channel in channels:
            count = 1
            if mode == "weekly":
                count = 5
            if mode == "campaign":
                count = 3
            for idx in range(count):
                item = _make_draft(
                    model=model,
                    person=person,
                    channel=channel,
                    input_context=input_context,
                    identity_context=identity,
                    strictness=strictness,
                )
                copy = str(item.get("copy", ""))
                signature = " ".join(copy.lower().split()[:12])
                repeats[signature] = repeats.get(signature, 0) + 1

                score = _quality_score(copy)
                banned = (person.get("constraints", {}) or {}).get("topics_to_avoid", []) or []
                rules = (person.get("constraints", {}) or {}).get("hard_rules", []) or []
                flags = _compliance_flags(copy, banned_topics=banned, hard_rules=rules)
                draft_id = f"{person.get('id','p')}-{channel}-{idx+1}"
                if repeats[signature] > 1:
                    flags.append("anti_repetition:high")
                avg_score = (
                    score["clarity"]
                    + score["specificity"]
                    + score["novelty"]
                    + score["brand_alignment"]
                    + score["cta_fit"]
                ) / 5

                draft_items.append(
                    SocialDraft(
                        draft_id=draft_id,
                        person_id=str(person.get("id", "unknown")),
                        person_name=str(person.get("name", person.get("id", "unknown"))),
                        channel=channel,
                        objective=str(item.get("objective", "thought leadership")),
                        angle=str(item.get("angle", "insight")),
                        hook_type=str(item.get("hook_type", "insight")),
                        target_persona=str(item.get("target_persona", "GTM leaders")),
                        cta=str(item.get("cta", "Share your take in comments.")),
                        copy=copy,
                        rationale=str(item.get("rationale", "")),
                        compliance_flags=flags,
                        quality_scores=score,
                        confidence_score=round(avg_score, 2),
                        approval_state="approved" if draft_id in approved_draft_ids else "draft",
                    )
                )

    collisions = evaluate_draft_collisions(
        [(d.draft_id, d.person_id, d.copy) for d in draft_items],
        threshold=0.75,
    )
    collision_map: Dict[str, List[str]] = {}
    for a, b, score in collisions:
        collision_map.setdefault(a, []).append(f"{b}:{score:.2f}")
        collision_map.setdefault(b, []).append(f"{a}:{score:.2f}")
    for draft in draft_items:
        if draft.draft_id in collision_map:
            draft.compliance_flags.append("uniqueness_gate:collision")
            draft.compliance_flags.append(f"uniqueness_refs:{','.join(collision_map[draft.draft_id][:3])}")

    if mode == "campaign":
        # Add a simple campaign pacing marker in the plan notes.
        plan_notes = f"Campaign mode schedule window: {run_time.date()} to {(run_time + timedelta(days=14)).date()}"
    else:
        plan_notes = f"{mode.title()} mode run with {input_mode} inputs."

    batch = SocialBatch(
        batch_id=f"social_{uuid.uuid4().hex[:10]}",
        generated_at=run_time.isoformat(),
        mode=mode,
        input_mode=input_mode,
        strictness=strictness,
        channels=channels,
        people=[str(p.get("id", "unknown")) for p in people],
        plan_notes=plan_notes,
        source_refs=source_refs,
        drafts=draft_items,
    )

    batch_json = save_batch_json(batch, output_dir)
    review_pack = save_review_pack(batch, output_dir)
    export_paths = save_scheduler_exports(batch, output_dir)

    learning_dir = os.path.join(SOCIAL_DIR, "_learning")
    os.makedirs(learning_dir, exist_ok=True)
    run_log_path = os.path.join(learning_dir, "run_log.jsonl")
    prompt_fingerprint = hashlib.sha256(
        (identity + "\n" + input_context + "\n" + strictness + "\n" + ",".join(channels)).encode("utf-8")
    ).hexdigest()[:16]
    with open(run_log_path, "a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {
                    "timestamp": run_time.isoformat(),
                    "batch_id": batch.batch_id,
                    "mode": mode,
                    "input_mode": input_mode,
                    "strictness": strictness,
                    "channels": channels,
                    "draft_count": len(batch.drafts),
                    "source_refs": source_refs,
                    "prompt_fingerprint": prompt_fingerprint,
                    "output_dir": output_dir,
                },
                ensure_ascii=False,
            )
            + "\n"
        )

    return {
        "batch_id": batch.batch_id,
        "output_dir": output_dir,
        "batch_json": batch_json,
        "review_pack": review_pack,
        "exports": export_paths,
        "run_log": run_log_path,
        "draft_count": len(batch.drafts),
    }


if __name__ == "__main__":
    result = run_social_agent(
        mode=os.getenv("SOCIAL_MODE", "daily"),  # type: ignore[arg-type]
        input_mode=os.getenv("SOCIAL_INPUT_MODE", "brief_only"),  # type: ignore[arg-type]
        strictness=os.getenv("SOCIAL_STRICTNESS", "balanced"),  # type: ignore[arg-type]
        channels=[c.strip() for c in os.getenv("SOCIAL_CHANNELS", "linkedin").split(",") if c.strip()],  # type: ignore[list-item]
    )
    print(json.dumps(result, indent=2))
