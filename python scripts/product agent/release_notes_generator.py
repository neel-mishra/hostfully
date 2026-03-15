#!/usr/bin/env python3
"""
Release Notes → Changelog Generator

Transforms raw release notes into polished, audience-appropriate changelogs.
Generates advertiser-facing, reader-facing, and internal versions.

Usage:
  python release_notes_generator.py --file path/to/notes.md   # from file
  python release_notes_generator.py --dry-run                   # preview
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
COMMANDS_DIR = WORKSPACE_ROOT / "commands"
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "product_assets" / "changelogs"


def _resolve_env_key(name: str) -> str | None:
    val = os.environ.get(name)
    if val:
        return val
    current = Path(__file__).resolve().parent
    while current != current.parent:
        env_file = current / ".env"
        if env_file.exists():
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(f"{name}="):
                        return line.split("=", 1)[1].strip().strip("'\"")
        current = current.parent
    return None


CLAUDE_API_BASE = "https://api.anthropic.com/v1/messages"


def claude_generate(prompt: str, api_key: str, max_tokens: int = 4096, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            resp = requests.post(
                CLAUDE_API_BASE,
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=120,
            )
            if resp.status_code == 200:
                return resp.json()["content"][0]["text"]
            if resp.status_code == 429:
                time.sleep(min(60, 2 ** (attempt + 2)))
                continue
            time.sleep(5)
        except Exception as e:
            print(f"  ⚠ Claude exception: {e}")
            time.sleep(10)
    raise Exception("Max retries reached")


def generate_changelog(raw_notes: str, api_key: str) -> str:
    voice_context = ""
    try:
        voice_context = (COMMANDS_DIR / "identity" / "brand_voice_matrix.md").read_text()[:1500]
    except FileNotFoundError:
        pass

    prompt = f"""You are a product communications specialist for TLDR, the largest daily tech newsletter (7M+ subscribers, 12 newsletters).

Transform these raw release notes into polished changelogs for three audiences.

RAW RELEASE NOTES:
{raw_notes[:10000]}

VOICE CONTEXT:
{voice_context}

TLDR operates a 2-sided network:
- Readers (subscribers): care about content quality, personalization, experience
- Advertisers: care about targeting, reporting, formats, ROI

Generate in this EXACT format:

# Release Notes — {datetime.now().strftime('%Y-%m-%d')}

---

## Advertiser-Facing Update

### What's New
- **[Feature]:** [One sentence — focus on benefit for advertisers. ROI-oriented.]

### Improvements
- [improvement that affects ad performance, reporting, or experience]

### Bug Fixes
- [fix relevant to advertisers]

---

## Reader-Facing Update

### What's New
- **[Feature]:** [One sentence — focus on reading experience. Casual, friendly.]

### Improvements
- [improvement that affects content quality or subscriber experience]

---

## Internal Changelog

### Added
- [detailed technical description with ticket/PR reference if available]

### Changed
- [what changed, why, any migration notes]

### Fixed
- [bug description and fix details]

### Technical Notes
- [breaking changes, performance impacts, infrastructure notes]

RULES:
- Advertiser version: professional, value-oriented, focus on ROI/performance
- Reader version: casual, friendly, focus on experience improvements
- Internal version: precise, comprehensive, include technical details
- Don't include internal details in external versions
- Lead with the most impactful change in each section"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="Release Notes → Changelog Generator")
    parser.add_argument("--file", type=str, required=True, help="Path to raw release notes")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    source = Path(args.file)
    if not source.exists():
        print(f"❌ File not found: {source}")
        sys.exit(1)

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    raw_notes = source.read_text(encoding="utf-8")
    print(f"  📄 Processing: {source.name}")

    if args.dry_run:
        print("  🧪 DRY RUN: would generate changelog")
        return

    changelog = generate_changelog(raw_notes, api_key)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    path = OUTPUT_DIR / f"{today}_changelog.md"
    path.write_text(changelog, encoding="utf-8")
    print(f"  ✅ Changelog saved to {path}")


if __name__ == "__main__":
    main()
