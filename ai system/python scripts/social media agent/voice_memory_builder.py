import os
import json
from datetime import datetime
from typing import Any, Dict, List

import google.generativeai as genai
from dotenv import load_dotenv

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
AGENTS_DIR = os.path.join(REPO_ROOT, "ai system", "agents")
SOCIAL_DIR = os.path.join(REPO_ROOT, "docs", "social media")

ROSTER_PATH = os.path.join(AGENTS_DIR, "social", "roster.yaml")


def _load_env_and_model() -> Any:
    """Configure Gemini using GEMINI_API_KEY from .env or env."""
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


def _find_latest_raw_posts(person_id: str) -> str | None:
    """
    Find the latest raw_posts_*.json file for a person under
    docs/social media/_source/people/<person_id>/

    Playwright-based scrapers (external or future) should write into this folder.
    """
    base_dir = os.path.join(SOCIAL_DIR, "_source", "people", person_id)
    if not os.path.isdir(base_dir):
        return None
    candidates = [
        os.path.join(base_dir, f)
        for f in os.listdir(base_dir)
        if f.startswith("raw_posts_") and f.endswith(".json")
    ]
    if not candidates:
        return None
    candidates.sort()
    return candidates[-1]


def _load_posts(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Expect either a list of posts or an object with \"posts\" key
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("posts"), list):
        return data["posts"]  # type: ignore[return-value]
    raise ValueError(f"Unexpected posts JSON structure in {path}")


def _summarise_tone(model: Any, person: Dict[str, Any], posts: List[Dict[str, Any]]) -> str:
    """
    Use Gemini to derive a tone / style memory markdown for a single person.
    """
    name = person.get("name", person.get("id", "Unknown"))
    role = person.get("role", "")

    # Take up to 60 posts, prioritising those with engagement metadata if present.
    sample = posts[:60]
    serialised_posts = []
    for p in sample:
        serialised_posts.append(
            {
                "text": p.get("text") or p.get("body") or "",
                "likes": p.get("likes") or p.get("reactions"),
                "comments": p.get("comments"),
                "shares": p.get("shares"),
                "created_at": p.get("created_at") or p.get("timestamp"),
            }
        )

    prompt = f"""
You are a voice analyst building a reusable \"tone memory\" for a GTM leader's LinkedIn posts.

PERSON:
- Name: {name}
- Role: {role}

TASK:
Given the following JSON list of posts, infer this person's natural writing style.
Focus on hooks, structure, sentence length, formatting, favorite patterns, and what they NEVER do.

Return a concise Markdown document with these sections:

## Voice Summary
- 3–5 bullets that capture the essence of how this person writes.

## Hooks & Openings
- Common hook patterns and first-line structures.

## Structure & Formatting
- Paragraph length, bullet usage, line breaks, emojis, and typical post length.

## Language & Phrasing
- Typical vocabulary, metaphors, and turns of phrase.

## Topics & Angles
- The themes and angles they come back to repeatedly.

## DOs
- 10 short bullets starting with \"Do ...\" that a model should follow to stay on-voice.

## DON'Ts
- 10 short bullets starting with \"Don't ...\" that a model should avoid.

Keep it practical and specific. Avoid generic advice like \"be authentic\".

POSTS JSON:
{json.dumps(serialised_posts, ensure_ascii=False)}
"""

    response = model.generate_content(prompt)
    return response.text or ""


def build_voice_memories() -> None:
    model = _load_env_and_model()
    roster = _load_roster()

    people = roster.get("people", [])
    if not isinstance(people, list):
        raise ValueError("Invalid roster: 'people' must be a list")

    output_dir = os.path.join(SOCIAL_DIR, "_voice")
    os.makedirs(output_dir, exist_ok=True)

    for person in people:
        person_id = person.get("id")
        if not person_id:
            continue

        raw_path = _find_latest_raw_posts(person_id)
        if not raw_path:
            # Nothing scraped yet for this person; skip gracefully.
            continue

        posts = _load_posts(raw_path)
        if not posts:
            continue

        memory_md = _summarise_tone(model, person, posts)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        out_path = os.path.join(output_dir, f"{person_id}_tone.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"<!-- Auto-generated tone memory for {person_id} at {timestamp} -->\n\n")
            f.write(memory_md.strip() + "\n")


if __name__ == "__main__":
    build_voice_memories()

