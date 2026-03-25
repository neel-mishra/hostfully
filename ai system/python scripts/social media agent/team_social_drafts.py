import os
from datetime import datetime
from typing import Any, Dict, List

import google.generativeai as genai
from dotenv import load_dotenv

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AGENTS_DIR = os.path.join(REPO_ROOT, "agents")
SOCIAL_DIR = os.path.join(REPO_ROOT, "docs", "social media")
COMMANDS_DIR = os.path.join(REPO_ROOT, "commands")

ROSTER_PATH = os.path.join(AGENTS_DIR, "social", "roster.yaml")


def _load_env_and_model() -> Any:
    load_dotenv(os.path.join(REPO_ROOT, ".env"))
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def _load_roster() -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to load ai system/agents/social/roster.yaml")
    if not os.path.exists(ROSTER_PATH):
        raise FileNotFoundError(f"Roster file not found at {ROSTER_PATH}")
    with open(ROSTER_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _week_folder_for_today(now: datetime) -> str:
    month_name = now.strftime("%B")
    # Reuse the 1–4 week number convention from social_media_agent.py
    # Simplified: ISO week of month capped at 4.
    first_day = now.replace(day=1)
    while first_day.weekday() != 0:
        first_day = first_day.replace(day=first_day.day + 1)
    if now < first_day:
        week_num = 1
    else:
        delta = now - first_day
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


def _load_identity_context() -> str:
    parts: List[str] = []
    icp_path = os.path.join(COMMANDS_DIR, "core", "ideal_customer_profile.md")
    if os.path.exists(icp_path):
        with open(icp_path, "r", encoding="utf-8") as f:
            parts.append(f"=== ideal_customer_profile.md ===\n{f.read()}\n")

    messaging_path = os.path.join(COMMANDS_DIR, "identity", "messaging_pillars.md")
    if os.path.exists(messaging_path):
        with open(messaging_path, "r", encoding="utf-8") as f:
            parts.append(f"=== messaging_pillars.md ===\n{f.read()}\n")

    creative_path = os.path.join(COMMANDS_DIR, "identity", "creative_direction.md")
    if os.path.exists(creative_path):
        with open(creative_path, "r", encoding="utf-8") as f:
            parts.append(f"=== creative_direction.md ===\n{f.read()}\n")

    return "\n".join(parts)


def _load_daily_brief(date: datetime) -> str:
    brief_dir = os.path.join(SOCIAL_DIR, "_briefs")
    slug = date.strftime("%Y-%m-%d")
    path = os.path.join(brief_dir, f"daily_brief_{slug}.md")
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _load_tone_memory(person_id: str) -> str:
    path = os.path.join(SOCIAL_DIR, "_voice", f"{person_id}_tone.md")
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _build_prompt(
    person: Dict[str, Any],
    identity_context: str,
    daily_brief: str,
    tone_memory: str,
    posts_per_day: int,
) -> str:
    name = person.get("name", person.get("id", "Unknown"))
    role = person.get("role", "")
    primary_audience = person.get("primary_audience", [])
    content_pillars = person.get("content_pillars", [])
    constraints = person.get("constraints", {}) or {}
    topics_to_avoid = constraints.get("topics_to_avoid", [])
    hard_rules = constraints.get("hard_rules", [])

    return f"""
You are writing LinkedIn drafts for {name} ({role}) at TLDR.

IDENTITY CONTEXT:
{identity_context}

DAILY BRIEF:
{daily_brief}

VOICE MEMORY FOR THIS PERSON:
{tone_memory}

PERSON CONFIG:
- Primary audience: {primary_audience}
- Content pillars: {content_pillars}
- Topics to avoid: {topics_to_avoid}
- Hard rules: {hard_rules}

TASK:
Write {posts_per_day} LinkedIn post drafts that:
- Sound exactly like this person, not like a generic brand account.
- Tie clearly to TLDR's narrative and products where natural, but do NOT feel like ads.
- Include at least one specific example, anecdote, or situation.
- Respect topics-to-avoid and hard rules.
- Stay within 5–14 lines, with deliberate line breaks.

For each draft, output in this JSON shape (and only JSON, no extra text):
[
  {{
    "angle": "short label for the angle",
    "hook_type": "e.g. story, contrarian, tactical, social_proof",
    "target_persona": "short description of who this post is speaking to",
    "copy": "full LinkedIn post text with line breaks"
  }},
  ...
]
"""


def _generate_drafts_for_person(
    model: Any,
    person: Dict[str, Any],
    identity_context: str,
    daily_brief: str,
) -> List[Dict[str, Any]]:
    person_id = person.get("id")
    if not person_id:
        return []

    tone_memory = _load_tone_memory(person_id)
    if not tone_memory:
        return []

    defaults_posts = 1
    posts_per_day = person.get("posts_per_day", defaults_posts)
    prompt = _build_prompt(
        person=person,
        identity_context=identity_context,
        daily_brief=daily_brief,
        tone_memory=tone_memory,
        posts_per_day=posts_per_day,
    )

    response = model.generate_content(
        prompt, generation_config={"response_mime_type": "application/json"}
    )
    text = response.text or "[]"
    try:
        # Lazy import to avoid mandatory dependency at top-level.
        import json  # type: ignore

        data = json.loads(text)
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict)]
        return []
    except Exception:
        return []


def _save_drafts_for_person(
    person: Dict[str, Any],
    drafts: List[Dict[str, Any]],
    date: datetime,
) -> None:
    if not drafts:
        return

    person_id = person.get("id", "unknown")
    day_name = date.strftime("%A")
    week_folder = _week_folder_for_today(date)
    day_folder = _day_prefix(day_name)

    base_dir = os.path.join(SOCIAL_DIR, week_folder, person_id, day_folder)
    os.makedirs(base_dir, exist_ok=True)

    # Metadata index for quick human review.
    index_lines = [
        f"# Drafts for {person.get('name', person_id)} on {date.date()}",
        "",
        "| Draft | Angle | Hook type | Target persona | File |",
        "|-------|-------|-----------|----------------|------|",
    ]

    for idx, draft in enumerate(drafts, start=1):
        angle = draft.get("angle", "")
        hook_type = draft.get("hook_type", "")
        target_persona = draft.get("target_persona", "")
        copy = draft.get("copy", "")

        filename = f"draft_{idx:02d}.md"
        path = os.path.join(base_dir, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"id: {person_id}\n")
            f.write(f"date: {date.date()}\n")
            f.write(f"angle: {angle}\n")
            f.write(f"hook_type: {hook_type}\n")
            f.write(f"target_persona: {target_persona}\n")
            f.write("---\n\n")
            f.write(copy.strip() + "\n")

        index_lines.append(
            f"| {idx} | {angle} | {hook_type} | {target_persona} | {filename} |"
        )

    index_path = os.path.join(base_dir, "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines) + "\n")


def run_team_social_drafts() -> None:
    model = _load_env_and_model()
    roster = _load_roster()
    people = roster.get("people", [])
    if not isinstance(people, list):
        raise ValueError("Invalid roster: 'people' must be a list")

    today = datetime.now()
    identity_context = _load_identity_context()
    daily_brief = _load_daily_brief(today)

    for person in people:
        drafts = _generate_drafts_for_person(
            model=model,
            person=person,
            identity_context=identity_context,
            daily_brief=daily_brief,
        )
        _save_drafts_for_person(person, drafts, today)


if __name__ == "__main__":
    run_team_social_drafts()

